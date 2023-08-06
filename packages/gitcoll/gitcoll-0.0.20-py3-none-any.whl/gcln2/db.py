# Database

# py38 support:
from __future__ import annotations

import os
import re
import base64
import typing
import logging
import concurrent.futures

import yaml
import pydantic
import gitlab
import gitlab.v4.objects

try:
    from gcln2 import helpers
except:
    import helpers

# data in cache:
# per repository (gitlab project):
# * project nr
# * branches we care about
# * full_name and full_path
# * workspace path (normally full_name, but there are substitution possibilities)
# * UID

# * for every branch:
#   * name
#   * latest known commit ID
#   * gitmodules

# per workspace:
# * path
# * project uid and path


#@dataclasses.dataclass
class Branch(pydantic.BaseModel):
    name: str
    commit: str
    submodules: typing.Dict[str, str]        # submodule UIDs to path. TODO: record if we track a branch?



#@dataclasses.dataclass
class Project(pydantic.BaseModel):
    project_id: int         # gitlab project number
    main_branch: str        # empty str if no main_branch
    full_path: str      # https path without the https
    full_name: str      # group/project names, ie, should be used for workspace etc.
    #ws_full_name: str
    branches: typing.Dict[str, Branch]
    tags: typing.Dict[str, str]        # tag => commit-id
    uid: str
    alt_uids: typing.List[str]
    is_home: bool

    @classmethod
    def from_gl(cls, gl_project, update_context: "UpdateContext"):
        logging.debug(str(gl_project))
        return project_from_gl(gl_project, update_context)


class MinimalUpdateContext:

    def __init__(self, branch_whitelist, branch_blacklist):
        self.branch_whitelist = [re.compile(b) for b in branch_whitelist]
        self.branch_blacklist = [re.compile(b) for b in branch_blacklist]

#        vb = "^main|master|[di]-.*"  # TODO: set this from caller. Right now hardcoded for sync
#        self.re_valid_branches = re.compile(vb)


    def valid_branch_name(self, branch_name):
        if branch_name in ["master", "main", "_config"]:
            return True
        if branch_name in ["HEAD"]:
            return False
        for b in self.branch_whitelist:
            if not b.fullmatch(branch_name):
                return False
        for b in self.branch_blacklist:
            if b.fullmatch(branch_name):
                return False
        return True


class Cache(pydantic.BaseModel):
    filename: str = ""  # note that this is removed when saving, and should not be part of data on disk
    projects: typing.Dict[int, Project] = {}       # mapping form GL project ID to project
    timestamp: float = 0.0

    def build_uid_map(self) -> typing.Dict[str, Project]:
        ret = {}
        for p in self.projects.values():
            if not p.uid:
                continue
            if p.uid in ret:
                raise Exception(
                    "Duplicate uid: %s (%s and %s)"
                    % (p.uid, p.full_path, ret[p.uid].full_path)
                )
            ret[p.uid] = p
        return ret


    @classmethod
    def load(cls, fn: str, allow_missing=False) -> Cache:
        if allow_missing:
            if not os.path.exists(fn):
                ret = Cache()
                ret.filename = fn
                return ret
        with open(fn, "rt") as fh:
            data = yaml.safe_load(fh)
            ret = Cache(**data)
            ret.filename = fn
            return ret


    def clean_branch_names(
        self, branch_whitelist: list[str], branch_blacklist: list[str]
    ):
        uc = MinimalUpdateContext(branch_whitelist, branch_blacklist)
        for p in self.projects.values():
            branches = set(p.branches.keys())
            for b in branches:
                if not uc.valid_branch_name(b):
                    print(f"**Remove branchname {b} from cache")
                    del p.branches[b]


    def save(self, timestamp: float):
        self.timestamp = timestamp
        data = self.dict()
        del data["filename"]
        with open(self.filename, "wt") as fh:
            yaml.dump(data, fh)

    def remove_uids(self, blacklist: list[str] | set[str]):
        bl_set = set(blacklist)
        map_uid_to_pid = {
            proj.uid: pid for pid, proj in self.projects.items() if proj.uid
        }
        for bl in blacklist:
            if bl in map_uid_to_pid:
                del self.projects[map_uid_to_pid[bl]]

    def update_cache_from_server(
        self,
        gl,
        num_threads: int,
        branch_whitelist: list[str],
        branch_blacklist: list[str],
    ) -> typing.Dict[str, Project]:
        """return map uid2project"""
        SINCE = helpers.timestamp2isotime(self.timestamp)

        uc = MinimalUpdateContext(branch_whitelist, branch_blacklist)

        if num_threads == 0:
            for gl_proj in gl.projects.list(iterator=True, last_activity_after=SINCE):
                p = Project.from_gl(gl_proj, uc)
                self.projects[p.project_id] = p
        else:
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_threads
            ) as executor:
                futures = []
                for gl_proj in gl.projects.list(
                    iterator=True, last_activity_after=SINCE
                ):
                    futures.append(executor.submit(Project.from_gl, gl_proj, uc))
                    print("Got %d projects " % len(futures), end="\r")
                print("Got %d projects " % len(futures))
                i = 0
                for future in concurrent.futures.as_completed(futures):
                    if future.result() is None:
                        continue
                    i += 1
                    print(
                        "Got detailed info for %d/%d projects " % (i, len(futures)),
                        end="\r",
                    )
                    p: Project = future.result()  # to trigger exceptions
                    self.projects[p.project_id] = p
                print()

        map_uid2project = self.build_uid_map()

        logging.debug(
            "mapped %d uids to projects. Total nr of projects=%d"
            % (len(map_uid2project), len(self.projects))
        )

        return map_uid2project


