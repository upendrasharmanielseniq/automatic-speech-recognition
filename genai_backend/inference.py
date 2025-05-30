
from openai import AzureOpenAI
from schemas import TranscriptRequest
from config import (
    AZURE_OPENAI_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION
    )

client = AzureOpenAI(
    api_key=AZURE_OPENAI_KEY,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_endpoint=AZURE_OPENAI_ENDPOINT
)


def build_prompt(chunks):
    full_text = " ".join([c.transcript for c in chunks])
    return f"""
    You are an expert in identifying TV shows and movies from dialogue transcripts.
    Given a transcript from a TV show or a movie, identify:
    1. Title (Required)
    2. Type (Movie or TV Show)
    3. If and only if it's a TV show, identify correct **season and episode number** (or reply with "N/A"). **AVOID HALLUCINATING**.
    4. Detect the **language** of the transcript.
    5. Provide a **confidence percentage**.
    6. If a window confidence >= 80%, return the prediction immediately.

    Transcript:
    \"\"\"
    {full_text}
    \"\"\"

    Respond in the following format, adjust accordingly to movie or TV show:
    Title: <Movie or TV Show title with year if available or series run time>
    Type: <Movie or TV Show>
    Season: <Season number or "N/A"> Omit if N/A
    Episode: <Episode number or "N/A"> Omit if N/A
    Language: <Detected Language>
    Confidence: <Confidence score>
    """

def predict_content(transcript):
    """
    Predict the content of a transcription.
    """
    prompt = build_prompt(transcript.chunks)
    try:
        response = client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[
                {"role": "system", "content": "You are a streaming content classifier."},
                {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
                )
        return parse_response(response.choices[0].message.content)
    except Exception as e:
        print("OpenAI API call failed:", e)
        return {"error": "Prediction failed", "details": str(e)}

def sliding_window_prediction(chunks,window_size=10, step_size=2):
    predictions = []

    for i in range(0, len(chunks) - - window_size + 1, step_size):
        window = chunks[i:i + window_size]
        transcript_request = TranscriptRequest(chunks=window)
        prediction = predict_content(transcript_request)

        print(f"Window {i}-{i+window_size}: {prediction}")

        if prediction.get("title") and prediction["title"].lower() != "unknown":
            if prediction.get("confidence", "0").isdigit() and int(prediction["confidence"]) >= 7:
                return prediction
            else:
                predictions.append(prediction)
    
    return predictions[0] if predictions else {"error": "No confident prediction in any window"}
    
def parse_response(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.lower()] = value.strip()
    return result