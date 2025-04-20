from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# 🔄 Load model from prediction.pkl
with open('prediction.pkl', 'rb') as f:
    data = pickle.load(f)

model = data['model']

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json.get('features')

    if not input_data:
        return jsonify({'error': 'No input features provided'}), 400

    if len(input_data) != 13:
        return jsonify({'error': f'Expected 13 features, but got {len(input_data)}'}), 400

    try:
        input_array = np.array(input_data).reshape(1, -1)

        # Predict probability
        prob = model.predict_proba(input_array)[0][1]
        percentage = prob * 100
        pred = model.predict(input_array)[0]

        # Recommendation logic
        if percentage >= 80:
            recommendation = "HIGH RISK - Seek immediate medical consultation"
        elif percentage >= 50:
            recommendation = "MODERATE RISK - Schedule a heart health check-up soon"
        else:
            recommendation = "LOW RISK - Maintain a healthy lifestyle"

        return jsonify({
            'risk_percent': round(percentage, 2),
            'prediction': int(pred),
            'recommendation': recommendation
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
