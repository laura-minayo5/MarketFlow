import csv
from config.paths import SEEDS


def load_lookup(csv_file: str) -> list[dict]:
    """
    Load a lookup table from the seeds folder.
    Args:
        csv_file:
            Name of the CSV file.
    Returns:
        A list of dictionaries.
    """

    file_path = SEEDS / csv_file

    with open(file_path, mode="r", encoding="utf-8", newline="") as file:

        # Read each row as a dictionary.
        reader = csv.DictReader(file)

        return list(reader)

# Use load_column() when you only need one column.
def load_column(csv_file: str, column: str) -> list[str]:
    """
    Load the values from a single column in a lookup table.
    Args:
        csv_file:
            Name of the CSV file.
        column:
            Name of the column to extract.
    Returns:
        A list containing the values from the specified column.
    """

    # Read the CSV file as a list of dictionaries.
    rows = load_lookup(csv_file)

    # Store the extracted values.
    result = []

    # Iterate through each row (dictionary) in the lookup table.
    for row in rows:

        # Extract the value from the requested column
        # and add it to the result list.
        result.append(row[column])

    # Return a list containing only the requested column values.
    return result