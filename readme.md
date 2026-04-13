# DE Assignment 3 — AI 620: Fundamentals of Data Engineering

---

## Project Structure

```
25280074_DE_ASSIGN.../
├── data/
│   ├── clean_synthetic_dataset.csv
│   ├── corrupted_synthetic_dataset.csv
│   ├── cleaned_synthetic_dataset.csv
│   ├── cleaned_pakwheels_dataset.csv
│   └── pakwheels.csv
├── models/
│   └── pakwheels_svm_model.pkl
├── reports/
│   ├── clean_validation_report.txt
│   ├── corrupted_validation_report.txt
│   ├── cleaned_synthetic_report.txt
│   ├── cleaned_pakwheels_report.txt
│   └── pakwheels_validation_report.txt
├── scripts/
│   ├── part1_task2_run_validation.py
│   ├── part1_task3_pakwheels_validation.ipynb
│   ├── part1_task4_cleaning.ipynb
│   └── part2_task1_train_model.py
├── sql/
│   └── (SQL scripts for synthetic data generation)
├── backend.py 
├── frontend.py
└── README.md
```

---

# Part 1 — Task 1: Synthetic Dataset Generation

## Structure
- SQL scripts are in: `sql/`
- Output datasets are in: `data/`

## Database
- PostgreSQL database name: `synthetic_db`

## How to Run
1. Open pgAdmin and connect to PostgreSQL
2. Select database: `synthetic_db`
3. Open Query Tool
4. Run the SQL script from the `sql/` folder

## Output
- `data/clean_synthetic_dataset.csv`
- `data/corrupted_synthetic_dataset.csv`

Both files are generated in the `data/` folder.

---

# Part 1 — Task 2: Great Expectations Validation on Synthetic Datasets

## Structure
- Validation script: `scripts/part1_task2_run_validation.py`
- Input datasets: `data/`
- Reports: `reports/`

## Datasets Used
- `data/clean_synthetic_dataset.csv`
- `data/corrupted_synthetic_dataset.csv`


## How to Run
1. Open terminal in project root directory
2. Install required libraries:
   ```bash
   pip install great-expectations pandas
   ```
3. Run the validation script:
   ```bash
   python scripts/part1_task2_run_validation.py
   ```

## Output
- `reports/clean_validation_report.txt`
- `reports/corrupted_validation_report.txt`



---

# Part 1 — Task 3: Great Expectations Validation on PakWheels Dataset

## Structure
- Notebook: `scripts/part1_task3_pakwheels_validation.ipynb`
- Dataset: `data/pakwheels.csv`
- Report: `reports/`

## Dataset Used
- `data/pakwheels.csv` 

## Description
- Applied Great Expectations on the real-world PakWheels dataset
- Validated key attributes: mileage, engine size, city, body type, transmission, fuel type

## How to Run
1. Open the notebook:
   ```
   scripts/part1_task3_pakwheels_validation.ipynb
   ```
2. Run all cells (Kernel → Restart & Run All)

## Output
- `reports/pakwheels_validation_report.txt`

---

# Part 1 — Task 4: Data Cleaning and Re-validation

## Structure
- Cleaning notebook: `scripts/part1_task4_cleaning.ipynb`
- Input datasets: `data/`
- Cleaned datasets: `data/`
- Updated reports: `reports/`

## Datasets Used
- `data/corrupted_synthetic_dataset.csv`
- `data/pakwheels.csv`

## Description
Data cleaning techniques applied:
- Handling missing values (imputation and removal)
- Removing duplicate records
- Correcting invalid or out-of-range numerical values
- Standardizing categorical values
- Resolving data type inconsistencies


## How to Run
1. Open the notebook:
   ```
   scripts/part1_task4_cleaning.ipynb
   ```
2. Run all cells (Kernel → Restart & Run All)

## Output
- `data/cleaned_synthetic_dataset.csv`
- `data/cleaned_pakwheels_dataset.csv`
- `reports/cleaned_synthetic_report.txt`
- `reports/cleaned_pakwheels_report.txt`

---

# Part 2 — Task 1: Trained Machine Learning Model

## Structure
- Training script: `scripts/part2_task1_train_model.py`
- Model output: `models/pakwheels_svm_model.pkl`

## Description
- Model: SVM (Support Vector Machine) Classifier
- Target: High-price vs Low-price car category
- Features used: Year, Engine Capacity, Mileage, Transmission, Fuel Type, Body Type, City


## How to Run
```bash
python scripts/part2_task1_train_model.py
```

## Output
- `models/pakwheels_svm_model.pkl`

---

# Part 2 — Task 2: FastAPI Backend

## Structure
- Backend file: `backend.py`
- Model used: `models/pakwheels_svm_model.pkl`

## Description
FastAPI backend that:
- Loads the trained SVM model on startup
- Accepts car feature inputs via JSON requests
- Processes input and generates predictions
- Returns predicted price category as JSON response

## How to Run
```bash
uvicorn backend:app --reload
```

## API Endpoint
```
POST /predict
```

Example input:
```json
{
  "year": 2018,
  "engine": 1300,
  "mileage": 45000,
  "transmission": "Manual",
  "fuel": "Petrol"
}
```

---

# Part 2 — Tasks 3, 4 & 5: Streamlit Frontend + Integration + Demo

## Structure
- Frontend file: `frontend.py`
- Backend file: `backend.py`

## Description
A Streamlit web application that:
- Provides an interactive UI for entering car specifications

## System Workflow
1. User enters car details in the Streamlit interface
2. Frontend sends a POST request to the FastAPI backend
3. FastAPI loads the trained SVM model
4. Model processes the input features
5. Prediction is generated
6. Result is returned to Streamlit
7. Predicted category is displayed to the user

## How to Run

**Step 1 — Start the Backend:**
```bash 
python backend.py
```

**Step 2 — Start the Frontend:**
```bash
streamlit run frontend.py
```

**Step 3 — Open in Browser:**
```
http://localhost:8501

---

## Requirements

Install all dependencies:
```bash
pip install pandas numpy scikit-learn fastapi uvicorn streamlit great-expectations joblib
```

---

