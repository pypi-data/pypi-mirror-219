# sync.py - handles gitlab syncing
import os
import re
import sys
import yaml
import time

import pygit2
import gitlab
import pydantic
import requests

from gcln2 import db
from gcln2 import helpers
from gcln2 import yaml_loader


class SchemaServerDefServer(pydantic.BaseModel):

    class Config:
        extra = pydantic.Extra.forbid

    api_url: str
    git_url: str
    api_key: str


class SchemaServerDef(pydantic.BaseModel):

    class Config:
        extra = pydantic.Extra.forbid

    main: bool = False
    server: SchemaServerDefServer
    cache_file: str


class SchemaCtrl(pydantic.BaseModel):

    class Config:
        extra = pydantic.Extra.forbid

    num_threads: int = 0
    branch_whitelist: list[str] = []
    branch_blacklist: list[str] = []
    uid_blacklist: list[str] = []

class SchemaSyncCfg(pydantic.BaseModel):

    class Config:
        extra = pydantic.Extra.forbid

    servers: dict[str, SchemaServerDef]
    ctrl: SchemaCtrl

class SyncLocalInfo:
    def __init__(self, controlfile):
        d = yaml.load(controlfile, Loader=yaml_loader.IncludeLoader)
        self.root_path = os.path.split(controlfile.name)[0]
        self.cfg_sync = SchemaSyncCfg(**d)

        self.repos_path = os.path.join(self.root_path, "repos")
        if not os.path.exists(self.repos_path):
            os.mkdir(self.repos_path)

        self.branch_whitelist = [
            re.compile(b) for b in self.cfg_sync.ctrl.branch_whitelist
        ]
        self.branch_blacklist = [
            re.compile(b) for b in self.cfg_sync.ctrl.branch_blacklist
        ]


    def is_branch_ok(self, branch_name: str) -> bool:
        # TODO: check MinimalUpdateContext, has the same.
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


class SyncConnector:

    def __init__(
        self,
        server_def: SchemaServerDef,
        num_threads: int,
        update_all: bool,
        sli: SyncLocalInfo,
    ):
        master = server_def.main
        root_path = sli.root_path

        self.server_def = server_def
        self.master = master
        self.map_uid2project: dict[str, db.Project] = {}
        fn = os.path.join(root_path, server_def.cache_file)
        if update_all:
            self.cache = db.Cache()
            self.cache.filename = fn
        else:
            self.cache = db.Cache.load(fn, allow_missing=True)
            self.cache.clean_branch_names(
                sli.cfg_sync.ctrl.branch_whitelist, sli.cfg_sync.ctrl.branch_blacklist
            )
        self.uid_blacklist = sli.cfg_sync.ctrl.uid_blacklist
        self.cache.remove_uids(self.uid_blacklist)
        session = requests.Session()

        # testing revieled that we need one more than nr of threads.
        # The session.mount is requests magic to reconfigure things:
        n = max(5, num_threads + 1)
        session.mount("https://", requests.adapters.HTTPAdapter(pool_maxsize=n))
        session.mount("http://", requests.adapters.HTTPAdapter(pool_maxsize=n))
        self.gl: gitlab.Gitlab = gitlab.Gitlab(
            server_def.server.api_url,
            private_token=server_def.server.api_key,
            keep_base_url=True,  # important as it might be via ssh tunnel or similar
            session=session,
        )
        self.group_cache: dict[str, gitlab.Group] = {}  # key is path.
                                                        # This is just a cache, not complete set

    def update_cache_from_server(self, num_threads: int, wh, bl):
        self.cache.update_cache_from_server(self.gl, num_threads, wh, bl)
        self.cache.remove_uids(self.uid_blacklist)
        self.map_uid2project = self.cache.build_uid_map()



