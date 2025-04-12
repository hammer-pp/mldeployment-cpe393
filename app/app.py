from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

@app.route("/")
def home():
    return "ML Model is Running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Check if the features key exists
    if "features" not in data:
        msg = "Features key is missing"
        print("[ERROR]", msg)
        return jsonify({"error": msg}), 400

    input_features = np.array(data["features"])
    
    #check if the input have exactly 4 values
    if input_features.shape[1] != 4:
        msg = "Each input must have exactly 4 values"
        print("[ERROR]", msg)
        return jsonify({"error": msg}), 400
    
    # Check if the input is a list of numbers
    for feature in input_features:
        if not all(isinstance(i, (int, float)) for i in feature):
            msg = "Each input value must be a number"
            print("[ERROR]", msg)
            return jsonify({"error": msg}), 400

    predictions = model.predict(input_features)
    probs = model.predict_proba(input_features)

    results = []
    for pred, prob in zip(predictions, probs):
        confidence = np.max(prob)  # Confidence is the highest probability
        results.append({
            "prediction": int(pred),
            "confidence": round(confidence, 4)
        })

    return jsonify({"results": results})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001) 
