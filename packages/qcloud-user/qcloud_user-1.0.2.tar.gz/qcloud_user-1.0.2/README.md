-----------------------------------------------------------------------

<h1 align="center"> Q-Cloud User Documentation </h1>

-----------------------------------------------------------------------


## Setup

Before submitting any calculations, you will need to install and configure
the Q-Cloud command line interface:
```
python3 -m pip install  qcloud_user
qcloud --configure
```
You will be prompted for several configuration values that can be obtained from
your Q-Cloud administrator.  You should have received an email with an initial
password for your account, and you will be prompted to change this the first
time you attempt to submit a job.


## Job Control

### Submitting Jobs

Use the `--submit` option to submit Q-Chem jobs to the cluster, e.g.:
```
qcloud --submit job1.inp job2.inp [...]
```
Several jobs can be submitted at the same time and they will be submitted with
the default queue parameters.   If there are no compute nodes available, the
jobs will sit in the QUEUED state for a couple of minutes while a fresh compute
node is launched and configured.  Once the queue has cleared, the compute nodes
will automatically shut down after the configure time frame (default is five minutes).

Jobs will be submitted with the default queue parameters.  To override the
default parameters and/or specify additional parameters, add them to the first
line of the Q-Chem input file. For example, the following limits the job to 1
hour:
```
--time=1:00:00
$molecule
0  1
he
$end
$rem
...
```
The number of threads can be specified by using the `--ncpu` flag, for example:
```
qcloud --submit --ncpu 4 job1.inp 
```
Note that if the number of threads specified exceeds the number of cores on 
an individual compute node, the job will not run.  Your QCloud administrator
will be able to inform you what this limit is.

If the job submission is successful, a unique job identifier will be returned:
```
[✓] Submitted job id gv6uqutvNmU0:             helium
```
A local registry of these IDs is kept, so it is not essential to use them in the
commands below. However, they may be required to disambiguate multiple jobs
submitted with the same input file basename.


### Monitoring Jobs

To monitor the progress of jobs, use the `--status` option along with a string, 
which could be the file name, job ID or substring:
```
qcloud --status <jobid|jobname> 
```

The progress of jobs in the RUNNING state can be obtained using:
```
qcloud --tail <jobid|jobname> 
```

A job in the QUEUED or RUNNING state can be cancelled, which will remove it from the queue:
```
qcloud --cancel <jobid|jobname>
```

### Downloading Results

Once a job in in the ARCHIVED state, it can be downloaded from the S3 bucket onto 
the local machine:
```
qcloud --get <pattern> 
```
The download will create a new directory with the same basename as the input file 
containing the output from the calculation.


Jobs in the DOWNLOADED state can be cleared from the job registry on the local machine:
```
qcloud --clear <pattern> 
```
Note that this does not remove the results from the S3 bucket.
If you want to remove the job from the registry regardless of status, use the
`--remove` option.


## Other commands

The following will give a full list of commands available using the CLI:
```
qcloud --help
```

## Troubleshooting

If you encounter additional problems not covered in this guide, please contact your 
Q-Cloud administrator or email support@q-chem.com for assistance.

