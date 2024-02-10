from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass


@dataclass
class Config:
    dvc_remote_name: str = "local"
    dvc_remote_url: str = r"E:\DVC_REMOTE_STORAGE"
    dvc_raw_data_folder: str = "data/raw"


def setup_config() -> None:
    cs = ConfigStore.instance()
    cs.store(name="config_schema", node=Config)
