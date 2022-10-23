import json

from exceptions.database import NodeExistsError

DATABASE_FILE_PATH = "database/database.json"


def load_database(file_path: str) -> dict:

    try:
        with open(file_path, "r") as file_handle:
            database = json.load(file_handle)

            return database

    except Exception:
        return {}


def add_item_to_database(file_path: str, item: dict):

    database = load_database(file_path)

    for wiggle_number, _ in item.items():
        # todo check agaisnts wiggle number state
        if str(wiggle_number) in database.keys():
            raise NodeExistsError(
                f"Node {wiggle_number} already exisits did you mean to update"
            )

    database.update(item)

    with open(file_path, "w") as file_handle:
        json.dump(database, file_handle, ensure_ascii=False)


def wipe_database(file_path: str):

    with open(file_path, "w") as file_handle:
        file_handle.write("")


if __name__ == "__main__":
    x = load_database(DATABASE_FILE_PATH)
    i = {
        109: {
            "wiggle_number": 19,
            "node_label": "NodeLabel",
            "created_at": 1666534101.384132,
            "updated_at": None,
            "belongings": {"uuid": "7e48f6ae-b25a-4634-91af-b1fb67b90ad9"},
            "relations": None,
        }
    }
    # update_database(DATABASE_FILE_PATH)

    add_item_to_database(DATABASE_FILE_PATH, i)

    # wipe_database(DATABASE_FILE_PATH)
