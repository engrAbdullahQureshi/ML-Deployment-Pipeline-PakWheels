from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
import uvicorn


# STEP 1: Load the trained model when server starts
print("Loading model...")
pipeline = joblib.load("models/pakwheels_svm_model.pkl")

model          = pipeline["model"]
scaler         = pipeline["scaler"]
label_encoders = pipeline["label_encoders"]
features       = pipeline["features"]

print("Model loaded successfully!")


# STEP 2: Create FastAPI app
app = FastAPI(
    title="PakWheels Car Price Predictor",
    description="Predicts whether a car is High Price or Low Price",
    version="1.0"
)

class CarFeatures(BaseModel):
    year         : float
    engine       : float
    mileage      : float
    transmission : str
    fuel         : str
    body         : str
    city         : str


@app.get("/")
def home():
    return {"message": "PakWheels Car Price Predictor API is running!"}

@app.post("/predict")
def predict(car: CarFeatures):

   
    try:
        transmission_encoded = label_encoders["transmission"].transform([car.transmission])[0]
    except:
        transmission_encoded = 0

    try:
        fuel_encoded = label_encoders["fuel"].transform([car.fuel])[0]
    except:
        fuel_encoded = 2  # default to Petrol

    try:
        body_encoded = label_encoders["body"].transform([car.body])[0]
    except:
        body_encoded = 0

    try:
        city_encoded = label_encoders["city"].transform([car.city])[0]
    except:
        city_encoded = 0

    # --- Build feature array in correct order ---
    input_features = np.array([[
        car.year,
        car.engine,
        car.mileage,
        transmission_encoded,
        fuel_encoded,
        body_encoded,
        city_encoded
    ]])

    
    input_scaled = scaler.transform(input_features)
    prediction = model.predict(input_scaled)[0]

    if prediction == 1:
        label = "High Price"
        message = f"This car is likely priced ABOVE PKR 2,700,000"
    else:
        label = "Low Price"
        message = f"This car is likely priced BELOW PKR 2,700,000"

    return {
        "prediction"      : int(prediction),
        "price_category"  : label,
        "message"         : message,
        "input_received"  : {
            "year"         : car.year,
            "engine"       : car.engine,
            "mileage"      : car.mileage,
            "transmission" : car.transmission,
            "fuel"         : car.fuel,
            "body"         : car.body,
            "city"         : car.city
        }
    }

if __name__ == "__main__":
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)