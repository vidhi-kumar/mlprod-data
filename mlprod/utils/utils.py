import logging
import socket
import subprocess

# from mlprod.utils.utils import get_logger


# DATA_UTILS_LOGGER = get_logger(Path(__file__).name)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"[{socket.gethostname()}] {name}")


def run_shell_command(cmd: str) -> str:
    print(f"Running shell command: {cmd}")
    return subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True).stdout
