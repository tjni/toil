.. _commandRef:

.. _workflowOptions:

Commandline Options
===================

A quick way to see all of Toil's commandline options is by executing the following on a workflow language front-end::

    $ toil-wdl-runner --help

Or a Toil Python workflow::

    $ python3 example.py --help

For a basic toil workflow, Toil has one mandatory argument, the job store.  All other arguments are optional.

The Config File
---------------
Instead of changing the arguments on the command line, Toil offers support for using a configuration file.

Options will be applied with priority:

  1. Command line options

  2. Environmental Variables

  3. Config file values

     a. Provided config file through ``--config``

     b. Default config value in ``$HOME/.toil/default.yaml``

  4. Defaults

You can manually generate an example configuration file to a path you select. To generate a configuration file, run::

    $ toil config [filename].yaml

Then uncomment options as necessary and change/provide new values.

After editing the config file, you can run Toil with its settings by passing it on the command line::

    $ python3 example.py --config=[filename].yaml

Alternatively, you can edit the default config file, which is located at ``$HOME/.toil/default.yaml``

If CLI options are used in addition to the configuration file, the CLI options will overwrite the configuration file
options. For example::

    $ python3 example.py --config=[filename].yaml --defaultMemory 80Gi

This will result in a default memory per job of 80GiB no matter what is in the configuration file provided.

The Job Store
-------------

Running Toil workflows requires a file path or URL to a central location for all of the intermediate files for the workflow: the job store.
For ``toil-cwl-runner`` and ``toil-wdl-runner`` a job store can often be selected automatically or can be specified with the ``--jobStore`` option; Toil Python workflows generally require the job store as a positional command line argument.
To use the :ref:`Python quickstart <pyquickstart>` example,
if you're on a node that has a large **/scratch** volume, you can specify that the jobstore be created there by
executing: ``python3 HelloWorld.py /scratch/my-job-store``, or more explicitly,
``python3 HelloWorld.py file:/scratch/my-job-store``.

Syntax for specifying different job stores:

    Local: ``file:job-store-name``

    AWS: ``aws:region-here:job-store-name``

    Google: ``google:projectID-here:job-store-name``

Different types of job store options can be found below.

.. _optionsRef:

Commandline Options
-------------------

**Core Toil Options**
Options to specify the location of the Toil workflow and turn on stats collation
about the performance of jobs.

  --workDir WORKDIR     Absolute path to directory where temporary files
                        generated during the Toil run should be placed.
                        Standard output and error from batch system jobs
                        (unless ``--noStdOutErr`` is set) will be placed in
                        this directory. A cache directory may be placed in this
                        directory. Temp files and folders will be placed in a
                        directory ``toil-<workflowID>`` within workDir. The
                        workflowID is generated by Toil and will be reported in
                        the workflow logs. Default is determined by the
                        variables (TMPDIR, TEMP, TMP) via mkdtemp. For CWL,
                        the temporary output directory is used instead
                        (see CWL option ``--tmp-outdir-prefix``). This
                        directory needs to exist on all machines running jobs;
                        if capturing standard output and error from batch
                        system jobs is desired, it will generally need to be on
                        a shared file system. When sharing a cache between
                        containers on a host, this directory must be shared
                        between the containers.
  --coordinationDir COORDINATION_DIR
                        Absolute path to directory where Toil will keep state
                        and lock files. When sharing a cache between containers
                        on a host, this directory must be shared between the
                        containers.
  --noStdOutErr         Do not capture standard output and error from batch system jobs.
  --stats               Records statistics about the toil workflow to be used
                        by 'toil stats'.
  --clean=STATE
                        Determines the deletion of the jobStore upon
                        completion of the program. Choices: 'always',
                        'onError','never', or 'onSuccess'. The ``--stats`` option
                        requires information from the jobStore upon completion
                        so the jobStore will never be deleted with that flag.
                        If you wish to be able to restart the run, choose
                        'never' or 'onSuccess'. Default is 'never' if stats is
                        enabled, and 'onSuccess' otherwise
  --cleanWorkDir STATE
                        Determines deletion of temporary worker directory upon
                        completion of a job. Choices: 'always', 'onError', 'never',
                        or 'onSuccess'. Default = always. WARNING: This option
                        should be changed for debugging only. Running a full
                        pipeline with this option could fill your disk with
                        intermediate data.
  --clusterStats FILEPATH
                        If enabled, writes out JSON resource usage statistics
                        to a file. The default location for this file is the
                        current working directory, but an absolute path can
                        also be passed to specify where this file should be
                        written. This option only applies when using scalable
                        batch systems.
  --restart             If ``--restart`` is specified then will attempt to restart
                        existing workflow at the location pointed to by the
                        ``--jobStore`` option. Will raise an exception if the
                        workflow does not exist.

