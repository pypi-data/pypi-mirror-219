import os
import dotenv
from datetime import datetime
from rich.panel import Panel
from rich.console import Console
from agentmemory import (
    count_memories,
    create_memory,
    search_memory,
    get_memories
)

dotenv.load_dotenv()

console = Console()

DEFAULT_TYPE_COLORS = {
    "unknown": "white",
    "error": "red",
    "warning": "yellow",
    "info": "blue",
    "success": "green",
    "debug": "magenta",
    "critical": "red",
    "start": "green",
    "stop": "red",
    "pause": "yellow",
    "resume": "green",
    "epoch": "blue",
    "summary": "cyan",
    "reasoning": "blue",
    "action": "green",
    "system": "magenta",
}


def create_event(
    content,
    type=None,
    subtype=None,
    creator=None,
    metadata={},
    type_colors=DEFAULT_TYPE_COLORS,
    panel=True,
):
    """
    Create an event with provided metadata and saves it to the event log file

    Parameters:
    - content: Content of the event
    - type (optional): Type of the event.
        Defaults to None.
    - subtype (optional): Subtype of the event.
        Defaults to None.
    - creator (optional): Creator of the event.
        Defaults to None.
    - metadata (optional): Additional metadata for the event.
        Defaults to empty dictionary.
    - type_colors (optional): Dictionary with event types as keys and colors
        Defaults to empty dictionary.
    - panel (optional): Determines if the output should be within a Panel
        Defaults to True.

    Returns: None
    """
    metadata["type"] = type
    metadata["subtype"] = subtype
    metadata["creator"] = creator
    metadata["epoch"] = get_epoch()

    color = type_colors.get(type, "white")

    # if any keys are None, delete them
    metadata = {k: v for k, v in metadata.items() if v is not None}

    event = {
        "document": content,
        "metadata": metadata,
    }

    event_string = event_to_string(event)

    create_memory("events", content, metadata=metadata)
    if panel:
        console.print(Panel(event_string, style=color))
    else:
        console.print(event_string, style=color)
    write_to_log(f"{event_string}")


def get_events(type=None, n_results=None, filter_metadata=None):
    """
    Retrieve the last n events from the 'events' collection

    Parameters:
    - type (str, optional): The type of events to retrieve.
        Defaults to None.
    - n_results (int, optional): The number of results to return.
        Defaults to None.
    - filter_metadata (dict, optional): Filter by metadata keys.
        Defaults to None.

    Returns: list of event documents
    """
    if filter_metadata is None:
        filter_metadata = {}
    if type is not None:
        filter_metadata = {"type": type}
    memories = get_memories(
        "events", filter_metadata=filter_metadata, n_results=n_results
    )
    return memories


def search_events(search_text, n_results=None):
    """
    Searches the 'events' collection for events that match the search text.

    Parameters:
    - search_text (str): The text to search for.
    - n_results (int, optional): The number of results to return.
        Defaults to None.

    Returns: list of event documents that match the search criteria
    """
    memories = search_memory("events", search_text, n_results=n_results)
    return memories


def event_to_string(event):
    """
    Converts an event document into a formatted string.

    Parameters:
    - event (dict): The event document to be formatted.

    Returns: str - The formatted event string.
    """
    # Create an event with a formatted string and annotations
    e_m = event["metadata"]
    # check if e_m['epoch'] is none, set it to 0 if it is
    if e_m.get("epoch") is None:
        e_m["epoch"] = 0
    if e_m.get("type") is None:
        e_m["type"] = "unknown"
    new_event = f"{e_m['epoch']} | {e_m['type']}"
    if e_m.get("subtype") is not None:
        new_event += f"::{e_m['subtype']}"
    if e_m.get("creator") is not None:
        new_event += f" ({e_m['creator']})"
    new_event += f": {event['document']}"
    return new_event


def check_log_dirs():
    """
    Checks if ./logs and ./logs/loop exist, if not they are created.
    This function does not take any arguments or return any outputs.
    """
    if not os.path.isdir("./logs"):
        os.mkdir("./logs")
    if not os.path.isdir("./logs/loop"):
        os.mkdir("./logs/loop")


def get_epoch():
    """
    Return the current event epoch or initializes it to 0 if it is not set.
    This function does not take any arguments.
    Return: Integer value of the current event epoch.
    """
    count = count_memories("epoch")
    return count


def increment_epoch():
    """
    Increment the event epoch by 1.
    This function does not take any arguments.
    Return: Integer value of the new event epoch.
    """
    new_epoch_index = get_epoch() + 1
    document = f"Epoch {new_epoch_index} started at {str(datetime.utcnow())}"
    create_memory("epoch", document, id=new_epoch_index)
    return new_epoch_index


def write_to_log(content, write_to_debug=False, filename="logs/events.txt"):
    """
    Writes content to the event log file.
    Arguments:
    - content: String to be written in the log file.
    - write_to_debug: Whether the content is written to debug file or not.
    - filename: Name of the file where the content is written.
    Return: None
    """
    for i in range(len(filename.split("/")) - 1):
        if not os.path.exists("/".join(filename.split("/")[: i + 1])):
            os.mkdir("/".join(filename.split("/")[: i + 1]))

    if write_to_debug is False:
        with open(filename, "a") as f:
            f.write(f"{content}\n")
        return

    if write_to_debug is True or os.environ.get("DEBUG") in [
        "1",
        "true",
        "True",
    ]:
        debug_filename = filename.replace(".txt", "_debug.txt")
        with open(debug_filename, "a") as f:
            f.write(f"DEBUG >>> {content}\n")
