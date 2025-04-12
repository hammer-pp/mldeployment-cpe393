from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Load the trained model
with open("model_housing.pkl", "rb") as f:
    model = pickle.load(f)

# Load the feature scaler
with open("scaler_feature_housing.pkl", "rb") as f:
    scaler_feature = pickle.load(f)

# Load the target scaler
with open("scaler_target_housing.pkl", "rb") as f:
    scaler_target = pickle.load(f)

# Load the expected feature columns
with open("feature_columns.pkl", "rb") as f:
    expected_columns = pickle.load(f)

@app.route("/")
def home():
    return "ML Homework Model is Running"

@app.route("/predict", methods=["POST"])
def predict():
    
    data = request.get_json()

    columns = ["area", "bedrooms", "bathrooms", "stories", "mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning", "parking", "prefarea","furnishingstatus"]  # exact same order as in training
    input_features = pd.DataFrame(data["features"], columns=columns)

    #### Data Preprocessing ####
    # Define the features should be mapped

    # Binary map
    binary_cols = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']
    input_features[binary_cols] = input_features[binary_cols].apply(lambda x: x.map({'yes': 1, 'no': 0}))

    # Get the dummy variables for the feature 'furnishingstatus' and store it in a new variable - 'status'
    status = pd.get_dummies(input_features['furnishingstatus'], drop_first = True)

    input_features = input_features.drop(['furnishingstatus'], axis = 1)  

    # Add the results to the original housing dataframe
    input_features = pd.concat([input_features, status], axis = 1)

    #Apply the scaler to the dataframe
    num_vars = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking']
    input_features[num_vars] = scaler_feature.transform(input_features[num_vars])

    # Add any missing columns
    for col in expected_columns:
        if col not in input_features.columns:
            input_features[col] = 0
    input_features = input_features[expected_columns]  # Ensure correct column order


    predictions = model.predict(input_features)
    predictions = scaler_target.inverse_transform(predictions.reshape(-1, 1)) # Inverse transform the predictions prices to get the original scale

    predictions  = np.round(predictions, 0)  # rounds to 0 decimal places
    predictions = predictions.tolist()  # Convert ndarray to regular list

    return jsonify({"PRICES PREDICTION": predictions})
    
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002) 
