from pathlib import Path

from project_root import get_project_root

GRAPH_LOGGER_FILEPATH = Path(
    f"{get_project_root()}/wiggle_graph_logger/graph_logger.log"
)
