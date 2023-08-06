from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from pydantic import BaseModel, ValidationError

from ames_model.config.core import config


def validate_inputs(input_data: pd.DataFrame) -> Tuple[pd.DataFrame, Optional[dict]]:
    """Check model inputs for unprocessable values."""
    input_data = input_data.rename(columns=config.mod_config.variables_to_rename)
    input_data[
        config.mod_config.impute_zero_vars
        + config.mod_config.impute_from_other_vars
        + config.mod_config.impute_median_vars
    ] = input_data[
        config.mod_config.impute_zero_vars
        + config.mod_config.impute_from_other_vars
        + config.mod_config.impute_median_vars
    ].astype(
        "float"
    )
    input_data[
        config.mod_config.impute_none_vars + config.mod_config.impute_mode_vars
    ] = input_data[
        config.mod_config.impute_none_vars + config.mod_config.impute_mode_vars
    ].astype(
        "object"
    )
    # convert syntax error field names (beginning with numbers)
    errors = None

    try:
        # replace numpy nans so that pydantic can validate
        MultipleHouseDataInputs(
            inputs=input_data.replace({np.nan: None}).to_dict(orient="records")
        )
    except ValidationError as error:
        errors = error.json()

    return input_data, errors


class HouseDataInputSchema(BaseModel):
    Alley: Optional[str] = None
    BedroomAbvGr: Optional[int] = None
    BldgType: Optional[str] = None
    BsmtCond: Optional[str] = None
    BsmtExposure: Optional[str] = None
    BsmtFinSF1: Optional[int] = None
    BsmtFinSF2: Optional[int] = None
    BsmtFinType1: Optional[str] = None
    BsmtFinType2: Optional[str] = None
    BsmtFullBath: Optional[int] = None
    BsmtHalfBath: Optional[int] = None
    BsmtQual: Optional[str] = None
    BsmtUnfSF: Optional[int] = None
    CentralAir: Optional[str] = None
    Condition1: Optional[str] = None
    Condition2: Optional[str] = None
    Electrical: Optional[str] = None
    EnclosedPorch: Optional[int] = None
    ExterCond: Optional[str] = None
    ExterQual: Optional[str] = None
    Exterior1st: Optional[str] = None
    Exterior2nd: Optional[str] = None
    Fence: Optional[str] = None
    FireplaceQu: Optional[str] = None
    Fireplaces: Optional[int] = None
    FirstFlrSF: Optional[int] = None
    Foundation: Optional[str] = None
    FullBath: Optional[int] = None
    Functional: Optional[str] = None
    GarageArea: Optional[int] = None
    GarageCars: Optional[int] = None
    GarageCond: Optional[str] = None
    GarageFinish: Optional[str] = None
    GarageQual: Optional[str] = None
    GarageType: Optional[str] = None
    GarageYrBlt: Optional[float] = None
    GrLivArea: Optional[int] = None
    HalfBath: Optional[int] = None
    Heating: Optional[str] = None
    HeatingQC: Optional[str] = None
    HouseStyle: Optional[str] = None
    Id: Optional[int] = None
    KitchenAbvGr: Optional[int] = None
    KitchenQual: Optional[str] = None
    LandContour: Optional[str] = None
    LandSlope: Optional[str] = None
    LotArea: Optional[int] = None
    LotConfig: Optional[str] = None
    LotFrontage: Optional[float] = None
    LotShape: Optional[str] = None
    LowQualFinSF: Optional[int] = None
    MSSubClass: Optional[int] = None
    MSZoning: Optional[str] = None
    MasVnrArea: Optional[float] = None
    MasVnrType: Optional[str] = None
    MiscFeature: Optional[str] = None
    MiscVal: Optional[int] = None
    MoSold: Optional[int] = None
    Neighborhood: Optional[str] = None
    OpenPorchSF: Optional[int] = None
    OverallCond: Optional[int] = None
    OverallQual: Optional[int] = None
    PavedDrive: Optional[str] = None
    PoolArea: Optional[int] = None
    PoolQC: Optional[str] = None
    RoofMatl: Optional[str] = None
    RoofStyle: Optional[str] = None
    SaleCondition: Optional[str] = None
    SaleType: Optional[str] = None
    ScreenPorch: Optional[int] = None
    SecondFlrSF: Optional[int] = None
    Street: Optional[str] = None
    ThreeSsnPortch: Optional[int] = None
    TotRmsAbvGrd: Optional[int] = None
    TotalBsmtSF: Optional[int] = None
    Utilities: Optional[str] = None
    WoodDeckSF: Optional[int] = None
    YearBuilt: Optional[int] = None
    YearRemodAdd: Optional[int] = None
    YrSold: Optional[int] = None


class MultipleHouseDataInputs(BaseModel):
    inputs: List[HouseDataInputSchema]