**Logging Options**
Toil hides stdout and stderr by default except in case of job failure. Log
levels in toil are based on priority from the logging module:

  --logOff
                        Only CRITICAL log messages are shown.
                        Equivalent to ``--logLevel=OFF`` or ``--logLevel=CRITICAL``.
  --logCritical
                        Only CRITICAL log messages are shown.
                        Equivalent to ``--logLevel=OFF`` or ``--logLevel=CRITICAL``.
  --logError
                        Only ERROR, and CRITICAL log messages are shown.
                        Equivalent to ``--logLevel=ERROR``.
  --logWarning
                        Only WARN, ERROR, and CRITICAL log messages are shown.
                        Equivalent to ``--logLevel=WARNING``.
  --logInfo
                        All non-debugging-related log messages are shown.
                        Equivalent to ``--logLevel=INFO``.
  --logDebug
                        Log messages at DEBUG level and above are shown.
                        Equivalent to ``--logLevel=DEBUG``.
  --logTrace
                        Log messages at TRACE level and above are shown.
                        Equivalent to ``--logLevel=TRACE``.
  --logLevel=LOGLEVEL
                        May be set to: ``OFF`` (or ``CRITICAL``),
                        ``ERROR``, ``WARN`` (or ``WARNING``), ``INFO``, ``DEBUG``,
                        or ``TRACE``.
  --logFile FILEPATH
                        Specifies a file path to write the logging output to.
  --rotatingLogging
                        Turn on rotating logging, which prevents log files from
                        getting too big (set using ``--maxLogFileSize BYTESIZE``).
  --maxLogFileSize BYTESIZE
                        The maximum size of a job log file to keep (in bytes),
                        log files larger than this will be truncated to the last
                        X bytes. Setting this option to zero will prevent any
                        truncation. Setting this option to a negative value will
                        truncate from the beginning. Default=100MiB
                        Sets the maximum log file size in bytes (``--rotatingLogging`` must be active).
  --log-dir DIRPATH
                        For CWL and local file system only. Log stdout and stderr (if tool requests stdout/stderr) to the DIRPATH.
  --logColors BOOL
                        Enable or disable colored logging. Default=True.

