
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
    Given a transcript from a TV show or a movie, analyze the text and predict the following:
    - The title of the content (use "Unknown" if not obvious)
    - Whether it is a movie or a TV show
    - If it is a TV show, return the season and episode numbers (or "N/A" if not known)
    - The language of the transcript
    - Confidence in your prediction (1-10 scale)
    Transcript:
    \"\"\"
    {full_text}
    \"\"\"

    Respond ONLY in the following format:
    Title: <Movie or TV Show title>
    Season: <Season number or "N/A">
    Episode: <Episode number or "N/A">
    Language: <Detected Language>
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

def sliding_window_prediction(chunks,window_size=5, step_size=1):
    for i in range(0, len(chunks) - - window_size + 1, step_size):
        window = chunks[i:i + window_size]
        transcript_request = TranscriptRequest(chunks=window)
        prediction = predict_content(transcript_request)
        
        if prediction.get("title") and prediction["title"].lower() != "unknown":
            return prediction
    
    return {"error": "No confident prediction in any window"}
    
def parse_response(text):
    lines = text.strip().split("\n")
    result = {}
    for line in lines:
        if ": " in line:
            key, value = line.split(": ", 1)
            result[key.lower()] = value.strip()
    return result