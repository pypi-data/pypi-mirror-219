import logging

import pandas as pd

from .constants import (
    ANNOTATION_COLS,
    ANNOTATIONS_COLS_MAPPING,
    FILE_COLUMNS,
    HIERARCHY_COLS,
    RESPONSE_COLS_MAPPING,
    TASK_COLUMNS,
    TASK_TO_FORMRESPONSE_MAPPING,
    TASK_TYPE_MAPPING,
)
from .flywheel_api_helpers import (
    get_acquisition,
    get_file,
    get_file_annotations,
    get_files,
    get_form_responses,
    get_project,
    get_session,
    get_subject,
    get_task_annotations,
)

log = logging.getLogger(__name__)


def process_task_list(client, tasks, protocol_name):
    """Process a list of tasks into a reusable DataFrame.

    Args:
        client (FW_Client): The Flywheel API client.
        tasks (list): A list of tasks.
        protocol_name (str): The name of the protocol used.


    TODO: The tasks could be filtered by container level
          (project, subject, session, acquisition)

    Returns:
        DataFrame: The DataFrame of processed tasks.
    """
    if tasks:
        tasks_df = pd.json_normalize(tasks)
        tasks_df["task_type"] = tasks_df["task_type"].apply(
            lambda x: TASK_TYPE_MAPPING.get(x, "Unknown")
        )
        tasks_df["protocol.label"] = protocol_name
        tasks_df = add_hierarchy_labels(client, tasks_df)
        tasks_df["session_url"] = tasks_df["parents.session"].apply(
            lambda x: f"{client.baseurl}/#/sessions/{x}"
        )
    else:
        tasks_df = pd.DataFrame(columns=TASK_COLUMNS)
    return tasks_df


def add_task_n_file_info(tasks_df, files_df, working_df):
    """Add task and file info to a working dataframe.

    Args:
        tasks_df (DataFrame): Tasks dataframe.
        files_df (DataFrame): Files dataframe.
        working_df (DataFrame): Working dataframe.

    Returns:
        DataFrame: Working dataframe with added task and file info.
    """

    # add task info stubs
    for v in TASK_TO_FORMRESPONSE_MAPPING.values():
        working_df[v] = None

    # add hierarchy info stubs
    for v in HIERARCHY_COLS:
        working_df[v] = None

    for task_id in working_df["task_id"].unique():
        if not task_id:
            continue
        task = tasks_df.loc[tasks_df["_id"] == task_id]

        # for all matching rows, add task info
        matc_inds = working_df["task_id"] == task_id

        # if there is no matching task, skip and delete rows from working_df
        if task.empty:
            log.info("Task %s not found, skipping", task_id)
            working_df.drop(working_df.index[matc_inds], inplace=True)
            continue
        task = task.iloc[0]

        # add task info
        for k, v in TASK_TO_FORMRESPONSE_MAPPING.items():
            working_df.loc[matc_inds, v] = task[k]

        # add parent info
        # TODO: can this be done exclusively with files_df?
        for v in HIERARCHY_COLS:
            working_df.loc[matc_inds, v] = task[v]

    # If there is no file_id column, we are done
    if "file_ref.file_id" not in working_df.columns:
        return working_df

    # annotations always have file ids, supercede task info
    for file_id in working_df["file_ref.file_id"].unique():
        if not file_id:
            continue  # TODO: How to test?
        file_ref = files_df.loc[files_df["file_id"] == file_id]
        if file_ref.empty:
            log.info("File %s not found", str(file_ref))
            continue
        file_ref = file_ref.iloc[0]

        matc_inds = working_df["file_ref.file_id"] == file_id

        # add parent info
        for v in HIERARCHY_COLS:
            working_df.loc[matc_inds, v] = (
                file_ref[v] if v in files_df.columns else None
            )
        working_df.loc[matc_inds, "parents.file"] = file_ref["file_id"]
        working_df.loc[matc_inds, "file.name"] = file_ref["name"]
    return working_df


