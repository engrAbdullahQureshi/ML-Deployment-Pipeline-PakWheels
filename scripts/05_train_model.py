import pandas as pd
import numpy as np
import joblib
import os
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report


# STEP 1: Loading clean PakWheels dataset
print("Loading cleaned PakWheels dataset...")
df = pd.read_csv("data/cleaned_pakwheels_dataset.csv")
print(f"Dataset shape: {df.shape}")


# STEP 2: Select the features we need
features = ["year", "engine", "mileage", "transmission", "fuel", "body", "city"]
target_col = "price"

df = df[features + [target_col]].copy()
print(f"\nAfter selecting features: {df.shape}")


# STEP 3: Handle missing values
print("\nNull values before handling:")
print(df.isnull().sum())

df["year"] = df["year"].fillna(df["year"].median())
df["engine"] = df["engine"].fillna(df["engine"].median())
df["fuel"] = df["fuel"].fillna(df["fuel"].mode()[0])
df["body"] = df["body"].fillna(df["body"].mode()[0])

df = df.dropna(subset=["price"])

print("\nNull values after handling:")
print(df.isnull().sum())
print(f"Shape after handling nulls: {df.shape}")


# STEP 4: Feature Engineering
median_price = df["price"].median()
print(f"\nMedian price (threshold): PKR {median_price:,.0f}")
df["price_category"] = (df["price"] > median_price).astype(int)

print(f"Low price  (0): {(df['price_category'] == 0).sum()} cars")
print(f"High price (1): {(df['price_category'] == 1).sum()} cars")

# we only need the category
df = df.drop(columns=["price"])


# STEP 5: Encode categorical variables
print("\nEncoding categorical variables...")

categorical_cols = ["transmission", "fuel", "body", "city"]
label_encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le
    print(f"  {col}: {list(le.classes_)}")


# STEP 6: Feature Selection
X = df[features]
y = df["price_category"]

print(f"\nFeatures shape : {X.shape}")
print(f"Target shape   : {y.shape}")


# STEP 7: Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"\nTraining set : {X_train.shape[0]} rows")
print(f"Testing set  : {X_test.shape[0]} rows")


# STEP 8: Feature Scaling using StandardScaler
print("\nScaling features...")
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)


# STEP 9: Train the SVM model
print("\nTraining SVM model..")
model = SVC(kernel="rbf", C=1.0, gamma="scale", random_state=42)
model.fit(X_train_scaled, y_train)
print("Training complete!")

# STEP 10: Evaluate the model
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n{'='*45}")
print(f"  MODEL EVALUATION")
print(f"{'='*45}")
print(f"  Accuracy : {accuracy * 100:.2f}%")
print(f"\nClassification Report:")
print(classification_report(y_test, y_pred,
      target_names=["Low Price", "High Price"]))


# STEP 11: Save everything needed for deployment
os.makedirs("models", exist_ok=True)

# Save the complete pipeline as one object
model_pipeline = {
    "model"          : model,
    "scaler"         : scaler,
    "label_encoders" : label_encoders,
    "median_price"   : median_price,
    "features"       : features
}

joblib.dump(model_pipeline, "models/pakwheels_svm_model.pkl")
print(f"\nModel saved → models/pakwheels_svm_model.pkl")
print("\nDone.")