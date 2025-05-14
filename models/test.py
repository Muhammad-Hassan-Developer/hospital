import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Step 1: Load the dataset
df = pd.read_csv('heart_data.csv')

# Step 2: Clean rows that contain non-numeric values in numeric columns
# Drop rows where numeric columns have non-numeric strings (like 'python', 'data', etc.)
df = df[pd.to_numeric(df['rest_bp'], errors='coerce').notnull()]
df = df[pd.to_numeric(df['age'], errors='coerce').notnull()]

# Step 3: Inspect the dataset
print("First 5 rows of the cleaned dataset:")
print(df.head())

# Step 4: Preprocessing
# Assuming some columns are categorical and need encoding
df['chest_pain'] = df['chest_pain'].astype('category').cat.codes
df['thalassemia'] = df['thalassemia'].astype('category').cat.codes
df['exercise_angina'] = df['exercise_angina'].astype('category').cat.codes
df['gender'] = df['gender'].astype('category').cat.codes
df['st_slope'] = df['st_slope'].astype('category').cat.codes
df['rest_ecg'] = df['rest_ecg'].astype('category').cat.codes

# Step 5: Define features (X) and target (y)
X = df.drop('diagnosis', axis=1)
y = df['diagnosis']

# Step 6: Split the dataset
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 7: Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Step 8: Train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Step 9: Evaluate
y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Step 10: Save the model and scaler
with open('heart_disease_model.pkl', 'wb') as file:
    pickle.dump(model, file)

with open('scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Model and scaler saved successfully!")
