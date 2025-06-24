import pandas as pd

FEE: float = 0.15        # Fixed fee applied to advance
HOLDBACK: float = 0.10   # Percentage of future sales to hold back as security
FORECAST_THRESHOLD: float = 30_000  # Minimum average forecast to be eligible


def determine_eligibility(forecast_df: pd.DataFrame) -> dict:
    """
    Determines if a merchant is eligible for a cash advance based on forecasted sales.

    The merchant is eligible if the average monthly forecast exceeds a defined threshold.
    If eligible, a cash advance offer is calculated based on the total sales volume,
    applying a fee and a holdback percentage.

    Args:
        forecast_df (pd.DataFrame): Forecasted sales data for a single merchant.
            Expected columns:
                - 'anonymous_uu_id': str, unique identifier for merchant
                - 'predicted_sales': float, forecasted sales for each future month

    Returns:
        dict: A dictionary with:
            - 'merchant_id': str
            - 'eligible': bool
            - 'average_forecast': float
            - 'forecast_next_6_months': list of float
            - 'cash_advance_offer': float or None
            - 'offer_formula': str
            - 'params': dict (fee and holdback)
            - 'error': optional str if input is invalid
    """
    if forecast_df.empty or "predicted_sales" not in forecast_df.columns:
        return {"error": "Invalid forecast data."}

    sales_forecast = forecast_df["predicted_sales"].tolist()
    avg_forecast = sum(sales_forecast) / len(sales_forecast)

    is_eligible = avg_forecast > FORECAST_THRESHOLD

    offer_amount = None
    if is_eligible:
        total_volume = sum(sales_forecast)
        offer_amount = round(total_volume * HOLDBACK / (1 + FEE), 2)

    return {
        "merchant_id": forecast_df["anonymous_uu_id"].iloc[0],
        "eligible": is_eligible,
        "average_forecast": round(avg_forecast, 2),
        "forecast_next_6_months": sales_forecast,
        "cash_advance_offer": offer_amount,
        "offer_formula": "sales_volume * holdback / (1 + fee)",
        "params": {"fee": FEE, "holdback": HOLDBACK}
    }
