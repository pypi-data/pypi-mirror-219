"""This module contains helper functions for interacting with the Flywheel API.

TODO: Move this to a separate package.
"""
import logging
from functools import lru_cache

from fw_client import ClientError

log = logging.getLogger(__name__)


@lru_cache(maxsize=512)
def get_task(client, task_id):
    """Get task from api by task_id.

    Args:
        client (FW_Client): The Flywheel api client.
        task_id (str): The ID of the task.

    Returns:
        dict: Result of the api call.
    """
    try:
        result = client.get(f"/api/readertasks/{task_id}")
    except ClientError:
        # If the task does not exist, return None
        result = None
    except Exception:  # pylint: disable=broad-except
        # If another error occurs, handle it by returning None
        result = None

    return result


def put_reader_task(client, task_id, task_data):
    """Put task to api by task_id.

    Args:
        client (FW_Client): The Flywheel api client.
        task_id (str): The ID of the task.
        task_data (dict): The task data to put.

    Returns:
        dict: Result of the api call.
    """
    return client.put(f"/api/readertasks/{task_id}", json=task_data)


@lru_cache(maxsize=512)
def get_project_tasks(
    client, project_id, protocol_id=None, parent_type=None, parent_id=None
):
    """Get tasks from api by project_id.

    Args:
        client (FW_Client): The Flywheel api client.
        project_id (str): The ID of the project.
        protocol_id (str, optional): The ID of the protocol. Defaults to None.
        parent_type (str, optional): The type of the parent container. Defaults to None.
        parent_id (str, optional): The ID of the parent container. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    filter_str = ""
    # NOTE: This API endpoint requires that the protocol_id in the filter string
    #       has double quotes around it.
    #       This is not the case for other container ids.
    if protocol_id:
        filter_str = f'protocol_id="{protocol_id}"'
    # If the destination container is a subject, session, or acquisition
    if parent_type in ["subject", "session", "acquisition"] and parent_id:
        filter_str += "," if filter_str else ""
        filter_str += f"parents.{parent_type}={parent_id}"
    if filter_str:
        return client.get(
            f"/api/readertasks/project/{project_id}",
            params={"filter": filter_str},
        )
    else:
        return client.get(f"/api/readertasks/project/{project_id}")


@lru_cache(maxsize=512)
def get_task_annotations(client, task_id):
    """Get task annotations from api by task_id.

    TODO: Can this be filtered by the container in which the gear is run?

    Args:
        client (FW_Client): The Flywheel api client.
        task_id (str): The ID of the task.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/readertasks/{task_id}/annotations")


def batch_create_tasks(client, tasks_definition):
    """Batch create tasks.

    Args:
        client (FW_Client): The Flywheel api client.
        tasks_definition (dict): Dictionary of tasks to create.

    Returns:
        dict: Result of the api call.
    """
    return client.post("/api/readertasks/batch", json=tasks_definition)


def post_viewer_config(client, config):
    """Post viewer config to api client.

    Args:
        client (FW_Client): The Flywheel api client.
        config (dict): The viewer config object.

    Returns:
        dict: Result of the api call.
    """
    return client.post("/api/viewerconfigs", json=config)


@lru_cache(maxsize=512)
def get_viewer_config(client, config_id=None, config_name=None):
    """Get viewer config by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        config_id (str): The ID of the viewer config.
        config_name (str): The name of the viewer config.

    Returns:
        dict: Result of the api call.
    """
    if config_name:
        params = {"filter": f"name={config_name}"}
        return client.get("/api/viewerconfigs", params=params)
    if config_id:
        return client.get(f"/api/viewerconfigs/{config_id}")
    return {}


def post_protocol(client, protocol: dict):
    """Post protocol to api client.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol (dict): The protocol object.

    Returns:
        dict: Result of the api call.
    """
    return client.post("/api/read_task_protocols", json=protocol)


@lru_cache(maxsize=512)
def get_protocol(client, protocol_id=None, protocol_name=None, project_id=None):
    """Get protocol by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_id (str): The ID of the protocol. Defaults to None.
        protocol_name (str): The name of the protocol. Defaults to None.
        project_id (str): The ID of the project. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    if protocol_name and project_id:
        params = {"filter": f"name={protocol_name},parents.project={project_id}"}
        return client.get("/api/read_task_protocols", params=params)
    if protocol_id:
        return client.get(f"/api/read_task_protocols/{protocol_id}")
    return client.get("/api/read_task_protocols")


def put_protocol(client, protocol_id, protocol):
    """Put protocol to api client.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_id (str): The ID of the protocol.
        protocol (dict): The protocol object.

    Returns:
        dict: Result of the api call.
    """
    return client.put(f"/api/read_task_protocols/{protocol_id}", json=protocol)


def post_form(client, form_data: dict):
    """Post form to api client.

    Args:
        client (FW_Client): The Flywheel api client.
        form (dict): The form object.

    Returns:
        dict: Result of the api call.
    """
    return client.post("/api/forms", json=form_data)


@lru_cache(maxsize=512)
def get_form(client, form_id=None, project_id=None):
    """Get form by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        form_id (str): The ID of the form. Defaults to None.
        project_id (str): The ID of the project. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    if project_id:
        params = {"filter": f"parents.project={project_id}"}
        return client.get("/api/forms", params=params)
    if form_id:
        return client.get(f"/api/forms/{form_id}")
    return client.get("/api/forms")


