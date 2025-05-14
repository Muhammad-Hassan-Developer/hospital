from flask import Flask, render_template, request,jsonify
import pickle
import numpy as np
import os

# Create the Flask app
app = Flask(__name__)

# Load the trained heart and kidney models and scalers
with open('heart_disease_model.pkl', 'rb') as heart_model_file:
    heart_model = pickle.load(heart_model_file)

with open('scaler.pkl', 'rb') as heart_scaler_file:
    heart_scaler = pickle.load(heart_scaler_file)

with open('kidney_disease_model.pkl', 'rb') as kidney_model_file:
    kidney_model = pickle.load(kidney_model_file)

with open('kidney_disease_scaler.pkl', 'rb') as kidney_scaler_file:
    kidney_scaler = pickle.load(kidney_scaler_file)


# Landing Page with options
@app.route('/')
def landing():
    return render_template('landing.html')

# Route for Heart Disease Form
@app.route('/heart-disease')
def heart_disease_form():
    return render_template('heart_disease_form.html')

# Route for Kidney Disease Form
@app.route('/kidney-disease')
def kidney_disease_form():
    return render_template('kidney_disease_form.html')

# Route for Pneumonia Detection Form
@app.route('/pneumonia-disease')
def pneumonia_disease_form():
    return render_template('pneumonia_disease_form.html')

# Handle Heart Disease Prediction
@app.route('/predict-heart', methods=['POST'])
def predict_heart_disease():
   # Get the form data for heart disease
    rest_bp = float(request.form['rest_bp'])
    chest_pain = int(request.form['chest_pain'])
    thalassemia = int(request.form['thalassemia'])
    age = int(request.form['age'])
    fasting_bs = int(request.form['fasting_bs'])
    max_hr = int(request.form['max_hr'])
    exercise_angina = int(request.form['exercise_angina'])
    gender = int(request.form['gender'])
    st_slope = int(request.form['st_slope'])
    cholesterol = float(request.form['cholesterol'])
    st_depression = float(request.form['st_depression'])
    rest_ecg = int(request.form['rest_ecg'])
    num_vessels = int(request.form['num_vessels'])

    # Create a NumPy array for model input
    features = np.array([[rest_bp, chest_pain, thalassemia, age, fasting_bs, max_hr, exercise_angina,
                          gender, st_slope, cholesterol, st_depression, rest_ecg, num_vessels]])

    # Scale the features using heart disease scaler
    features_scaled = heart_scaler.transform(features)

    # Make the prediction using heart disease model
    prediction = heart_model.predict(features_scaled)

    # Return the result for heart disease
    result = "The patient is likely to have heart disease." if prediction[0] == 1 else "The patient is unlikely to have heart disease."
    return render_template('result.html', result=result)
    
@app.route('/predict-heart-json', methods=['POST'])
def predict_heart_disease_json():
    # Get the JSON data for heart disease
    data = request.get_json()

    # Access the data from the JSON object
    rest_bp = float(data['rest_bp'])
    chest_pain = int(data['chest_pain'])
    thalassemia = int(data['thalassemia'])
    age = int(data['age'])
    fasting_bs = int(data['fasting_bs'])
    max_hr = int(data['max_hr'])
    exercise_angina = int(data['exercise_angina'])
    gender = int(data['gender'])
    st_slope = int(data['st_slope'])
    cholesterol = float(data['cholesterol'])
    st_depression = float(data['st_depression'])
    rest_ecg = int(data['rest_ecg'])
    num_vessels = int(data['num_vessels'])

    # Create a NumPy array for model input
    features = np.array([[rest_bp, chest_pain, thalassemia, age, fasting_bs, max_hr, exercise_angina,
                          gender, st_slope, cholesterol, st_depression, rest_ecg, num_vessels]])

    # Scale the features using heart disease scaler (assuming you've loaded the scaler)
    features_scaled = heart_scaler.transform(features)

    # Make the prediction using the heart disease model (assuming you've loaded the model)
    prediction = heart_model.predict(features_scaled)

    # Return the result for heart disease
    result = "The patient is likely to have heart disease." if prediction[0] == 1 else "The patient is unlikely to have heart disease."
    return jsonify({"prediction": result})

# Handle Kidney Disease Prediction
@app.route('/predict-kidney', methods=['POST'])
def predict_kidney_disease():
    # Get the form data for kidney disease
    gender = float(request.form['Gender'])
    age = float(request.form['Age'])
    has_diabetes = float(request.form['HasDiabetes'])
    has_heart_disease = float(request.form['HasHeartDisease'])
    has_vascular_disease = float(request.form['HasVascularDisease'])
    has_smoking_history = float(request.form['HasSmokingHistory'])
    has_high_blood_pressure = float(request.form['HasHighBloodPressure'])
    has_high_cholesterol = float(request.form['HasHighCholesterol'])
    has_obesity = float(request.form['HasObesity'])
    takes_cholesterol_meds = float(request.form['TakesCholesterolMeds'])
    takes_diabetes_meds = float(request.form['TakesDiabetesMeds'])
    takes_blood_pressure_meds = float(request.form['TakesBloodPressureMeds'])
    takes_acei_arb = float(request.form['TakesACEIorARB'])
    cholesterol_level = float(request.form['CholesterolLevel'])
    creatinine_level = float(request.form['CreatinineLevel'])
    kidney_function = float(request.form['KidneyFunction_eGFR'])
    systolic_blood_pressure = float(request.form['SystolicBloodPressure'])
    diastolic_blood_pressure = float(request.form['DiastolicBloodPressure'])
    body_mass_index = float(request.form['BodyMassIndex'])

    # Create a NumPy array for model input
    features = np.array([[gender, age, has_diabetes, has_heart_disease, has_vascular_disease,
                          has_smoking_history, has_high_blood_pressure, has_high_cholesterol,
                          has_obesity, takes_cholesterol_meds, takes_diabetes_meds,
                          takes_blood_pressure_meds, takes_acei_arb, cholesterol_level,
                          creatinine_level, kidney_function, systolic_blood_pressure,
                          diastolic_blood_pressure, body_mass_index]])

    # Scale the features using kidney disease scaler
    features_scaled = kidney_scaler.transform(features)

    # Make the prediction using kidney disease model
    prediction = kidney_model.predict(features_scaled)

    # Return the result for kidney disease
    result = "The patient is likely to have kidney disease." if prediction[0] == 1 else "The patient is unlikely to have kidney disease."
    return render_template('result.html', result=result)


if __name__ == '__main__':
    app.run(debug=True)
