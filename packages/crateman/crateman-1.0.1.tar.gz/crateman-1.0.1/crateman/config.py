"""
::

    from crateman.config import file_to_raw, raw_to_config

    # Opening the supposed file
    f = open("crateman.toml", "r")

- Detailed way::

    raw = file_to_raw(f)
    config = raw_to_config(raw)

- Shortcut::

    config = parse_file(f)

"""

import re
import toml

from io import TextIOWrapper

from crateman import log
from crateman.exception import CratemanException

table_header_re = re.compile(r"^\[([^\[\]]*)\][^\[\]]*$")


class ActionCondition:
    """Base class for determining whether to execute action or not"""


class ActionAlways(ActionCondition):
    """Always execute"""


class ActionOnProfile(ActionCondition):
    """Execute only if specific profile is set"""

    def __init__(self, profile: str):
        self.profile = profile


class ActionOnEnv(ActionCondition):
    """Execute only if specific crate has specific environment variable's value"""

    def __init__(self, crate: str, key: str, value: str):
        self.crate = crate
        self.key = key
        self.value = value


class ActionOnDep(ActionCondition):
    """Execute only if specific crate has specific dependency"""

    def __init__(self, crate: str, dep: str):
        self.crate = crate
        self.dep = dep


class Header:
    """A crate without this header can not be considered a crate."""

    def __init__(self, name: str, version: str, build_cmd: str):
        self.name = name
        self.version = version
        self.build_cmd = build_cmd


class EnvAction:
    """
    Modifies the environment of any crate.

    Attributes
    ==========
    - `unset_op` (list[str]):
    Keys to completely remove from environment

    - `sub` (dict[str, list[str]]):
    Maps keys to what values should be removed from variable's set

    - `set_op` (dict[str, list[str]]):
    Maps keys to what values they need to be set to

    - `add` (dict[str, list[str]]):
    Maps keys to what values should be added to variable's set

    Order of execution
    ==================
    `unset_op` -> `sub` -> `set_op` -> `add`
    """

    def __init__(self):
        self.unset_op = list[str]()
        self.sub = dict[str, list[str]]()
        self.set_op = dict[str, list[str]]()
        self.add = dict[str, list[str]]()


class DepAction:
    """
    Modifies dependencies of any crate.

    Attributes
    ==========
    - `sub` (list[str]):
    Dependencies to remove

    - `add` (list[str]):
    Dependencies to add

    Order of execution
    ==================
    `sub` -> `add`
    """

    def __init__(self):
        self.sub = list[str]()
        self.add = list[str]()


class Action:
    """
    Presents an action for resolver to execute.

    Attributes
    ==========
    - `path` (str) (optional):
    Set crate's location to specific value

    - `env` (EnvAction):
    Modify crate's environment

    - `deps` (DepAction):
    Modify crate's deps

    - `accept_version` (dict[str, str]) (optional):
    Set crate's version requirement

    Order of execution
    ==================
    `path` -> `env` -> `deps` -> `accept_version`
    """

    def __init__(self):
        self.path = None
        self.env = EnvAction()
        self.deps = DepAction()
        self.accept_version = dict[str, str]()


class Config:
    """
    This is it. This is to what config files map to.

    Attributes
    ==========
    - `root_header` (Header):
    Crate header for a crate located in config file directory (required)

    - `discoveries` (dict[str, Header]):
    Define additional crates at different paths

    - `actions` (list[(ActionCondition, dict[str, Action])]):
    List of actions for resolver to execute if a certain condition is met
    Read the type as "In order: if ActionCondition is met,
    for each mentioned crate execute corresponding action"
    """

    def __init__(self, root_header: Header):
        self.root_header = root_header
        self.discoveries = dict[str, Header]()
        self.actions = list[(ActionCondition, dict[str, Action])]()


class WrongType(CratemanException):
    """
    When the field in toml dictonary was of wrong type
    """

    def __init__(self, key: str, t: type):
        super().__init__(5)
        self.key = key
        self.t = t

    def __str__(self) -> str:
        return f"Field {self.key} is not of a type {self.t.__name__}"


class MalformedActionCondition(CratemanException):
    """
    When it is impossible to parse a string into `ActionCondition`
    """

    def __init__(self, action_str: str):
        super().__init__(6)
        self.action_str = action_str

    def __str__(self) -> str:
        return f"Malformed action declaration: {self.action_str}"


