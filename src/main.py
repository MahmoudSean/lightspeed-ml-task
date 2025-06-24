from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
import structlog
from src.pipeline import forecast_and_eligibility_for_merchant
from src.utils.preprocess import preprocess_for_training
from typing import Dict, Any

logger = structlog.get_logger()

app = FastAPI(title="Lightspeed Forecasting API")

MODEL_PATH = "src/models/global_model.pkl"
DATA_PATH = "data/monthly_transactions.csv"

logger.info("Loading model and data into memory", model_path=MODEL_PATH, data_path=DATA_PATH)

model = joblib.load(MODEL_PATH)
raw_df = pd.read_csv(DATA_PATH)
preprocessed_df = preprocess_for_training(raw_df)
preprocessed_df["merchant_index"] = preprocessed_df["anonymous_uu_id"].astype("category").cat.codes

logger.info("Model and data loaded successfully", merchants_count=preprocessed_df["anonymous_uu_id"].nunique())


@app.get("/predict/{merchant_id}")
def predict(merchant_id: str) -> Dict[str, Any]:
    """
    Endpoint to generate sales forecast and eligibility for a given merchant_id.

    Args:
        merchant_id (str): The unique identifier of the merchant.

    Returns:
        dict: Forecast results and eligibility info.
    """
    if merchant_id not in preprocessed_df["anonymous_uu_id"].unique():
        logger.warning("Merchant ID not found", merchant_id=merchant_id)
        raise HTTPException(status_code=404, detail="Merchant ID not found")

    forecast_output, eligibility = forecast_and_eligibility_for_merchant(
        merchant_id, preprocessed_df, model
    )

    logger.info(
        "Forecast and eligibility computed",
        merchant_id=merchant_id,
        eligible=eligibility.get("eligible"),
        average_forecast=eligibility.get("average_forecast"),
        cash_advance_offer=eligibility.get("cash_advance_offer")
    )

    return {
        "merchant_id": merchant_id,
        "forecast_next_6_months": forecast_output.to_dict(orient="records"),
        "eligible": eligibility["eligible"],
        "average_forecast": eligibility["average_forecast"],
        "cash_advance_offer": eligibility["cash_advance_offer"],
        "offer_formula": eligibility["offer_formula"],
        "params": eligibility["params"]
    }
