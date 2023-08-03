import logging
import sys

graph_logger = logging.getLogger()
graph_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler("graph_logger.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)


graph_logger.addHandler(file_handler)
graph_logger.addHandler(stdout_handler)