**Batch System Options**

  --batchSystem BATCHSYSTEM
                        The type of batch system to run the job(s) with. Default = single_machine.
  --disableAutoDeployment
                        Should auto-deployment of Toil Python workflows be
                        deactivated? If True, the workflow's Python code should
                        be present at the same location on all workers. Default = False.
  --maxJobs MAXJOBS
                        Specifies the maximum number of jobs to submit to the
                        backing scheduler at once. Not supported on Mesos or
                        AWS Batch. Use 0 for unlimited. Defaults to unlimited.
  --maxLocalJobs MAXLOCALJOBS
                        Specifies the maximum number of housekeeping jobs to
                        run simultaneously on the local system. Use 0 for
                        unlimited. Defaults to the number of local cores.
  --manualMemArgs       Do not add the default arguments: 'hv=MEMORY' &
                        'h_vmem=MEMORY' to the qsub call, and instead rely on
                        TOIL_GRIDGENGINE_ARGS to supply alternative arguments.
                        Requires that TOIL_GRIDGENGINE_ARGS be set.
  --memoryIsProduct
                        If the batch system understands requested memory as a product of the requested
                        memory and the number of cores, set this flag to properly allocate memory. This
                        can be fairly common with grid engine clusters (Ex: SGE, PBS, Torque).
  --runCwlInternalJobsOnWorkers
                        Whether to run CWL internal jobs (e.g. CWLScatter) on
                        the worker nodes instead of the primary node. If false
                        (default), then all such jobs are run on the primary node.
                        Setting this to true can speed up the pipeline for very
                        large workflows with many sub-workflows and/or scatters,
                        provided that the worker pool is large enough.
  --statePollingWait STATEPOLLINGWAIT
                        Time, in seconds, to wait before doing a scheduler
                        query for job state. Return cached results if within
                        the waiting period. Only works for grid engine batch
                        systems such as gridengine, htcondor, torque, slurm,
                        and lsf.
  --statePollingTimeout STATEPOLLINGTIMEOUT
                        Time, in seconds, to retry against a broken scheduler.
                        Only works for grid engine batch systems such as
                        gridengine, htcondor, torque, slurm, and lsf.
  --batchLogsDir BATCHLOGSDIR
                        Directory to tell the backing batch system to log into.
                        Should be available on both the leader and the workers,
                        if the backing batch system writes logs to the worker
                        machines' filesystems, as many HPC schedulers do. If
                        unset, the Toil work directory will be used. Only
                        works for grid engine batch systems such as gridengine,
                        htcondor, torque, slurm, and lsf.
  --mesosEndpoint MESOSENDPOINT
                        The host and port of the Mesos server separated by a
                        colon. (default: <leader IP>:5050)
  --mesosFrameworkId MESOSFRAMEWORKID
                        Use a specific Mesos framework ID.
  --mesosRole MESOSROLE
                        Use a Mesos role.
  --mesosName MESOSNAME
                        The Mesos name to use. (default: toil)
  --scale SCALE         A scaling factor to change the value of all submitted
                        tasks' submitted cores. Used in single_machine batch
                        system. Useful for running workflows on smaller
                        machines than they were designed for, by setting a
                        value less than 1. (default: 1)
  --slurmAllocateMem SLURM_ALLOCATE_MEM
                        If False, do not use --mem. Used as a workaround for
                        Slurm clusters that reject jobs with memory
                        allocations.
  --slurmTime SLURM_TIME
                        Slurm job time limit, in [DD-]HH:MM:SS format.
  --slurmPartition SLURM_PARTITION
                        Partition to send Slurm jobs to.
  --slurmGPUPartition SLURM_GPU_PARTITION
                        Partition to send Slurm jobs to if they ask for GPUs.
  --slurmPE SLURM_PE    Special partition to send Slurm jobs to if they ask
                        for more than 1 CPU. Useful for Slurm clusters that do
                        not offer a partition accepting both single-core and
                        multi-core jobs.
  --slurmArgs SLURM_ARGS
                        Extra arguments to pass to Slurm.
  --kubernetesHostPath KUBERNETES_HOST_PATH
                        Path on Kubernetes hosts to use as shared inter-pod temp
                        directory.
  --kubernetesOwner KUBERNETES_OWNER
                        Username to mark Kubernetes jobs with.
  --kubernetesServiceAccount KUBERNETES_SERVICE_ACCOUNT
                        Service account to run jobs as.
  --kubernetesPodTimeout KUBERNETES_POD_TIMEOUT
                        Seconds to wait for a scheduled Kubernetes pod to
                        start running. (default: 120s)
  --kubernetesPrivileged BOOL
                        Whether to allow Kubernetes pods to run as privileged. This can be
                        used to enable FUSE mounts for faster runtimes with Singularity.
                        When launching Toil-managed clusters, this will be set to true by --allowFuse.
                        (default: False)
  --kubernetesPodSecurityContext KUBERNETES_POD_SECURITY_CONTEXT
                        Path to a YAML defining a pod security context to apply to all pods.
  --kubernetesSecurityContext KUBERNETES_SECURITY_CONTEXT
                        Path to a YAML defining a security context to apply to all containers.
  --awsBatchRegion AWS_BATCH_REGION
                        The AWS region containing the AWS Batch queue to submit
                        to.
  --awsBatchQueue AWS_BATCH_QUEUE
                        The name or ARN of the AWS Batch queue to submit to.
  --awsBatchJobRoleArn AWS_BATCH_JOB_ROLE_ARN
                        The ARN of an IAM role to run AWS Batch jobs as, so they
                        can e.g. access a job store. Must be assumable by
                        ecs-tasks.amazonaws.com

