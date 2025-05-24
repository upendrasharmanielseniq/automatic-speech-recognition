import requests
import json

API_URL = "http://localhost:8000/predict"

def parse_transcript_file(file_path):
    chunks = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if "]" in line:
                minute_str, text = line.strip().split("]", 1)
                minute = int(minute_str.replace("[", "").replace(":", ""))
                chunks.append({"min": minute, "transcript": text.strip()})
    return {"chunks": chunks}

if __name__ == "__main__":
        payload = parse_transcript_file("transcript.txt")
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            print("\n Prediction Result:")
            print(json.dumps(response.json(), indent=2))
        else:
            print("\n Request failed:")
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")