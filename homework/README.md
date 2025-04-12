# Housing Price Prediction API
This project provides a Flask-based REST API that predicts house prices based on various features like area, number of bedrooms, bathrooms, and amenities. The model was trained using a housing dataset and is deployed using Docker.

1. Clone the Repo
git clone https://github.com/hammer-pp/Housing-Price-Prediction-API.git
cd housing-prediction-api

2. Install Requirements
pip install -r app/requirements.txt

3. Run the API
cd app
python app.py

Docker Instructions
1. Build the Docker Image
docker build -t your image name .

 2. Run the Container
docker run -p 5002:5002 your image name # you can switch your port.

API Usage
Endpoint: /predict
Method: POST
Content-Type: application/json

✅ Input Example

{
  "features": [
    [7420, 4, 2, 2, "yes", "yes", "yes", "no", "yes", 3, "yes", "semi-furnished"]
  ]
}

Example:  run on terminal with Invoke-RestMethod

$body = @'
{
  "features": [
    [5200, 3, 2, 1, "yes", "no", "yes", "no", "yes", 2, "yes", "semi-furnished"]
  ]
}
'@

Invoke-RestMethod -Uri "http://localhost:5001/predict" `
                  -Method Post `
                  -ContentType "application/json" `
                  -Body $body


🔁 Output Example
{
  "PRICES": [6841231]
}

training methods are in train_housing.ipynb