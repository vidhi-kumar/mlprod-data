from pathlib import Path
from mlprod.utils.utils import get_logger, run_shell_command
from subprocess import CalledProcessError


DATA_UTILS_LOGGER = get_logger(Path(__file__).name)


def is_dvc_initialized() -> bool:
    return (Path().cwd() / ".dvc").exists()


def initialize_dvc() -> None:
    if is_dvc_initialized():
        DATA_UTILS_LOGGER.info("DVC is already initialized")
        return
    
    DATA_UTILS_LOGGER.info("Initializing DVC")
    run_shell_command("dvc init")
    run_shell_command("dvc config core.analytics false")
    run_shell_command("dvc config core.autostage true")
    run_shell_command("git config --global --add safe.directory /app")
    run_shell_command("git add .dvc")
    run_shell_command("git commit -nm 'Initialized DVC'")


def initialize_dvc_storage(dvc_remote_name: str, dvc_remote_url: str) -> None:
    if not run_shell_command("dvc remote list"):
        DATA_UTILS_LOGGER.info("Initializing DVC storage")
        run_shell_command(f"dvc remote add -d {dvc_remote_name} {dvc_remote_url}")
        DATA_UTILS_LOGGER.info("adding dvc config file to git")
        run_shell_command("git add .dvc/config")
        DATA_UTILS_LOGGER.info("making git commit after successful dvc configuration")
        run_shell_command("git commit -nm 'Configured remote DVC storage'")
    else:
        DATA_UTILS_LOGGER.info("DVC storage already initialized")


def commit_to_dvc(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    current_version = ""
    if not current_version:
        current_version = "0"
    DATA_UTILS_LOGGER.info(f"Current version {current_version}")
    next_version = f"v{int(current_version)+1}"
    run_shell_command(f"dvc add {dvc_raw_data_folder}")
    run_shell_command(f"git add .")
    run_shell_command("git config --global --add safe.directory /app")
    DATA_UTILS_LOGGER.info(f"doing git commit for version update")
    run_shell_command(f"git commit -m 'Updated version of data from v{current_version} to {next_version}'")
    DATA_UTILS_LOGGER.info(f"adding new tag for the new version")
    run_shell_command(f"git tag -a {next_version} -m 'Data version {next_version}'")
    DATA_UTILS_LOGGER.info(f"pushing data to remote location")
    run_shell_command(f"dvc push {dvc_raw_data_folder}.dvc --remote {dvc_remote_name}")
    run_shell_command("git push --follow-tags")
    run_shell_command("git push -f --tags")
        

def make_new_data_version(dvc_raw_data_folder: str, dvc_remote_name: str) -> None:
    try:
        status = run_shell_command(f"dvc status {dvc_raw_data_folder}.dvc")
        if status == "Data and pipelines are up to date.\n":
            DATA_UTILS_LOGGER.info("Data and pipelines are up to date.")
            return
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)
    except CalledProcessError:
        commit_to_dvc(dvc_raw_data_folder, dvc_remote_name)