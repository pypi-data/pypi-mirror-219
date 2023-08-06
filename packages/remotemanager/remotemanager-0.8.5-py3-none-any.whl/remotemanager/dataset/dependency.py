import warnings

from remotemanager.logging import LoggingMixin
from remotemanager.storage.sendablemixin import SendableMixin


class Dependency(SendableMixin, LoggingMixin):

    _do_not_package = ["_network"]

    def __init__(self):
        self._logger.info("new Dependency created")

        self._network = []
        self._parents = []
        self._children = []

    def add_edge(self, primary, secondary):
        pair = (primary, secondary)
        if pair not in self._network:
            self._logger.info(f"adding new edge {pair}")

            self._parents.append(primary.short_uuid)
            self._children.append(secondary.short_uuid)

            self._network.append(pair)

    @property
    def network(self):
        return self._network

    def get_children(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._parents)):
            if self._parents[i] == uuid:
                tmp.append(self.network[i][1])

        return tmp

    def get_parents(self, dataset):
        uuid = dataset.short_uuid

        tmp = []
        for i in range(len(self._children)):
            if self._children[i] == uuid:
                tmp.append(self.network[i][0])

        return tmp

    @property
    def ds_list(self):

        datasets = []
        for pair in self.network:
            for ds in pair:
                if ds not in datasets:
                    datasets.append(ds)

        return datasets

    def remove_run(self, id: bool = False) -> bool:
        out = []
        for ds in self.ds_list:
            out.append(ds.remove_run(id=id, dependency_call=True))

        return all(out)

    def clear_runs(self) -> None:
        for ds in self.ds_list:
            ds.clear_runs(dependency_call=True)

    def clear_results(self) -> None:
        for ds in self.ds_list:
            ds.clear_results(dependency_call=True)

    def wipe_local(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_local(files_only=files_only, dependency_call=True)

    def wipe_remote(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.wipe_remote(files_only=files_only, dependency_call=True)

    def hard_reset(self, files_only: bool = False) -> None:
        for ds in self.ds_list:
            ds.hard_reset(files_only=files_only, dependency_call=True)

    def append_run(self, caller, chain_run_args, run_args, *args, **kwargs):
        """
        Appends runs with the same args to all datasets

        Args:
            caller:
                (Dataset): The dataset which defers to the dependency
            chain_run_args (bool):
                for dependency runs, will not propagate run_args to other datasets in
                the chain if False (defaults True)
            *args:
                append_run args
            **kwargs:
                append_run keyword args

        Returns:
            None
        """
        self._logger.info(f"appending run from {caller}")

        datasets = self.ds_list
        self._logger.info(f"There are {len(datasets)} datasets in the chain")

        if chain_run_args:
            self._logger.info("chain_args is True, propagating")
            kwargs.update(run_args)

        for ds in datasets:
            if ds == caller:
                caller_args = {k: v for k, v in kwargs.items()}
                caller_args.update(run_args)
                ds.append_run(dependency_call=True, *args, **caller_args)
            else:
                ds.append_run(dependency_call=True, *args, **kwargs)

        for ds in datasets:
            parents = self.get_parents(ds)
            if len(parents) > 1:
                warnings.warn(
                    "Multiple parents detected. "
                    "Variable passing in this instance is unstable!"
                )
            for parent in parents:
                # TODO this is broken with multiple parents
                lstr = (
                    f"import os.path\n"
                    f'if os.path.getmtime("'
                    f'{parent.runners[-1].runfile.name}") > '
                    f'os.path.getmtime("'
                    f'{parent.runners[-1].resultfile.name}"):\n'
                    f'\traise RuntimeError("outdated '
                    f'result file for parent")\n'
                    f'repo.loaded = repo.load("'
                    f'{parent.runners[-1].resultfile.name}")'
                )
                ds.runners[-1]._dependency_info["parent_import"] = lstr

            tmp = []
            for child in self.get_children(ds):
                runner = child.runners[-1]
                tmp.append(
                    f"{child.url.submitter} {runner.jobscript.name} "
                    f"2>> {runner.errorfile.name}"
                )

            ds.runners[-1]._dependency_info["child_submit"] = tmp

            ds.database.update(ds.pack())

    def run(self, *args, **kwargs):
        self._logger.info("dependency internal run call")

        ds_store = {}
        for ds in self.ds_list:
            ds_store[ds] = len(ds.runners)

        if not len(set(ds_store.values())) == 1:
            msg = f"Datasets do not have matching numbers of runners!: " f"{ds_store}"
            self._logger.critical(msg)
            raise RuntimeError(msg)

        delay = []
        for ds in ds_store:
            # if a dataset is a child, it will skip the exec, and only send files
            # we want to wait for all files to be present, so add the datasets that
            # exec (parentless parents) to a list and exec later
            if ds.is_child:
                ds._run(*args, **kwargs)
            else:
                delay.append(ds)

        for ds in delay:
            ds._run(*args, **kwargs)
