from feature_engine import encoding as ce
from feature_engine import imputation as mdi
from feature_engine import selection as sel
from lightgbm import LGBMRegressor
from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor

from ames_model.config.core import config
from ames_model.processing import feateng

fc_pipeline = Pipeline(
    [
        (
            "impute_none",
            mdi.CategoricalImputer(
                fill_value="None",
                variables=config.mod_config.impute_none_vars,
                return_object=True,
                ignore_format=True,
            ),
        ),
        (
            "impute_missing",
            mdi.CategoricalImputer(
                fill_value="Missing",
                variables=config.mod_config.impute_mode_vars,
                return_object=True,
                ignore_format=True,
            ),
        ),
        (
            "impute_zero",
            mdi.ArbitraryNumberImputer(
                arbitrary_number=0,
                variables=config.mod_config.impute_zero_vars,
            ),
        ),
        (
            "impute_median",
            mdi.MeanMedianImputer(variables=config.mod_config.impute_median_vars),
        ),
        (
            "impute_from_other_vars",
            feateng.UseOtherColumnsImputer(
                variables=config.mod_config.impute_from_other_vars,
                references=config.mod_config.ref_vars,
            ),
        ),
        ("create", feateng.FeatureCreator()),
    ]
)

dt_pipeline = Pipeline(
    [
        ("binariser", feateng.Binariser(config.mod_config.binarise_vars)),
        (
            "rare_encoder",
            ce.RareLabelEncoder(
                tol=0.05,
                n_categories=1,
                variables=config.mod_config.cat_vars_dt
                + config.mod_config.discrete_vars_dt,
                ignore_format=True,
            ),
        ),
        (
            "cat_encoder",
            ce.OrdinalEncoder(
                encoding_method="ordered",
                variables=config.mod_config.cat_vars_dt
                + config.mod_config.discrete_vars_dt,
            ),
        ),
    ]
)

fs_pipeline = Pipeline(
    [
        ("drop", sel.DropFeatures(config.mod_config.drop_vars)),
        ("constant", sel.DropConstantFeatures()),
        ("duplicates", sel.DropDuplicateFeatures()),
        (
            "correl",
            sel.SmartCorrelatedSelection(
                selection_method="model_performance",
                estimator=DecisionTreeRegressor(
                    random_state=config.mod_config.random_state
                ),
                scoring="neg_mean_squared_error",
            ),
        ),
    ]
)

total_pipeline = Pipeline(
    [("fc", fc_pipeline), ("dt", dt_pipeline), ("fs", fs_pipeline)]
)

model_pipeline = Pipeline(
    [
        ("total", total_pipeline),
        (
            "model",
            LGBMRegressor(
                **config.mod_config.str_model_hyperp,
                **config.mod_config.int_model_hyperp,
                **config.mod_config.float_model_hyperp,
                random_state=config.mod_config.random_state,
            ),
        ),
    ]
)
