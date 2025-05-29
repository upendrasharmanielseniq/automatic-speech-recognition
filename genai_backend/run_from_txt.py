import requests
import json
import os

API_URL = "http://localhost:8000/predict"

file_path = "genai-backend/transcript.txt"

def parse_transcript_file(file_path):
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            line = line.strip()
            if line:
                chunks.append({"min": i, "transcript": line})
    return {"chunks": chunks}

if __name__ == "__main__":
        payload = parse_transcript_file(file_path)
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            print("\n Prediction Result:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("\n Request failed:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")