def add_hierarchy_labels(client, working_df):
    """Add hierarchy labels to a dataframe.

    Args:
        client (FW_Client): The Flywheel api client.
        working_df (DataFrame): DataFrame with hierarchy ids.

    Returns:
        DataFrame: DataFrame with added hierarchy labels.
    """
    for i, row in working_df.iterrows():
        working_df.loc[i, "project.label"] = (
            get_project(client, row["parents.project"]).get("label")
            if not pd.isna(row["parents.project"])
            else None
        )
        working_df.loc[i, "group"] = (
            get_project(client, row["parents.project"]).get("group")
            if not pd.isna(row["parents.project"])
            else None
        )
        working_df.loc[i, "subject.label"] = (
            get_subject(client, row["parents.subject"]).get("label")
            if not pd.isna(row["parents.subject"])
            else None
        )
        working_df.loc[i, "session.label"] = (
            get_session(client, row["parents.session"]).get("label")
            if not pd.isna(row["parents.session"])
            else None
        )
        working_df.loc[i, "session.timestamp"] = (
            get_session(client, row["parents.session"]).get("timestamp")
            if not pd.isna(row["parents.session"])
            else None
        )
        working_df.loc[i, "acquisition.label"] = (
            get_acquisition(client, row["parents.acquisition"]).get("label")
            if not pd.isna(row["parents.acquisition"])
            else None
        )
        if "parents.file" in working_df.columns:
            working_df.loc[i, "file.name"] = (
                get_file(client, row["parents.file"]).get("name")
                if not pd.isna(row["parents.file"]) and row["parents.file"]
                else None
            )
        elif "file_id" in working_df.columns:
            working_df.loc[i, "file.name"] = (
                get_file(client, row["file_id"]).get("name")
                if not pd.isna(row["file_id"]) and row["file_id"]
                else None
            )

    return working_df


def build_form_responses_list(
    client, form_id, form_responses_scope, parent_type, parent_id
):
    """Get a list of form responses for a given form.

    Args:
        client (FW_client): The Flywheel api client.
        form_id (str): The id of the form.
        form_responses_scope (str): The scope of the form responses. Task-associated or
                                    not.
        parent_type (str): The type of the parent container.
        parent_id (str): The id of the parent container.

    Returns:
        list: List of form responses.
    """

    export_list = []
    results_list = get_form_responses(client, parent_type, parent_id, form_id)

    if form_responses_scope in ["task", "both"]:
        export_list.extend(
            [resp for resp in results_list["results"] if resp.get("task_id")]
        )

    if form_responses_scope in ["non-task", "both"]:
        export_list.extend(
            [resp for resp in results_list["results"] if not resp.get("task_id")]
        )

    return export_list


def build_form_responses_dataframe(tasks_df, form_responses):
    """Process form responses into a DataFrame.

    Args:
        tasks_df (DataFrame): The DataFrame of associated Tasks.
        form_responses (list): List of form responses.

    Returns:
        DataFrame: Processed dataframe to save as output.
    """

    # If we have no form responses, return an empty DataFrame with the correct columns
    if not form_responses:
        log.warning("No form responses found")
        return pd.DataFrame(columns=RESPONSE_COLS_MAPPING.values())

    raw_df = pd.json_normalize(form_responses)

    # Select columns representing the form responses
    prefix = "response_data"
    selected_columns = [col for col in raw_df.columns if col.startswith(prefix)]

    # Keep columns that do not have the specific prefix
    other_columns = [col for col in raw_df.columns if not col.startswith(prefix)]

    # Melt the DataFrame to create key-value pairs
    melted_df = pd.melt(
        raw_df,
        id_vars=other_columns,
        value_vars=selected_columns,
        var_name="question",
        value_name="answer",
    )

    # This will drop rows where the answer is NaN (i.e. no response)
    # But it will not drop rows where the task_id is None and the answer is not NaN
    melted_df.dropna(subset=["answer"], inplace=True)
    melted_df["question"] = melted_df["question"].apply(
        lambda x: ".".join(x.split(prefix + ".")[1:])
    )
    melted_df.sort_values(by=["task_id"], inplace=True)

    log.info("Adding task, protocol, and hierarchy information")
    melted_df = add_task_n_file_info(tasks_df, pd.DataFrame(), melted_df)

    # Trim the columns to only those we want to export and rename them
    melted_df = melted_df[RESPONSE_COLS_MAPPING.keys()]
    melted_df.rename(columns=RESPONSE_COLS_MAPPING, inplace=True)

    return melted_df


