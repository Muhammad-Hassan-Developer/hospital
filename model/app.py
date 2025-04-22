from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all origins (or use: CORS(app, origins=['http://localhost']))

# Load model and scaler
def load_model():
    with open("heart_probability_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data["model"], data["scaler"]

model, scaler = load_model()

# Prediction function
def predict_heart_disease_risk(input_features):
    if not isinstance(input_features, list) or len(input_features) != 13:
        return {"error": "Invalid input. Please provide a list of 13 numeric features."}

    try:
        input_array = np.array(input_features).reshape(1, -1)
        input_scaled = scaler.transform(input_array)

        prediction = model.predict(input_scaled)[0]

        if prediction == 1:
            suggestion = "🔴 High Risk: Recommend ECG, Echo, Stress Test, and Angiography."
        else:
            suggestion = "🟢 Low Risk: Maintain a healthy lifestyle."

        return {
            "prediction": prediction,
            "message": f"Heart Disease Risk: {'High' if prediction == 1 else 'Low'}",
            "suggestion": suggestion
        }

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_data = request.get_json()
        input_features = input_data.get("features")

        if input_features is None or len(input_features) != 13:
            return jsonify({"error": "Please provide exactly 13 numeric features."}), 400

        result = predict_heart_disease_risk(input_features)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
