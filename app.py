import streamlit as st
import pandas as pd
import pickle


# Load the encoder, scaler, and trained model from saved files
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scaler_path = os.path.join(BASE_DIR, 'scaler.pkl')

scaler = pickle.load(open(scaler_path, 'rb'))
model_path = os.path.join(BASE_DIR, 'Model_new.pkl')
def predict_chronic_disease(age, bp, sg, al, hemo, sc, htn, dm, cad, appet, pc):
    # Create a DataFrame with input variables, following the correct order
    data_dict = {
        'age': [age],
        'bp': [bp],
        'sg': [sg],
        'al': [al],
        'hemo': [hemo],
        'sc': [sc],
        'htn': [htn],
        'dm': [dm],
        'cad': [cad],
        'appet': [appet],
        'pc': [pc]
    }
    data = pd.DataFrame(data_dict)

    # Encode the categorical columns
    data['htn'] = data['htn'].map({'yes':1, "no":0})
    data['dm'] = data['dm'].map({'yes':1, "no":0})
    data['cad'] = data['cad'].map({'yes':1, "no":0})
    data['appet'] = data['appet'].map({'good':1, "poor":0})
    data['pc'] = data['pc'].map({'normal':1, "abnormal":0})

    # Scale the numeric columns using the previously fitted scaler
    numeric_cols = ['age', 'bp', 'sg', 'al', 'hemo', 'sc']
    data[numeric_cols] = scaler.transform(data[numeric_cols])

    # Make the prediction
    prediction = Model.predict(data)

    # Return the predicted class
    return prediction[0]


# Streamlit UI
st.title('Chronic Kidney Disease Prediction')


col1, col2 = st.columns(2)

with col1:
    # Input fields for the user to enter data
    age = st.number_input("Age", min_value=1, max_value=120, value=48)
    bp = st.number_input("Blood Pressure", min_value=40, max_value=200, value=80)
    sg = st.number_input("Specific Gravity", min_value=1.005, max_value=1.050, value=1.020)
    al = st.number_input("Albumin", min_value=0.0, max_value=5.0, value=1.0)
    hemo = st.number_input("Hemoglobin", min_value=5.0, max_value=20.0, value=15.4)
    sc = st.number_input("Serum Creatinine", min_value=0.5, max_value=10.0, value=1.2)

with col2:
    # Dropdown for conditions
    htn = st.selectbox("Hypertension", ["yes",'no'])
    dm = st.selectbox("Diabetes", ["yes",'no'])
    cad = st.selectbox("Coronary Artery Disease", ["yes",'no'])
    appet = st.selectbox("Appetite", ["good", "poor"])
    pc = st.selectbox("Protein in Urine", ["normal", "abnormal"])


# When the user clicks the "Predict" button
if st.button('Predict'):
    # Make the prediction
    result = predict_chronic_disease(age,bp,sg,al,hemo,sc,htn,dm,cad,appet,pc)
    # Display the result
    if result == 1:
        st.write("### The patient has Chronic Kidney Disease (CKD).")
    else:
        st.write("### The patient does not have Chronic Kidney Disease (CKD).")pip