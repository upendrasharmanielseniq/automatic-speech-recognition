import requests
import json

API_URL = "http://localhost:8000/predict"

transcript_payload = {
    "chunks": [
        {"min": 0, "transcript": "In a world where one man breaks bad."},
        {"min": 1, "transcript": "Heisenberg just made a deal with Tuco."}
    ]
}

response = requests.get(API_URL, json=transcript_payload)

if response.status_code == 200:
    print("\n Prediction Result:")
    print(json.dumps(response.json(), indent=2))
else:
    print("\n Request failed:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")