import numpy as np
from sklearn.model_selection import train_test_split

from ames_model.config.core import config
from ames_model.pipeline import model_pipeline
from ames_model.processing.data_manager import load_dataset, save_pipeline


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    data[
        config.mod_config.impute_zero_vars
        + config.mod_config.impute_from_other_vars
        + config.mod_config.impute_median_vars
    ] = data[
        config.mod_config.impute_zero_vars
        + config.mod_config.impute_from_other_vars
        + config.mod_config.impute_median_vars
    ].astype(
        "float"
    )
    data[
        config.mod_config.impute_none_vars + config.mod_config.impute_mode_vars
    ] = data[
        config.mod_config.impute_none_vars + config.mod_config.impute_mode_vars
    ].astype(
        "object"
    )

    # # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(
        data[data.columns[data.columns != config.mod_config.target]],  # predictors
        data[config.mod_config.target],
        test_size=config.mod_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.mod_config.random_state,
    )
    y_train = np.log(y_train + 1)

    # fit model
    model_pipeline.fit(X_train, y_train)

    # # # persist trained model
    save_pipeline(pipeline_to_persist=model_pipeline)


if __name__ == "__main__":
    run_training()
