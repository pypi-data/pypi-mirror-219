"""Parser module to parse gear config.json."""
import logging
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

log = logging.getLogger(__name__)


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str, bool, bool]:
    """Parse the gear config.

    Return the requisit inputs and options for the gear.

    Returns:
        Tuple: api_key, protocol_name, annotations_scope, form_responses_scope
    """
    api_key = gear_context.get_input("api-key").get("key")
    protocol_name = gear_context.config.get("protocol_name")

    # Assign the annotations_scope and form_responses_scope variables to empty strings
    # if "none" is selected in the gear config.
    annotations_scope = gear_context.config.get("annotations-scope")
    annotations_scope = "" if annotations_scope == "none" else annotations_scope

    form_responses_scope = gear_context.config.get("form-responses-scope")
    form_responses_scope = (
        "" if form_responses_scope == "none" else form_responses_scope
    )

    return api_key, protocol_name, annotations_scope, form_responses_scope


def validate_config(protocol_name, form_responses_scope, annotations_scope):
    """Validate the gear config.

    Args:
        protocol_name (str): The name of the protocol to export.
        form_responses_scope (str): The scope of the form responses to export
                                    [task, non-task, both, none].
        annotations_scope (str): The scope of annotations to export
                                 [task, non-task, both, none].
    """

    # If annotations_scope and form_responses_scope are both empty strings, then
    # log an error and return False.
    if not annotations_scope and not form_responses_scope:
        log.error("Please select at least one of the annotations or form responses.")
        return False

    # If protocol_name is not provided, then annotations_scope and form_responses_scope
    # must be "non-task" or "".
    if not protocol_name:
        if annotations_scope not in ["non-task", ""] or form_responses_scope not in [
            "non-task",
            "",
        ]:
            log.error("A valid protocol name is needed if tasks options are selected.")
            return False

        # if form_responses_scope is "non-task" and no annotations_scope:
        if form_responses_scope == "non-task" and not annotations_scope:
            log.error("A protocol name is needed if form responses are selected.")
            return False

        # if annotations_scope is "non-task" and valid form_responses_scope:
        if form_responses_scope == "non-task":
            log.info("A protocol name is needed if form responses are selected.")
    else:
        if annotations_scope not in ["non-task", ""] and form_responses_scope not in [
            "non-task",
            "",
        ]:
            log.info("A protocol name is not needed if non-tasks options are selected.")

    return True
