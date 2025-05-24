from fastapi import FastAPI, Request
from backend.schemas import TranscriptRequest
from backend.inference import predict_content
# from backend.tmdb_api import enrich_with_metadata

app = FastAPI()

@app.get("/predict")
async def predict(transcript: TranscriptRequest):
    """
    Predict the content of a transcription.
    """
    prediction = predict_content(transcript)
    # enriched = enrich_with_metadata(prediction['title'])
    # return {**prediction, **enriched}
    return prediction