**Data Storage Options**
Allows configuring Toil's data storage.

  --symlinkImports BOOL
                        When using a filesystem based job store, CWL input files
                        are by default symlinked in. Setting this option to True
                        instead copies the files into the job store, which may
                        protect them from being modified externally. When set
                        to False and as long as caching is enabled, Toil will
                        protect the file automatically by changing the permissions
                        to read-only. (Default=True)
  --moveOutputs BOOL
                        When using a filesystem based job store, output files
                        are by default moved to the output directory, and a
                        symlink to the moved exported file is created at the
                        initial location. Setting this option to True instead
                        copies the files into the output directory. Applies to
                        filesystem-based job stores only. (Default=False)
  --caching BOOL        
                        Enable or disable worker level file caching. Set to "true" if
                        caching is desired. By default, caching is enabled on supported
                        batch systems. Does not affect CWL or WDL task caching.
  --symlinkJobStoreReads BOOL
                        Allow reads and container mounts from a JobStore's
                        shared filesystem directly via symlink. Can be turned
                        off if the shared filesystem can't support the IO load
                        of all the jobs reading from it at once, and you want
                        to use ``--caching=True`` to make jobs on each node
                        read from node-local cache storage. (Default=True)

**Autoscaling Options**
Allows the specification of the minimum and maximum number of nodes in an
autoscaled cluster, as well as parameters to control the level of provisioning.

  --provisioner CLOUDPROVIDER
                        The provisioner for cluster auto-scaling. This is the
                        main Toil ``--provisioner`` option, and defaults to None
                        for running on single_machine and non-auto-scaling batch
                        systems. The currently supported choices are 'aws' or
                        'gce'.
  --nodeTypes NODETYPES
                        Specifies a list of comma-separated node types, each of which is
                        composed of slash-separated instance types, and an optional spot
                        bid set off by a colon, making the node type preemptible. Instance
                        types may appear in multiple node types, and the same node type
                        may appear as both preemptible and non-preemptible.

                        Valid argument specifying two node types:
                            c5.4xlarge/c5a.4xlarge:0.42,t2.large
                        Node types:
                            c5.4xlarge/c5a.4xlarge:0.42 and t2.large
                        Instance types:
                            c5.4xlarge, c5a.4xlarge, and t2.large
                        Semantics:
                            Bid $0.42/hour for either c5.4xlarge or c5a.4xlarge instances,
                            treated interchangeably, while they are available at that price,
                            and buy t2.large instances at full price
  --minNodes MINNODES   Minimum number of nodes of each type in the cluster,
                        if using auto-scaling. This should be provided as a
                        comma-separated list of the same length as the list of
                        node types. default=0
  --maxNodes MAXNODES   Maximum number of nodes of each type in the cluster,
                        if using autoscaling, provided as a comma-separated
                        list. The first value is used as a default if the list
                        length is less than the number of nodeTypes.
                        default=10
  --targetTime TARGETTIME
                        Sets how rapidly you aim to complete jobs in seconds.
                        Shorter times mean more aggressive parallelization.
                        The autoscaler attempts to scale up/down so that it
                        expects all queued jobs will complete within targetTime
                        seconds. (Default: 1800)
  --betaInertia BETAINERTIA
                        A smoothing parameter to prevent unnecessary
                        oscillations in the number of provisioned nodes. This
                        controls an exponentially weighted moving average of the
                        estimated number of nodes. A value of 0.0 disables any
                        smoothing, and a value of 0.9 will smooth so much that
                        few changes will ever be made.  Must be between 0.0 and
                        0.9. (Default: 0.1)
  --scaleInterval SCALEINTERVAL
                        The interval (seconds) between assessing if the scale of
                        the cluster needs to change. (Default: 60)
  --preemptibleCompensation PREEMPTIBLECOMPENSATION
                        The preference of the autoscaler to replace
                        preemptible nodes with non-preemptible nodes, when
                        preemptible nodes cannot be started for some reason.
                        Defaults to 0.0. This value must be between 0.0 and
                        1.0, inclusive. A value of 0.0 disables such
                        compensation, a value of 0.5 compensates two missing
                        preemptible nodes with a non-preemptible one. A value
                        of 1.0 replaces every missing pre-emptable node with a
                        non-preemptible one.
  --nodeStorage NODESTORAGE
                        Specify the size of the root volume of worker nodes
                        when they are launched in gigabytes. You may want to
                        set this if your jobs require a lot of disk space. The
                        default value is 50.
  --nodeStorageOverrides NODESTORAGEOVERRIDES
                        Comma-separated list of nodeType:nodeStorage that are used
                        to override the default value from ``--nodeStorage`` for the
                        specified nodeType(s). This is useful for heterogeneous
                        jobs where some tasks require much more disk than others.
  --metrics             Enable the prometheus/grafana dashboard for monitoring
                        CPU/RAM usage, queue size, and issued jobs.
  --assumeZeroOverhead  Ignore scheduler and OS overhead and assume jobs can use every
                        last byte of memory and disk on a node when autoscaling.

