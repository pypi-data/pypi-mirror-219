import collections
import gc
import os
import typing
import time
import shutil
import warnings

from remotemanager.dataset.lazy_append import LazyAppend
from remotemanager.storage.remotefunction import cached_functions
from remotemanager.connection.url import URL
from remotemanager.storage.database import Database
from remotemanager.storage.function import Function
from remotemanager.dataset.runner import Runner, localwinerror
import remotemanager.transport as tp
import remotemanager.serialisation as sr
from remotemanager.storage import SendableMixin, TrackedFile
from remotemanager.utils.uuid import generate_uuid
from remotemanager.utils import ensure_list, ensure_filetype, check_dir_is_child
from remotemanager.logging.utils import format_iterable
from remotemanager.dataset.dependency import Dependency
from remotemanager.logging import LoggingMixin
from remotemanager.logging.verbosity import Verbosity
from remotemanager.logging.quiet import Quiet


class Dataset(SendableMixin, LoggingMixin):
    """
    Bulk holder for remote runs. The Dataset class handles anything regarding
    the runs as a group. Running, retrieving results, sending to remote, etc.

    Args:
        function (Callable):
            function to run
        url (URL):
            connection to remote (optional)
        transport (tp.transport.Transport):
            transport system to use, if a specific is required. Defaults to
            transport.rsync
        serialiser (serial.serial):
            serialisation system to use, if a specific is required. Defaults
            to serial.serialjson
        script (str):
            callscript required to run the jobs in this dataset
        submitter (str):
            command to exec any scripts with. Defaults to "bash"
        name (str):
            optional name for this dataset. Will be used for runscripts
        extra_files_send(list, str):
            extra files to send with this run
        extra_files_recv(list, str):
            extra files to retrieve with this run
        skip (bool):
            skip dataset creation if possible. Defaults True
        global_run_args:
            any further (unchanging) arguments to be passed to the runner(s)
    """

    _do_not_package = ["_database"]

    # DEV NOTE: arguments must be None for computer-url override to function
    def __init__(
        self,
        function: [typing.Callable, str],
        url: URL = None,
        dbfile: str = None,
        transport: tp.transport.Transport = None,
        serialiser: sr.serial = None,
        script: str = None,
        name: str = None,
        extra_files_send: list = None,
        extra_files_recv: list = None,
        verbose: int = None,
        add_newline: bool = True,
        block_reinit: bool = None,
        skip: bool = True,
        **global_run_args,
    ):
        self._verbose = Verbosity(verbose)

        self._logger.info("dataset initialised")

        self._function = Function(function)

        self._global_run_args = {}
        if " " in global_run_args.get("remote_dir", ""):
            raise ValueError(f"Space character detected in remote_dir")
        if " " in global_run_args.get("run_dir", ""):
            raise ValueError(f"Space character detected in run_dir")
        if " " in os.path.abspath(global_run_args.get("local_dir", "")):
            raise ValueError(f"Space character detected in local_dir")
        self._global_run_args.update(global_run_args)

        # dataset uuid is equal to Function uuid for now
        self._name = name or "dataset"
        self._uuid = generate_uuid(self._function.uuid + self.name)
        self._logger.info(f"uuid is {self.uuid}")

        self._script = script or ""
        self._extra_files = {
            "send": ensure_list(extra_files_send)
            if extra_files_send is not None
            else [],
            "recv": ensure_list(extra_files_recv)
            if extra_files_recv is not None
            else [],
        }
        self._add_newline = add_newline

        self._last_run = -1

        self._url = None
        self._transport = None
        self._computer = False
        self._serialiser = None
        self._dbfile_override = dbfile
        self._dependency = None
        self._do_not_recurse = False

        self.url = url
        self.transport = transport
        self.serialiser = serialiser
        self._submitter = None

        if block_reinit is not None:
            warnings.warn(
                "block_reinit is soon to be deprecated, " "use skip=False instead"
            )
            skip = not block_reinit

        if not skip:
            try:
                os.remove(self.dbfile)
                self._logger.warning(
                    f"deleted database file {self.dbfile}", silent=True
                )
            except FileNotFoundError:
                pass

        self._run_cmds = []
        self._repo_files = []
        self._master_scripts = []
        if os.path.isfile(self.dbfile):
            self._create_from_db()
        else:
            self._create_fresh()

        self._logger.info(f"Dataset {self.name} init complete")

    def _create_from_db(self):
        self._logger.info(f"unpacking database from {self.dbfile}")

        # create a "temporary" database from the found file
        self._database = Database(self.dbfile)
        old_uuid = next(iter(self._database._storage))  # get uuid by first key
        self._logger.info(f"unpacked uuid is {old_uuid}")
        if old_uuid != self.uuid:
            dst = f"{self.dbfile}.old"
            self._logger.warning(
                "new and old UUID mismatch "
                "(did something change?)\n"
                "Creating a fresh dataset and backing up the "
                f"old dbfile at {dst}. \nUse "
                f"Dataset.from_file('{dst}') to recover the "
                f"old dataset."
            )
            shutil.copyfile(self.dbfile, dst)
            return self._create_fresh()
        # update it with any new values
        self.database.update(self.pack())
        # unpack from here to retrieve
        payload = self.database._storage[self.uuid]
        self.inject_payload(payload)

    def _create_fresh(self):
        self._logger.info("No database file found, creating anew")
        self._runs = collections.OrderedDict()
        self._uuids = []
        self._results = []

        # database property creates the database if it does not exist
        self.database.update(self.pack())

    def __hash__(self) -> int:
        return hash(self.uuid)

    def __getattribute__(self, item):
        """
        Redirect Dataset.attribute calls to _global_run_args if possible.
        Allows for run global_run_args to be kept seperate

        Args:
            item:
                attribute to fetch
        """
        try:  # attempt to get item from self
            return object.__getattribute__(self, item)
        except AttributeError:  # if not found, check the run arguments
            # print('falling back on _global_run_args for', item)
            if item != "_global_run_args" and hasattr(self, "_global_run_args"):
                try:
                    return self._global_run_args[item]
                except:  # noqa E772
                    # if it's not in the run args anyway, go back
                    # to original behaviour for proper flow
                    return object.__getattribute__(self, item)

    def __delattr__(self, item):
        """
        As with __getattribute__, redirect del to global_run_args if possible.

        Args:
            item:
                attribute to delete
        """
        try:
            return object.__delattr__(self, item)
        except AttributeError:
            # print('falling back on _global_run_args for', item)
            if item != "_global_run_args" and hasattr(self, "_global_run_args"):
                del self._global_run_args[str(item)]

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return self.uuid == other.uuid

    def __repr__(self):
        return f"dataset-{self.name}-{self.short_uuid}"

    @classmethod
    def recreate(cls, raise_if_not_found: bool = True, *args, **kwargs):
        """
        Attempts to extract a dataset matching the given args from the python
        garbage collection interface

        Args:
            raise_if_not_found (bool):
                raise ValueError if the Dataset was not found
            *args:
                args as passed to Dataset
            **kwargs:
                keyword args as passed to Dataset
        Returns:
            Dataset
        """

        for obj in gc.get_objects():
            if type(obj) == cls:

                tmp = cls(*args, **kwargs)
                if obj == tmp:
                    print("returning stored obj")
                    return obj

        if raise_if_not_found:
            raise ValueError("Dataset with args not found!")

        return cls(*args, **kwargs)

    @classmethod
    def from_file(cls, file: str):
        """
        Alias for Dataset.unpack(file=...)

        Args:
            file (str):
                Dataset dbfile

        Returns:
            (Dataset): unpacked Dataset
        """
        return Dataset.unpack(file=file)

    @property
    def verbose(self) -> Verbosity:
        """
        Return the current verbosity setting

        Returns:
            (Verbosity): current verbosity
        """
        return self._verbose

    @property
    def database(self) -> Database:
        """
        Access to the stored database object.
        Creates a connection if none exist.

        Returns (Database):
            Database
        """
        if self.is_missing("_database"):
            self._database = Database(file=self.dbfile)
        return self._database

    @property
    def dbfile(self) -> str:
        """
        Name of the database file
        """
        if self._dbfile_override is not None:
            return ensure_filetype(self._dbfile_override, "yaml")
        if self.name == "dataset":
            return ensure_filetype(f"{self.name}-{self.short_uuid}", "yaml")
        return ensure_filetype(f"dataset-{self.name}-{self.short_uuid}", "yaml")

    @property
    def remote_dir(self) -> [str, bool]:
        """
        Accesses the remote_dir property from the run args. Tries to fall back
        on run_dir if not found, then returns default as a last resort.
        """
        remote = self.global_run_args.get("remote_dir", False)
        if not remote:
            return self.global_run_args.get("run_dir", Runner._default_remote_dir)
        return remote

    @property
    def local_dir(self) -> str:
        """
        Accesses the local_dir property from the run args. Returns default if
        not found.
        """
        return self.global_run_args.get("local_dir", Runner._default_local_dir)

    @property
    def repofile(self) -> str:
        return f"{self.name}-{self.short_uuid}-repo"

    @property
    def master_script(self) -> str:
        return f"{self.name}-{self.short_uuid}-master.sh"

    @property
    def argfile(self) -> str:
        return f"args-{self.name}-{self.short_uuid}"

    @property
    def do_not_recurse(self) -> bool:
        self._do_not_recurse = False
        return True

    @property
    def dependency(self) -> Dependency:
        return self._dependency

    @property
    def is_child(self) -> bool:
        if self.dependency is None:
            return False
        return self.short_uuid in self.dependency._children

    @property
    def is_parent(self) -> bool:
        if self.dependency is None:
            return False
        return self.short_uuid in self.dependency._parents

    def _mirror_dependency(self, dataset) -> None:

        self._logger.info(f"connecting with dataset {dataset}")
        if dataset.dependency is not None:
            self._logger.info("target has dependency, joining")
            self._dependency = dataset.dependency
        elif self.dependency is not None:
            self._logger.info("self has dependency, joining")
            dataset._dependency = self._dependency
        else:
            self._logger.info("creating a dependency and entering")
            self._dependency = Dependency()
            dataset._dependency = self.dependency

        self.database.update(self.pack())

    def set_downstream(self, dataset) -> None:
        self._mirror_dependency(dataset)

        self.dependency.add_edge(self, dataset)

        if not dataset.do_not_recurse:
            dataset._do_not_recurse = True
            dataset.set_upstream(self)

    def set_upstream(self, dataset) -> None:
        self._mirror_dependency(dataset)

        self.dependency.add_edge(dataset, self)

        if not dataset.do_not_recurse:
            dataset._do_not_recurse = True
            dataset.set_downstream(self)

    def pack(self, **kwargs) -> dict:
        """
        Override for the SendableMixin.pack() method, ensuring the dataset is
        always below a uuid

        Args:
            **kwargs:
                Any arguments to be passed onwards to the SendableMixin.pack()

        Returns:
            (dict) packing result
        """
        if len(kwargs) == 0:
            self._logger.info("Dataset override pack called")
        else:
            self._logger.info("Data override pack called with kwargs")
            self._logger.info(f"{format_iterable(kwargs)}")
        return super().pack(uuid=self._uuid, **kwargs)

    def set_run_option(self, key: str, val) -> None:
        """
        Update a global run option `key` with value `val`

        Args:
            key (str):
                option to be updated
            val:
                value to set
        """
        self._global_run_args[key] = val

    def append_run(
        self,
        args: dict = None,
        arguments: dict = None,
        name: str = None,
        extra_files_send: list = None,
        extra_files_recv: list = None,
        dependency_call: bool = False,
        verbose: int = None,
        quiet: bool = False,
        skip: bool = True,
        lazy: bool = False,
        chain_run_args: bool = True,
        **run_args,
    ):
        """
        Serialise arguments for later runner construction

        Args:
            args (dict):
                dictionary of arguments to be unpacked
            arguments (dict):
                alias for args
            name (str):
                 append a runner under this name
            extra_files_send (list, str):
                extra files to send with this run
            extra_files_recv (list, str):
                extra files to retrieve with this run
            dependency_call (bool):
                True if called via the dependency handler
            verbose (int, Verbose, None):
                verbose level for this runner (defaults to Dataset level)
            quiet (bool):
                disable printing for this append if True
            skip (bool):
                ignores checks for an existing runner if set to False
            lazy (bool):
                performs a "lazy" append if True, skipping the dataset update. You MUST
                call ds.finish_append() after you are done appending to avoid strange
                behaviours
            chain_run_args (bool):
                for dependency runs, will not propagate run_args to other datasets in
                the chain if False (defaults True)
            run_args:
                any extra arguments to pass to runner
        """
        self._logger.debug("#### Dataset append_run called")
        Quiet.state = quiet
        if args is None and arguments is not None:
            args = arguments

        if verbose is None:
            verbose = self.verbose.value

        if self.dependency is not None and not dependency_call:
            return self.dependency.append_run(
                caller=self,
                chain_run_args=chain_run_args,
                args=args,
                name=name,
                extra_files_send=extra_files_send,  # noqa: E251
                extra_files_recv=extra_files_recv,  # noqa: E251
                verbose=verbose,
                skip=skip,
                lazy=lazy,
                run_args=run_args,
            )

        # first grab global arguments and update them with explicit args
        run_arguments = {k: v for k, v in self._global_run_args.items()}
        run_arguments.update(run_args)

        extra_files_send = ensure_list(extra_files_send) + self._extra_files["send"]

        extra_files_recv = ensure_list(extra_files_recv) + self._extra_files["recv"]

        rnum = len(self.runners)
        if name is not None:
            run_arguments["name"] = name
            r_id = name

            if name in self.runner_dict:
                self._logger.warning(
                    f"{self} overwriting already existing runner {r_id}"
                )
        else:
            r_id = f"runner-{rnum}"

        tmp = Runner(
            arguments=args,
            dbfile=self.dbfile,
            parent=self,
            self_id=r_id,
            extra_files_send=extra_files_send,
            extra_files_recv=extra_files_recv,
            verbose=verbose,
            **run_arguments,
        )

        tmp.result_extension = self.serialiser.extension

        if not skip:
            self._runs[r_id] = tmp
            self._uuids.append(tmp.uuid)
            self._logger.important(f"force appended run {tmp.name}")
        elif tmp.uuid not in self._uuids:
            self._runs[r_id] = tmp
            self._uuids.append(tmp.uuid)
            self._logger.important(f"appended run {tmp.name}")
        else:
            self._logger.important(f"runner {tmp.name} already exists")

        if not lazy:
            self.finish_append()
        Quiet.state = False

    def finish_append(self):
        self.database.update(self.pack())

    def lazy_append(self):
        return LazyAppend(self)

    def remove_run(self, id: any) -> bool:
        """
        Remove a runner with the given identifier. Search methods are identical
        get_runner(id)

        Args:
            id:
                identifier

        Returns:
            (bool): True if succeeded
        """
        runner = self.get_runner(id)

        if runner is None:
            self._logger.info(f"could not find runner to remove")
            return False

        del self._runs[runner.id]
        self._uuids.remove(runner.uuid)

        self._logger.important(f"removed runner {runner}")

        # need to override attribute first, as updating can only add
        self.database._storage[self.uuid]["_runs"] = {}
        self.database.update(self.pack())

        return True

    def get_runner(self, id) -> [Runner, None]:
        """
        Collect a runner with the given identifier. Depending on the type of
        arg passed, there are different search methods:

        - int: the runners[id] of the runner to remove
        - str: searches for a runner with the matching uuid
        - dict: attempts to find a runner with matching args

        Args:
            id:
                identifier

        Returns:
            (Runner): collected Runner, None if not available
        """

        def get_by_id(id):
            self._logger.info(f"getting runner by id {id}")
            try:
                key = list(self.runner_dict.keys())[id]
                return self.runner_dict[key]
            except IndexError:
                return

        def get_by_str(id):
            self._logger.info(f'getting runner by string "{id}"')

            if id.lower() in self.runner_dict:
                return self.runner_dict[id.lower()]

            for r_id, r in self.runner_dict.items():
                if len(id) == 64 and r.uuid == id:
                    self._logger.info(f"full uuid")
                    return r
                elif len(id) == 8 and r.short_uuid == id:
                    self._logger.info(f"short uuid")
                    return r

        def get_by_dict(id):
            self._logger.info(f"getting runner by args {id}")
            for r_id, r in self.runner_dict.items():
                if format_iterable(r.args) == format_iterable(id):
                    return r

        dispatch = {int: get_by_id, str: get_by_str, dict: get_by_dict}

        return dispatch.get(type(id))(id)

    def clear_runs(self) -> None:
        """
        Wipes all runners
        """
        self._logger.info("wiping all runners and updating the db")

        self._uuids = []
        self._runs = {}

        self.database._storage[self.uuid]["_runs"] = {}
        self.database.update(self.pack())

    def clear_results(self) -> None:
        """
        Remove any results from the stored runners and attempt to delete their
        result files.

        .. warning::
            This is a potentially destructive action, be careful with this
            method
        """
        for runner in self.runners:
            runner.clear_result()

    def _collect_files(self, attribute: str) -> list:
        """
        Collects attribute `attribute` from both Dataset and each runner,
        returning a list.

        Used primarily for deleting those files.

        Used for file collection via `_collect_files('remote_dir')`,
        for example

        Args:
            attribute (str):
                attribute to collect
        Returns:
            (list): collection result
        """
        try:
            tmp = [getattr(self, attribute)]
        except AttributeError:
            tmp = []
        for runner in self.runners:
            file = getattr(runner, attribute)
            if file not in tmp:
                tmp.append(file)
        return tmp

    def wipe_local(self, files_only: bool = False) -> None:
        """
        Clear out the local directory

        Args:
            files_only (bool):
                delete individual files instead of whole folders (preserves
                extra files)

        Returns:
            None
        """
        if not check_dir_is_child:
            raise RuntimeError(
                f"local dir {self.local_dir} is not a child directory, "
                f"deleting could have catastrophic effects"
            )

        if not files_only:
            locals = self._collect_files("local_dir")
            self._logger.warning(f"removing remote_dir(s): {locals}")

            for local in locals:
                try:
                    shutil.rmtree(local)
                except FileNotFoundError:
                    self._logger.warning(f"{local} not found")

        else:
            local = [s.local for s in self._master_scripts]
            local += [r.local for r in self._repo_files]
            attrs = ["runfile", "resultfile", "jobscript"]
            for attr in attrs:
                local += [f.local for f in self._collect_files(attr)]
            for file in local:
                try:
                    os.remove(file)
                except FileNotFoundError:
                    pass

    def wipe_remote(self, files_only: bool = False) -> None:
        """
        Clear out the remote directory (including run dir)

        Args:
            files_only (bool):
                delete individual files instead of whole folders (preserves
                extra files)

        Returns:
            None
        """
        if not files_only:
            remotes = self._collect_files("remote_dir")
        else:
            remotes = [s.remote for s in self._master_scripts]
            remotes += [r.remote for r in self._repo_files]
            attrs = ["runfile", "resultfile", "jobscript"]
            for attr in attrs:
                remotes += [f.remote for f in self._collect_files(attr)]

        self._logger.warning(f"removing remote(s): {remotes}")

        if len(remotes) > 1:
            remotestring = ",".join(remotes)
            self._logger.info(f"removing several remotes with string {remotestring}")
            self.url.cmd(f"rm -r {{{remotestring}}}", raise_errors=False)
        else:
            self.url.cmd(f"rm -r {remotes[0]}", raise_errors=False)

    def hard_reset(self, files_only: bool = False) -> None:
        """
        Hard reset the dataset, including wiping local and remote folders

        Args:
            files_only (bool):
                delete individual files instead of whole folders (preserves
                extra files)

        Returns:
            None
        """
        self.wipe_local(files_only)
        self.wipe_remote(files_only)
        self.clear_runs()

        try:
            os.remove(self.dbfile)
        except FileNotFoundError:
            pass

    @property
    def runner_dict(self) -> dict:
        """
        Stored runners in dict form, where the keys are the append id
        """
        return dict(self._runs)

    @property
    def runners(self) -> list:
        """
        Stored runners as a list
        """
        return list(self.runner_dict.values())

    @property
    def function(self) -> Function:
        """
        Currently stored Function wrapper
        """
        return self._function

    @property
    def global_run_args(self) -> dict:
        """
        Global run args to be passed to runners by default.

        "Fakes" attributes added to dataset after init by adding anything that
        does not exist within the base Dataset (ignoring private vars)
        """
        out = {}
        for k, v in self.__dict__.items():
            if k not in Dataset.__dict__ and not k.startswith(("_", "~")):
                out[k] = v
        out.update(self._global_run_args)
        return out

    def _script_sub(self, avoid_nodes: bool = False, **sub_args) -> str:
        """
        Substitutes run argmuents into the computer script, if it exists

        Args:
            avoid_nodes (bool):
                ignore submission scripts if True
            **sub_args:
                jobscript arguments

        Returns:
            (str):
                jobscript
        """
        if avoid_nodes:
            self._logger.info("creating a jobscript for the login nodes")
            return self._script
        if not self._computer:
            self._logger.info("not a computer, returning base script")
            return self._script
        if "name" not in sub_args:
            self._logger.info(
                f"name not found in args, appending self name {self.name}"
            )
            sub_args["name"] = self.name
        return self.url.script(**sub_args)

    @property
    def script(self, **sub_args) -> str:
        """
        Currently stored run script

        Args:
            sub_args:
                arguments to substitute into the script() method

        Returns:
            (str):
                arg-substituted script
        """
        sub_args.update(self.global_run_args)
        return self._script_sub(**sub_args)

    @script.setter
    def script(self, script: str) -> None:
        """
        Set the run script
        """
        self._script = script

    @property
    def add_newline(self):
        return self._add_newline

    @add_newline.setter
    def add_newline(self, add_newline):
        self._add_newline = add_newline

    @property
    def submitter(self) -> str:
        """
        Currently stored submission command
        """
        return self._submitter

    @submitter.setter
    def submitter(self, submitter) -> None:
        """
        Set the submission command
        """
        self._submitter = submitter

    @property
    def url(self) -> URL:
        """
        Currently stored URL object
        """
        if not hasattr(self, "_url"):
            # noinspection PyTypeChecker
            self.url = None
        return self._url

    @url.setter
    def url(self, url: [URL, None] = None) -> None:
        """
        Verifies and sets the URL to be used.
        Will create an empty (local) url connection if url is None

        Args:
            url (URL):
                url to be verified
        """
        self._logger.info(f"new url is being set to {url}")
        if url is None:
            self._logger.info(
                "no URL specified for this dataset, creating " "localhost"
            )
            self._url = URL(verbose=self.verbose)
        else:
            if not isinstance(url, URL):
                raise ValueError("URL is not a valid URL instance")
            self._url = url

        if not type(url) == URL and issubclass(type(url), URL):
            self._computer = True

        timeout = self._global_run_args.get("timeout", None)
        max_timeouts = self._global_run_args.get("max_timeouts", None)

        self._url.timeout = timeout
        self._url.max_timeouts = max_timeouts

    @property
    def transport(self) -> tp.transport.Transport:
        """
        Currently stored Transport system
        """
        if not hasattr(self, "_transport"):
            # noinspection PyTypeChecker
            self.transport = None
        return self._transport

    @transport.setter
    def transport(self, transport: [tp.transport.Transport, None] = None) -> None:
        """
        Verifies and sets the Transport to be used.
        Will use rsync if transport is None

        Args:
            transport (Transport):
                transport to be verified
        """
        if transport is None:
            self._logger.info(
                "no transport specified for this dataset, " "creating basic rsync"
            )
            self._transport = tp.rsync(self.url)
        else:
            if not isinstance(transport, tp.transport.Transport):
                raise ValueError("transport is not a valid transport instance")
            self._transport = transport

        self._transport.set_remote(self.url)

    @property
    def serialiser(self) -> sr.serial.serial:
        if not hasattr(self, "_serialiser"):
            self.serialiser = None
        return self._serialiser

    @serialiser.setter
    def serialiser(self, serialiser: sr.serial.serial = None) -> None:
        """
        Verifies and sets the serialiser to be used.
        Will use serialjson if serialiser is None

        Args:
            serialiser (serialiser):
                serialiser to be verified
        """
        if serialiser is None:
            self._logger.info("no serialiser specified," "creating basic json")
            self._serialiser = sr.serialjson()

        else:
            if not isinstance(serialiser, sr.serial.serial):
                raise ValueError("serialiser is not a valid serial instance")
            self._serialiser = serialiser

    @property
    def extra_files(self) -> dict:
        """
        Extra files to send and recieve
        """
        return self._extra_files

    def remove_database(self) -> None:
        """
        Deletes the database file
        """
        os.remove(self.dbfile)

    @property
    def name(self) -> str:
        """
        Name of this dataset
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """
        Sets the dataset name
        """
        if not isinstance(name, str):
            try:
                name = str(name)
            except TypeError:
                raise ValueError("name can only be str type")

        self._name = name

    @property
    def uuid(self) -> str:
        """
        This Dataset's full uuid (64 characcter)
        """
        return self._uuid

    @property
    def short_uuid(self) -> str:
        """
        This Dataset's short format (8 character) uuid
        """
        return self._uuid[:8]

    def set_runner_states(self, state: str, uuids: list = None) -> None:
        """
        Update runner states to `state`

        Args:
            (str) state:
                state to set
            (list) uuids:
                list of uuids to update, updates all if not passed
        """
        self._logger.info("updating runner states")
        if uuids is not None:
            self._logger.info(f"using uuid list: {uuids}")
            for runner in self.runners:
                if runner.uuid in uuids:
                    runner.state = state

            return

        for runner in self.runners:
            runner.state = state

    def get_all_runner_states(self) -> list:
        """
        Check all runner states, returning a list

        Returns (list):
            states
        """
        return [r.state for r in self.runners]

    def check_all_runner_states(self, state: str) -> bool:
        """
        Check all runner states against `state`, returning True if `all`
        runners have this state

        Args:
            state (str):
                state to check for

        Returns (bool):
            all(states)
        """
        return all([r == state for r in self.get_all_runner_states()])

    @property
    def last_run(self) -> [int, None]:
        """
        Returns the unix time of the last _run call

        Returns:
            (int): unix time of last  _run call, or None if impossible
        """
        if self._last_run > 0:
            return self._last_run
        return None

    def run(
        self,
        force: bool = False,
        dry_run: bool = False,
        quiet: bool = False,
        avoid_nodes: bool = False,
        **run_args,
    ):
        """
        Run the functions

        Args:
            force (bool):
                force all runs to go through, ignoring checks
            dry_run (bool):
                create files, but do not run
            avoid_nodes (bool):
                if True, will attempt to avoid running on avoid_nodes using a standard
                'bash' submission
            run_args:
                any arguments to pass to the runners during this run.
                will override any "global" arguments set at Dataset init
        """
        Quiet.state = quiet

        if os.name == "nt" and self.url.is_local:
            raise RuntimeError(localwinerror)
        if self.is_parent:
            self._logger.warning(f"dataset {self} is a parent, skipping run")
            Quiet.state = quiet
            return

        if self.dependency:
            self._logger.runtime(
                f"dataset {self} is a part of a dependency "
                f"chain, calling from there"
            )
            self.dependency.run(force=force, dry_run=dry_run, **run_args)
            Quiet.state = quiet
            return

        self._run(force, dry_run, avoid_nodes, **run_args)
        Quiet.state = quiet

    def _run(
        self,
        force: bool = False,
        dry_run: bool = False,
        avoid_nodes: bool = False,
        **run_args,
    ) -> None:
        """
        Seperation of run and _run allows for dependency runs. Any
        functionality intended for run that does not interact with
        dependencies should be placed here
        """
        self.avoid_runtime()
        runtime = int(time.time())
        self._logger.runtime(f"#### Dataset _run called at {runtime}")
        self._last_run = runtime
        self._run_cmds = []
        self._repo_files = []
        self._master_scripts = []
        # initial run args
        if len(run_args) != 0:
            self._logger.info(f"extra run args: {format_iterable(run_args)}")
        temp_args = {"force": force}
        temp_args.update(run_args)

        runners_to_update = []
        master_scripts = {}
        any_file_written = False
        asynchronous = None
        for runner in self.runners:
            if not runner._assess_run(**temp_args):
                continue

            runner._write_runfile(self)
            any_file_written = True

            self._logger.info("writing script with run args:")
            self._logger.info(format_iterable(runner.run_args))

            script = self._script_sub(avoid_nodes, **runner.run_args)
            runner._write_script(self.url.python, script)

            self.transport.queue_for_push(
                [runner.jobscript.name, runner.runfile.name],
                runner.local_dir,
                runner.remote_dir,
            )

            if avoid_nodes:
                submitter = self.submitter or "bash"
            else:
                submitter = self.url.submitter
            runline = f"{submitter} {runner.jobscript.name}"

            asynchronous = runner.run_option("asynchronous", True)
            if asynchronous and self.url.submitter == "bash":
                self._logger.debug('appending "&" for async run')
                runline += f" 2>> {runner.errorfile.name} &"

            if runner.remote_dir not in master_scripts:
                master_scripts[runner.remote_dir] = []
            master_scripts[runner.remote_dir].append(runline)

            for file in runner.extra_files["send"]:
                self.transport.queue_for_push(
                    os.path.split(file)[1], os.path.split(file)[0], runner.remote_dir
                )

            runners_to_update.append(runner.uuid)
            runner.state = "staged"

        if not any_file_written:
            return self._run_finalise()

        cmds = []
        i = 0
        for remote, lines in master_scripts.items():
            if not self.is_child:
                scriptname = f"{i}-{self.master_script}"
                i += 1
                _scriptfile = TrackedFile(self.local_dir, remote, scriptname)
                self._master_scripts.append(_scriptfile)
                # newline='\n' is required to stop windows clients adding the \r\n
                self._logger.info(f"writing to master script at {_scriptfile.local}")

                with open(_scriptfile.local, "w+", newline="\n") as o:
                    o.write(f"rm -f *{self.short_uuid}*error.out\n")
                    content = "\n".join(lines)
                    if self.add_newline:
                        content += "\n"
                    o.write(content)
                self.transport.queue_for_push(scriptname, self.local_dir, remote)
                cmd = f"cd {remote} && {self.url.shell} {scriptname}"
                cmds.append(cmd)

            # send a repo for each new remote dir
            # TODO this should ideally be reduced to just _one_
            self._write_to_repo(self.local_dir, remote)

        if not dry_run:
            self.transport.transfer()
            self.set_runner_states("submit pending", runners_to_update)
            if self.is_child:
                self._logger.info(f"{self} is child, returning")
                return self._run_finalise()
            for cmd in cmds:
                self._run_cmds.append(self.url.cmd(cmd, asynchronous=asynchronous))
        else:
            self.transport.wipe_transfers()
            for cmd in cmds:
                self._logger.important(f"launch command: {cmd}")
            self.set_runner_states("dry run", runners_to_update)

        self._run_finalise()

    def _run_finalise(self) -> None:
        self.database.update(self.pack())

    def _write_to_repo(self, local=None, remote=None) -> None:
        """
        Writes the function to a "repo" file which can be imported from
        """
        if local is None:
            local = self.local_dir
        if remote is None:
            remote = self.remote_dir

        repo = TrackedFile(local, remote, self.repofile + ".py")

        if not os.path.isdir(repo.local_dir):
            os.makedirs(repo.local_dir)

        with open(repo.local, "w+") as o:
            if len(cached_functions) > 0:
                o.write("### cached functions ###\n")

                for fname, f in cached_functions.items():
                    o.write(f.source + "\n")
                o.write("\n")

            o.write("### primary function ###\n")
            o.write(self.function.source)

            o.write("\n### serialiser functions ###")
            o.write(self.serialiser.dumpfunc())
            o.write("\n")
            o.write(self.serialiser.loadfunc())

        self.transport.queue_for_push(repo.name, repo.local_dir, repo.remote_dir)

        self._repo_files.append(repo)

    @property
    def run_cmds(self) -> list:
        """
        Access to the storage of CMD objects used to run the scripts

        Returns:
            (list): List of CMD objects
        """
        return self._run_cmds

    def _check_for_runner_outputs(self) -> [dict, dict]:
        """
        Scans the remote for resultfiles and error files, using a single call

        Returns:
            dict: mtimes of result files, if present
            dict: mtimes of error files, if present
        """
        self._logger.important("checking remotely for finished runs")
        files_to_check = []
        _error_files = []
        for runner in self.runners:
            files_to_check.append(runner.resultfile.remote)

            if runner.errorfile is not None:
                self._logger.info(f"looking for error file {runner.errorfile.remote}")
                _error_files.append(runner.errorfile.remote)

        # check all at once for both result and error files in a single call
        result = self.url.utils.file_mtime(
            files_to_check + _error_files, ignore_empty=True
        )

        # separate out the error files into their own dict
        errors = {}
        for file in _error_files:
            try:
                errors[file] = result.pop(file)
            except KeyError:
                pass

        return result, errors

    def fetch_results(
        self,
        raise_if_not_finished: bool = False,
        quiet: bool = False,
    ) -> None:
        """
        Collect any scripted run resultfiles and insert them into their runners

        Args:
            raise_if_not_finished (bool):
                raise an error if all calculations not finished

        Returns:
            None
        """
        Quiet.state = quiet
        self._logger.runtime("#### Dataset fetch_results called")
        self.avoid_runtime()

        result_mtimes, error_mtimes = self._check_for_runner_outputs()

        # no reason to continue if we don't have any files, find out if that's the case
        valid_results = [t for t in result_mtimes.values() if t is not None]
        valid_errors = [t for t in error_mtimes.values() if t is not None]
        if len(valid_results) + len(valid_errors) == 0:
            self._logger.info("no valid results or errors found, exiting early")
            Quiet.state = False
            return

        self._logger.info(f"found {len(valid_results)} valid result files")
        self._logger.info(f"found {len(valid_errors)} valid error files")

        self._logger.info("present result files:")
        self._logger.info(format_iterable(result_mtimes))
        for runner in self.runners:
            if result_mtimes[runner.resultfile.remote]:
                self.transport.queue_for_pull(
                    os.path.split(runner.resultfile.remote)[1],
                    runner.local_dir,
                    os.path.split(runner.resultfile.remote)[0],
                )
            if error_mtimes[runner.errorfile.remote]:
                self.transport.queue_for_pull(
                    os.path.split(runner.errorfile.remote)[1],
                    runner.local_dir,
                    os.path.split(runner.errorfile.remote)[0],
                )

            for file in runner.extra_files["recv"]:
                rmt = (
                    runner.run_dir if runner.run_dir is not None else runner.remote_dir
                )
                remote = os.path.join(rmt, os.path.split(file)[0])
                self.transport.queue_for_pull(
                    os.path.split(file)[1], runner.local_dir, remote
                )

        self._logger.info("pulling completed result and error files")
        self.transport.transfer()
        for runner in self.runners:
            runner.read_local_files()

        self.database.update(self.pack())

        if raise_if_not_finished and not all(self._is_finished()):
            raise RuntimeError("Calculations not yet completed!")
        Quiet.state = False

    @property
    def is_finished(self) -> list:
        return self._is_finished()

    def _is_finished(self, verbose: bool = True) -> list:
        """
        Check if the runners have finished

        Args:
            verbose (bool):
                disables printing if False

        Returns (list):
            boolean list corresponding to the Runner order
        """
        checktime = int(time.time())
        self._logger.runtime(f"#### Dataset _is_finished called at {checktime}")
        self.avoid_runtime()

        if not verbose:
            Quiet.state = True
        # initialise an empty return dict
        ret = {r.uuid: None for r in self.runners}
        # if we're skipping, check in with the runners
        # since runner.is_finished = True will be valid...
        for runner in self.runners:
            if not runner.run_args.get("skip") or runner.run_args.get("force", False):
                continue
            self._logger.info(f"checking in with runner {runner}")

            if runner.is_finished:
                ret[runner.uuid] = True

        self._logger.runtime("checking for files")
        # look for the resultfiles
        files, errs = self._check_for_runner_outputs()

        # create a list of the resultfiles that are available
        def check_file_mtime(mtime: int, last_sub: int) -> bool:
            """
            Checks mtime against last_sub, returning True if mtime is after the sub.
            Uses unix epoch time.

            Args:
                mtime:
                    mtime of the file, None is accepted and returns False
                last_sub:
                    submission time for the runner

            Returns:
                bool
            """
            if not mtime:
                return False
            if last_sub is None:
                return False
            if mtime >= last_sub:
                return True
            return False

        for runner in self.runners:
            # if we've already decided this runner, ignore it
            if ret[runner.uuid] is not None:
                continue
            # get last submission time and the mtimes of the relevant files
            last_submitted = runner.last_submitted
            mtime_result = files[runner.resultfile.remote]
            mtime_error = errs[runner.errorfile.remote]
            # check the mtimes. A missing file will have a time of None
            finished_result = check_file_mtime(mtime_result, last_submitted)
            finished_error = check_file_mtime(mtime_error, last_submitted)

            ret[runner.uuid] = finished_result or finished_error

            self._logger.debug(
                f"checking file {runner.resultfile.remote}. "
                f"mtime {mtime_result} vs runner submit time "
                f"{last_submitted} -> {ret[runner.uuid]}"
            )

        Quiet.state = False
        return list(ret.values())

    @property
    def all_finished(self) -> bool:
        """
        Check if `all` runners have finished

        Returns (bool):
            True if all runners have completed their runs
        """
        return all(self.is_finished)

    def wait(
        self, interval: int = 10, timeout: int = None, watch: bool = False
    ) -> None:
        """
        Watch the calculation, printing updates as runners complete

        Args:
            interval:
                check interval time in seconds
            timeout:
                maximum time to wait in seconds
            watch:
                print an updating table of runner states

        Returns:

        """
        if watch:
            from IPython.display import clear_output

        t0 = time.time()

        states = self._is_finished(verbose=False)
        while not all(states):
            time.sleep(interval)

            states = self._is_finished(verbose=False)

            if watch:
                clear_output(wait=True)
                print(
                    f"watching {len(self.runners)} runners, with a {interval}s interval"
                )

                if timeout:
                    print(f"will time out if t > {timeout}")

            dt = time.time() - t0

            if watch:
                print(f"t={dt:.2f}")

                for runner, state in zip(self.runners, states):
                    statetxt = "completed" if state else "running..."
                    print(f"{runner.name}, {statetxt}")

            if timeout is not None and dt > timeout:
                raise RuntimeError("wait timed out")

    @property
    def results(self) -> list:
        """
        Access the results of the runners

        Returns (list):
            runner.result for each runner
        """
        self._logger.runtime("#### Dataset results called")
        return [r.result for r in self.runners]

    @property
    def errors(self) -> list:
        """
        Access the errors of the runners

        Returns (list):
            runner.result for each runner
        """
        self._logger.runtime("#### Dataset errors called")
        return [r.error for r in self.runners]

    def avoid_runtime(self) -> None:
        """
        Call for last_runtime sensitive operations such as is_finished and fetch_results

        Waits for 1s if we're too close to the saved _last_run time

        Returns:
            None
        """
        checktime = int(time.time())

        if checktime <= self._last_run:
            self._logger.runtime("call is too soon after last run, sleeping for 1s")
            time.sleep(1)
