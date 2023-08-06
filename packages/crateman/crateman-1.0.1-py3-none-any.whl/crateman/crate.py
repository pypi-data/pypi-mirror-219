"""
Provides `Crate` class and functionality to build it

Example
=======

::

    from crateman.crate import Crate

    # Creating a crate structure
    root_crate = Crate("root", "1.0.0", os.getcwd(), "make")
    root_crate.env["CFLAGS"] = "-Os"
    root_crate.deps.append(Crate("dep", "2.2.8", f"{os.getcwd()}/dep", "./build.py")

    # Checking it for errors
    root_crate.check()

    # Building it
    root_crate.build(f"{os.getcwd()}/out")

"""


import os
import subprocess

from threading import Semaphore
from concurrent import futures

from crateman.exception import CratemanException
from crateman import log


class CircularDependency(CratemanException):
    def __init__(self, a: str, b: str):
        """
        Parameters
        ==========
        - `a`, `b`:
        names of crates mutually depending on each other
        """

        super().__init__(1)
        self.a = a
        self.b = b

    def __str__(self) -> str:
        return f"Circular dependency detected between {self.a} <-> {self.b}"


class DirectoryError(CratemanException):
    def __init__(self, dir: str, err: OSError):
        super().__init__(2)
        self.dir = dir
        self.err = err

    def __str__(self) -> str:
        return f"In directory {self.dir}: {self.err}"


class FileError(CratemanException):
    def __init__(self, path: str, err: OSError):
        super().__init__(3)
        self.path = path
        self.err = err

    def __str__(self) -> str:
        return f"In file {self.path}: {self.err}"


class BuildError(CratemanException):
    def __init__(self, crate_name: str, exit_code: int):
        super().__init__(4)
        self.crate_name = crate_name
        self.exit_code = exit_code

    def __str__(self) -> str:
        return f"Build process for {self.crate_name} failed with exit code {self.exit_code}"


class BuildState:
    """
    State of parallel crate build.
    Is not supposed to be used standalone, but rather passed to Crate.build function
    """

    def __init__(self):
        self.locks = dict[str, Semaphore]()
        self.mutex = Semaphore(1)

    def try_initiate_build(self, crate: str) -> Semaphore | None:
        """
        - If build of crate was not initiated, returns a `locked semaphore`.
        - Otherwise, returns `None`.
        - If someone is currently building this crate
        (holding corresponding semaphore locked),
        waits for that thread to finish and returns `None`.
        """

        self.mutex.acquire()
        try:
            if crate not in self.locks:
                self.locks[crate] = Semaphore(0)
                return self.locks[crate]
        finally: self.mutex.release()

        # Wait for job to be done
        self.locks[crate].acquire()
        self.locks[crate].release()
        return None


class Crate:
    """
    Class presenting a crate, which you can build or examine its dependencies.

    Attributes
    ==========
    - `name` (str):
    Name of a crate. Can be any string, but names must be unique across dependency graph.

    - `version` (str):
    Crate version. Serves no purpose in actual building.

    - `build_cmd` (str):
    A shell command which should be invoked in order to build a crate.

    - `path` (str):
    Location of a crate in a filesystem.
    Should be an absolute path.
    Process executing `build_cmd` will start with its working directory equal to `path`

    - `env` (dict[str, str]):
    Additional environment variables to supply to `build_cmd` process.
    Process will get the resulting environment as::
        os.environ + crate.env + {"OUT_DIR": ...}

    - `deps` (list[Crate]):
    Other crates as dependencies to this crate.
    When building, dependencies are processed from first to last element,
    in a Depth-First Search fashion.
    That means, if a crate `a` has dependencies [`b`, `c`], and `b` has [`d`],
    order of processing will be:
    `a` -> `b` -> `d` -> `c`

    Main methods
    ============
    - `build`:
    Build a crate with all its dependencies.

    - `check`:
    Check correctness of a crate's dependency graph.
    """

    def __init__(self, name: str, version: str, build_cmd: str, path: str):
        """
        Creates a crate with no additional env and no dependencies
        """

        self.name      = name
        self.version   = version
        self.build_cmd = build_cmd
        self.path      = path
        self.env       = dict[str, str]()
        self.deps      = list[Crate]()

    def build_deps(self, out_dir: str, state: BuildState = BuildState()):
        """
        Builds dependencies of a crate in parallel.
        """

        if len(self.deps) == 0:
            return

        with futures.ThreadPoolExecutor(max_workers=len(self.deps)) as executor:
            jobs = [executor.submit(Crate.build, i, out_dir, state) for i in self.deps]
            for i in jobs: i.result()

    def build(self, out_dir: str, state: BuildState = BuildState()):
        """
        Builds a crate with all of its dependencies.

        Parameters
        ==========
        - `out_dir`:
        Path to a directory where all build artifacts supposed to go.
        Must be an existing directory.

        - `state`:
        Build state which gets passed to nested invocations of build methods.
        First call should start with empty build state.

        Warning
        =======
        If dependency graph contains a circular dependency, build process will deadlock.
        Therefore, it is advised to run `self.check()` first before building.
        """

        lock = state.try_initiate_build(self.name)
        if lock is None: return

        try:
            if len(self.deps) > 0:
                log.dbg(f"Building dependencies of {self.name}...")
                self.build_deps(out_dir, state)

            log_dir = f"{out_dir}/log"
            try:
                if not os.path.exists(log_dir):
                    log.info(f"Creating log directory {log_dir}...")
                    os.mkdir(log_dir)
            except OSError as e: raise DirectoryError(e.filename, e)

            log.dbg(f"Creating log files {log_dir}/{self.name}.std{{out,err}}.log...")
            stdout_file, stderr_file = None, None
            try:
                stdout_path = f"{log_dir}/{self.name}.stdout.log"
                stderr_path = f"{log_dir}/{self.name}.stderr.log"

                stdout_file = open(stdout_path, "w")
                stderr_file = open(stderr_path, "w")
            except OSError as e: raise FileError(e.filename, e)

            env = {}
            env.update(os.environ)
            env.update(self.env)
            env["OUTDIR"] = out_dir

            log.info(f"Building crate {self.name}-{self.version}...")
            try:
                log.dbg(f"Starting process with cmd = {self.build_cmd}, cwd = {self.path}...")
                subprocess.run(self.build_cmd, shell=True, cwd=self.path, env=env,
                               stdout=stdout_file, stderr=stderr_file).check_returncode()

                log.ok(f"Successfully built crate {self.name}-{self.version}")
            except subprocess.CalledProcessError as e:
                raise BuildError(self.name, e.returncode) from None
            except OSError as e:
                raise BuildError(self.name, e.errno) from None
            finally:
                stdout_file.close()
                stderr_file.close()
        finally: lock.release()

    def check(self):
        """
        Checks crate's dependency graph.

        Returns
        =======
        Nothing. If this method returned without an exception, no errors were detected.

        Raises
        ======
        - `CircularDependency`
        """

        progress = dict[str, int | None]()
        stack = [self]

        while len(stack) > 0:
            crate = stack[-1]

            # Absolutely not visited
            if crate.name not in progress:
                progress[crate.name] = 0
            # Visited and fully checked
            elif progress[crate.name] is None:
                log.dbg(f"{crate.name}: dependency graph is OK")
                _ = stack.pop()
            # Time to end the processing
            elif progress[crate.name] == len(crate.deps):
                progress[crate.name] = None
            # Processing still going
            else:
                dep = crate.deps[progress[crate.name]]
                if type(progress.get(dep.name)) == int:
                    raise CircularDependency(crate.name, dep.name)
                stack.append(dep)
                progress[crate.name] += 1
