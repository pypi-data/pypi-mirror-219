from ames_model.config.core import config
from ames_model.processing.feateng import Binariser, FeatureCreator


def test_feature_creator(sample_input_data):
    transformed = FeatureCreator().fit_transform(sample_input_data)
    assert len(transformed.columns) == 81 + 6

    new_features = [
        "TotBathrooms",
        "TotRms",
        "TotalSF",
        "TotPorchSF",
        "TotLivArea",
        "IsNew",
    ]

    for feat in new_features:
        assert feat in transformed.columns


def test_binarise(sample_input_data):
    transformed = Binariser(config.mod_config.binarise_vars).fit_transform(
        sample_input_data[config.mod_config.binarise_vars]
    )
    for var in config.mod_config.binarise_vars:
        assert transformed[var].nunique() == 2
