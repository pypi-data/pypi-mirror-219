# Oqtant Walkthrough 2: Barrier Manipulator

### This walkthrough covers authorizing an Oraqle session using the OqtantClient, generating, running and viewing the results of a Barrier Manipulator OqtantJob.

For more information about Oqtant refer to our documentation: https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/README.md

_Batch job functionality is available for users with a subscription tier of EXPLORER or INNOVATOR._

`get_user_token` creates a temporary web server on your machine to handle authenticating with Oraqle. By default this server will run on port 8080, if that port is unavailable you can edit the `get_user_token` default port `token = get_user_token(auth_server_port=8080)` with one of the following: 8081, 8082, 8083, 8084, 8085.

# Authenticate with Oraqle

## Before you can view and submit OqtantJobs you must first authenticate with your Oraqle account

Run the below cell to be re-directed to our login page and provide your account credentials. Once authenticated you can safely close out that tab and return to this notebook.

```python
from matplotlib import pyplot as plt
from lmfit import Model
import numpy as np
import inspect
from oqtant.oqtant_client import get_oqtant_client
from oqtant.util.auth import get_user_token
from oqtant.schemas.job import (
    OqtantJob,
    Gaussian_dist_2D,
    TF_dist_2D,
    bimodal_dist_2D,
    round_sig
)

token = get_user_token(auth_server_port=8080)
```

## Creating a OqtantClient Instance

### After successfully logging in, create an authorized session with the OqtantClient

- The OqtantClient interacts with the Oraqle server to perform remote lab functions.
- The OqtantClient object also contains all the OqtantJobs which have been submitted, run, or loaded (from database or file) during this python session

```python
oqtant_client = get_oqtant_client(token)
```

## Generate parameters to create an OqtantJob

Every OqtantJob is specified by a name, job_type, and a dictionary of input parameters. Below is an example with default parameters for a Barrier Manipulator OqtantJob:

_Ultracold Matter and Barrier Manipulator jobs are represented as OqtantJob objects with different `job_type` fields_

- Ultracold Matter: `BEC`
- Barrier Manipulator: `BARRIER`

```python
barrier_manipulator_job = {
    "name": "Example Barrier Manipulator Job",
    "job_type": "BARRIER",
    "inputs": [
        {
            "values": {
                "time_of_flight_ms": 7.0,
                "image_type": "IN_TRAP",
                "end_time_ms": 20.0,
                "rf_evaporation": {
                    "powers_mw": [500.0, 500.0, 475.0, 360.0, 220.0],
                    "frequencies_mhz": [17.0, 8.0, 4.0, 1.2, 0.1],
                    "interpolation": "LINEAR",
                    "times_ms": [-1600, -1200, -800, -400, 0],
                },
                "optical_barriers": [
                    {
                        "heights_khz": [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 25.0, 25.0, 25.0, 25.0, 25.0],
                        "positions_um": [-10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0, -10.0],
                        "interpolation": "OFF",
                        "widths_um": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        "times_ms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "shape": "GAUSSIAN",
                    },
                    {
                        "heights_khz": [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 40.0, 40.0],
                        "positions_um": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0],
                        "interpolation": "OFF",
                        "widths_um": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        "times_ms": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                        "shape": "GAUSSIAN",
                    },
                ],
                "optical_landscape": None,
                "lasers": None,
            }
        },
    ],
}

barrier_manipulator_job = oqtant_client.generate_oqtant_job(job=barrier_manipulator_job)
print(barrier_manipulator_job)
```

## Add notes to your OqtantJob input (Optional)

Every OqtantJob input can hold notes up to 500 characters long. These notes can be used to add context and additional information to each input. Notes remain tied to their inputs and can be referenced later. To add a note to a job input simply provide a string value to your desired input object like below:

```python
# In this example we are only working with a single input
# so we will add the note to the first and only input in the array
barrier_manipulator_job.inputs[0].notes = "This is an Ultracold Matter job created from Oqtant walkthrough #1"
```

## Submit the OqtantJob to run on the Oraqle hardware

`OqtantClient.run_jobs()` takes a list of OqtantJob objects, `job_list=[*OqtantJob]` and submits them to the online queue. For each OqtantJob added to the queue a unique UUID is generated and associated to it.

The output of `OqtantClient.run_jobs()` is a list of the unique UUIDs generated during submission.

If you are submitting a list of OqtantJobs and wish to wait for the results to return, use the flag `track_status=True`.

If you would like the resulting unique UUIDs to be written to a file for later reference you can do so by providing the following flags:

- `track_status=True`
- `filename="name_of_file"`
- `write=True`

When writing to a file be sure to <span style="color:red">not overwrite it</span>

```python
[barrier_manipulator_job_uuid] = oqtant_client.run_jobs(job_list=[barrier_manipulator_job], track_status=True)
```

## Best practices for referencing

To easily reference OqtantJobs from the current or previous sessions it is useful to write their ids to a file named after the job. This file can be used later to access the OqtantJob.

In this case we are saving this OqtantJob's id under a file named after this walkthrough.

```python
with open('walkthrough_2_barrier_manipulator.txt', 'w') as f:
    f.write(barrier_manipulator_job_uuid)
```

