# DE Assignment 3 - Task 1 (Part A)

## Structure
- SQL code is in: `sql/part1_Task1_DataGeneration.sql`
- Output datasets are in: `data/`

## Database
- PostgreSQL database name: `synthetic_db`

## How to Run
1. Open pgAdmin and connect to PostgreSQL
2. Select database: `synthetic_db`
3. Open Query Tool
4. Run the SQL file:
   `sql/part1_task1_data_generation.sql`

## Output
- `clean_synthetic_dataset.csv`
- `corrupted_synthetic_dataset.csv`

Both files will be generated in the `data/` folder.

## -------------------------------------------------------------------------


# DE Assignment 3 - Task 2 (Part B)

## Structure
- Validation script is in: `scripts/part1_task2_run_validation.py`
- Input datasets are in: `data/`
- Generated reports are in: `reports/`

## Datasets Used
- `clean_synthetic_dataset.csv`
- `corrupted_synthetic_dataset.csv`

Both datasets were generated in Task 1 and are used here for data quality validation.

## How to Run
1. Open terminal in project root directory  
2. Install required libraries:
   ```bash
   pip install great-expectations pandas

   python scripts/part1_task2_run_validation.py

## Output
1. reports/clean_validation_report.txt
2. reports/corrupted_validation_report.txt

Both reports contain detailed validation results, including passed and failed expectations for each dataset.