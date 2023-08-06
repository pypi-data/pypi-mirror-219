"""
Every piece of functionality to resolve dependencies and information about
crates is in this module.
While `crate` module is about building crates, and `config` module
is about producing configs, `resolver` is a bridge from `config` to a `crate`.

Example
=======

::
    import os
    from crateman.resolver import ResolverState

    resolver_state = ResolverState(cratedir=f"{os.getcwd()}/crates")
    resolver_state.resolve(config, os.getcwd())
    crate = resolver_state.extract(config.root_header.name)
"""

import re

from crateman import log
from crateman.config import Config, Header, Action, parse_file, \
                            ActionOnEnv, ActionAlways, ActionOnDep, ActionOnProfile
from crateman.crate import Crate
from crateman.exception import CratemanException

CFG_FILENAME = "crateman.toml"
RE_EVERY_VERSION = re.compile(".*")


class WrongCrate(CratemanException):
    def __init__(self, path: str, expected: str, got: str):
        self.path = path
        self.expected = expected
        self.got = got
        super().__init__(8)

    def __str__(self) -> str:
        return f"At path {self.path}: expected to find crate {self.expected}, got {self.got}"


class CrateNotFound(CratemanException):
    def __init__(self, path: str, err: OSError):
        self.path = path
        self.err = err
        super().__init__(9)

    def __str__(self) -> str:
        return f"At path {self.path}: crate not found due to OS error: {self.err}"


class InvalidPath(CratemanException):
    def __init__(self):
        super().__init__(10)

    def __str__(self) -> str:
        return "Path to crate can not be an empty string!"


class InvalidCrateExtract(CratemanException):
    def __init__(self, crate: str):
        self.crate = crate
        super().__init__(11)

    def __str__(self) -> str:
        return f"Can not extract crate {self.crate} if it wasn't processed"


class InvalidVersion(CratemanException):
    def __init__(self, parent: str, dep: str, expected: re.Pattern, got: str):
        self.parent   = parent
        self.dep      = dep
        self.expected = expected
        self.got      = got
        super().__init__(12)

    def __str__(self) -> str:
        return f"Crate {self.parent} expected version of {self.dep} match {self.expected.pattern}, but got {self.got}"


class State:
    UNDEFINED  = -1
    UNCHARTED  = 0
    DISCOVERED = 1
    PROCESSED  = 2


class CrateInfo:
    """
    Temporary presentation of a crate.
    Not used alone, but rather inside `ResolverState` class
    """

    def __init__(self):
        self.path      = None
        self.env       = dict[str, set[str]]()
        self.deps      = list[str]()
        self.version   = None
        self.build_cmd = None
        self.state     = State.UNCHARTED
        self.required_versions = dict[str, re.Pattern]()

    def add_action(self, action: Action):
        if self.state < State.DISCOVERED and action.path is not None:
            self.path = action.path

        for i in action.env.unset_op:
            if i in self.env:
                _ = self.env.pop(i)

        for i, v in action.env.sub.items():
            value = self.env.get(i)
            if value is None: continue

            value.difference_update(v)

        for i, v in action.env.set_op.items():
            self.env[i] = v

        for i, v in action.env.add.items():
            value = self.env.get(i)
            if value is None:
                self.env[i] = set[str]()
                value = self.env[i]

            value.update(v)

        self.deps = [j for j in self.deps if j not in action.deps.sub]
        self.deps += action.deps.add

        for i, v in action.accept_version.items():
            self.required_versions[i] = re.compile(v)


