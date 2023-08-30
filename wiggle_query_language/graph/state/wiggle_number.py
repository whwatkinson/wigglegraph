from pathlib import Path

from testing import WIGGLE_NUMBER_TEST_FILE_PATH
from wiggle_graph_logger.graph_logger import graph_logger


def get_current_wiggle_number(file_path: Path) -> int:
    """
    Gets the current WiggleNumber, which is the next available.
    :param file_path: The filepath to the Wiggle number file
    :return: The Current Wiggle number
    """
    graph_logger.debug("Attempting getting WiggleNumber")
    with open(file_path, "r") as file_handle:
        wiggle_number_string = file_handle.read()

    if wiggle_number_string:
        graph_logger.debug("Wiggle number found, casting to int")
        wiggle_number = int(wiggle_number_string)
    else:
        # TODO find a better solution
        raise Exception("HOLD FIRE on overwriting the issue!")
        graph_logger.info("Wiggle number not set retuning 0")
        wiggle_number = 0
    graph_logger.info(f"Successfully got Wiggle number was {wiggle_number}")
    return wiggle_number


def update_wiggle_number(file_path: Path, new_wiggle_number: int) -> int:
    """
    Updates the WiggleNumber file to the next available number.
    :param file_path: The file path to the Wiggle number file.
    :param new_wiggle_number: The Current Wiggle number
    :return: The Wiggle number
    """

    graph_logger.debug("Updating state for WiggleNumber")
    with open(file_path, "w") as file_handle:
        file_handle.write(str(new_wiggle_number))
    graph_logger.debug("Successfully updated state for WiggleNumber")
    return new_wiggle_number


if __name__ == "__main__":
    wn = get_current_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH)

    for _ in range(10):
        wn += 1

    update_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH, wn)

    wn = get_current_wiggle_number(WIGGLE_NUMBER_TEST_FILE_PATH)

    print(wn)
