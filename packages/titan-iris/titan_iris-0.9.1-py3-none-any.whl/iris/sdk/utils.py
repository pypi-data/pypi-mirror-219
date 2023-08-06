"""This file contains the helper functions for the Iris package."""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #

import functools
import gzip
import io
import json
import tarfile
from logging import getLogger
from pathlib import Path
from typing import Callable, Mapping, Optional

import docker
import jmespath
import requests
import wget
from rich.progress import Progress
from tabulate import tabulate
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

from iris.sdk.exception import DownloadLinkNotFoundError

from .conf_manager import conf_mgr

logger = getLogger("iris.utils")

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                         Utils                                                        #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #

# rw = RefinedWed ==> Falcon
VALID_QLORA_MODELS = ["t5", "pythia", "opt", "gptj", "gptneo", "falcon"]
# ------------------------------  Helper Function for Iris Pull, Upload and Download   ------------------------------ #


def make_targz(local_folder_path: str):
    """Create a tar.gz archive of the local folder - make this deterministic / exclude timestamp info from gz header.

    Args:
        local_folder_path: The folder to be converted to a tar.gz

    Returns: A buffer containing binary of the folder as a tar.gz file

    """
    tar_buffer = io.BytesIO()
    block_size = 4096
    # Add files to a tarfile, and then by-chunk to a tar.gz file.
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(
            local_folder_path,
            arcname=".",
            filter=lambda x: None if "pytorch_model.bin" in x.name else x,
        )
    # Exclude pytorch_model.bin if present, as safetensors should be uploaded instead.
    with gzip.GzipFile(
        filename="",  # do not emit filename into the output gzip file
        mode="wb",
        fileobj=tar_buffer,
        mtime=0,
    ) as myzip:
        for chunk in iter(lambda: tar_buffer.read(block_size), b""):
            myzip.write(chunk)

    return tar_buffer


def copy_local_folder_to_image(container, local_folder_path: str, image_folder_path: str) -> None:
    """Helper function to copy a local folder into a container."""
    tar_buffer = io.BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w") as tar:
        tar.add(local_folder_path, arcname=".")
    tar_buffer.seek(0)

    # Copy the tar archive into the container
    container.put_archive(image_folder_path, tar_buffer)


def show_progress(line, progress, tasks):  # sourcery skip: avoid-builtin-shadow
    """Show task progress for docker pull command (red for download, green for extract)."""
    if line["status"] == "Downloading":
        id = f'[red][Download {line["id"]}]'
    elif line["status"] == "Extracting":
        id = f'[green][Extract  {line["id"]}]'
    else:
        # skip other statuses
        return

    if id not in tasks.keys():
        tasks[id] = progress.add_task(f"{id}", total=line["progressDetail"]["total"])
    else:
        progress.update(tasks[id], completed=line["progressDetail"]["current"])


def download_model(
    download_url: str,
    model_name: str,
    path: str = "model_storage",
    json_output: bool = False,
):
    """Helper function for iris download to download model to local machine giving download url.

    Args:
        download_url (str): url to download the model
        model_name (str): name of the model
        path (str, optional): path for model storage . Defaults to "model_storage".
        json_output (bool, optional): Whether to output the progress in json format. Defaults to False.

    Raises:
        DownloadLinkNotFoundError: Download link expired error
    """
    # download the tar file
    try:
        if json_output:
            tarfile_path = wget.download(download_url, path, bar=None)
            try:
                json.loads(tarfile_path)
            except json.JSONDecodeError:
                pass
        else:
            tarfile_path = wget.download(download_url, path)
    except Exception as e:
        raise DownloadLinkNotFoundError from e

    # Extract the tar file to a folder on the local file system
    with tarfile.open(tarfile_path) as tar:
        tar.extractall(path=f"model_storage/{model_name}/models")

    # delete the tar file
    Path(tarfile_path).unlink()


def pull_image(
    model_folder_path: str,
    container_name: str,
    job_tag: str,
    task_name: str,
    baseline_model_name: str,
    baseline: bool,
    json_output: bool = False,
):
    """Pull image.

    This function handles the logic of pulling the base image and creating a new image with
    the model files copied into it.

    Args:
        model_folder_path: The path to the model folder
        container_name: The name of the container
        job_tag: The tag of the job
        task_name: The name of the task
        baseline_model_name: The name of the baseline model
        baseline: Whether the model is the baseline model
        json_output: Whether to output the progress in json format

    """
    temp_container_name = f"temp-{container_name}"

    env_var = {
        "TASK_NAME": task_name,
        "BASELINE_MODEL_NAME": baseline_model_name,
        "BASELINE": str(baseline),
    }

    tasks = {}
    with Progress() as progress:
        # docker pull the base image
        client = docker.from_env()
        resp = client.api.pull(conf_mgr.BASE_IMAGE, stream=True, decode=True)
        for line in resp:
            if not json_output:
                show_progress(line, progress, tasks)

    # Create a new temp container
    container = client.containers.create(image=conf_mgr.BASE_IMAGE, name=temp_container_name, environment=env_var)

    copy_local_folder_to_image(container, model_folder_path, "/usr/local/triton/models/")

    # Commit the container to a new image
    container.commit(repository=container_name)

    client.images.get(container_name).tag(f"{container_name}:{job_tag}")

    # Remove the original tag
    client.images.remove(container_name)
    # Remove the temp container
    container.remove()


