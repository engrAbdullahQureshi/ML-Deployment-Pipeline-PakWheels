import great_expectations as gx
import pandas as pd
import os

# STEP 1: Loading both CSV files

print("Loading datasets\n")

clean_df = pd.read_csv("data/clean_synthetic_dataset.csv")
corrupt_df = pd.read_csv("data/corrupted_synthetic_dataset.csv")

print(f"Clean dataset    : {clean_df.shape[0]} rows, {clean_df.shape[1]} columns")
print(f"Corrupted dataset: {corrupt_df.shape[0]} rows, {corrupt_df.shape[1]} columns")

# STEP 2: Creating GX context
context = gx.get_context()


# STEP 3: Build the Expectation Suite
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.expectations import (
    ExpectColumnValuesToNotBeNull,
    ExpectColumnValuesToBeUnique,
    ExpectColumnValuesToBeBetween,
    ExpectColumnValuesToBeInSet,
    ExpectColumnValuesToBeOfType,
)

suite = ExpectationSuite(name="sales_data_suite")

#  1. COMPLETENESS mean These columns not equal to NULL
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="sale_id"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="customer_id"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="product_id"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="sale_ts"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="quantity"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="amount"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="channel"))
suite.add_expectation(ExpectColumnValuesToNotBeNull(column="currency"))


# 2. UNIQUENESS: sale_id = unique 
suite.add_expectation(ExpectColumnValuesToBeUnique(column="sale_id"))

# 3 NUMERICAL RANGE CHECKS

suite.add_expectation(ExpectColumnValuesToBeBetween(
    column="quantity",
    min_value=1,
    max_value=10
))

suite.add_expectation(ExpectColumnValuesToBeBetween(
    column="amount",
    min_value=0.0,
    max_value=5000.0
))

# ── 4. VALID CATEGORIES ──
suite.add_expectation(ExpectColumnValuesToBeInSet(
    column="channel",
    value_set=["online", "store", "app"]
))

suite.add_expectation(ExpectColumnValuesToBeInSet(
    column="currency",
    value_set=["USD", "EUR", "PKR"]
))

# 5. DATA TYPE CHECKS 
suite.add_expectation(ExpectColumnValuesToBeOfType(
    column="quantity",
    type_="int64"
))
suite.add_expectation(ExpectColumnValuesToBeOfType(
    column="amount",
    type_="float64"
))

# 6. ROW COUNT CHECK 

from great_expectations.expectations import ExpectTableRowCountToBeBetween
suite.add_expectation(ExpectTableRowCountToBeBetween(min_value=90000, max_value=200000))
print(f"\nExpectation suite built with {len(suite.expectations)} expectations")

# STEP 4: Validation function (reusable for both datasets)
def validate_dataframe(df, suite, label):
    print(f"\n{'='*55}")
    print(f"  VALIDATING: {label}")
    print(f"{'='*55}")

    ds = context.data_sources.add_or_update_pandas(name=label)
    asset = ds.add_dataframe_asset(name=f"{label}_asset")
    batch_def = asset.add_batch_definition_whole_dataframe(f"{label}_batch")
    batch = batch_def.get_batch(batch_parameters={"dataframe": df})

    # now eunning validation against our suite
    results = batch.validate(suite)

    # Count passes and failures
    total  = len(results.results)
    passed = sum(1 for r in results.results if r.success)
    failed = total - passed

    print(f"\n  Total Expectations : {total}")
    print(f"  Passed             : {passed}  ")
    print(f"  Failed             : {failed}  ")
    print(f"  Overall Success    : {'PASSED' if results.success else 'FAILED'}")

    if failed > 0:
        print(f"\n Failed Checks -----")
        for r in results.results:
            if not r.success:
                exp_type = r.expectation_config.type
                col = getattr(r.expectation_config, 'column', 'TABLE-LEVEL')
                print(f"  ✗  Column: [{col}]  →  {exp_type}")

    return results

# STEP 5 Run validation on BOTH datasets

clean_results   = validate_dataframe(clean_df,   suite, "clean_dataset")
corrupt_results = validate_dataframe(corrupt_df, suite, "corrupted_dataset")

# STEP 6: Save detailed text reports to reports/ folder

os.makedirs("reports", exist_ok=True)

def save_report(results, filepath, label):
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{'='*55}\n")
        f.write(f"  DATA QUALITY REPORT — {label}\n")
        f.write(f"{'='*55}\n\n")

        total  = len(results.results)
        passed = sum(1 for r in results.results if r.success)
        failed = total - passed

        f.write(f"Overall Result : {'PASSED' if results.success else 'FAILED'}\n")
        f.write(f"Total Checks   : {total}\n")
        f.write(f"Passed         : {passed}\n")
        f.write(f"Failed         : {failed}\n\n")
        f.write(f"{'─'*55}\n")
        f.write(f"  DETAILED RESULTS\n")
        f.write(f"{'─'*55}\n\n")

        for r in results.results:
            status   = "PASS" if r.success else "FAIL"
            exp_type = r.expectation_config.type
            col      = r.expectation_config.kwargs.get("column", "TABLE-LEVEL")
            f.write(f"[{status}]  Column: {col}\n")
            f.write(f"         Check : {exp_type}\n")
            if not r.success and r.result:
                f.write(f"         Detail: {r.result}\n")
            f.write("\n")

    print(f"Report saved → {filepath}")

save_report(clean_results,   "reports/clean_validation_report.txt",     "CLEAN DATASET")
save_report(corrupt_results, "reports/corrupted_validation_report.txt", "CORRUPTED DATASET")

print("\n DONE! Your reports are in the reports/ folder.")