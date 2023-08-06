import fnmatch
import re
import os
import threading

from enum import Enum
from stat import S_ISDIR
from dataclasses import dataclass

from buildstream import Source, SourceFetcher, SourceError
from buildstream.utils import url_directory_name

from dulwich.repo import Repo
from dulwich.objects import Commit, Tag
from dulwich.client import get_transport_and_path
from dulwich.errors import GitProtocolError
from dulwich.refs import ANNOTATED_TAG_SUFFIX


REF_REGEX = re.compile(r"(?:(.*)(?:-(\d+)-g))?([0-9a-f]{40})")
SPLITTER_REGEX = re.compile(r"[a-zA-Z]+|[0-9]+")


def pattern_to_regex(pattern):
    """
    Transforms a glob pattern into a regex to match refs.

    If the pattern doesn't start with "refs/", it will be considered to only match refs in
    refs/tags/ and refs/heads.
    """
    if pattern.startswith("refs/"):
        return re.compile(fnmatch.translate(pattern))

    return re.compile("refs/(heads|tags)/" + fnmatch.translate(pattern))


def version_sort_key(elt):
    """
    A sort key that can be used to versions. It sorts letters before numbers (so 1.beta is earlier
    than 1.0) and disregards separators (so 1.beta, 1~beta and 1beta are the same).
    """
    return [
        # to sort letters before digits
        (-1, part) if part.isalpha() else (int(part), "")
        for part in SPLITTER_REGEX.findall(elt)
    ]


def init_repo(mirror_dir):
    """
    Open a repo at the given mirror_dir, creating an empty bare repo if it doesn't exist.
    """
    try:
        return Repo.init_bare(mirror_dir, mkdir=True)
    except FileExistsError:
        return Repo(mirror_dir, bare=True)


def stage_repo(mirror_dir, tag, sha, directory, log):
    """
    Stage a checkout of the repository at mirror_dir, with a minimal repo that is just enough for
    common operations (like `git describe --dirty` and `git log .`).

    sha is the commit sha to stage and tag is the tag that should be staged so that `git describe`
    is relative to it (could point to the same commit).
    log is the logging context (e.g. bst plugin).
    """

    with init_repo(mirror_dir) as repo, log.timed_activity(
        f"Checking out {sha} from git"
    ):
        commit = repo.get_object(sha.encode())
        commit_id = commit.id.decode()

        # Compatibility: some older git plugins can generate refs where the sha isn't a commit
        # if isinstance(commit, Tag):
        #     log.warn(f"{commit_id} points to a tag, not to a commit")
        #     commit = repo.get_object(commit.object[1])

        log.status(f"Checking out {commit_id}")

        objects = {}
        if tag:
            tag_ref = f"refs/tags/{tag}".encode()
            tag_obj = repo[tag_ref]

            if tag_obj.type_name == b"tag":
                objects[tag_obj.id] = tag_obj
                base = repo[tag_obj.object[1]]
            else:
                base = tag_obj
        else:
            base = commit

        # I've seen this once at least: a tag that points to a tag, but we don't go recursing
        if isinstance(base, Tag):
            base = repo.get_object(base.object[1])

        assert isinstance(
            base, Commit
        ), f"Tag {tag} does not point to a commit (type {type(tag_obj)}"

        log.debug(
            f"Staging commit {commit.id.decode()}, base {base.id.decode()}"
        )

        if commit == base:
            objects[commit.id] = commit
        else:
            for entry in repo.get_walker(commit.id, base.parents):
                objects[entry.commit.id] = entry.commit

        # The shallow bases
        shallow = [base.id]

        # All the tree objects. `git log .` and `git describe --dirty` need them
        trees = set()

        def collect_trees(repo, root_sha):
            if root_sha in trees:
                return
            trees.add(root_sha)

            for _, mode, sha in repo[root_sha].items():
                if S_ISDIR(mode):
                    collect_trees(repo, sha)

        for obj in objects.values():
            if not isinstance(obj, Commit):
                continue

            if not all(p in objects for p in obj.parents):
                shallow.append(obj.id)

            collect_trees(repo, obj.tree)

        for tree in trees:
            objects[tree] = repo[tree]

        with Repo.init(directory) as dest:
            log.status(f"Adding {len(objects)} objects")
            # Takes a Sequence[Tuple[ShaFile, Optional[str]]] in theory,
            # but in practice second field of tuple is ignored
            # and len() is called on the sequence (so it needs to be a
            # list, not an iterator)
            dest.object_store.add_objects(
                [(o, None) for o in objects.values()]
            )

            if tag:
                dest.refs[tag_ref] = tag_obj.id

            dest.refs[b"HEAD"] = commit.id
            dest.update_shallow(shallow, [])

        # checkout
        with Repo(directory, object_store=repo.object_store) as dest:
            dest.reset_index(commit.tree)