**Service Options**
Allows the specification of the maximum number of service jobs in a cluster. By
keeping this limited we can avoid nodes occupied with services causing deadlocks.
(Not for CWL).

  --maxServiceJobs MAXSERVICEJOBS
                        The maximum number of service jobs that can be run
                        concurrently, excluding service jobs running on
                        preemptible nodes. default=9223372036854775807
  --maxPreemptibleServiceJobs MAXPREEMPTIBLESERVICEJOBS
                        The maximum number of service jobs that can run
                        concurrently on preemptible nodes.
                        default=9223372036854775807
  --deadlockWait DEADLOCKWAIT
                        Time, in seconds, to tolerate the workflow running only
                        the same service jobs, with no jobs to use them, before
                        declaring the workflow to be deadlocked and stopping.
                        default=60
  --deadlockCheckInterval DEADLOCKCHECKINTERVAL
                        Time, in seconds, to wait between checks to see if the
                        workflow is stuck running only service jobs, with no
                        jobs to use them. Should be shorter than
                        ``--deadlockWait``. May need to be increased if the batch
                        system cannot enumerate running jobs quickly enough, or
                        if polling for running jobs is placing an unacceptable
                        load on a shared cluster. default=30

**Resource Options**
The options to specify default cores/memory requirements (if not specified by
the jobs themselves), and to limit the total amount of memory/cores requested
from the batch system.

  --defaultMemory INT   The default amount of memory to request for a job.
                        Only applicable to jobs that do not specify an
                        explicit value for this requirement. Standard suffixes
                        like K, Ki, M, Mi, G or Gi are supported. Default is
                        2.0Gi
  --defaultCores FLOAT  The default number of CPU cores to dedicate a job.
                        Only applicable to jobs that do not specify an
                        explicit value for this requirement. Fractions of a
                        core (for example 0.1) are supported on some batch
                        systems, namely Mesos and single_machine. Default is
                        1.0
  --defaultDisk INT     The default amount of disk space to dedicate a job.
                        Only applicable to jobs that do not specify an
                        explicit value for this requirement. Standard suffixes
                        like K, Ki, M, Mi, G or Gi are supported. Default is
                        2.0Gi
  --defaultAccelerators ACCELERATOR
                        The default amount of accelerators to request for a
                        job. Only applicable to jobs that do not specify an
                        explicit value for this requirement. Each accelerator
                        specification can have a type (gpu [default], nvidia,
                        amd, cuda, rocm, opencl, or a specific model like
                        nvidia-tesla-k80), and a count [default: 1]. If both a
                        type and a count are used, they must be separated by a
                        colon. If multiple types of accelerators are used, the
                        specifications are separated by commas. Default is [].
  --defaultPreemptible BOOL
                        Make all jobs able to run on preemptible (spot) nodes
                        by default.
  --maxCores INT        The maximum number of CPU cores to request from the
                        batch system at any one time. Standard suffixes like
                        K, Ki, M, Mi, G or Gi are supported.
  --maxMemory INT       The maximum amount of memory to request from the batch
                        system at any one time. Standard suffixes like K, Ki,
                        M, Mi, G or Gi are supported.
  --maxDisk INT         The maximum amount of disk space to request from the
                        batch system at any one time. Standard suffixes like
                        K, Ki, M, Mi, G or Gi are supported.

