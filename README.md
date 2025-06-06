# Speech-to-Text GenAI Classifier
This project is a production-grade backend for identifying TV Shows, Movies, or Episodes from speech transcript text using Azure OpenAI's GPT-4o-mini model. It is designed to work alongside embedded C++ speech-to-text systems (e.g., Whisper.cpp or Vosk) and provides a clean API for transcript-based content classification.

---

## Features
🔊 Real-time or batch transcript ingestion (JSON or `.txt`)
🧠 GenAI-powered classification (Azure OpenAI GPT-4o-mini)
🎬 Returns title, season, episode, language and confidence
⚙️ Designed to work with embedded C++ STT modules
🧩 Easily extendable with TMDb metadata and frontend UI

---

## API Endpoints
### `POST /predictFromUpload` 
### `POST /batchPredict` 
**Request Body:**
```txt
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
    "confidence": "95%"
}
```

## Setup
### 1. Clone this Repository
```
git clone https://github.com/upendrasharmanielseniq/automatic-speech-recognition.git
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
AZURE_OPENAI_KEY=<paste your azure_openai_key here without " ">
AZURE_OPENAI_ENDPOINT=https://hackfest25-openai-40.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

## Running the genai-backend
```
uvicorn main:app --reload
```
Or with explicit PYTHONPATH:
```
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload # Powershell
# OR
PYTHONPATH=. uvicorn backend.main:app --reload # Bash/macOS
```

## Running the frontend
```
1. Make sure you have node.js installed
2. Check node version by going into the terminal - Open cmd
node -v
npm -v
cd frontend
npm install (This installs the dependencies from package.json)
npm run start
```

## Testing

```
The genai-backend runs on localhost:8000
The frontend UI runs on localhost:3000

```
Make sure you have your backend running to test the application from the UI.

## Roadmap to test and explore
- Uncomment the sliding window function in main.py to test the sliding window approach

## TBD
- Integrate RAT and SQUEAK (Whisper C++ with GenAI model to develop an integrated solution)
- Deploy via Docker / Azure App Service

## License
MIT License

## Author
Developed by Media Maverick - Team MM for Hackfest 2025
