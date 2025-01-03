from argparse import ArgumentParser

from toil.lib.conversions import human2bytes


def add_runner_options(
    parser: ArgumentParser, cwl: bool = False, wdl: bool = False
) -> None:
    """
    Add to the WDL or CWL runners options that are shared or the same between runners
    :param parser: parser to add arguments to
    :param cwl: bool
    :param wdl: bool
    :return: None
    """
    # This function should be constructed so that even when wdl and cwl are false, the "default" options are still added
    run_imports_on_workers_arguments = ["--runImportsOnWorkers"]
    if cwl:
        run_imports_on_workers_arguments.append("--run-imports-on-workers")
    parser.add_argument(
        *run_imports_on_workers_arguments,
        action="store_true",
        default=False,
        dest="run_imports_on_workers",
        help="Run the file imports on a worker instead of the leader. This is useful if the leader is not optimized for high network performance. "
        "If set to true, the argument --importWorkersDisk must also be set."
    )
    import_workers_threshold_argument = ["--importWorkersThreshold"]
    if cwl:
        import_workers_threshold_argument.append("--import-workers-threshold")
    parser.add_argument(
        *import_workers_threshold_argument,
        dest="import_workers_threshold",
        type=lambda x: human2bytes(str(x)),
        default="1 GiB",
        help="Specify the file size threshold that determines how many files go into a batched import. As many files will go into a batch import job until this threshold "
             "is reached. This should be set in conjunction with the argument --runImportsOnWorkers."
    )
    import_workers_disk_argument = ["--importWorkersDisk"]
    if cwl:
        import_workers_disk_argument.append("--import-workers-disk")
    parser.add_argument(
        *import_workers_disk_argument,
        dest="import_workers_disk",
        type=lambda x: human2bytes(str(x)),
        default="1 MiB",
        help="Specify the disk size each import worker will get. This may be necessary when file streaming is not possible. For example, downloading from AWS to a GCE "
             "job store. If specified, this should be set to the largest file size of all files to import. This should be set in conjunction with the arguments "
             "--runImportsOnWorkers and --importWorkersThreshold."
    )