@lru_cache(maxsize=512)
def get_form_responses(
    client, parent_type=None, parent_id=None, form_id=None, task_id=None
):
    """Get form responses from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        parent_type (str): The type of parent container. Defaults to None.
        parent_id (str): The ID of the parent container. Defaults to None.
        form_id (str): The ID of the form. Defaults to None.
        task_id (str): The ID of the task. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    filter_string = ""
    if parent_type and parent_id:
        filter_string = f"parents.{parent_type}={parent_id}"

    if form_id:
        filter_string += "," if filter_string else ""
        filter_string += f"form_id={form_id}"

    if task_id:
        filter_string += "," if filter_string else ""
        filter_string += f"task_id={task_id}"

    params = {"filter": filter_string}
    return client.get("/api/formresponses", params=params)


def post_form_responses(
    client, parent_type, parent_id, form_id, task_id, response_data
):
    """Post form responses to api client.

    Args:
        client (FW_Client): The Flywheel api client.
        parent_type (str): The type of parent container.
        parent_id (str): The ID of the parent container.
        form_id (str): The ID of the form.
        task_id (str): The ID of the task.
        response_data (dict): The response_data of the form data object.

    Returns:
        dict: Result of the api call.
    """
    post_data = {
        "form_id": form_id,
        "parent": {"id": parent_id, "type": parent_type},
        "task_id": task_id,
        "response_data": response_data,
    }
    return client.post("/api/formresponses", json=post_data)


@lru_cache(maxsize=512)
def get_project(client, project_id):
    """Get project by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        project_id (str): The ID of the project.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/projects/{project_id}")


@lru_cache(maxsize=512)
def get_subject(client, subject_id):
    """Get subject by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        subject_id (str): The ID of the subject.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/subjects/{subject_id}")


@lru_cache(maxsize=512)
def get_session(client, session_id):
    """Get session by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        session_id (str): The ID of the session.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/sessions/{session_id}")


@lru_cache(maxsize=512)
def get_acquisition(client, acquisition_id):
    """Get the acquisition by id from api client.

    Args:
        client (FW_Client): The Flywheel api client.
        acquisition_id (str): The ID of the acquisition.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/acquisitions/{acquisition_id}")


@lru_cache(maxsize=512)
def get_file(client, file_id):
    """Get a file object by file_id and version

    Args:
        client (FW_Client): The Flywheel api client.
        file_id (str): The ID of the file.

    Returns:
        dict: Result of the api call.
    """
    return client.get(f"/api/files/{file_id}")


@lru_cache(maxsize=512)
def get_files(client, parent_type, parent_id):
    """Get files by container.
    Args:
        client (FW_Client): The Flywheel api client.
        parent_type (str): Container type of the parent the gear is run within.
        parent_id (str): Container ID of the parent the gear is run within.

    Returns:
        dict: Result of the api call.
    """

    filter_string = f"parents.{parent_type}={parent_id}"
    params = {"filter": filter_string}
    return client.get("/api/files", params=params)


@lru_cache(maxsize=512)
def get_file_annotations(client, file_id, version=None):
    """Get all annotations for a file version.

    Args:
        client (FW_Client): The Flywheel api client.
        file_id (str): The id of the file.
        version (int, optional): Version of the file. Defaults to None.

    Returns:
        dict: Result of the api call.
    """
    if version:
        filter_string = f"file_ref.file_id={file_id},file_ref.version={version}"
    else:
        filter_string = f"file_ref.file_id={file_id}"

    return client.get("/api/annotations", params={"filter": filter_string})


def post_file_annotation(client, data, viewer_format, file_id=None, task_id=None):
    """Post annotations for a file.

    Args:
        client (FW_Client): The Flywheel api client.
        data (dict): The annotation data to post.
        viewer_format (str): The viewer format of the annotation.
        file_id (str): The id of the file. Defaults to None.
        task_id (str): The id of the task. Defaults to None.

    Returns:
        dict: Result of the api call.
    """

    post_data = {
        "_id": "",
        "file_id": file_id,
        "task_id": task_id,
        "data": data,
        "viewer_format": viewer_format,
    }

    return client.post("/api/annotations", json=post_data)


def post_file_annotations(client, annotations, file_id=None, task_id=None):
    """Iterate through annotations and post them into the api.

    Args:
        client (FW_Client): The Flywheel api client.
        annotations (dict): The annotation data to post.
        file_id (str): The id of the file. Defaults to None.
        task_id (str): The id of the task. Defaults to None.

    Returns:
        dict: A dictionary of results.
    """
    results = {"count": 0, "total": 0, "results": []}
    for annotation in annotations:
        result = post_file_annotation(
            client, annotation["data"], annotation["viewer_format"], file_id, task_id
        )
        if result:
            results["count"] += 1
            results["total"] += 1
            results["results"].append(result)

    return results


@lru_cache(maxsize=512)
def get_protocol_from_name(client, protocol_name, project_id=None):
    """Get Protocol object from api by name.

    Args:
        client (FW_Client): The Flywheel api client.
        protocol_name (str): The name of the protocol. Protocol Names are unique within
                             a project.
        project_id (str, optional): The ID of the project. Defaults to None.

    Returns:
        dict or None: The protocol object or None if not found.
    """
    filter_string = f"label={protocol_name}"
    if project_id:
        filter_string += f",project={project_id}"

    protocols = client.get("/api/read_task_protocols", params={"filter": filter_string})
    if protocols["count"] == 1:
        protocol = protocols["results"][0]
    elif protocols["count"] > 1:
        log.warning(
            "Found %s protocols with name %s.", protocols["count"], protocol_name
        )
        log.warning("Using first protocol found.")
        protocol = protocols["results"][0]
    else:
        if project_id:
            log.error(
                "No protocol found with name %s for project %s.",
                protocol_name,
                project_id,
            )
            log.error(
                "Ensure you have the protocol define for the project you are "
                "running the gear under."
            )
        else:
            log.warning("No protocol found with name %s.", protocol_name)
        protocol = None
    return protocol
