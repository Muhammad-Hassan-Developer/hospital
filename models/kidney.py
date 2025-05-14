import pandas as pd

# Step 1: Load the dataset
# Replace 'kidney_disease_data.csv' with the actual path of your dataset
df = pd.read_csv('ChronicKidneyDisease.csv')

# Step 2: Inspect the first few rows of the dataset
#print("Initial Dataset Overview:")
#print(df.head())

# Step 3: Remove unwanted columns
df = df.drop(columns=['TimeToEventMonths', 'TIME_YEAR'])

# Inspect the dataset after dropping the columns
#print("Dataset after removing unwanted columns:")
#print(df.head())

# Step 4: Rename columns for better understanding
df = df.rename(columns={
    'Sex': 'Gender',
    'AgeBaseline': 'Age',
    'HistoryDiabetes': 'HasDiabetes',
    'HistoryCHD': 'HasHeartDisease',
    'HistoryVascular': 'HasVascularDisease',
    'HistorySmoking': 'HasSmokingHistory',
    'HistoryHTN': 'HasHighBloodPressure',
    'HistoryDLD': 'HasHighCholesterol',
    'HistoryObesity': 'HasObesity',
    'DLDmeds': 'TakesCholesterolMeds',
    'DMmeds': 'TakesDiabetesMeds',
    'HTNmeds': 'TakesBloodPressureMeds',
    'ACEIARB': 'TakesACEIorARB',
    'CholesterolBaseline': 'CholesterolLevel',
    'CreatinineBaseline': 'CreatinineLevel',
    'eGFRBaseline': 'KidneyFunction_eGFR',
    'sBPBaseline': 'SystolicBloodPressure',
    'dBPBaseline': 'DiastolicBloodPressure',
    'BMIBaseline': 'BodyMassIndex',
    'EventCKD35': 'HasChronicKidneyDisease'
})

# Inspect the dataset after renaming the columns
#print("Dataset with renamed columns:")
#print(df.head())

from sklearn.impute import SimpleImputer

# Step 5: Handle missing values in numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

# Using SimpleImputer to fill missing values with the median
imputer = SimpleImputer(strategy='median')
df[numeric_columns] = imputer.fit_transform(df[numeric_columns])

# Check if there are still any missing values
#print("Missing values after imputation:")
#print(df.isnull().sum())

# Step 6: Encode the 'Gender' column
df['Gender'] = df['Gender'].apply(lambda x: 1 if x == 'Male' else 0)

# Verify the encoding
#print("Dataset after encoding the 'Gender' column:")
#print(df.head())

from sklearn.preprocessing import StandardScaler

# Step 7: Scale the numeric features
# Identifying the numeric columns for scaling (all except the target 'HasChronicKidneyDisease')
numeric_columns = df.drop(columns=['HasChronicKidneyDisease']).columns

# Initialize the StandardScaler
scaler = StandardScaler()

# Fit and transform the numeric data
df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

# Inspect the scaled dataset
#print("Dataset after scaling:")
#print(df.head())

from sklearn.model_selection import train_test_split

# Step 8: Define features (X) and target variable (y)
X = df.drop(columns=['HasChronicKidneyDisease'])  # Features
y = df['HasChronicKidneyDisease']  # Target variable (0 = No CKD, 1 = CKD)

# Step 9: Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Verify the shapes of the split data
#print("Training feature set shape:", X_train.shape)
#print("Testing feature set shape:", X_test.shape)
#print("Training target set shape:", y_train.shape)
#print("Testing target set shape:", y_test.shape)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Step 10: Initialize the Random Forest model
model = RandomForestClassifier(random_state=42)

# Step 11: Train the model on the training data
model.fit(X_train, y_train)

# Step 12: Make predictions on the testing set
y_pred = model.predict(X_test)

# Step 13: Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
#print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Optional: Print the classification report for more detailed evaluation
#print("Classification Report:")
#print(classification_report(y_test, y_pred))

import pickle

# Step 14: Save the trained model to a .pkl file
#with open('kidney_disease_model.pkl', 'wb') as file:
    #pickle.dump(model, file)

#print("Model saved successfully as 'kidney_disease_model.pkl'")

# Step 16: Save the scaler to a .pkl file with a descriptive name
with open('kidney_disease_scaler.pkl', 'wb') as file:
    pickle.dump(scaler, file)

print("Scaler saved successfully as 'kidney_disease_scaler.pkl'")
