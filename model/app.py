from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the model and scaler at the start to avoid reloading for every request
def load_model():
    with open("heart_probability_model.pkl", "rb") as f:
        data = pickle.load(f)
    return data["model"], data["scaler"]

model, scaler = load_model()

# Heart Disease Prediction Function
def predict_heart_disease_risk(input_features):
    if not isinstance(input_features, list) or len(input_features) != 13:
        return {"error": "Invalid input. Please provide a list of 13 numeric features."}

    try:
        # Preprocess input
        input_array = np.array(input_features).reshape(1, -1)
        input_scaled = scaler.transform(input_array)

        # Predict probability
        probability = model.predict_proba(input_scaled)[0][1]
        percent = round(probability * 100, 2)

        # Suggestion based on risk
        if percent >= 75:
            suggestion = "🔴 High Risk: Recommend ECG, Echo, Stress Test, and Angiography."
        elif percent >= 50:
            suggestion = "🟠 Medium Risk: Recommend ECG, Echo, and Blood Test."
        elif percent >= 25:
            suggestion = "🟡 Low Risk: Recommend Lifestyle Check & Regular Monitoring."
        else:
            suggestion = "🟢 Very Low Risk: No urgent tests, maintain healthy lifestyle."

        # Return structured response
        return {
            "risk_percent": percent,
            "message": f"❤️ Heart Disease Risk: {percent}%",
            "suggestion": suggestion
        }

    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}

# API endpoint to make prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data (13 features) from the JSON request body
        input_data = request.get_json()
        input_features = input_data.get("features")

        if input_features is None or len(input_features) != 13:
            return jsonify({"error": "Please provide exactly 13 numeric features."}), 400

        result = predict_heart_disease_risk(input_features)

        # Return the result as JSON
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