class ResolverState:
    """
    Stores information about crates, their dependencies and version requirements.
    Can add more information from configs, or give you a fully functional crate,
    suitable for building.

    Main methods
    ============
    - `resolve`: create a complete dependency tree from just one config
    - `extract`: get a crate

    Everything else is not supposed for manual usage
    """

    def __init__(self, cratedir: str, profile: str = "default"):
        """
        Parameters
        ==========
        - `cratedir` (str):
        An *absolute* path to a directory where all crates without
        fixed path will be searched

        - `profile` (str):
        Toggles various actions' conditions.
        Can be any string
        """

        self.cratedir = cratedir
        self.profile  = profile
        self.crate_infos = dict[str, CrateInfo]()

    def get_crate_state(self, crate_name: str) -> int:
        crate_info = self.crate_infos.get(crate_name)
        return State.UNDEFINED if crate_info is None else crate_info.state

    def discover(self, path: str, header: Header):
        """
        Internal use: discovers a crate at path.
        Overwrites the header if it was already discovered
        """

        if header.name not in self.crate_infos:
            self.crate_infos[header.name] = CrateInfo()

        crate_info = self.crate_infos[header.name]
        if crate_info.state >= State.DISCOVERED:
            log.warn(f"Refusing to rediscover already discovered crate {header.name} at {path}")
            return

        crate_info.path      = path
        crate_info.version   = header.version
        crate_info.build_cmd = header.build_cmd
        crate_info.state = State.DISCOVERED

    def add_config(self, config: Config, config_dir: str):
        """
        Internal use: add a single config to the deptree.
        Does not proceed to dependencies.
        """

        self.discover(config_dir, config.root_header)

        for i, v in config.discoveries.items():
            path = i
            if len(path) == 0:
                raise InvalidPath()
            if path.find('/') == -1:
                path = f"{self.cratedir}/{path}"
            elif path[0] != '/':
                path = f"{config_dir}/{path}"
            self.discover(path, v)

        for cond, actions in config.actions:
            if not cond.verify(self):
                continue

            for crate_name, action in actions.items():
                crate_info = self.crate_infos.get(crate_name)
                if crate_info is None:
                    crate_info = CrateInfo()
                    self.crate_infos[crate_name] = crate_info

                if crate_info.state >= State.PROCESSED:
                    continue

                crate_info.add_action(action)

        self.crate_infos[config.root_header.name].state = State.PROCESSED

    def resolve(self, config: Config, config_dir: str):
        """
        Add a config to the deptree, then process all dependencies of a root crate.
        If dependency wasn't discovered, `resolve` it as well.

        Parameters
        ==========
        - `config` (Config):
        self-explanatory.

        - `config_dir` (str):
        An *absolute* path to directory where that `config` was found.
        `config_dir` will be treated like root crate's location.

        Raises
        ======
        - `WrongCrate`
        - `CrateNotFound`
        - `InvalidPath`
        """

        self.add_config(config, config_dir)

        name = config.root_header.name
        for i in self.crate_infos[name].deps:
            if self.get_crate_state(i) >= State.DISCOVERED:
                self.crate_infos[i].state = State.PROCESSED
                continue

            dep_path = None
            dep_info = self.crate_infos.get(i)
            if dep_info is None or dep_info.path is None:
                dep_path = f"{self.cratedir}/{i}"
            else:
                dep_path = dep_info.path
            if len(dep_path) == 0 or dep_path[0] != '/':
                dep_path = f"{config_dir}/{dep_path}"

            filepath = f"{dep_path}/{CFG_FILENAME}"
            dep_config = None
            try:
                with open(filepath, "r") as f:
                    dep_config = parse_file(f)
            except OSError as e:
                raise CrateNotFound(dep_path, e) from None

            if dep_config.root_header.name != i:
                raise WrongCrate(dep_path, i, dep_config.root_header.name)
            self.resolve(dep_config, dep_path)

    def extract(self, crate_name: str,
                cache: dict[str, Crate] = {}) -> Crate:
        """
        Extracts an actual crate from resolved state.

        Parameters
        ==========
        - `crate_name` (str):
        Name of a crate we want to get

        - `cache` (dict[str, Crate]):
        Maps already extracted crates' names to values.
        Is not supposed to be set manually, just stick with `{}`

        Raises
        ======
        - `InvalidCrateExtract`
        - `InvalidVersion`
        """

        if crate_name in cache:
            return cache[crate_name]

        crate_info = self.crate_infos.get(crate_name)
        if crate_info is None or crate_info.state < State.PROCESSED:
            raise InvalidCrateExtract(crate_name)

        crate = Crate(crate_name, crate_info.version,
                      crate_info.build_cmd, crate_info.path)
        crate.env = {i: ' '.join(v) for i, v in crate_info.env.items()}
        crate.env['PROFILE'] = self.profile

        cache[crate_name] = crate
        for i in crate_info.deps:
            version_req = crate_info.required_versions.get(i)
            if version_req is None:
                version_req = RE_EVERY_VERSION

            dep_info = self.crate_infos.get(i)
            if dep_info is None:
                raise InvalidCrateExtract(i)

            match = version_req.match(dep_info.version)
            if match is None or match.end() < len(dep_info.version):
                raise InvalidVersion(crate_name, i, version_req, dep_info.version)

            dep_crate = self.extract(i, cache)
            crate.deps.append(dep_crate)

        return crate


def always_verify(_self: ActionAlways, _state: ResolverState) -> bool:
    return True


def on_profile_verify(self: ActionOnProfile, state: ResolverState) -> bool:
    return self.profile == state.profile


def on_env_verify(self: ActionOnProfile, state: ResolverState) -> bool:
    try:
        return self.value in state.crate_infos[self.crate].env[self.key]
    except KeyError:
        return False


def on_dep_verify(self: ActionOnProfile, state: ResolverState) -> bool:
    try:
        return self.dep in state.crate_infos[self.crate].deps
    except KeyError:
        return False


ActionAlways.verify = always_verify
ActionOnProfile.verify = on_profile_verify
ActionOnEnv.verify = on_env_verify
ActionOnDep.verify = on_dep_verify
