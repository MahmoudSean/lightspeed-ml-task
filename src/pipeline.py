import pandas as pd
from typing import Tuple, Any
from src.forecast import forecast_next_months_for_one
from src.eligibility import determine_eligibility


def forecast_and_eligibility_for_merchant(
    merchant_id: str,
    df: pd.DataFrame,
    model: Any,
    forecast_months: int = 6,
    threshold: float = 10000
) -> Tuple[pd.DataFrame, dict]:
    """
    Generate sales forecasts and compute eligibility for a specific merchant.

    Args:
        merchant_id (str): Unique identifier for the merchant.
        df (pd.DataFrame): Preprocessed DataFrame containing merchant transactions.
        model (Any): Trained forecasting model with a `.predict()` method.
        forecast_months (int, optional): Number of months to forecast ahead. Defaults to 6.
        threshold (float, optional): Minimum forecast threshold for eligibility (not currently used). Defaults to 10000.

    Returns:
        Tuple[pd.DataFrame, dict]: 
            - DataFrame with forecasted sales for the next `forecast_months` months.
            - Dictionary containing eligibility information.
    """
    merchant_df = df[df["anonymous_uu_id"] == merchant_id].copy()
    forecast_output = forecast_next_months_for_one(merchant_df, model, forecast_months)
    eligibility = determine_eligibility(forecast_output)

    return forecast_output, eligibility