def dump(response, query: Optional[str] = None):
    """load, a response, optionally apply a query to its returned json, and then pretty print the result."""
    content = response
    if hasattr(response, "json"):
        content = response.json()  # shorthand for json.loads(response.text)
    if query:
        try:
            content = jmespath.search(query, content)
        except jmespath.exceptions.ParseError as e:
            print("Error parsing response")
            raise e

    return json.dumps(
        {"response": content},
        indent=4,
    )


def upload_from_file(tarred: io.BytesIO, dst: str, json_output: bool = False):
    """Upload a file from src (a path on the filesystm) to dst.

    e Args:
         tarred (io.BytesIO): The file to upload. (e.g. a tarred file).
         dst (str): The url of the destination.
         Must be a url to which we have permission to send the src, via PUT.
         json_output (bool, optional): Whether to output the progress in json format. Defaults to False.

    Returns:
         Tuple[str, requests.Response]: A hash of the file, and the response from the put request.
    """
    if json_output:
        tarred.seek(0)
        response = requests.put(dst, data=tarred)
        response.raise_for_status()
        return response
    else:
        with tqdm(
            desc="Uploading",
            total=tarred.getbuffer().nbytes,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        ) as t:
            tarred.seek(0)
            reader_wrapper = CallbackIOWrapper(t.update, tarred, "read")
            response = requests.put(dst, data=reader_wrapper)
            response.raise_for_status()
            return response


def valid_qlora(model_name: str):
    """Cleanses an input model name and then checks if QLoRA has been implemented for it.

    This is based on those available in Olympus.

    Args:
        model_name: A model name as from model_name_or_path

    Returns: (Bool) Whether QLoRa is supported for the given model.

    """

    def clean(x: str) -> str:
        return x.replace("-", "").replace("_", "").lower()

    if any(ext in clean(model_name) for ext in VALID_QLORA_MODELS):
        return True
    return False


def exception_to_json_error(e: Exception):
    """Convert an exception to a json string with the error message and type."""
    logger.error(e)
    error_dict = {"status": "failed", "error": str(e), "type": type(e).__name__}
    if hasattr(e, "status_code"):
        error_dict["status_code"] = e.status_code
    return json.dumps(error_dict, indent=4)


def flatten_dict(dict: dict) -> dict:
    """Flatten a nested dictionary.

    Args:
        dict (dict): a nested dictionary

    Returns:
        dict: a flattened dictionary
    """
    flattened_dict = {}
    for key, sub_dict in dict.items():
        for sub_key, value in sub_dict.items():
            flattened_key = f"{key}/{sub_key}"
            flattened_dict[flattened_key] = value
    return flattened_dict


def print_status_dict_results(dict: Mapping[str, float]) -> None:
    """Print a dictionary in a pretty format. Notice that the dictionary is flattened.

    e.g. input should be:
    {
        "status": "success",
        "message": "dispatched",
        "output": 15
    }.

    Args:
        dict (Mapping[str, float]): dictionary to print
    """
    headers = dict.keys()
    table = [[dict[k] for k in headers]]

    headers = [f"\033[1;31m{i}\033[0m" for i in headers]

    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def print_get_dict_results(dict: Mapping[str, float], experiment: bool = True, key_name: str = "UUID") -> None:
    """Print a dictionary in a pretty format.

    Args:
        dict (Mapping[str, float]): dictionary to print
        experiment (bool, optional): Whether the dict is a response from iris get experiment. Defaults to True.
        key_name (str, optional): The name of the key to use as the first column. Defaults to "UUID".
    """
    dict = flatten_dict(dict) if experiment else dict
    first_col = ["ID/Name"] if experiment else [key_name]

    headers = first_col + list(next(iter(dict.values())).keys())
    # Transform the data into a list of lists
    table = []  # table headers
    for key, values in dict.items():
        row = [key]
        for k in headers:
            if k in {"ID/Name", key_name}:
                pass
            elif k == "Job Results":
                if values[k] is not None:
                    row.append("\n".join(values[k]))
                else:
                    row.append("None")
            else:
                row.append(values[k])
        table.append(row)

    headers = [f"\033[1;31m{i}\033[0m" for i in headers]  # make the headers red and bold
    # Print the table
    print(tabulate(table, headers=headers, tablefmt="fancy_grid"))


