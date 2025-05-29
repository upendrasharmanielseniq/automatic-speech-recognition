from fastapi import FastAPI
from schemas import TranscriptRequest
from inference import predict_content
# from backend.tmdb_api import enrich_with_metadata

app = FastAPI()

@app.post("/predict")
async def predict(transcript: TranscriptRequest):
    """
    Predict the content of a transcription.
    """
    prediction = predict_content(transcript)
    print("Request /predict received:", transcript)
    # enriched = enrich_with_metadata(prediction['title'])
    # return {**prediction, **enriched}
    return prediction