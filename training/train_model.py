import os
import logging
from dotenv import load_dotenv
import pandas as pd
from sklearn.metrics import root_mean_squared_error, r2_score
import joblib
from xgboost import XGBRegressor
from src.utils.preprocess import preprocess_for_training


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


FEATURES = [
    "merchant_index", "month", "year", "month_index",
    "sales_lag_1", "sales_lag_2", "rolling_mean_3", "rolling_std_3"
]
TARGET = "sales_amount"


def train_model(data_path: str, model_path: str, test_size: float = 0.2, random_state: int = 42) -> None:
    """
    Train an XGBoost regression model on merchant sales data.

    Args:
        data_path (str): Path to the CSV file containing raw transaction data.
        model_path (str): Path to save the trained model file.
        test_size (float): Proportion of data to use for testing.
        random_state (int): Random seed for reproducibility.

    Returns:
        None
    """
    logging.info("Loading data from %s", data_path)
    df = pd.read_csv(data_path)

    logging.info("Preprocessing data")
    df_processed = preprocess_for_training(df)

    logging.info("Encoding merchant IDs")
    merchant_cats = df_processed["anonymous_uu_id"].astype("category")
    df_processed["merchant_index"] = merchant_cats.cat.codes

    logging.info("Creating timestamp for sorting")
    df_processed["timestamp"] = pd.to_datetime(
        df_processed["year"].astype(str) + df_processed["month"].astype(str).str.zfill(2),
        format="%Y%m"
    )
    df_sorted = df_processed.sort_values("timestamp")

    split_point = int(len(df_sorted) * (1 - test_size))
    train_df = df_sorted.iloc[:split_point]
    test_df = df_sorted.iloc[split_point:]

    X_train = train_df[FEATURES]
    y_train = train_df[TARGET]
    X_test = test_df[FEATURES]
    y_test = test_df[TARGET]

    logging.info("Training XGBRegressor model")
    model = XGBRegressor(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    logging.info("Evaluating model")
    y_pred = model.predict(X_test)
    rmse = root_mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    logging.info(f"Model evaluation metrics - RMSE: {rmse:.2f}, R2: {r2:.4f}")

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    logging.info("Model saved to %s", model_path)


if __name__ == "__main__":
    load_dotenv()
    logging.info("Starting training process")
    train_model(
        data_path="data/monthly_transactions.csv",
        model_path="src/models/global_model.pkl"
    )
    logging.info("Training completed successfully")