**Options for rescuing/killing/restarting jobs.**
The options for jobs that either run too long/fail or get lost (some batch
systems have issues!).

  --retryCount INT
                        Number of times to retry a failing job before giving
                        up and labeling job failed. default=1
  --stopOnFirstFailure BOOL
                        Stop the workflow at the first complete job failure. 
  --enableUnlimitedPreemptibleRetries
                        If set, preemptible failures (or any failure due to an
                        instance getting unexpectedly terminated) will not count
                        towards job failures and ``--retryCount``.
  --doubleMem           If set, batch jobs which die due to reaching memory
                        limit on batch schedulers will have their memory
			doubled and they will be retried. The remaining
			retry count will be reduced by 1. Currently only
			supported by LSF. default=False.
  --maxJobDuration INT
                        Maximum runtime of a job (in seconds) before we kill
                        it (this is a lower bound, and the actual time before
                        killing the job may be longer).
  --rescueJobsFrequency INT
                        Period of time to wait (in seconds) between checking
                        for missing/overlong jobs, that is jobs which get lost
                        by the batch system. Expert parameter.
  --jobStoreTimeout FLOAT
                        Maximum time (in seconds) to wait for a job's update to
                        the job store before declaring it failed.

**Log Management Options**

  --maxLogFileSize MAXLOGFILESIZE
                        The maximum size of a job log file to keep (in bytes),
                        log files larger than this will be truncated to the
                        last X bytes. Setting this option to zero will prevent
                        any truncation. Setting this option to a negative
                        value will truncate from the beginning. Default=62.5 K
  --writeLogs FILEPATH
                        Write worker logs received by the leader into their
                        own files at the specified path. Any non-empty standard
                        output and error from failed batch system jobs will also
                        be written into files at this path. The current working
                        directory will be used if a path is not specified
                        explicitly. Note: By default only the logs of failed
                        jobs are returned to leader. Set log level to 'debug' or
                        enable ``--writeLogsFromAllJobs`` to get logs back from
                        successful jobs, and adjust ``--maxLogFileSize`` to
                        control the truncation limit for worker logs.
  --writeLogsGzip FILEPATH
                        Identical to ``--writeLogs`` except the logs files are
                        gzipped on the leader.
  --writeMessages FILEPATH
                        File to send messages from the leader's message bus to.
  --realTimeLogging BOOL
                        Enable real-time logging from workers to leader.

**Miscellaneous Options**

  --disableChaining BOOL
                        Disables chaining of jobs (chaining uses one job's
                        resource allocation for its successor job if
                        possible).
  --disableJobStoreChecksumVerification
                        Disables checksum verification for files transferred
                        to/from the job store. Checksum verification is a safety
                        check to ensure the data is not corrupted during transfer.
                        Currently only supported for non-streaming AWS files
  --sseKey SSEKEY       Path to file containing 32 character key to be used
                        for server-side encryption on awsJobStore or
                        googleJobStore. SSE will not be used if this flag is
                        not passed.
  --setEnv NAME, -e NAME
                        NAME=VALUE or NAME, -e NAME=VALUE or NAME are also valid.
                        Set an environment variable early on in the worker. If
                        VALUE is omitted, it will be looked up in the current
                        environment. Independently of this option, the worker
                        will try to emulate the leader's environment before
                        running a job, except for some variables known to vary
                        across systems. Using this option, a variable can be
                        injected into the worker process itself before it is
                        started.
  --servicePollingInterval SERVICEPOLLINGINTERVAL
                        Interval of time service jobs wait between polling for
                        the existence of the keep-alive flag (default=60)
  --forceDockerAppliance
                        Disables sanity checking the existence of the docker
                        image specified by TOIL_APPLIANCE_SELF, which Toil uses
                        to provision mesos for autoscaling.
  --statusWait INT      Seconds to wait between reports of running jobs.
                        (default=3600)
  --disableProgress     Disables the progress bar shown when standard error is
                        a terminal.
  --publishWorkflowMetrics PUBLISHWORKFLOWMETRICS
                        Whether to publish workflow metrics reports (including
                        unique workflow and task run IDs, job names, and
                        version and Toil feature use information) to Dockstore
                        when a workflow completes. Selecting "current" will
                        publish metrics for the current workflow. Selecting
                        "all" will also publish prior workflow runs from the
                        Toil history database, even if they themselves were run
                        with "no". Note that once published, workflow metrics
                        CANNOT be deleted or un-published; they will stay
                        published forever!