def create_project(
    sli: SyncLocalInfo, c_from: SyncConnector, c_to: SyncConnector, uid: str
):
    src_proj = c_from.map_uid2project[uid]
    if not src_proj.main_branch:
        print(
            f"Project f{src_proj.full_path} doesn't have a main/master branch - ignore it"
        )
        return
    if src_proj.is_home:
        print(f"Project f{src_proj.full_path} is a home - ignore it")
        return

    if not "/" in src_proj.full_path:
        return  #  skip root projects

    # src_proj_nr: int = src_proj.project_id
    namespace = src_proj.full_path.rsplit("/", maxsplit=1)[0]
    names = src_proj.full_name.split("/")
    # print(namespace)

    # parent_group = c_from.gl.namespaces.get(namespace)
    # print(parent_group)

    # TODO: should also consider renames of namespaces... Maybe need to cache them? Or just heuristics? Ie, if a known project has another namespace, compare with master server.
    # if all projects in the namespaces matches projects on sync server/old path, then rename?
    splt = namespace.split("/")
    path = ""
    parent_group = None
    for i, s in enumerate(splt):
        if path:
            path += "/"
        path += s
        if path in c_to.group_cache:
            parent_group = c_to.group_cache[path]
            continue
        try:
            parent_group = c_to.group_cache[path] = c_to.gl.namespaces.get(path)
        except gitlab.exceptions.GitlabGetError:
            # not available on target server
            print("Not in target, need to create namespace first", path)
            if not parent_group:
                print("create group", s, names[i])
                group = c_to.gl.groups.create({"name": names[i], "path": s})
            else:
                print("create group", s, names[i], parent_group)
                group = c_to.gl.groups.create(
                    {
                        "name": names[i],
                        "path": s,
                        "parent_id": parent_group.get_id(),
                    }
                )
            parent_group = c_to.group_cache[path] = group

    #  have the parent group. Now create the project
    name = src_proj.full_name.split("/")[-1]
    path = src_proj.full_path.split("/")[-1]

    if path[0] in "_" or path[-1] in "_":
        print(f"Must change path {src_proj.full_path}, invalid with newer gitlabs")
        return

    local_path = os.path.join(sli.repos_path, src_proj.uid)
    if not os.path.exists(local_path):
        # no local copy of the project, so cannot push it up. Then don't create it either
        return


    for p in c_to.cache.projects.values():
        if p.full_path == src_proj.full_path:
            print(
                f"Dst project path {p.full_path } already exists, but probably missing _config branch. Try to push"
            )
            break
    else:
        print(f"Create project on server {path} with name {name}")
        try:
            gl_project = c_to.gl.projects.create(
                {"name": name, "namespace_id": parent_group.get_id(), "path": path}
            )
        except:
            print("*" * 80)
            print(f"ERROR: couldn't create project {src_proj.full_path} {name} {path}")
            print("*" * 80)
            return
    print(f"** push {name} to {path}")
    url = c_to.server_def.server.git_url + "/" + src_proj.full_path + ".git"
    helpers.cmd(["git", "push", url, "*:*"], work_dir=local_path, raise_exception=False)


def remove_local_bad_branches(
    sli: SyncLocalInfo,
    repo: pygit2.Repository | str,
) -> dict[str, str]:
    branches = {}
    try:
        if isinstance(repo, str):
            rep = pygit2.Repository(repo)
        else:
            rep = repo
        for b in rep.branches:
            if b.startswith("origin/"):
                if sli.is_branch_ok(b[7:]):
                    branches[b] = rep.branches[b].raw_target
                    continue
            else:
                if sli.is_branch_ok(b):
                    branches[b] = rep.branches[b].raw_target
                    continue
            print(f"*** Deleting local branch {b} in {rep.path}")
            rep.branches.delete(b)
        return branches
    finally:
        if isinstance(repo, str):
            rep.free()


