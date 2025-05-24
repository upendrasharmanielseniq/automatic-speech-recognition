# Speech-to-Text GenAI Classifier
This project is a production-grade backend for identifying TV Shows, Movies, or Episodes from speech transcript text using OpenAI's GPT model. It is designed to work with a C++ speech-to-text system (e.g. Whisper) on embedded devices and can receive transcript text for classification.

---

## Features
- Real-time or batch transcript ingestion (JSON or `.txt`)
- GenAI-powdered classification (GPT-4 / GPT-3.5)
- Returns title, season, episode, and language
- Designed to work with embedded C++ STT modules
- Easily extendable with TMDb metadata and frontend UI

---

## API Endpoint
### `POST /predict`
**Request Body:**
```json
{
    "chunks": [
        { "minute": 0, "transcript": "In a world where one man breaks bad."},
        { "minute": 1, "transcript": "Heisenberg just made a deal with Tuco."}
    ]
}

### Response:
{
    "title": "Breaking Bad",
    "season": "1",
    "episode": "1",
    "language": "English"
}

## Setup
### 1. Clone this Repo
### 2. Setup Environment
cd backend
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux

pip install -r requirements.txt

### 3. Add .env in backend/
OPENAI_API_KEY=
TMDB_API_KEY= (optional)

## Running the backend
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload # Powershell
# OR
PYTHONPATH=. uvicorn backend.main:app --reload # Bash/macOS

## Testing
WIth Curl:
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"chunks\":[{\"minute\":0,\"transcript\":\"In a world where one man breaks bad.\"},{\"minute\":1,\"transcript\":\"Heisenberg just made a deal with Tuco.\"}]}"

From File:
python backend/run_from_txt.py

## Roadmap
- Add sliding window evaluation and scoring
- Integrate TMDb metadata and poster fetching
- Build Shazam-style React UI
- Deploy via Docker / Azure 

## License
MIT License

## Author
Developed by Aayushi Iyer