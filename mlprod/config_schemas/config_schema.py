from hydra.core.config_store import ConfigStore
from pydantic.dataclasses import dataclass

@dataclass
class Config:
    dvc_remote_name: str = "google-drive-storage"
    dvc_remote_url: str = "gdrive://1NqO-ve9wRnGZyOfR88UM88qsHtFz71LU"

def setup_config() -> None:
    cs = ConfigStore.instance() 
    cs.store(name="config_schema", node=Config)