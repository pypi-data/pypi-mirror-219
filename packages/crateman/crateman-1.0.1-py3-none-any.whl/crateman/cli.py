import os
import re

from sys import stdout, argv

from crateman import log, config, resolver
from crateman.crate import Crate
from crateman.exception import CratemanException


BUILD_FUNC = Crate.build


class Args:
    LOG_LEVEL_RE = re.compile(r'log=([0-5])')
    COLOR_RE = re.compile(r'color=([0-1])')
    USAGE_MSG = "Usage: crateman [log=(0-5)] [color=(0-1)]"

    def __init__(self):
        self.log_level = 4
        self.colors = None
        self.help = False
        self.deps_only = False

    def apply(self) -> bool:
        log_nothing = lambda x: ()
        if self.log_level < 5:
            log.dbg = log_nothing
        if self.log_level < 4:
            log.info = log_nothing
        if self.log_level < 3:
            log.ok = log_nothing
        if self.log_level < 2:
            log.warn = log_nothing
        if self.log_level < 1:
            log.err = log_nothing

        if self.colors is not None:
            if self.colors:
                log.colors_enable()
            else:
                log.colors_disable()

        if self.deps_only:
            BUILD_FUNC = Crate.build_deps

        if self.help:
            log.info(Args.USAGE_MSG)
            return False

        return True

    def parse(self, args: list[str]):
        for i in args:
            match = Args.LOG_LEVEL_RE.match(i)
            if match is not None:
                self.log_level = int(match.group(1))
                continue

            match = Args.COLOR_RE.match(i)
            if match is not None:
                self.colors = bool(int(match.group(1)))
                continue

            if i == "help":
                self.help = True
                continue

            if i == "deps_only":
                self.deps_only = True
                continue


class EnvUndefined(CratemanException):
    def __init__(self, key: str):
        self.key = key
        super().__init__(12)

    def __str__(self) -> str:
        return f"Environment variable {self.key} undefined"


def crateman_error_handler(f) -> int:
    try:
        f()
        return 0
    except CratemanException as e:
        log.err(f"{e}")
        return e.exit_code


def crateman():
    if os.isatty(stdout.fileno()):
        log.colors_enable()

    args = Args()
    args.parse(argv)
    if not args.apply():
        return

    log.dbg("Successfully parsed command-line arguments")

    cwd = os.getcwd()

    log.dbg(f"Looking for {resolver.CFG_FILENAME} in cwd...")
    try:
        f = open(resolver.CFG_FILENAME, 'r')
    except OSError as e:
        raise resolver.CrateNotFound(cwd, e) from None

    log.dbg("Converting file into raw config...")
    raw_config = config.file_to_raw(f)
    f.close()

    log.dbg("Converting raw config into normal config...")
    cfg = config.raw_to_config(raw_config)

    log.ok("Acquired config from current directory")

    log.dbg("Getting environment variables...")

    profile = os.getenv('PROFILE') or 'default'
    log.dbg(f"profile = {profile}")

    cratesdir = os.getenv('CRATESDIR')
    if cratesdir is None:
        raise EnvUndefined('CRATESDIR')
    if len(cratesdir) == 0 or cratesdir[0] != '/':
        cratesdir = f"{cwd}/{cratesdir}"
    log.dbg(f"cratesdir = {cratesdir}")

    log.dbg("Resolving dependencies...")
    resolver_state = resolver.ResolverState(cratedir=cratesdir, profile=profile)
    resolver_state.resolve(cfg, cwd)

    log.dbg("Extracting crate...")
    crate = resolver_state.extract(cfg.root_header.name)
    crate.check()

    log.ok("Successfully resolved dependencies")

    outdir = os.getenv('OUTDIR')
    if outdir is None:
        raise EnvUndefined('OUTDIR')
    if len(outdir) == 0 or outdir[0] != '/':
        outdir = f"{cwd}/{outdir}"
    log.dbg(f"outdir = {outdir}")

    BUILD_FUNC(crate, outdir)

    log.ok("Successfully built all crates")


def crateman_entry() -> int:
    return crateman_error_handler(crateman)
