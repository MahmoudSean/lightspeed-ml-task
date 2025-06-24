import pandas as pd
from src.eligibility import determine_eligibility


def test_determine_eligibility_eligible_case() -> None:
    """
    Test determine_eligibility with a forecast where average predicted sales
    exceed the eligibility threshold, expecting eligibility to be True.
    """
    df = pd.DataFrame({
        "anonymous_uu_id": ["test-merchant"] * 6,
        "forecast_month": ["2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"],
        "predicted_sales": [31000, 32000, 33000, 34000, 35000, 36000]  # average > 30k
    })

    result = determine_eligibility(df)

    assert result["eligible"] is True
    assert result["cash_advance_offer"] is not None and result["cash_advance_offer"] > 0
    assert result["merchant_id"] == "test-merchant"
    assert len(result["forecast_next_6_months"]) == 6


def test_determine_eligibility_ineligible_case() -> None:
    """
    Test determine_eligibility with a forecast where average predicted sales
    are below the eligibility threshold, expecting eligibility to be False.
    """
    df = pd.DataFrame({
        "anonymous_uu_id": ["test-merchant"] * 6,
        "forecast_month": ["2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"],
        "predicted_sales": [10000, 11000, 12000, 13000, 14000, 15000]  # average < 30k
    })

    result = determine_eligibility(df)

    assert result["eligible"] is False
    assert result["cash_advance_offer"] is None
