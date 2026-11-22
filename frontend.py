import streamlit as st
import requests


# PAGE CONFIGURATION
st.set_page_config(
    page_title="PakWheels Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)


# TITLE AND DESCRIPTION

st.title(" PakWheels Car Price Predictor")
st.markdown("Enter the car details below to predict whether it is a **High Price** or **Low Price** car.")
st.divider()


# INPUT FORM 
st.subheader("Car Specifications")

col1, col2 = st.columns(2)

with col1:
    year = st.number_input(
        "Year",
        min_value=1990,
        max_value=2023,
        value=2018,
        step=1
    )
    engine = st.number_input(
        "Engine Capacity (cc)",
        min_value=660,
        max_value=5000,
        value=1300,
        step=100
    )
    mileage = st.number_input(
        "Mileage (km)",
        min_value=100,
        max_value=500000,
        value=45000,
        step=1000
    )
    transmission = st.selectbox(
        "Transmission",
        options=["Automatic", "Manual"]
    )

with col2:
    fuel = st.selectbox(
        "Fuel Type",
        options=["Petrol", "Diesel", "Hybrid"]
    )
    body = st.selectbox(
        "Body Type",
        options=[
            "Sedan", "Hatchback", "SUV", "Crossover",
            "Compact SUV", "Compact sedan", "MPV",
            "Van", "Mini Van", "Pick Up", "Double Cabin",
            "Station Wagon", "Coupe", "Convertible",
            "Micro Van", "High Roof", "Truck",
            "Single Cabin", "Off-Road Vehicles",
            "Mini Vehicles", "Compact hatchback"
        ]
    )
    city = st.selectbox(
        "City",
        options=[
            "Lahore", "Karachi", "Islamabad", "Rawalpindi",
            "Faisalabad", "Multan", "Peshawar", "Quetta",
            "Gujranwala", "Sialkot", "Hyderabad", "Gujrat",
            "Bahawalpur", "Sargodha", "Sukkur", "Larkana",
            "Mardan", "Abbottabad", "Sahiwal", "Okara",
            "Other"
        ]
    )

st.divider()


# PREDICT BUTTON

if st.button(" Predict Price Category", use_container_width=True):

    # Build the JSON payload to send to FastAPI
    payload = {
        "year"         : year,
        "engine"       : engine,
        "mileage"      : mileage,
        "transmission" : transmission,
        "fuel"         : fuel,
        "body"         : body,
        "city"         : city
    }

    # Send request to FastAPI backend
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=payload,
            timeout=10
        )

        if response.status_code == 200:
            result = response.json()

            st.divider()
            st.subheader("Prediction Result")

            # Show result with color based on category
            if result["prediction"] == 1:
                st.success(f"💰 **{result['price_category']}**")
            else:
                st.info(f"💵 **{result['price_category']}**")

            st.markdown(f"📊 {result['message']}")

            # Show what was sent
            st.divider()
            st.subheader("Input Summary")
            st.json(payload)

        else:
            st.error(f"API returned error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the backend. Make sure backend.py is running in another terminal.")
    except Exception as e:
        st.error(f"Something went wrong: {e}")


# FOOTER

st.divider()
st.caption("PakWheels Car Price Predictor · SVM model served with FastAPI")