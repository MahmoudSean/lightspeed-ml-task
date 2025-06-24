# Merchant Forecasting & Cash Advance Eligibility API

This project forecasts monthly sales for merchants and determines their eligibility for cash advances based on projected sales performance.

---

## 🔍 Problem Statement

Given historical monthly transaction data, forecast the next 6 months' sales revenue for each merchant and determine whether they qualify for a cash advance. If eligible, calculate the offer amount based on Lightspeed Capital's business rules.

---

## 📁 Folder Structure

<pre lang="text"> ```text lightspeed-ml-task/ │ ├── data/ # Raw input data (monthly_transactions.csv) ├── src/ # Core source code (API, ML pipeline, utilities) │ ├── forecast.py # Forecasting logic and models │ ├── utils/ # Helper functions (e.g., preprocessing) │ ├── models/ # Trained model artifacts │ ├── eligibility.py # Eligibility logic │ ├── pipeline.py # Orchestration of forecasting + eligibility │ └── main.py # FastAPI app entrypoint ├── tests/ # Unit and integration tests ├── Dockerfile # Container setup ├── requirements.txt # Python dependencies ├── run_tests.sh # Script to run unit/integration tests └── README.md # This file ``` </pre>


---

## 🧪 Setup Instructions

1. **Clone this repo**

```bash
git clone <your_repo_url>
cd lightspeed-ml-task
```

2. **Add data file**

Place the monthly_transactions.csv file inside the data/ directory.


3. **Set up Python environment**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. **Train the model and run the API**

```bash
./training/train.sh
```

5. **Run locally**

In a bash terminal run: 
```bash
./run_app.sh
```
Then open your browser:
📍 http://localhost:8000/docs for Swagger UI.


Or you can run the application using docker:
- Build and run:

```bash
docker build -t merchant-api .
docker run -p 8000:8000 merchant-api
```


| Endpoint         | Method | Description                              |
| ---------------- | ------ | ---------------------------------------- |
| `/predict/{merchant_id}` | GET    | Returns 6-month forecast for merchant + Returns eligibility & cash advance offer


6. **Testing**

This repo includes both unit and integration tests.

- tests/test_eligibility.py — Unit tests for eligibility logic
- tests/test_api.py — Integration tests for API endpoints

```bash
./run_tests.sh
```

7. **🚀 Next Steps / Improvements**
- Use Poetry for more robust dependency and environment management.

- Add CORS support to the FastAPI app for cross-origin requests.

- Expand test coverage with additional unit and integration tests.

- Secure API endpoints by implementing authentication and authorization, especially if deployed outside a private subnet.

- Use a secrets manager (e.g., Azure Key Vault, AWS Secrets Manager) for storing sensitive config such as API keys or DB credentials.

- Automate builds and deployment by adding a CI/CD pipeline (GitHub Actions, Azure Pipelines, etc.) YAML file to the repo.

