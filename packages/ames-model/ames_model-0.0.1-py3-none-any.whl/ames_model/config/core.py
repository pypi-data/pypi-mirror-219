from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel
from strictyaml import YAML, load

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATA_DIR = PACKAGE_ROOT / "data"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained"


class AppConfig(BaseModel):
    """
    Application-level config.
    """

    package_name: str
    training_data_file: str
    test_data_file: str
    pipeline_save_file: str


class ModelConfig(BaseModel):
    """
    All configuration relevant to model
    training and feature engineering.
    """

    target: str
    test_size: float
    random_state: int
    variables_to_rename: Dict[str, str]
    impute_none_vars: List[str]
    impute_mode_vars: List[str]
    impute_zero_vars: List[str]
    impute_median_vars: List[str]
    impute_from_other_vars: List[str]
    ref_vars: List[str]
    binarise_vars: List[str]
    cat_vars_dt: List[str]
    discrete_vars_dt: List[str]
    drop_vars: List[str]
    int_model_hyperp: Dict[str, int]
    float_model_hyperp: Dict[str, float]
    str_model_hyperp: Dict[str, str]


class Config(BaseModel):
    """Master config object."""

    app_config: AppConfig
    mod_config: ModelConfig


def find_config_file() -> Path:
    """Locate the configuration file."""
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")


def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    """Parse YAML containing the package configuration."""

    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            parsed_config = load(conf_file.read())
            return parsed_config
    raise OSError(f"Did not find config file at path: {cfg_path}")


def create_and_validate_config(parsed_config: YAML = None) -> Config:
    """Run validation on config values."""
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # specify the data attribute from the strictyaml YAML type.
    _config = Config(
        app_config=AppConfig(**parsed_config.data),
        mod_config=ModelConfig(**parsed_config.data),
    )

    return _config


config = create_and_validate_config()

if __name__ == "__main__":
    # print(PACKAGE_ROOT)
    print(config)