def git_describe(repo, revision):
    """
    Returns the equivalent of `git describe --tags --abbrev=40`
    """
    # Get a list of all tags
    tags = repo.refs.as_dict(b"refs/tags")

    if not tags:
        return revision

    commit_tags = {}
    for tag_name, tag_sha in list(tags.items()):
        commit = repo.get_object(tag_sha)
        while isinstance(commit, Tag):
            commit = repo.get_object(commit.object[1])

        commit_tags[commit.id] = tag_name.decode()

    count = 0

    walker = repo.get_walker([revision.encode()])
    for entry in walker:
        commit_id = entry.commit.id
        if commit_id in commit_tags:
            return f"{commit_tags[commit_id]}-{count}-g{revision}"

        count += 1

    return revision


LOCKS = {}


class GitMirror(SourceFetcher):
    def __init__(self, source, url, ref):
        super().__init__()
        self.mark_download_url(url)

        self.source = source
        self.url = url

        tag, depth, sha = REF_REGEX.match(ref).groups()

        self.sha = sha
        self.tagref = f"refs/tags/{tag}".encode() if tag else None
        self.depth = int(depth) + 1 if depth else None

    def fetch(self, alias_override=None):
        url = self.source.translate_url(
            self.url, alias_override=alias_override
        )
        lock = LOCKS.setdefault(self.source.mirror_dir, threading.Lock())

        with lock, init_repo(
            self.source.mirror_dir
        ) as repo, self.source.timed_activity(f"Fetching from {url}"):
            if self.sha.encode() in repo and (
                not self.tagref or self.tagref in repo.refs
            ):
                return

            self.source.status(f"Fetching {self.sha}")

            def wants(refs, depth=None):
                wanted = set()
                if self.tagref:
                    if self.tagref in refs:
                        wanted.add(refs[self.tagref])
                    else:
                        raise SourceError(
                            f"ref {self.tagref.decode()} not found in remote {url}"
                        )

                if self.sha.encode() in refs.values():
                    wanted.add(self.sha.encode())
                else:
                    # we want everything
                    self.source.warn(
                        f"No ref matches {self.sha}, downloading everything."
                    )
                    wanted.update(refs.values())

                return wanted

            client, path = get_transport_and_path(url)

            try:
                remote_refs = client.fetch(
                    path, repo, determine_wants=wants, depth=self.depth
                )
            except GitProtocolError as e:
                raise SourceError(f"failed to fetch: {e}") from e
            except Exception as e:
                # should be more specific
                raise SourceError(f"failed to fetch: {e}") from e

            # check that we actually pulled the required commit
            if self.sha.encode() not in repo:
                raise SourceError(f"{self.sha} not found in remote {url}")

            if self.tagref:
                repo.refs.add_if_new(self.tagref, remote_refs[self.tagref])
                return

            local_refs = repo.get_refs()

            extra_wants = []
            extra_haves = []
            for ref in remote_refs:
                if not ref.startswith(b"refs/tags"):
                    continue
                if ref.endswith(ANNOTATED_TAG_SUFFIX):
                    continue
                if ref in local_refs:
                    continue
                if remote_refs[ref] in repo:
                    repo.refs.add_if_new(ref, remote_refs[ref])
                else:
                    peeled_ref = ref + ANNOTATED_TAG_SUFFIX
                    if (
                        peeled_ref in remote_refs
                        and remote_refs[peeled_ref] in repo
                    ):
                        extra_haves.append(remote_refs[peeled_ref])
                        extra_wants.append(remote_refs[ref])
            if extra_wants:
                self.source.status(f"Fetching {len(extra_wants)} extra tags")
                f, commit, abort = repo.object_store.add_pack()
                try:
                    walker = repo.get_graph_walker(extra_haves)
                    remote_refs = client.fetch_pack(
                        path, lambda _: extra_wants, walker, f.write
                    )
                except Exception as e:
                    # should be more specific
                    abort()
                    raise SourceError(f"failed to fetch: {e}") from e

                commit()
                for ref, value in remote_refs.items():
                    if value in extra_wants:
                        repo.refs.add_if_new(ref, value)