def main_sync(args):
    sli = SyncLocalInfo(args.controlfile)

    nt = sli.cfg_sync.ctrl.num_threads
    main_connector = None
    connectors: list[SyncConnector] = []
    for name, s in sli.cfg_sync.servers.items():
        c = SyncConnector(s, nt, args.all, sli)
        if c.server_def.main:
            if main_connector:
                raise Exception("several main servers")
            main_connector = c
        connectors.append(c)

    print(connectors)
    # update cache from servers
    for c in connectors:
        # when we started. Used when save cache. As gitlab caches the statitics, we add 30 minutes margin.
        ts = time.time() - 30 * 60
        print("Updating from", c.server_def.server.api_url)
        c.update_cache_from_server(
            sli.cfg_sync.ctrl.num_threads,
            sli.cfg_sync.ctrl.branch_whitelist,
            sli.cfg_sync.ctrl.branch_blacklist,
        )
        print("projects:", len(c.cache.projects), len(c.map_uid2project))
        c.cache.save(ts)

    if main_connector:
        c1 = main_connector
        for c2 in connectors:
            if c2 == c1:
                continue
            uids_1 = set(c1.map_uid2project.keys())
            uids_2 = set(c2.map_uid2project.keys())
            common = uids_1 and uids_2
            for co in common:
                p1 = c1.map_uid2project[co]
                p2 = c2.map_uid2project[co]
                if p1.full_name != p2.full_name or p1.full_path != p2.full_path:
                    print(
                        f"differs {p1.full_name} {p2.full_name}  or  {p1.full_path} {p2.full_path}"
                    )
                lastpath_1 = p1.full_path.split("/")[-1]
                lastpath_2 = p2.full_path.split("/")[-1]
                lastname_1 = p1.full_name.split("/")[-1]
                lastname_2 = p2.full_name.split("/")[-1]
                change = False

                if lastname_1 != lastname_2:
                    change = True
                elif lastpath_1 != lastpath_2:
                    change = True
                elif p1.full_path != p2.full_path:
                    # neither last name nor path differs, but full path. Ie, see if we can move it.
                    group_name = p1.full_path[: -len(lastpath_1) - 1]
                    try:
                        c2group = c2.gl.groups.get(group_name)
                        # c2group = c2.gl.namespaces.get(group_name)
                        print("Target grp exists, move project")
                        gl_proj = c2.gl.projects.get(p2.project_id)
                        # print(gl_proj)
                        c2group.transfer_project(p2.project_id)
                    except gitlab.exceptions.GitlabGetError:
                        print("  Missing target grp")

                # else:
                  #  print("=>Same?", p1.full_name, p2.full_name)
                if change:
                    gl_proj = c2.gl.projects.get(p2.project_id)
                    # print(gl_proj)
                    gl_proj.name = lastname_1
                    gl_proj.path = lastpath_1
                    gl_proj.save()




    # pull all repos from server to local storage:

    def get_local_project_info(uid: str) -> db.Project | None:
        # helper function to query local bare repo.
        path =  os.path.join(sli.repos_path, uid)
        try:
            repo = pygit2.Repository(path)
        except:
            print("**ERROR: bad repository in {path}. Try to remove it")
            helpers.rmtree_with_permissions(path)
            return None
        try:
            branches = set()
            for b in repo.branches:
                b2 = b
                if b.startswith("origin/"):
                    b2 = b[7:]
                if sli.is_branch_ok(b2):
                    branches.add(b2)
                else:
                    print(f"*** Deleting local branch {b} in {uid}")
                    repo.branches.delete(b)
            # print(branches)
            ret = db.Project(
                project_id=0,
                main_branch="",
                full_path="",
                full_name="",
                branches={},
                tags={},
                uid=uid,
                alt_uids=[],
                is_home=False,
            )
            if "main" in branches:
                ret.main_branch = "main"
            elif "master" in branches:
                ret.main_branch = "master"
            else:
                return None
            for b in branches:
                if b in repo.branches:
                    br = repo.branches[b]
                elif "origin/" + b in repo.branches:
                    br = repo.branches["origin/" + b]
                else:
                    print("*** Missing", b, list(repo.branches))
                    continue
                ret.branches[b] = db.Branch(
                    name=b,
                    commit=str(br.raw_target),
                    submodules={},
                )
            return ret
        except:
            print("ERROR* " * 20)
            print(branches)
            raise
        finally:
            repo.free() # important to free resource


    changed_uids = set()
    # setup a local cache of our local bare repos status. Ie, this is a local shared database of repos.
    local_cache: dict[str, db.Project] = {}
    for c in connectors:
        print("pulling from:", c.server_def.server.git_url)
        for uid, proj in c.map_uid2project.items():
            dirpath: str = os.path.join(sli.repos_path, uid)
            url = c.server_def.server.git_url + "/" + proj.full_path + ".git"

            if not os.path.exists(dirpath):
                #  note we check for _config here due to cache can have it. Recent cache update should not populate _config into main_branch
                if proj.main_branch and proj.main_branch != "_config":
                    print(f"* Cloning {uid} from {url} ({proj.main_branch})")
                    helpers.cmd(
                        ["git", "clone", "--bare", url, uid], work_dir=sli.repos_path
                    )
                    remove_local_bad_branches(sli, dirpath)
                    lprj = get_local_project_info(uid)
                    if lprj:
                        local_cache[uid] = lprj
                        changed_uids.add(uid)
                else:
                    print(f"* {url} doesn't have a main branch")
            else:
                if uid in local_cache:
                    lprj = local_cache[uid]
                else:
                    lprj = get_local_project_info(uid)
                    if not lprj:
                        print(
                            f"***Error: dir exists but found no primary branch: {uid}"
                        )
                        if 1:
                            print("=> remove it so we can handle it next time")
                            helpers.rmtree_with_permissions(dirpath)
                        continue
                    local_cache[uid] = lprj

                remote_branches = set(proj.branches.keys())
                local_branches = set(lprj.branches.keys())
                update = False
                for b in remote_branches.intersection(local_branches):
                    if proj.branches[b].commit != lprj.branches[b].commit:
                        update = True
                        break
                if remote_branches - local_branches:
                    print("Missing from remote", remote_branches - local_branches)
                    print("**", remote_branches)
                    print("**", local_branches)
                    update = True
                if local_branches-remote_branches:
                    # consider to have several update flags. When set below, it will make a new explicit fetch to local cache. But actually, we only want to make a push. Also, maybe remember to which server.
                    print("Missing to remote", local_branches-remote_branches)
                    print("**", remote_branches)
                    print("**", local_branches)
                    update = True
                if 0 and uid == "7DB2BB830DF62AA2":
                    print ("-"*40)
                    print (c.server_def)
                    print (update)
                    print(local_branches)
                    print(remote_branches)
                    print(local_branches-remote_branches)
                    print(remote_branches-local_branches)
                    print ("-"*40)
                if update:
                    try:
                        helpers.cmd(["git", "fetch", url, "*:*"], work_dir=dirpath)
                    except:
                        print(f"*SYNC error, diverged branches {uid} {proj.full_name}")
                    remove_local_bad_branches(sli, dirpath)
                    p = get_local_project_info(uid)
                    if p:
                        changed_uids.add(uid)
                        local_cache[uid] = p

    # now cross check what is different:
    # check cross sync
    for c_from in connectors:
        for c_to in connectors:
            if c_to == c_from:
                continue
            uids_from = set(c_from.map_uid2project.keys())
            uids_to = set(c_to.map_uid2project.keys())
            missing = uids_from - uids_to
            changed_uids |= missing


    for uid in changed_uids:
        for c in connectors:
            if uid not in c.map_uid2project:
                for c_from in connectors:
                    if uid in c_from.map_uid2project:
                        break
                else:
                    raise Exception(
                        "Should not happen - found missing uid, but no server has it"
                    )

                print(
                    f"missing {uid} ({c_from.map_uid2project[uid].full_name}), trying to add it to {c.server_def.server.api_url}"
                )
                create_project(sli, c_from, c, uid)
            else:
                for br in local_cache[uid].branches.values():
                    brs = c.map_uid2project[uid].branches
                    if (br.name not in brs) or br.commit != brs[br.name].commit:
                        url = c.server_def.server.git_url + "/"
                        url += c.map_uid2project[uid].full_path + ".git"
                        lpath = os.path.join(sli.repos_path, uid)
                        try:
                            print(f"Pushing {uid} to {url} ({br.name})")
                            helpers.cmd(["git", "push", url, "--all"], work_dir=lpath)
                        except:
                            print(f"***Failed to push {uid} to {url}")
                        break