def build_annotations_list(client, tasks_df, annotations_scope, parent_type, parent_id):
    """Build a list of annotation for tasks and files.

    Args:
        client (FW_Client): The Flywheel api client.
        tasks_df (DataFrame): The DataFrame of associated Tasks.
        annotations_scope (str): The scope of the annotations. Task-associated or not.
        container_id (str): The ID of the container to search for annotations.
        parent_type (str): The type of the parent container.
        parent_id (str): The id of the parent container.

    Returns:
        list: A list of annotations.
    """
    annotations_list = []
    files_list = []
    if annotations_scope in ["task", "both"]:
        for _, task in tasks_df.iterrows():
            annotations = get_task_annotations(client, task["_id"])
            if annotations["count"] > 0:
                annotations_list.extend(annotations["results"])

    # all annotations are associated with a file, so we need to get all files
    # and filter to the ones that are associated with annotations
    files = get_files(client, parent_type, parent_id)
    for fl in files["results"]:
        # TODO: The api call requires a file_id for the call. It would be better to
        #       use the container_id and then filter the results by the container_id
        #       Then, as above, we can create a files_df to add hierarchy
        #       information.
        annotations = get_file_annotations(client, fl["file_id"], fl["version"])
        if annotations["count"] > 0:
            # remove annotations that are associated with a task
            # contingent on the annotations_scope
            annotations = [
                annot
                for annot in annotations["results"]
                if not annot["task_id"] and annotations_scope in ["non-task", "both"]
            ]
            annotations_list.extend(annotations)
            # This is a list of files that have annotations "task" or "non-task"
            files_list.append(fl)

    files_df = pd.DataFrame(columns=FILE_COLUMNS)
    if files_list:
        files_df = pd.json_normalize(files_list)
        files_df = add_hierarchy_labels(client, files_df)
        files_df["session_url"] = files_df["parents.session"].apply(
            lambda x: f"{client.baseurl}/#/sessions/{x}"
        )

    return annotations_list, files_df


def add_units_of_measurement(annotations_df):
    """Add units of measurement to the annotations DataFrame.

    Args:
        annotations_df (DataFrame): DataFrame to add units of measurement to.

    Returns:
        DataFrame: DataFrame with units of measurement added.
    """
    # OHIF has units of measurement as Hz and AU that do not mean anything
    # TODO: Account for Area measurements
    annotations_df["data.units"] = "px"
    column_name = "data.viewport.displayedArea.rowPixelSpacing"
    if column_name in annotations_df.columns:
        annotations_df.loc[annotations_df[column_name].notnull(), "data.units"] = "mm"

    # Account for Angle measurements
    toolType = "Angle"
    angle_indices = annotations_df["data.toolType"] == toolType
    annotations_df.loc[angle_indices, "data.units"] = "degrees"

    # Account for Area Measurements
    toolTypes = [
        "RectangleRoi",
        "EllipticalRoi",
        "CircleRoi",
        "FreehandRoi",
        "ContourRoi",
    ]
    area_indices = annotations_df["data.toolType"].str.contains("|".join(toolTypes))
    annotations_df.loc[area_indices, "data.units"] += "^2"

    return annotations_df


def build_annotations_dataframe(tasks_df, files_df, annotations_list):
    """Build a DataFrame from annotations list.

    Args:
        tasks_df (DataFrame): The DataFrame of associated Tasks.
        files_df (DataFrame): The DataFrame of associated Files.
        annotations_list (list): A list of selected annotations.

    Returns:
        DataFrame: The resultant DataFrame.
    """

    # if there are no annotations, return empty dataframe
    if not annotations_list:
        log.warning("No annotations found")
        return pd.DataFrame(columns=ANNOTATIONS_COLS_MAPPING.values())

    annotations_df = pd.json_normalize(annotations_list)

    # Include Units of Measurement:
    annotations_df = add_units_of_measurement(annotations_df)

    # Select columns representing the desired annotation values
    selected_columns = [
        col for col in annotations_df.columns if col in ANNOTATION_COLS.keys()
    ]

    # Keep columns that do not have the desired annotation values
    other_columns = [
        col for col in annotations_df.columns if col not in ANNOTATION_COLS.keys()
    ]

    # Melt the DataFrame to create key-value pairs
    melted_df = pd.melt(
        annotations_df,
        id_vars=other_columns,
        value_vars=selected_columns,
        var_name="property",
        value_name="value",
    )
    # This will drop rows where the answer is NaN (i.e. no response)
    # But it will not drop rows where the task_id is None and the answer is not NaN
    melted_df.dropna(subset=["value"], inplace=True)

    # Rename the properties based on a key and sort the DataFrame
    melted_df["property"] = melted_df["property"].map(ANNOTATION_COLS)
    melted_df.sort_values(by=["task_id", "_id"], inplace=True)

    log.info("Adding task, protocol, and hierarchy information")
    melted_df = add_task_n_file_info(tasks_df, files_df, melted_df)

    # Trim the columns to only those we want to export and rename them
    melted_df = melted_df[ANNOTATIONS_COLS_MAPPING.keys()]
    melted_df.rename(columns=ANNOTATIONS_COLS_MAPPING, inplace=True)

    return melted_df