class RefFormat(Enum):
    SHA1 = "sha1"
    GIT_DESCRIBE = "git-describe"


@dataclass
class RepoInfo:
    primary: bool
    ref: str
    url: str


class GitSource(Source):
    BST_MIN_VERSION = "2.0"

    def configure(self, node):
        CONFIG_KEYS = ["ref", "url", "track", "exclude", "ref-format"]

        node.validate_keys(Source.COMMON_CONFIG_KEYS + CONFIG_KEYS)
        self.ref = None
        self.load_ref(node)

        self.url = node.get_str("url")
        self.mark_download_url(self.url)

        if self.url.endswith(".git"):
            norm_url = self.url[:-4]
        else:
            norm_url = self.url

        self.mirror_dir = os.path.join(
            self.get_mirror_directory(),
            url_directory_name(norm_url) + ".git",
        )

        self.tracking = node.get_str("track", None)
        self.exclude = node.get_str_list("exclude", [])

        self.ref_format = node.get_enum(
            "ref-format", RefFormat, RefFormat.SHA1
        )

        # make the url-manifest script happy
        self.mirror = RepoInfo(primary=True, ref=self.ref, url=self.url)

    def preflight(self):
        pass

    def get_unique_key(self):
        return {"ref": self.ref}

    # loading and saving refs
    def load_ref(self, node):
        if "ref" not in node:
            return
        ref = node.get_str("ref")
        if REF_REGEX.match(ref) is None:
            raise SourceError(f"ref {ref} is not in the expected format")
        self.ref = ref

    def get_ref(self):
        return self.ref

    def set_ref(self, ref, node):
        self.ref = ref
        node["ref"] = ref

    def is_cached(self):
        tag, _, sha = REF_REGEX.match(self.ref).groups()

        with Repo(self.mirror_dir, bare=True) as repo:
            cached = sha.encode() in repo
            if tag:
                ref = b"refs/tags/" + tag.encode()
                cached_ref = ref in repo

                cached = cached and cached_ref

        return cached

    def track(self):
        if not self.tracking:
            return None

        url = self.translate_url(self.url)
        self.status(f"Tracking {self.tracking} from {url}")
        client, path = get_transport_and_path(url)
        refs_dict = {
            k.decode(): v.decode() for k, v in client.get_refs(path).items()
        }

        real_refs = {ref for ref in refs_dict if not ref.endswith("^{}")}
        matching_regex = pattern_to_regex(self.tracking)

        matching_refs = [ref for ref in real_refs if matching_regex.match(ref)]

        if self.exclude:
            exclude_regexs = [
                pattern_to_regex(pattern) for pattern in self.exclude
            ]
            matching_refs = [
                ref
                for ref in matching_refs
                if not any(regex.match(ref) for regex in exclude_regexs)
            ]

        if not matching_refs:
            raise SourceError("No matching refs")

        self.debug("Refs to be tracked", detail="\n".join(matching_refs))

        ref = max(matching_refs, key=version_sort_key)

        # peel the ref if possible
        peeled_ref = ref + "^{}"
        if peeled_ref in refs_dict:
            resolved = refs_dict[peeled_ref]
        else:
            resolved = refs_dict[ref]

        self.status(f"Tracked {ref}: {resolved}")

        if self.ref_format == RefFormat.SHA1:
            return resolved

        if "tags" in ref:
            tag = ref.split("/", 2)[-1]
            return f"{tag}-0-g{resolved}"

        # Need to fetch to generate the ref in git-describe format
        fetcher = GitMirror(self, self.url, resolved)
        fetcher.fetch()

        with Repo(self.mirror_dir) as repo:
            return git_describe(repo, resolved)

    def get_source_fetchers(self):
        yield GitMirror(self, self.url, self.ref)

    def stage(self, directory):
        tag, _, sha = REF_REGEX.match(self.ref).groups()

        stage_repo(self.mirror_dir, tag, sha, directory, self)


def setup():
    return GitSource