# helper commands to copy from other tree - just to speed up a little. Normally not used.
# can probably be removed. Ie, copies from gcln2 update tree into flat old type of tree (cache of sync). Also some issues with refs from this type (and origin etc).
def local_sync_copy(args):
    print(args)
    sli = SyncLocalInfo(args.sync_ctrlfile)
    print(sli)
    src_cache = db.Cache.load(args.cache_file, allow_missing=False)
    src_root = os.path.abspath(os.path.split(args.cache_file)[0])
    uid_map = src_cache.build_uid_map()
    for uid, proj in uid_map.items():
        print(uid)
        # TODO: need to fix ws replace logic
        src = os.path.join(src_root, proj.full_name)
        dst = os.path.join(sli.repos_path, uid)
        if not os.path.exists(src):
            print("Strange, missing source {src} - ignoring")
            continue
        print(src)
        print(dst)
        if not os.path.exists(dst):
            helpers.cmd(
                ["git", "clone", "--bare", src, uid], work_dir=sli.repos_path, retries=1
            )
            # note we do a fetch too, to make sure we get all branches.
        helpers.cmd(["git", "fetch", src, "*:*"], work_dir=dst, retries=1)



REPLACE_NAMESPACE = {
    "src/SW/SW0014-Panther": "rd/src/SW/SW0014-Panther",
    "src/SW/SW0032-GenIV_test_SW": "rd/src/SW/SW0032-GenIV_test_SW",
    "src/SW/SW0035-PrototypeTesting" : "rd/src/SW/SW0035-PrototypeTesting",
    "src/SW/SW0041-PC_Software/_old" : "rd/src/SW/SW0041-PC_Software/_old",
    "jt_projects" : "rd/projects/_old",
}

