# Speech-to-Text GenAI Classifier
This project is a production-grade backend for identifying TV Shows, Movies, or Episodes from speech transcript text using Azure OpenAI's GPT-4o-mini model. It is designed to work alongside embedded C++ speech-to-text systems (e.g., Whisper.cpp or Vosk) and provides a clean API for transcript-based content classification.

---

## Features
🔊 Real-time or batch transcript ingestion (JSON or `.txt`)
🧠 GenAI-powered classification (Azure OpenAI GPT-4o-mini)
🎬 Returns title, season, episode, and language
⚙️ Designed to work with embedded C++ STT modules
🧩 Easily extendable with TMDb metadata and frontend UI

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
```

### Response:
```json
{
    "title": "Breaking Bad",
    "season": "1",
    "episode": "1",
    "language": "English"
}
```

## Setup
### 1. Clone this Repository
```
git clone https://github.com/your-org/genai-backend.git
cd genai-backend
```
### 2. Setup Environment
```
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux

```
### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a .env file in the root directory:
```
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://hackfest25-openai-40.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
TMDB_API_KEY= (optional)
```

## Running the backend
```
uvicorn main:app --reload
```
Or with explicit PYTHONPATH:
```
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload # Powershell
# OR
PYTHONPATH=. uvicorn backend.main:app --reload # Bash/macOS
```

## Testing
With Curl:
```
curl -X POST http://localhost:8000/predict -H "Content-Type: application/json" -d "{\"chunks\":[{\"minute\":0,\"transcript\":\"In a world where one man breaks bad.\"},{\"minute\":1,\"transcript\":\"Heisenberg just made a deal with Tuco.\"}]}"
```

From File:
```
python genai-backend/run_from_txt.py
```

## Roadmap
- Add sliding window evaluation and scoring
- Integrate TMDb metadata and poster fetching
- Build Shazam-style React UI
- Deploy via Docker / Azure App Service

## License
MIT License

## Author
Developed by Aayushi Iyer
