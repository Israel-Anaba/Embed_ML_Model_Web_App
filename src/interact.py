import requests

# Define the URL of your FastAPI app on Hugging Face Spaces
url = "https://huggingface.co/spaces/gr8testgad-1/sepsis_prediction/predict_sepsis/"

# Define the input data as a Python dictionary
data = {
    "PRG": 0.1,
    "PL": 0.2,
    "PR": 0.3,
    "SK": 0.4,
    "TS": 0.5,
    "M11": 0.6,
    "BD2": 0.7,
    "Age": 30
}

# Send a POST request with JSON data
response = requests.post(url, json=data)

# Print the response
print(response.status_code)
print(response.json())
