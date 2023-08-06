from typing import List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class Binariser(BaseEstimator, TransformerMixin):
    """Changes a variable into a binary one, which takes
    on either 0 or 1 values.
    """

    def __init__(self, variables: List[str]):
        if not isinstance(variables, list):
            raise ValueError("Variables should be a list")

        self.variables = variables

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for var in self.variables:
            X[var] = np.where(X[var] == 0, 0, 1)

        return X


class UseOtherColumnsImputer(BaseEstimator, TransformerMixin):
    """Imputes missing values in a variable with values
    from a reference variable
    """

    def __init__(self, variables: List[str], references: List[str]):
        if (not isinstance(variables, list)) or (not isinstance(references, list)):
            raise ValueError("Inputs should be a list")

        if len(variables) != len(references):
            raise ValueError("Length of both lists should be the same")

        self.variables = variables
        self.references = references

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for i in range(len(self.variables)):
            X[self.variables[i]] = np.where(
                X[self.variables[i]].isnull(),
                X[self.references[i]],
                X[self.variables[i]],
            )
        return X


class FeatureCreator(BaseEstimator, TransformerMixin):
    """Creates extra features during feature engineering"""

    def fit(self, X: pd.DataFrame, y: pd.Series = None):
        return self

    def transform(self, X: pd.DataFrame):
        X = X.copy()

        # discrete
        X["TotBathrooms"] = (
            X["BsmtFullBath"]
            + X["BsmtHalfBath"] * 0.5
            + X["FullBath"]
            + X["HalfBath"] * 0.5
        )
        X["TotRms"] = X["TotBathrooms"] + X["TotRmsAbvGrd"]

        # continuous
        X["TotalSF"] = X["TotalBsmtSF"] + X["FirstFlrSF"] + X["SecondFlrSF"]
        X["TotPorchSF"] = (
            X["OpenPorchSF"]
            + X["ThreeSsnPortch"]
            + X["EnclosedPorch"]
            + X["ScreenPorch"]
            + X["WoodDeckSF"]
        )
        X["TotLivArea"] = X["GrLivArea"] + X["TotalBsmtSF"]

        # time diff
        year_vars = ["YearBuilt", "YearRemodAdd", "GarageYrBlt"]
        for var in year_vars:
            X[var] = X["YrSold"] - X[var]

        X["IsNew"] = np.where(X["YearRemodAdd"] == X["YearBuilt"], 0, 1)

        return X
