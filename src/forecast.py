import pandas as pd
import numpy as np
from typing import List, Dict, Any

# Features expected by the trained forecasting model
FEATURES: List[str] = [
    "merchant_index", "month", "year", "month_index",
    "sales_lag_1", "sales_lag_2", "rolling_mean_3", "rolling_std_3"
]


def forecast_next_months_for_one(
    merchant_df: pd.DataFrame,
    model: Any,
    months_ahead: int = 6
) -> pd.DataFrame:
    """
    Generates sales forecasts for a single merchant over a specified number of future months.

    This function uses a rolling window to simulate time-series progression.
    It updates lag and rolling statistics after each forecasted point.

    Args:
        merchant_df (pd.DataFrame): Preprocessed transaction data for one merchant.
            Required columns: ['anonymous_uu_id', 'transaction_month', 'sales_amount', ...FEATURES]
        model (Any): Trained machine learning model with a `.predict()` method.
        months_ahead (int, optional): Number of months to forecast ahead. Defaults to 6.

    Returns:
        pd.DataFrame: DataFrame containing:
            - 'anonymous_uu_id'
            - 'forecast_month' (YYYY-MM string)
            - 'predicted_sales' (float)
    """
    merchant_id = merchant_df["anonymous_uu_id"].iloc[0]
    last_month = pd.to_datetime(merchant_df["transaction_month"].max())
    forecasts: List[Dict[str, Any]] = []

    for i in range(1, months_ahead + 1):
        next_month = last_month + pd.DateOffset(months=i)
        year = next_month.year
        month = next_month.month
        month_index = (year - merchant_df["year"].min()) * 12 + month

        recent = merchant_df.iloc[-1]
        new_row = {
            "merchant_index": recent["merchant_index"],
            "month": month,
            "year": year,
            "month_index": month_index,
            "sales_lag_1": recent["sales_amount"],
            "sales_lag_2": recent["sales_lag_1"],
            "rolling_mean_3": merchant_df["sales_amount"].tail(3).mean(),
            "rolling_std_3": merchant_df["sales_amount"].tail(3).std()
        }

        X_pred = pd.DataFrame([new_row])[FEATURES]
        predicted_sales = model.predict(X_pred)[0]

        forecasts.append({
            "forecast_month": next_month.strftime("%Y-%m"),
            "predicted_sales": predicted_sales
        })

        merchant_df = pd.concat(
            [merchant_df, pd.DataFrame([{**new_row, "sales_amount": predicted_sales}])],
            ignore_index=True
        )

    return pd.DataFrame([
        {"anonymous_uu_id": merchant_id, **forecast} for forecast in forecasts
    ])
