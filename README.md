# PakWheels Car Price ML Pipeline

An end-to-end machine learning pipeline on **62,302 real used-car listings from PakWheels** (Pakistan's largest car marketplace): data generation → automated data-quality validation → cleaning → model training → a FastAPI prediction service with a Streamlit UI.

The model classifies a car as **High Price** or **Low Price** (above or below the median listing price) from its specifications, with **92.4% test accuracy**.

## Pipeline

```
sql/01  PostgreSQL ──► synthetic clean + corrupted datasets (100k rows each)
             │
scripts/02-03  Great Expectations ──► data-quality reports (reports/)
             │
scripts/04  cleaning ──► cleaned datasets (data/)
             │
scripts/05  scikit-learn SVM ──► models/pakwheels_svm_model.pkl
             │
backend.py  FastAPI  POST /predict  ◄── frontend.py  Streamlit UI
```

## 1. Data quality first

Before any modelling, the data is checked with **Great Expectations** suites covering completeness (no nulls), uniqueness, valid ranges, allowed category values and data types.

- **Synthetic test bed:** a PostgreSQL script generates a clean sales dataset and a deliberately corrupted copy (nulls, negative quantities, unknown categories). Running the same suite on both proves the checks catch real problems.
- **Real data:** on the PakWheels dataset, 16 of 19 checks passed. The 3 failures pointed at real issues: **2,453 out-of-range mileage values (3.9%)**, **455 invalid engine sizes** and **209 invalid prices plus 472 missing prices**.

Reports are in `reports/`, before and after cleaning.

## 2. Cleaning

Imputation and removal of missing values, de-duplication, correcting out-of-range numbers, standardising categories and fixing data types. 62,302 raw rows → 59,338 cleaned rows.

## 3. Model

| Step | Choice |
|---|---|
| Features | year, engine capacity, mileage, transmission, fuel, body type, city |
| Target | price above / below the median (binary) |
| Missing values | median (numeric), mode (categorical) |
| Encoding / scaling | label encoding, `StandardScaler` |
| Model | SVM, RBF kernel |
| Split | 80/20 train/test |

**Result: 92.4% test accuracy.** For context, a naive rule ("newer than the median year = expensive") gets about 76%, so the model adds roughly 17 points.

The model, scaler, encoders and threshold are saved together as one `joblib` bundle, so the API applies exactly the same preprocessing as training.

**Possible improvements:** one-hot encoding for city (label encoding implies an order), computing the median threshold on training data only, adding make/model as features, and returning a validation error for unknown categories instead of a default value.

## 4. Serving

- **`backend.py`**: FastAPI app that loads the model bundle at startup and exposes `POST /predict` with Pydantic input validation
- **`frontend.py`**: Streamlit form that calls the API and displays the prediction

```bash
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" \
  -d '{"year": 2018, "engine": 1300, "mileage": 45000, "transmission": "Manual", "fuel": "Petrol", "body": "Sedan", "city": "Lahore"}'
```

## Tech

Python, PostgreSQL, Great Expectations, Pandas, NumPy, scikit-learn, joblib, FastAPI, Pydantic, Uvicorn, Streamlit

## Run

```bash
pip install pandas numpy scikit-learn great-expectations joblib fastapi uvicorn streamlit requests

# optional: regenerate synthetic data (edit the output paths in the SQL file first)
#   run sql/01_generate_synthetic_data.sql in PostgreSQL

python scripts/02_validate_synthetic_data.py      # validation reports
# run scripts/03_validate_pakwheels.ipynb and scripts/04_clean_data.ipynb
python scripts/05_train_model.py                  # trains + saves the model

uvicorn backend:app --reload                      # API on http://localhost:8000
streamlit run frontend.py                         # UI
```

A trained model is already included in `models/`, so you can start the API and UI directly.

## Repository layout

```
data/      raw, synthetic and cleaned datasets
models/    trained SVM bundle
reports/   Great Expectations validation reports
scripts/   validation, cleaning and training (run in numbered order)
sql/       synthetic data generation
backend.py FastAPI service
frontend.py Streamlit UI
```
