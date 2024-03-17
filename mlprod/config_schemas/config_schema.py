from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class Config:
    # due to data not being populated during dvc get, i am changing to remote repo, asli wala
    # dvc_remote_name: str = "local"
    # dvc_remote_url: str = r"/home/VIDHI/dvc_remote_storage"
    # dvc_raw_data_folder: str = "data/raw"

    # dvc_remote_name: str = "gdrive"
    # # dvc_remote_url: str = r"/home/VIDHI/dvc_remote_storage"
    # dvc_remote_url: str = "gdrive://1OkozUBhgXYBaDc6qur5p7yX1o1tk-z_6"
    # dvc_raw_data_folder: str = "data/raw"
    
    # tbh, google cloud storage pe aana hi pada
    dvc_remote_name: str = "gcs-storage"
    dvc_remote_url: str = "gs://mlprod/data/raw"
    dvc_raw_data_folder: str = "data/raw"

def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
