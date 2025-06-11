from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from schemas import TranscriptRequest, TranscriptChunk
from inference import predict_content, sliding_window_prediction, sliding_window_prediction_new, predict_content_chain, predict_content_chain_new
from datetime import datetime, timedelta
from collections import Counter

import re
import os,json
import csv, io
from fastapi.responses import StreamingResponse
# from backend.tmdb_api import enrich_with_metadata

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class FileRequest(BaseModel):
    filename: str 

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

def parse_txt_to_minute_chunks(text):
    import re
    from datetime import datetime

    lines = text.strip().split("\n")
    chunks = []
    current_minute = 0
    current_block = []

    time_pattern = re.compile(r"\[(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\]\s*(.*)")

    def parse_time(t):
        return datetime.strptime(t, "%H:%M:%S.%f")

    for line in lines:
        match = time_pattern.match(line)
        if match:
            start, end, transcript = match.groups()
            minutes = parse_time(start).minute + parse_time(start).hour * 60

            if minutes > current_minute:
                if current_block:
                    chunks.append(current_block)
                    current_block = []
                current_minute = minutes

            current_block.append({
                "start": start,
                "end": end,
                "transcript": transcript.strip()
            })

    if current_block:
        chunks.append(current_block)

    print(f"Parsed {len(chunks)} minute-based chunks.")
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
        prediction = predict_content_chain_new(transcript_request)
        print("Request /predictFromUpload received.")
        return prediction
    except Exception as e:
        return {"error": "Failed to process file", "details": str(e)}
    
@app.post("/predict/sliding-window")
async def predictFromWindow(file: UploadFile = File(...)):
    """
    Predict the content from a .txt transcript file using sliding window prediction.
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

        minute_chunks = parse_txt_to_minute_chunks(file_text)
        predictions = sliding_window_prediction_new(minute_chunks)
        print("Request /predictFromWindow received.")

        valid_predictions = []
        for p in predictions:
            if not isinstance(p, dict):
                continue

            content_type = p.get("type", "").lower()
            if content_type == "tv show":
                if all(p.get(k) for k in ["title", "language", "season", "episode"]):
                    valid_predictions.append(p)
                else:
                    print("Skipping invalid TV show prediction:", p)
            else:  # Movie or other types
                if all(p.get(k) for k in ["title", "language"]):
                    valid_predictions.append(p)
                else:
                    print("Skipping invalid movie prediction:", p)

        # Count frequency for confidence weighting
        if valid_predictions:
            if any(p.get("type", "").lower() == "tv show" for p in valid_predictions):
                freq_keys = ["title", "type", "season", "episode", "language"]
            else:
                freq_keys = ["title", "type", "language"]

            freq_counter = Counter(tuple(p.get(k, "") for k in freq_keys) for p in valid_predictions)
            total_predictions = len(valid_predictions)

            for p in valid_predictions:
                key = tuple(p.get(k, "") for k in freq_keys)
                confidence_pct = (freq_counter[key] / total_predictions) * 100
                p["confidence_weighted"] = f"{confidence_pct:.1f}%"

        # Prepare CSV output
        output = io.StringIO()
        is_tv_show = any(p.get("type", "").lower() == "tv show" for p in valid_predictions)

        if is_tv_show:
            field_order = ["title", "type", "season", "episode", "language", "score", "minutes_used", "confidence_weighted", "prediction_time_seconds"]
        else:
            field_order = ["title", "type", "language", "score", "minutes_used", "confidence_weighted", "prediction_time_seconds"]

        writer = csv.DictWriter(output, fieldnames=field_order)
        writer.writeheader()

        for row in valid_predictions:
            filtered_row = {field: row.get(field, "") for field in field_order}
            writer.writerow(filtered_row)

        output.seek(0)
        return StreamingResponse(output, media_type="text/csv", headers={
            "Content-Disposition": f"attachment; filename={file.filename}_sliding_window_predictions.csv"
        })

    except Exception as e:
        return {"error": "Failed to process file", "details": str(e)}


@app.post("/batchPredict")
async def batchPredict(files: list[UploadFile] = File(...)):
    """
    Batch predict the content from multiple .txt transcript files.
    """
    predictions = []
    targets = []
    for file in files:
        contents = await file.read()
        try:
           text = contents.decode('utf-8')
        except UnicodeDecodeError:
            text = contents.decode('utf-16')

        chunks = parse_txt_to_chunks_from_string(text)
        transcript_request = TranscriptRequest(chunks=chunks)
        prediction = predict_content_chain_new(transcript_request)
        prediction["filename"] = file.filename
        predictions.append(prediction)

    output = io.StringIO()
    field_order = ["filename", "title", "type", "season", "episode", "language", "confidence", "time_taken"]
    writer = csv.DictWriter(output, fieldnames=field_order)
    writer.writeheader()
    for row in predictions:
        filtered_row = {key: row.get(key, "") for key in field_order}
        writer.writerow(filtered_row)


    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=filename={file.filename}batch_predictions.csv"})