class ConfigParseError(CratemanException):
    """
    When it is impossible to parse a string into `ActionCondition`
    """

    def __init__(self, err: toml.TomlDecodeError):
        super().__init__(13)
        self.err = err

    def __str__(self) -> str:
        return f"Config file error: {self.err}"


class RawConfig:
    """
    Intermediate form of config.
    Probably won't be useful alone, but rather be passed to `raw_to_config` function.
    """

    def __init__(self):
        self.general = dict()
        self.actions = list[(ActionCondition, dict)]()


def get_required_field(d: dict, key: list[str], t: type):
    """
    Gets an element from `d` at path `key`, and checks it to be a type `t`

    Parameters
    ==========
    - `d` (dict), `t` (type): self-explanatory I think
    - `key` (list[str]):
    If `key` is ['a'], then we try to get the d['a'] element.
    If `key` is ['a', 'b'], then we try to get the d['a']['b'] element.

    Returns
    =======
    - Value of a type `t`

    Raises
    ======
    - `WrongType`
    """

    result = d
    for i in key:
        if type(result) != dict: raise WrongType('.'.join(key), t)
        result = result.get(i)

    if result is None or type(result) != t: raise WrongType('.'.join(key), t)
    return result


def get_optional_field(d: dict, key: list[str], t: type):
    """
    Same as `get_required_field`, but with one difference.

    Returns
    =======
    - Value of a type `t`, or None if this key wasn't found

    Raises
    ======
    - `WrongType`
    """

    result = d
    for i in key:
        result = result.get(i)
        if result is None: return None

    # HOTFIX: toml dicts are actually some inner local type unaccessible to us,
    # instead of dict like I thought...
    if t == dict:
        try:
            _ = result.get('key')
            return dict(result)
        except Exception:
            raise WrongType('.'.join(key), dict) from None

    if result is None or type(result) != t: raise WrongType('.'.join(key), t)
    return result


def dict_to_header(d: dict) -> Header:
    name = get_required_field(d, ['name'], str)
    version = get_required_field(d, ['version'], str)
    build_cmd = get_required_field(d, ['build'], str)

    return Header(name, version, build_cmd)


def filter_list_with_warn(l: list, t: type) -> list:
    if not all(type(i) == t for i in l):
        log.warn(f"Found a list supposed to have {t.__name__} values, but is not, ignoring")
        return []
    return l


def dict_to_env_action(d: dict) -> EnvAction:
    result = EnvAction()

    unset = get_optional_field(d, ['unset'], list)
    if unset is not None:
        log.dbg("Setting 'unset' attribute...")
        result.unset_op = filter_list_with_warn(unset, str)

    log.dbg("Looking for 'add' attribute...")
    add = get_optional_field(d, ['add'], dict)
    if add is None: add = {}
    for i, v in add.items():
        if type(v) != list: raise WrongType(f"add.{i}", list)
        result.add[i] = filter_list_with_warn(v, str)

    log.dbg("Looking for 'sub' attribute...")
    sub = get_optional_field(d, ['sub'], dict)
    if sub is None: sub = {}
    for i, v in sub.items():
        if type(v) != list: raise WrongType(f"sub.{i}", list)
        result.sub[i] = filter_list_with_warn(v, str)

    log.dbg("Looking for 'set' attribute...")
    set_op = get_optional_field(d, ['set'], dict)
    if set_op is None: set_op = {}
    for i, v in set_op.items():
        if type(v) != list: raise WrongType(f"set.{i}", list)
        result.set_op[i] = filter_list_with_warn(v, str)

    return result


def dict_to_dep_action(d: dict) -> DepAction:
    result = DepAction()

    add = get_optional_field(d, ['add'], list)
    if add is not None:
        log.dbg("Setting 'add' attribute...")
        result.add = filter_list_with_warn(add, str)

    sub = get_optional_field(d, ['sub'], list)
    if sub is not None:
        log.dbg("Setting 'sub' attribute...")
        result.sub = filter_list_with_warn(sub, str)

    return result


