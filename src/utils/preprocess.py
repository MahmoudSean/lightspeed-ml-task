import pandas as pd


def preprocess_for_training(df: pd.DataFrame) -> pd.DataFrame:
    """
    Preprocesses the raw monthly transaction data to prepare it for model training.

    This function performs the following operations:
    - Converts the 'transaction_month' column to datetime format.
    - Sorts data by merchant ID and transaction month.
    - Extracts month and year from the transaction date.
    - Computes a continuous month index from the start of the dataset.
    - Creates lag features (1- and 2-month lags).
    - Adds rolling statistics (mean and standard deviation over 3 months).
    - Drops rows with NaNs introduced by lag and rolling operations.

    Args:
        df (pd.DataFrame): Raw input dataframe containing at least:
            - 'anonymous_uu_id': Unique merchant identifier
            - 'transaction_month': Month of transaction (in YYYYMM format)
            - 'sales_amount': Monthly sales value

    Returns:
        pd.DataFrame: Preprocessed dataframe with additional features and no NaNs.
    """
    df = df.copy()

    df["transaction_month"] = pd.to_datetime(df["transaction_month"].astype(str), format="%Y%m")

    df.sort_values(by=["anonymous_uu_id", "transaction_month"], inplace=True)

    df["month"] = df["transaction_month"].dt.month
    df["year"] = df["transaction_month"].dt.year
    df["month_index"] = (df["year"] - df["year"].min()) * 12 + df["month"]

    df["sales_lag_1"] = df.groupby("anonymous_uu_id")["sales_amount"].shift(1)
    df["sales_lag_2"] = df.groupby("anonymous_uu_id")["sales_amount"].shift(2)

    df["rolling_mean_3"] = (
        df.groupby("anonymous_uu_id")["sales_amount"]
        .shift(1)
        .rolling(window=3)
        .mean()
    )
    df["rolling_std_3"] = (
        df.groupby("anonymous_uu_id")["sales_amount"]
        .shift(1)
        .rolling(window=3)
        .std()
    )

    df.dropna(inplace=True)

    return df
