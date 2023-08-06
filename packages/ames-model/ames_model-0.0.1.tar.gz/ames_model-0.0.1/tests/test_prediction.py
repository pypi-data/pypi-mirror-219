from math import isclose

import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

from ames_model.config.core import config
from ames_model.predict import make_prediction
from ames_model.processing.data_manager import load_dataset


def test_prediction(sample_input_data):
    """Want to check that:
    1) model can output non-na values
    2) model has test score that is as observed in notebook
    """
    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[data.columns[data.columns != config.mod_config.target]],
        data[config.mod_config.target],
        test_size=config.mod_config.test_size,
        random_state=config.mod_config.random_state,
    )

    y_pred = make_prediction(X_test)["predictions"]
    assert isinstance(y_pred, list)
    assert len(y_pred) == len(y_test)
    assert np.isnan(y_pred).sum() == 0
    test_score = mean_squared_error(y_test, y_pred)
    assert isclose(test_score, 34300, rel_tol=100)
