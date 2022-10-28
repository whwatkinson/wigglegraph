from graph_logger.graph_logger import graph_logger

WIGGLE_NUMBER_FILE_PATH = "state/wiggle_number.txt"


def get_current_wiggle_number(file_path: str) -> int:
    """
    Gets the current Wiggle number, which is the next available.
    :param file_path: The file path to the Wiggle number state file
    :return: The Current Wiggle number
    """
    graph_logger.debug("Attempting getting Wiggle number")
    with open(file_path, "r") as file_handle:
        wiggle_number_string = file_handle.read()

    if wiggle_number_string:
        graph_logger.debug("Wiggle number found, casting to int")
        wiggle_number = int(wiggle_number_string)
    else:
        graph_logger.info("Wiggle number not set retuning 0")
        wiggle_number = 0
    graph_logger.info(f"Succesfully got Wiggle number was {wiggle_number}")
    return wiggle_number


def update_wiggle_number(file_path: str, wiggle_number: int) -> int:
    """
    Updates the Wiggle state file to the next availble number
    :param file_path: The file path to the Wiggle number state file
    :param wiggle_number: The Current Wiggle number
    :return: The Wiggle number
    """

    graph_logger.debug("Updating state for wiggle number")
    with open(file_path, "w") as file_handle:
        file_handle.write(str(wiggle_number))
    graph_logger.debug("Scuccesfully updated state for Wiggle number")
    return wiggle_number


if __name__ == "__main__":
    wn = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH)

    for _ in range(10):
        wn += 1

    update_wiggle_number(WIGGLE_NUMBER_FILE_PATH, wn)

    wn = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH)

    print(wn)