def dict_to_action(d: dict) -> Action:
    action = Action()

    path = get_optional_field(d, ['path'], str)
    if path is not None:
        log.dbg("Setting path...")
        action.path = path

    version = get_optional_field(d, ['accept_version'], dict)
    if version is not None:
        log.dbg("Setting version requirements...")
        for i, v in version.items():
            if type(v) != str:
                raise WrongType(f"accept_version.{i}", str)
            action.accept_version[i] = v

    env = get_optional_field(d, ['env'], dict)
    if env is not None:
        log.dbg("Setting env action...")
        try:
            action.env = dict_to_env_action(env)
        except WrongType as e:
            e.key = f"env.{e.key}"
            raise

    deps = get_optional_field(d, ['deps'], dict)
    if deps is not None:
        log.dbg("Setting deps action...")
        try:
            action.deps = dict_to_dep_action(deps)
        except WrongType as e:
            e.key = f"deps.{e.key}"
            raise

    return action


def dict_to_actions(d: dict) -> dict[str, Action]:
    actions = dict[str, Action]()

    for i, v in d.items():
        log.dbg(f'Processing action for crate "{i}"...')
        if type(v) != dict:
            raise WrongType(i, dict)

        try:
            actions[i] = dict_to_action(v)
        except WrongType as e:
            e.key = f"{i}.{e.key}"
            raise

    return actions


def toml_header_split(s: str) -> list[str]:
    def flatten(d: dict[str, str]) -> list[str]:
        keys = d.keys()
        result = list(keys)
        for i in keys:
            result += flatten(d[i])
        return result

    d = toml.loads(f"[{s}]")
    return flatten(d)


def str_to_action_condition(s: str) -> ActionCondition:

    try:
        l = toml_header_split(s)

        if l == ["*"]:
            return ActionAlways()
        if len(l) == 2 and l[0] == "profile":
            return ActionOnProfile(l[1])
        if len(l) == 4 and l[0] == "env":
            return ActionOnEnv(l[1], l[2], l[3])
        if len(l) == 3 and l[0] == "deps":
            return ActionOnDep(l[1], l[2])

        raise MalformedActionCondition(s)
    except toml.TomlDecodeError:
        raise MalformedActionCondition(s) from None


def raw_to_config(raw: RawConfig) -> Config:
    """
    Refines intermediate config into a real one.

    Raises
    ======
    - `WrongType`
    """

    log.dbg("Getting root crate's header...")
    root_header = dict_to_header(raw.general)
    config = Config(root_header)

    discover = get_optional_field(raw.general, ['discover'], dict)
    if discover is None:
        discover = {}

    for i, v in discover.items():
        log.dbg(f"Adding discovery request at {i}...")
        try:
            config.discoveries[i] = dict_to_header(v)
        except WrongType as e:
            e.key = f"discover.{i}.{e.key}"
            raise

    for cond, action_dict in raw.actions:
        log.dbg("Processing action table...")
        action = dict_to_actions(action_dict)
        config.actions.append((cond, action))

    return config


def file_to_raw(file: TextIOWrapper) -> RawConfig:
    """
    Translates contents of a `file` into an intermediate form of Config.

    Raises
    ======
    - `TomlDecodeException`
    - `MalformedAction`
    """

    lines = file.readlines()
    toml_blocks, table_headers = list[str](), list[str]()

    i = 0
    for j, v in enumerate(lines):
        match = table_header_re.match(v)
        if match is not None:
            contents = match.group(1)
            toml_blocks.append(''.join(lines[i:j]))
            table_headers.append(contents)
            i = j + 1
    toml_blocks.append(''.join(lines[i:]))

    raw_config = RawConfig()
    try:
        raw_config.general = toml.loads(toml_blocks[0])

        for i in range(1, len(toml_blocks)):
            table_header, toml_block = table_headers[i - 1], toml_blocks[i]
            tokens = toml_header_split(table_header)
            if len(tokens) == 2 and tokens[0] == 'discover':
                path = tokens[1]

                if raw_config.general.get('discover') is None:
                    raw_config.general['discover'] = dict()
                raw_config.general['discover'][path] = toml.loads(toml_block)
            else:
                cond = str_to_action_condition(table_header)
                raw_config.actions.append((cond, toml.loads(toml_block)))
    except toml.TomlDecodeError as e:
        raise ConfigParseError(e) from None

    return raw_config


def parse_file(file: TextIOWrapper) -> Config:
    """
    A shortcut from file to the whole Config. Useful if you don't need to handle
    intermediate config separately
    """

    return raw_to_config(file_to_raw(file))
