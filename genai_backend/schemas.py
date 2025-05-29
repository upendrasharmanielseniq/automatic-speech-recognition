from pydantic import BaseModel
from typing import List

class TranscriptChunk(BaseModel):
    start: str
    end: str
    transcript: str

class TranscriptRequest(BaseModel):
    chunks: List[TranscriptChunk]