#################


def project_from_gl(
    gl_project: gitlab.v4.objects.Project, update_context: "main.UpdateContext"
) -> typing.Optional[Project]:
    """returns NULL if cannot retrieve information for the project (permisison issues). We cannot trust the permission attribute :-("""
    full_name = gl_project.name_with_namespace.replace(" / ", "/").strip()

    my_branches = {}
    try:
        for b in gl_project.branches.list(iterator=True):
            if not update_context.valid_branch_name(b.name):
                continue
#            if b.name != "_config" and not update_context.re_valid_branches.fullmatch(b.name) and b.name != gl_project.default_branch:
#                continue

            # TODO: optional, but should check for submodules. Optimization: if cache already points to the same commit for this branch, then no need to retrieve it again
            if 0:
                for item in gl_project.repository_tree(path="", recursive=False, ref=b.name, iterator=True):
                    if item["name"] == ".gitmodules":
                        file_info = gl_project.repository_blob(item["id"])
                        content = base64.b64decode(file_info["content"])
                        # content is binary data from git, file .gitmodules. Need to parse it to understand submodules
                        #print (content)

            b2 = Branch(name=b.name, commit=b.attributes["commit"]["id"], submodules=set())
            my_branches[b.name] = b2
    except gitlab.exceptions.GitlabListError:
        # probably don't have access to this project.
        return None


    # optional to check for tags?
    tags = {}
    for tag in gl_project.tags.list(iterator=True):
        if 0: # TODO: check if valid tag
            continue
        #print (tag.attributes)
        tags[tag.attributes["name"]] =  tag.attributes["commit"]["id"]
    #print(tags)

    # optional to check for uid. If cache already has it, don't bother? Or at least (most common), if the _config branch hasn't changed, no need to check.
    uid = ""
    alt_uids = []
    if "_config" in my_branches:
        for item in gl_project.repository_tree(path="", recursive=False, ref="_config", iterator=True):
            if item["name"] == "attributes.yaml":
                file_info = gl_project.repository_blob(item["id"])
                content = base64.b64decode(file_info["content"])
                cfg = yaml.safe_load(content.decode("utf8"))
                uid = cfg.get("uid", "")
                alt_uids = cfg.get("alt_uids", [])
                break
    else:
        #print ("*** no _config", gl_project.path_with_namespace)
        pass

    # note that we try to retrieve information about projects, even if they're in the black list. This way, we can use the .cache.yaml file to find UIDs.

    main_branch = gl_project.default_branch
    assert isinstance(main_branch, str)
    if main_branch == "_config" or main_branch not in my_branches:
        main_branch = ""

#    if gl_project.namespace["kind"] == "group":
#        ws_full_name = full_name
#    else:
#        cfg.
#        ws_full_name = "home/" + full_name

    ret = Project(
        project_id=gl_project.get_id(),
        main_branch=main_branch,
        full_path=gl_project.path_with_namespace,
        full_name=full_name,
 #       ws_full_name=ws_full_name,
        branches=my_branches,
        tags=tags,
        uid=uid,
        alt_uids=alt_uids,
        is_home=gl_project.namespace["kind"]!="group",
    )

#    if ret.is_home:
#        print(ret)

    return ret
