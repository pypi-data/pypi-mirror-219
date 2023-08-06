from typing import Union

import numpy as np
import pandas as pd

from ames_model import __version__ as _version
from ames_model.config.core import config
from ames_model.processing.data_manager import load_pipeline
from ames_model.processing.validation import validate_inputs

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
model_pipeline = load_pipeline(file_name=pipeline_file_name)


def make_prediction(input_data: Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model pipeline."""

    X_test = pd.DataFrame(input_data)
    X_test, errors = validate_inputs(X_test)
    results = {"predictions": [], "version": _version, "errors": errors}

    if not errors:
        predictions = model_pipeline.predict(X_test)
        results = {
            "predictions": [np.exp(pred) - 1 for pred in predictions],
            "version": _version,
            "errors": errors,
        }

    return results


if __name__ == "__main__":
    from sklearn.model_selection import train_test_split

    from ames_model.processing.data_manager import load_dataset

    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[data.columns[data.columns != config.mod_config.target]],
        data[config.mod_config.target],
        test_size=config.mod_config.test_size,
        random_state=config.mod_config.random_state,
    )

    y_pred = make_prediction(X_test)["predictions"]
    # print(y_pred)
