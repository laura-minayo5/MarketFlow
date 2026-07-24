from datetime import datetime


def generate_timestamp() -> str:
    """
    Generate the current timestamp.

    Returns:
        Current timestamp in ISO 8601 format.
    """

    return datetime.now().isoformat(timespec="seconds")