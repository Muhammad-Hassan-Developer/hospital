<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Heart Disease Prediction</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f2f4f7;
      padding: 30px;
    }

    .container {
      display: flex;
      max-width: 1200px;
      margin: auto;
      background-color: #fff;
      padding: 25px;
      border-radius: 10px;
      box-shadow: 0 2px 12px rgba(0,0,0,0.1);
    }

    .left-col, .right-col {
      width: 50%;
      padding: 15px;
    }

    h2 {
      text-align: center;
      color: #333;
      margin-bottom: 20px;
    }

    .form-group {
      margin-bottom: 15px;
    }

    label {
      display: block;
      margin-bottom: 5px;
      font-weight: bold;
    }

    input[type="number"], input[type="text"], select {
      width: 100%;
      padding: 10px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }

    .radio-group {
      display: flex;
      gap: 15px;
      margin-top: 5px;
    }

    button {
      background-color: #007bff;
      color: white;
      padding: 12px;
      border: none;
      border-radius: 5px;
      width: 100%;
      font-size: 16px;
      cursor: pointer;
    }

    button:hover {
      background-color: #0056b3;
    }

    .result {
      margin-top: 20px;
      text-align: center;
      font-weight: bold;
      font-size: 16px;
    }

    .card {
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 15px;
    }
  </style>
</head>
<body>
  <div class="container">
    <!-- Left Side: Form for Heart Disease Prediction -->
    <div class="left-col">
      <h2>Heart Disease Prediction</h2>
      <form id="predictForm">
        <div class="form-group">
          <label for="age">Age:</label>
          <input type="number" id="age" name="age" placeholder="e.g. 63 (Range: 29-77)" required />
        </div>

        <div class="form-group">
          <label>Sex:</label>
          <div class="radio-group">
            <label><input type="radio" name="sex" value="1" required /> Male</label>
            <label><input type="radio" name="sex" value="0" /> Female</label>
          </div>
        </div>

        <div class="form-group">
          <label for="cp">Chest Pain Type (cp):</label>
          <select id="cp" name="cp" required>
            <option value="0">Typical Angina</option>
            <option value="1">Atypical Angina</option>
            <option value="2">Non-Anginal Pain</option>
            <option value="3">Asymptomatic</option>
          </select>
        </div>

        <div class="form-group">
          <label for="trestbps">Resting Blood Pressure (trestbps) [mm Hg]:</label>
          <input type="number" id="trestbps" name="trestbps" placeholder="e.g. 145 (Range: 90-200 mm Hg)" required />
        </div>

        <div class="form-group">
          <label for="chol">Cholesterol (chol) [mg/dl]:</label>
          <input type="number" id="chol" name="chol" placeholder="e.g. 233 (Range: 125-300 mg/dl)" required />
        </div>

        <div class="form-group">
          <label>Fasting Blood Sugar > 120 mg/dl (fbs):</label>
          <div class="radio-group">
            <label><input type="radio" name="fbs" value="1" required /> Yes</label>
            <label><input type="radio" name="fbs" value="0" /> No</label>
          </div>
        </div>

        <div class="form-group">
          <label for="restecg">Resting ECG (restecg):</label>
          <select id="restecg" name="restecg" required>
            <option value="0">Normal</option>
            <option value="1">ST-T Wave Abnormality</option>
            <option value="2">Left Ventricular Hypertrophy</option>
          </select>
        </div>

        <div class="form-group">
          <label for="thalach">Max Heart Rate Achieved (thalach) [bpm]:</label>
          <input type="number" id="thalach" name="thalach" placeholder="e.g. 150 (Range: 80-200 bpm)" required />
        </div>

        <div class="form-group">
          <label for="exang">Exercise Induced Angina (exang):</label>
          <select id="exang" name="exang" required>
            <option value="0">No</option>
            <option value="1">Yes</option>
          </select>
        </div>

        <div class="form-group">
          <label for="oldpeak">ST Depression (oldpeak) [mm]:</label>
          <input type="number" step="0.1" id="oldpeak" name="oldpeak" placeholder="e.g. 2.3 (Range: 0.0-6.0 mm)" required />
        </div>

        <div class="form-group">
          <label for="slope">Slope of ST Segment (slope):</label>
          <select id="slope" name="slope" required>
            <option value="0">Upsloping</option>
            <option value="1">Flat</option>
            <option value="2">Downsloping</option>
          </select>
        </div>

        <div class="form-group">
          <label for="ca">Number of Major Vessels (ca):</label>
          <select id="ca" name="ca" required>
            <option value="0">0</option>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
          </select>
        </div>

        <div class="form-group">
          <label for="thal">Thalassemia (thal):</label>
          <select id="thal" name="thal" required>
            <option value="1">Fixed Defect</option>
            <option value="2">Normal</option>
            <option value="3">Reversible Defect</option>
          </select>
        </div>

        <button type="submit">Predict</button>
      </form>

      <div class="result" id="result"></div>
    </div>

   <!-- Right Side: API Values -->
<div class="right-col" style="margin-top: 30px;">
  <h3 style="text-align:center; color:#333; margin-bottom: 15px;">
    <span style="font-weight: bold;">💓 Real-Time</span> Readings
  </h3>

  <div style="
    background: #fff;
    border-radius: 15px;
    padding: 30px 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    text-align: center;
    max-width: 350px;
    margin: auto;
  ">
    <div style="font-size: 60px; color: #e74c3c; animation: beat 1s infinite;">
      <i class="fas fa-heart"></i>
    </div>

    <p style="font-size: 20px; margin: 20px 0 10px; color: #555;">
      <strong>Message:</strong> <span id="api_msg" style="color: #333;">Loading...</span>
    </p>

    <p style="font-size: 20px; color: #555;">
      <strong>Heart Rate (BPM):</strong> <span id="api_bpm" style="color: #333;">Loading...</span>
    </p>
  </div>
</div>

<!-- CSS for Heart Animation -->
<style>
  @keyframes beat {
    0%, 100% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.2);
    }
  }
</style>


  <script>
    function fetchBPMData() {
      fetch('http://192.168.43.120/bpm')
        .then(response => response.json())
        .then(data => {
          document.getElementById('api_msg').textContent = data.msg || 'N/A';
          document.getElementById('api_bpm').textContent = data.bpm || 'N/A';
        })
        .catch(error => console.error('Error fetching API data:', error));
    }

    // Fetch data every 5 seconds
    setInterval(fetchBPMData, 5000);
    fetchBPMData();

    const form = document.getElementById("predictForm");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      const jsonData = {};

      formData.forEach((value, key) => {
        jsonData[key] = key === "oldpeak" ? parseFloat(value) : parseInt(value);
      });

      // Send request to Flask API for prediction
      fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features: Object.values(jsonData) }),
      })
        .then((res) => res.json())
        .then((data) => {
          resultDiv.innerHTML = `
            <p><strong>Heart Disease Risk:</strong> ${data['Heart Disease Risk']}</p>
            <p><strong>Recommendation:</strong> ${data['Recommendation']}</p>
          `;
        })
        .catch((err) => {
          resultDiv.innerText = "Error: " + err.message;
          resultDiv.style.color = "orange";
        });
    });
  </script>
</body>
</html>
