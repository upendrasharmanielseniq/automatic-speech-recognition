from pydantic import BaseModel
from typing import List

class TranscriptChunk(BaseModel):
    min: int
    transcript: str

class TranscriptRequest(BaseModel):
    chunks: List[TranscriptChunk]