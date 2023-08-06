"""Frontend for Home Assistant."""
from pathlib import Path


# pylint: disable=unused-variable
def where() -> Path:
    """Return path to the frontend."""
    return Path(__file__).parent
