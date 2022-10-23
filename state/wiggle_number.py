WIGGLE_NUMBER_FILE_PATH = "state/wiggle_number.txt"


def get_current_wiggle_number(file_path: str) -> int:

    with open(file_path, "r") as file_handle:
        wiggle_number_string = file_handle.read()

    if wiggle_number_string:
        wiggle_number = int(wiggle_number_string)
    else:
        wiggle_number = 0

    return wiggle_number


def update_wiggle_number(file_path: str, wiggle_number: int) -> int:

    with open(file_path, "w") as file_handle:
        file_handle.write(str(wiggle_number))

    return wiggle_number


if __name__ == "__main__":
    wn = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH)

    for _ in range(10):
        wn += 1

    update_wiggle_number(WIGGLE_NUMBER_FILE_PATH, wn)

    wn = get_current_wiggle_number(WIGGLE_NUMBER_FILE_PATH)

    print(wn)
