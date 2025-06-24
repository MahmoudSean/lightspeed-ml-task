from fastapi.testclient import TestClient
from src.main import app  # Adjusted import path assuming src/app/main.py

client = TestClient(app)


def test_predict_valid_merchant() -> None:
    """
    Test the /predict endpoint with a valid merchant_id.
    Replace the merchant_id with one existing in your dataset for real tests.
    """
    valid_merchant_id = "00315bf6-6762-4a1f-829d-8b04134efb09"

    response = client.get(f"/predict/{valid_merchant_id}")
    assert response.status_code == 200

    data = response.json()
    assert "forecast_next_6_months" in data
    assert isinstance(data["forecast_next_6_months"], list)
    assert "eligible" in data
    assert "cash_advance_offer" in data


def test_predict_invalid_merchant() -> None:
    """
    Test the /predict endpoint with an invalid merchant_id.
    Should return 404 with appropriate detail message.
    """
    response = client.get("/predict/merchant-does-not-exist")
    assert response.status_code == 404
    assert response.json()["detail"] == "Merchant ID not found"
