import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model and columns
model = joblib.load("logistic_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("Customer Churn Prediction App")

# UI Inputs
gender = st.selectbox("Gender", ['Male', 'Female'])
SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
Partner = st.selectbox("Has Partner", ['Yes', 'No'])
Dependents = st.selectbox("Has Dependents", ['Yes', 'No'])
tenure = st.slider("Tenure (months)", 0, 72, 12)
PhoneService = st.selectbox("Phone Service", ['Yes', 'No'])
MultipleLines = st.selectbox("Multiple Lines", ['Yes', 'No', 'No phone service'])
InternetService = st.selectbox("Internet Service", ['DSL', 'Fiber optic', 'No'])
OnlineSecurity = st.selectbox("Online Security", ['Yes', 'No', 'No internet service'])
OnlineBackup = st.selectbox("Online Backup", ['Yes', 'No', 'No internet service'])
DeviceProtection = st.selectbox("Device Protection", ['Yes', 'No', 'No internet service'])
TechSupport = st.selectbox("Tech Support", ['Yes', 'No', 'No internet service'])
StreamingTV = st.selectbox("Streaming TV", ['Yes', 'No', 'No internet service'])
StreamingMovies = st.selectbox("Streaming Movies", ['Yes', 'No', 'No internet service'])
Contract = st.selectbox("Contract", ['Month-to-month', 'One year', 'Two year'])
PaperlessBilling = st.selectbox("Paperless Billing", ['Yes', 'No'])
PaymentMethod = st.selectbox("Payment Method", 
    ['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'])
MonthlyCharges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 1500.0)

# Convert inputs into dataframe
input_dict = {
    'gender': 1 if gender == 'Male' else 0,
    'SeniorCitizen': SeniorCitizen,
    'Partner': 1 if Partner == 'Yes' else 0,
    'Dependents': 1 if Dependents == 'Yes' else 0,
    'tenure': tenure,
    'PhoneService': 1 if PhoneService == 'Yes' else 0,
    'PaperlessBilling': 1 if PaperlessBilling == 'Yes' else 0,
    'MonthlyCharges': MonthlyCharges,
    'TotalCharges': TotalCharges,
    # Add one-hot columns manually
    'MultipleLines_No phone service': int(MultipleLines == 'No phone service'),
    'MultipleLines_Yes': int(MultipleLines == 'Yes'),
    'InternetService_Fiber optic': int(InternetService == 'Fiber optic'),
    'InternetService_No': int(InternetService == 'No'),
    'OnlineSecurity_No internet service': int(OnlineSecurity == 'No internet service'),
    'OnlineSecurity_Yes': int(OnlineSecurity == 'Yes'),
    'OnlineBackup_No internet service': int(OnlineBackup == 'No internet service'),
    'OnlineBackup_Yes': int(OnlineBackup == 'Yes'),
    'DeviceProtection_No internet service': int(DeviceProtection == 'No internet service'),
    'DeviceProtection_Yes': int(DeviceProtection == 'Yes'),
    'TechSupport_No internet service': int(TechSupport == 'No internet service'),
    'TechSupport_Yes': int(TechSupport == 'Yes'),
    'StreamingTV_No internet service': int(StreamingTV == 'No internet service'),
    'StreamingTV_Yes': int(StreamingTV == 'Yes'),
    'StreamingMovies_No internet service': int(StreamingMovies == 'No internet service'),
    'StreamingMovies_Yes': int(StreamingMovies == 'Yes'),
    'Contract_One year': int(Contract == 'One year'),
    'Contract_Two year': int(Contract == 'Two year'),
    'PaymentMethod_Credit card (automatic)': int(PaymentMethod == 'Credit card (automatic)'),
    'PaymentMethod_Electronic check': int(PaymentMethod == 'Electronic check'),
    'PaymentMethod_Mailed check': int(PaymentMethod == 'Mailed check'),
}

# Create input dataframe with all columns
input_df = pd.DataFrame([input_dict])
# Add missing columns
for col in model_columns:
    if col not in input_df.columns:
        input_df[col] = 0
input_df = input_df[model_columns]

# Predict
if st.button("Predict Churn"):
    result = model.predict(input_df)[0]
    if result == 1:
        st.warning("🟡 This customer is **likely to churn**.")
    else:
        st.success("🟢 This customer is **likely to stay**.")
