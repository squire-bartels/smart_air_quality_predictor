import streamlit as st
import numpy as np
import joblib

# Load the trained model
model = joblib.load('./data/raw/aqi_linear_model.pkl')

# App title
st.title("Smart City AQI Predictor")

# Input fields for features
st.header("Input Features")
pm10 = st.number_input("PM10 (μg/m³)", value=20.0)
pm25 = st.number_input("PM2.5 (μg/m³)", value=10.0)
co = st.number_input("CO (ppm)", value=0.5)
no2 = st.number_input("NO2 (ppm)", value=0.03)
o3 = st.number_input("O3 (ppm)", value=0.04)
so2 = st.number_input("SO2 (ppm)", value=0.02)

# Predict button
if st.button("Predict AQI"):
    # Prepare the input array for prediction
    features = np.array([[pm10, pm25, co, no2, o3, so2]])
    
    # Make prediction
    aqi_prediction = model.predict(features)[0]
    
    # Display the prediction
    st.success(f"Predicted AQI: {aqi_prediction:.2f}")