def main_p_push_from_raw(args):
    ts = time.time() - 30 * 60
    sli = SyncLocalInfo(args.sync_ctrl)
    print(sli.cfg_sync)

    nt = sli.cfg_sync.ctrl.num_threads
    conn =  SyncConnector(sli.cfg_sync.servers[args.server], nt, False, sli)
    conn.update_cache_from_server(
        sli.cfg_sync.ctrl.num_threads,
        sli.cfg_sync.ctrl.branch_whitelist,
        sli.cfg_sync.ctrl.branch_blacklist,
    )
    print("projects:", len(conn.cache.projects), len(conn.map_uid2project))
    conn.cache.save(ts)

    with open(args.uid_map, "rt") as fh:
        uids = fh.read().split("\n")
    # print(uids)
    legacy_uid_map = {}
    for l in uids:
        l = l.strip()
        if not l or l[0] == "#":
            continue
        typ, uid, branch, rest = l.split(maxsplit=3)
        if typ != "git":
            continue
        if branch not in ["master", "main"]:
            continue
        m = re.compile(r'"(.*)"').match(rest)
        if not m or not m.group(1):
            continue
        print(uid, branch, m.group(1))
        legacy_uid_map[uid] = m.group(1)

    print("-" * 40)
    cache_namespaces = {}
    for i, uid_path in enumerate(os.listdir(args.raw_dir)):
#        if i > 10:
#            break

        if uid_path.endswith(".git"):
            uid = uid_path[:-4]
        else:
            uid = uid_path

        if uid in conn.map_uid2project:
            # already exists, ignore
            # print(conn.map_uid2project[uid])
            # print("Not Done!")
            continue
        else:
            if uid in legacy_uid_map:
                path = legacy_uid_map[uid]
            else:
                path = "old_uids/" + uid
            if path.startswith("projects"):
                path = "jt_" + path
            if not "/" in path:
                path = "old_uids/" + path

            namespace, project_path = path.rsplit("/", maxsplit=1)
            if namespace in REPLACE_NAMESPACE:
                namespace = REPLACE_NAMESPACE[namespace]
            name = project_path
            if project_path.startswith("_"):
                project_path = "x" + project_path
                if project_path.endswith("_"):
                    project_path = project_path + "x"
            # print(path, namespace)
            try:
                if namespace in cache_namespaces:
                    parent_group = cache_namespaces[namespace]
                else:
                    parent_group = conn.gl.namespaces.get(namespace)
                    cache_namespaces[namespace] = parent_group
            except:
                print(f"Failed to get namespace {namespace}")
                continue

            repo = pygit2.Repository(uid_path)
            print (repo)
            _cfg1 = "refs/remotes/origin/_config"
            _cfg2 = "refs/heads/_config"
            if _cfg1 not in repo.references and _cfg2 not in repo.references:
                print ("Repo needs an UID. Please run gcln2 set_uid")
                print ("Found:", list(repo.references))
                cfg_data = {
                    "uid": uid,
                }
                print (cfg_data)
                if 1:
                    person = (repo.config["user.name"], repo.config["user.email"])
                    tree = repo.TreeBuilder()
                    attr_oid = repo.create_blob(yaml.safe_dump(cfg_data).encode("utf8"))
                    tree.insert("attributes.yaml", attr_oid, pygit2.GIT_FILEMODE_BLOB)
                    tree_oid = tree.write()
                    signature = pygit2.Signature(*person)   # "system","system@none")
                    parents = []
                    comm_oid = repo.create_commit("refs/heads/_config", signature, signature, "create _config", tree_oid, parents)

            repo.free()

            print(f"Creating project {project_path} in {namespace}")
            try:
                if 0:
                    # don't need to do this - can push directly on gitlab
                    gl_project = conn.gl.projects.create(
                        {
                            "name": name,
                            "namespace_id": parent_group.get_id(),
                            "path": project_path,
                        }
                    )
            except:
                print(f"Failed to create {path}")
            url = (
                conn.server_def.server.git_url
                + "/"
                + namespace
                + "/"
                + project_path
                + ".git"
            )
            local_path = os.path.join(args.raw_dir, uid_path)
            print(local_path, url)
            helpers.cmd(["git", "push", url, "*:*"], work_dir=local_path)

    print("Done")



