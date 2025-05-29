from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from schemas import TranscriptRequest, TranscriptChunk
from inference import predict_content, sliding_window_prediction
import os,json
# from backend.tmdb_api import enrich_with_metadata

app = FastAPI()

class FileRequest(BaseModel):
    file_name: str 

def parse_txt_to_chunks_from_string(file_text: str):
    chunks = []
    lines = file_text.splitlines()
    for line in lines:
        if '-->' in line:
            parts = line.strip().split(']')
            if len(parts) == 2:
                timestamp = parts[0].strip('[')
                transcript = parts[1].strip()
                start, end = timestamp.split('-->')
                chunk = TranscriptChunk(
                    start=start.strip(),
                    end=end.strip(),
                    transcript=transcript
                )
                chunks.append(chunk)
    return chunks

def parse_txt_to_chunks(file_path: str):
    chunks = []
    for encoding in ['utf-8-sig', 'utf-16', 'iso-8859-1']:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                for line in f:
                    if '-->' in line:
                        parts = line.strip().split(']')
                        if len(parts) == 2:
                            timestamp = parts[0].strip('[')
                            transcript = parts[1].strip()
                            start, end = timestamp.split('-->')
                            chunk = TranscriptChunk(
                            start=start.strip(),
                            end=end.strip(),
                            transcript=transcript
                            )
                        chunks.append(chunk)
                return chunks
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode transcript file. Please use UTF-8 or UTF-16 encoded .txt file.")

@app.post("/predict")
async def predict(transcript: TranscriptRequest):
    """
    Predict the content of a transcription.
    """
    prediction = predict_content(transcript)
    print("Request /predict received:", transcript)
    return prediction

@app.post("/predictFromUpload")
async def predictFromUpload(file: UploadFile = File(...)):
    """
    Predict the content from a .txt transcript file, convert to JSON chunks, and return prediction.
    """
    try:
        file_content = await file.read()
        for encoding in ['utf-8-sig', 'utf-16', 'iso-8859-1']:
            try:
                file_text = file_content.decode(encoding)
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError("Unable to decode file with supported encodings.")
        chunks = parse_txt_to_chunks_from_string(file_text)

        json_output_path = os.path.splitext(file.filename)[0] + ".json"
        with open(json_output_path, "w", encoding="utf-8") as json_file:
            json.dump({"chunks": [chunk.dict() for chunk in chunks]}, json_file, ensure_ascii=False, indent=2)
                      
        transcript_request = TranscriptRequest(chunks=chunks)
        # prediction = predict_content(transcript_request)
        prediction = sliding_window_prediction(chunks)

        # prediction = sliding_window_prediction(chunks)
        print("Request /predictFromUpload received.")
        return prediction
    except Exception as e:
        return {"error": "Failed to process file", "details": str(e)}