def extract_experiment_results(experiment: dict, results_table: dict):
    """Extract the results from a experiment dict. return a clean format of dict of results.

    Args:
        experiment (dict): dict of detailed experiment information.
        results_table (dict): dict of results to be updated.
    """
    experiment_id = experiment["id"]  # store the numerical experiment id
    results_table[experiment_id] = {}
    if "jobs" in experiment:
        jobs = experiment["jobs"]
        if "tasks" in jobs[0]:
            tasks = jobs[0]["tasks"]

            # extract the results from the tasks
            for task in tasks:
                results_table[experiment_id][task["name"]] = {"Job Status": task["status"]}
                results_table[experiment_id][task["name"]]["Job Results"] = (
                    [f"{key}: {value}" for key, value in task["results"].items()] if task["results"] else None
                )


def handle_iris_get_response(response):
    """Handle the response from the iris get endpoint. Turn the json response into a pretty table.

    Args:
        response (str): a json format response from the iris get endpoint.
    """
    json_response = json.loads(response)["response"]
    # check if 'experiments' in the response, this is for the common case 'iris get'
    if "experiments" in json_response:
        experiments = json_response["experiments"]
        if experiments:
            results_table = {}
            for experiment in experiments:
                extract_experiment_results(experiment, results_table)
            # sort the results table by experiment id, get the most recent 5 experiments
            sorted_results_table = dict(sorted(results_table.items(), key=lambda item: item[0], reverse=True)[:5])
            print_get_dict_results(sorted_results_table)
        else:
            print_status_dict_results(json_response)
    elif "experiment" in json_response:
        experiment = json_response["experiment"]

        results_table = {}
        extract_experiment_results(experiment, results_table)
        print_get_dict_results(results_table)
    elif "artefacts" in json_response:
        artefacts = json_response["artefacts"]
        if artefacts:
            results_table = {
                artefact["uuid"]: {
                    "name": artefact["name"],
                    "type": artefact["artefact_type"],
                }
                for artefact in artefacts
            }
            print_get_dict_results(results_table, experiment=False, key_name="UUID")
        else:
            print_status_dict_results(json_response)
    elif "sessions" in json_response:
        sessions = json_response["sessions"]
        if sessions:
            results_table = {
                session["uuid"]: {
                    "model": session["model"],
                    "status": session["status"],
                }
                for session in sessions
            }
            print_get_dict_results(results_table, experiment=False, key_name="UUID")
        else:
            print_status_dict_results(json_response)
    elif len(json_response) > 0 and len(json_response[0][0]) > 0 and "message" in json_response[0][0]:
        messages = json_response[0]
        results_table = {
            message["name"]: {
                "status": message["status"],
                "message": message["message"]["message"],
                "progress": message["message"]["progress"],
            }
            for message in messages
        }
        print_get_dict_results(results_table, experiment=False, key_name="Task Name")
    else:
        print(json.dumps(json_response, indent=4))


def telemetry_decorator(function: Callable):
    """Decorator to send telemetry data to the metrics server."""

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        # Nickname is only present if the user is logged in, and
        # if the user is _a user_ i.e. not a client credentials flow machine.
        nickname = (
            conf_mgr.current_user["nickname"]
            if conf_mgr.current_user is not None and "nickname" in conf_mgr.current_user
            else None
        )
        # if str(obj) (w/ obj in args) contains any of these strings, it won't be sent
        mask_args = ["Authorization"]

        # any kwargs with these keys won't be sent
        mask_kwargs = []

        url = conf_mgr.metrics_url

        try:
            func = function(*args, **kwargs)

            headers = {"Content-Type": "application/json"}
            headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
            payload = {
                "username": nickname,
                "method": function.__name__,
                "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                "kwargs": {k: v for k, v in kwargs.items() if all(arg not in k for arg in mask_kwargs)},
                "error": None,
            }
            requests.post(url=url, headers=headers, json=payload)

            return func
        except requests.exceptions.ConnectionError:  # a more understandable message than the default ConnectionError
            ConnectionErrorMsg = json.dumps(
                {
                    "status": "failed",
                    "error": f"Error reaching {url}. Please check your internet connection.",
                    "type": "ConnectionError",
                },
                indent=4,
            )
            logger.error(str(ConnectionErrorMsg))
        except Exception as e:
            try:
                headers = {"Content-Type": "application/json"}
                headers.update({"Authorization": f"Bearer {conf_mgr.access_token}"})
                url = conf_mgr.metrics_url

                payload = {
                    "username": nickname,
                    "method": function.__name__,
                    "args": tuple(str(i) for i in args if all(arg not in str(i) for arg in mask_args)),
                    "kwargs": {k: v for k, v in kwargs.items() if k not in mask_kwargs},
                    "error": str(e),
                }
                requests.post(url=url, headers=headers, json=payload)
            except Exception as exc:
                raise exc

            raise e.with_traceback(None)

    @functools.wraps(function)
    def dummy_wrapper(*args, **kwargs):
        return function(*args, **kwargs)

    return wrapper if conf_mgr.TELEMETRY else dummy_wrapper
