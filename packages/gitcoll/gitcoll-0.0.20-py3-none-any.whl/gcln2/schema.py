# schema

import typing
import pydantic



class GeneralServer(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid
    api_url: str
    api_key: str
    git_url: str


class General(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    server: GeneralServer
    retries: int = 0                        # for git clone/update etc, how many times to retry?
    worker_threads = 0                      # how many threads to use for cloning/update. Set to 0 to disable multithreading.


class Rules(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid
    valid_branches: str                     # regexp which branches are valid. The list is searched in order, first match is valid.
    blacklist_branches: typing.List[str]           # list of regexps
    blacklist_repo_uids: typing.List[str]          # list of explicit UIDs
    #valid_tags: str                         # regexp for valid tags


class Workspace(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    only_main: bool = False                     # only checkout main branch, ignore the _branches subdirs
    home_dir_as_login_name: bool = True         # use login name instead of full user name
    home_dir_prefix: str = ""                   # prefix home-dirs with this.
    replace: typing.Dict[str, str] = {}         # ws paths beginning with key is replaced with value
    valid_paths: typing.List[str] = []          # two cases. Either reg-exp for valid checkout paths, or, if there is a " => " in the string, also replace it. The list is searched in order, first match is valid.
    config: typing.Dict[str, str] = {}          # direct git config variables to add
    add_remotes_bare: typing.Dict[str, str] = {}    # config remotes. Keys are remote name, value is prefix to UID. Ie, for UID=123, then git remote add <key> <value>/UID.git
    add_remotes_gitlab: typing.Dict[str, str] = {}  # config remotes. Keys are remote name, value is prefix gitlab server. Ie, for repo a/b, then git remote add <key> <value>/a/b.git
    #user_name: str                              # if set, explicitly set this as user in the workspace
    #user_email: str                             # if set, explicitly set this as email in the workspace
    #add_remote_uid: typing.Dict[str, typing.Dict] = {}      # add



class MainConfig(pydantic.BaseModel):
    class Config:
        extra = pydantic.Extra.forbid

    general: General
    workspace: Workspace
    rules: Rules