## Check the status of this session's active OqtantJobs

The OqtantClient object contains a dictionary (indexed by job_id) of all the active OqtantJobs from the current session. To keep inputs and results organized, all jobs are handled as objects of the OqtantJob class.

`OqtantClient.active jobs` contains OqtantJobs that have been submitted with `OqtantClient.run_jobs()` or loaded with either `OqtantClient.load_job_from_id()` or `OqtantClient.load_job_from_file()`.

<span style="color:red"> Note: `OqtantClient.active_jobs` does not automatically include OqtantJobs which were submitted on the Oraqle web application or in a different python session, even if those jobs are currently in the queue to run. </span>

### To access information about a OqtantJob object

**EXAMPLEJOB.DESIRED_INFO**

OqtantJob objects have the following relevant fields:

- name (str)
- job_type (str)
- status (str)
- time_submit (datetime)
- inputs (list) (see walkthrough 2 for specifics)

To see all the job information, you can print the object.

Click [here](https://www.learnpython.org/en/Classes_and_Objects) for an example-based intro to objects and classes in python.

```python
oqtant_client.see_active_jobs()
```

## Wait for OqtantJob results

If your OqtantJob is in the PENDING or RUNNING status, wait for 1 minute and run `OqtantClient.see_active_jobs()` again. When the OqtantJob "Example Ultracold Matter Generator Job" shows with status COMPLETE, proceed to the next code block

## Loading OqtantJob results

### From this session

When an OqtantJob is COMPLETE and `OqtantClient.active_jobs` is updated, the OqtantJob object is automatically populated with the job results. Define a variable to assign it to, or access it by it's id directly from the `OqtantJobs.active_jobs` dictionary.

```python
barrier_manipulator_job = oqtant_client.active_jobs[barrier_manipulator_job_uuid]
```

### Loading OqtantJob results from a previous session

When Oraqle is offline or you wish to analyze jobs from a previous run, use the job id to access it from the database and save it to the session's `OqtantClient.active_jobs`.

```python
# for jobs with multiple runs add `run=<int>` where <int> equals the input you wish to view. defaults to the first run
oqtant_client.load_job_from_id(barrier_manipulator_job_uuid)
# access job from active_jobs
barrier_manipulator_job = oqtant_client.active_jobs[barrier_manipulator_job_uuid]
```

## Accessing OqtantJob results - IT images

Results for OqtantJobs run with IT imaging contain the following fields:

```python
for key in barrier_manipulator_job.inputs[0].output.values.dict().keys():
    print(key)
```

## Viewing IT images

To view the TOF results in 2D or 1D, use the built in functions of the OqtantJob class to plot or access the results directly and plot them yourself.

```python
IT_OD = barrier_manipulator_job.get_IT()
pix_cal = barrier_manipulator_job.pix_cal

plt.figure(figsize=(12,4))
plt.title("In-Trap Optical Depth")
IT_plot = plt.imshow(IT_OD,origin="lower",
            cmap="nipy_spectral", extent=[-256, 256, -74, 74])
plt.xlabel("X position (um)")
plt.ylabel("Y position (um)")
plt.grid(visible=True)
plt.colorbar(IT_plot)

plt.show()
```

## Creating OqtantJobs based off previous ones

There may be times where you would like to create a new OqtantJob based off of a previous one. In these cases the OqtantClient class provides a method that retrieves an entire OqtantJob's input structure to allow for editing and submission. The steps to do this can be found below.

```python
# identify the job you wish to copy, this can be any job id you want to use.
# the status of the job does not matter
already_submitted_job_id = barrier_manipulator_job.external_id

# for jobs with multiple input runs add `run=<int>` where <int> equals the input you wish to view.
# without a targeted input run oqtant will default to the first run
new_barrier_manipulator_job_stub = oqtant_client.get_job_inputs_without_output(already_submitted_job_id, include_notes=False)

# at this point 'new_job_stub' is a python dict with the following keys
print("new barrier manipulator job stub keys:")
print(new_barrier_manipulator_job_stub.keys())
print("\n")

# if you wish to include any job notes associated with the existing job input you can run the
# same command above but with the `include_notes` flag set to True
# new_job_stub = oqtant_client.get_job_inputs_without_output(already_submitted_job_id, include_notes=True)

# from here you can update any of the inputs and the name of the job to your liking
new_barrier_manipulator_job_stub["name"] = "this is a stub of another job"

# at this point 'new_job_stub' can be provided to the 'generate_octant_job' function and then submitted with
# the 'run_jobs' function as demonstrated in previous steps
new_barrier_manipulator_job = oqtant_client.generate_oqtant_job(job=new_barrier_manipulator_job_stub)
print("new barrier manipulator job object:")
print(new_barrier_manipulator_job)
```

## View your current job limits

Your account provides you with a limited number of jobs which you can run in a given period of time. You can check your limits and current status against those limits via the `OqtantClient.get_limits()` method:

```python
limits = oqtant_client.get_job_limits()
print(limits)
```

If you are running batch jobs, each run is counted as a job against your limit (i.e., a batch job with 10 runs counts as 10 against your limits).