**Debug Options**
Debug options for finding problems or helping with testing.

  --debugWorker         Experimental no forking mode for local debugging.
                        Specifically, workers are not forked and stderr/stdout
                        are not redirected to the log. (default=False)
  --disableWorkerOutputCapture
                        Let worker output go to worker's standard out/error
                        instead of per-job logs.
  --badWorker BADWORKER
                        For testing purposes randomly kill ``--badWorker``
                        proportion of jobs using SIGKILL. (Default: 0.0)
  --badWorkerFailInterval BADWORKERFAILINTERVAL
                        When killing the job pick uniformly within the interval
                        from 0.0 to ``--badWorkerFailInterval`` seconds after the
                        worker starts. (Default: 0.01)
  --kill_polling_interval KILL_POLLING_INTERVAL
                        Interval of time (in seconds) the leader waits between
                        polling for the kill flag inside the job store set by
                        the "toil kill" command. (default=5)


Restart Option
--------------
In the event of failure, Toil can resume the pipeline by adding the argument
``--restart`` and rerunning the workflow. Toil Python workflows (but not CWL or WDL
workflows) can even be edited and resumed, which is useful for development or
troubleshooting.

Running Workflows with Services
-------------------------------

Toil supports jobs, or clusters of jobs, that run as *services* to other
*accessor* jobs. Example services include server databases or Apache Spark
Clusters. As service jobs exist to provide services to accessor jobs their
runtime is dependent on the concurrent running of their accessor jobs. The dependencies
between services and their accessor jobs can create potential deadlock scenarios,
where the running of the workflow hangs because only service jobs are being
run and their accessor jobs can not be scheduled because of too limited resources
to run both simultaneously. To cope with this situation Toil attempts to
schedule services and accessors intelligently, however to avoid a deadlock
with workflows running service jobs it is advisable to use the following parameters:

* ``--maxServiceJobs``: The maximum number of service jobs that can be run concurrently, excluding service jobs running on preemptible nodes.
* ``--maxPreemptibleServiceJobs``: The maximum number of service jobs that can run concurrently on preemptible nodes.

Specifying these parameters so that at a maximum cluster size there will be
sufficient resources to run accessors in addition to services will ensure that
such a deadlock can not occur.

If too low a limit is specified then a deadlock can occur in which toil can
not schedule sufficient service jobs concurrently to complete the workflow.
Toil will detect this situation if it occurs and throw a
:class:`toil.DeadlockException` exception. Increasing the cluster size
and these limits will resolve the issue.

Setting Options directly in a Python Workflow
---------------------------------------------

It's good to remember that commandline options can be overridden in the code of a Python workflow.  For example,
:func:`toil.job.Job.Runner.getDefaultOptions` can be used to get the default Toil options, ignoring what was passed on the command line. In this example,
this is used to ignore command-line options and always run with the "./toilWorkflow" directory as the jobstore:

.. code-block:: python

    options = Job.Runner.getDefaultOptions("./toilWorkflow") # Get the options object

    with Toil(options) as toil:
        toil.start(Job())  # Run the root job

However, each option can be explicitly set within the workflow by modifying the options object. In this example, we are setting
``logLevel = "DEBUG"`` (all log statements are shown) and ``clean="ALWAYS"`` (always delete the jobstore) like so:

.. code-block:: python

    options = Job.Runner.getDefaultOptions("./toilWorkflow") # Get the options object
    options.logLevel = "DEBUG" # Set the log level to the debug level.
    options.clean = "ALWAYS" # Always delete the jobStore after a run

    with Toil(options) as toil:
        toil.start(Job())  # Run the root job

However, the usual incantation is to accept commandline args from the user with the following:

.. code-block:: python

    parser = Job.Runner.getDefaultArgumentParser() # Get the parser
    options = parser.parse_args() # Parse user args to create the options object

    with Toil(options) as toil:
        toil.start(Job())  # Run the root job

We can also have code in the workflow to overwrite user supplied arguments:

.. code-block:: python

    parser = Job.Runner.getDefaultArgumentParser() # Get the parser
    options = parser.parse_args() # Parse user args to create the options object
    options.logLevel = "DEBUG" # Set the log level to the debug level.
    options.clean = "ALWAYS" # Always delete the jobStore after a run

    with Toil(options) as toil:
        toil.start(Job())  # Run the root job
