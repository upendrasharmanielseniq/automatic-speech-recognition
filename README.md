# RAT-SQUEAK: Speech-to-Text Audio Listener & GenAI Classifier
This project is a production-grade backend for identifying TV Shows, Movies, or Episodes from speech transcript text using Azure OpenAI's GPT-4o-mini model. It is designed to work alongside embedded C++ speech-to-text systems (e.g., Whisper.cpp) and provides a clean API for transcript-based content classification.

---

## Features
🔊 Real-time or batch transcript ingestion (JSON or `.txt`)
🧠 GenAI-powered classification (Azure OpenAI GPT-4o-mini)
🎬 Returns title, season, episode, language, confidence and time taken
⚙️ Designed to work with embedded C++ STT modules
🧩 Easily extendable with TMDb metadata and frontend UI

---

## API Endpoints
### `POST /predictFromUpload` 
### `POST /batchPredict` 
### `POST /predictFromWindow` 
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
    "language": "English",
    "confidence": "95%",
    "time_taken": "16.25 seconds"
}
```

## Setup

### 1. Clone this Repository
```
git clone https://github.com/upendrasharmanielseniq/automatic-speech-recognition.git
```
### 2. Configure RAT
cd inside automatic-speech-recognition/whisper_cpp folder
run following commands in the same order

✅ 1. Remove any old build
```
rm -rf build
```
```
mkdir build
```
```
cd build
```

✅ 2. Run CMake
```
cmake .. -DWHISPER_BUILD_STREAM=ON
```

💡 If you're missing SDL2, and CMake gives you an error, install it:
```
brew install sdl2
```

✅ 3. Build the binaries
```
cmake --build . --config Release
```


## Running RAT(Realtime Audio Transcriptor)
In order to run RAT, pre-configured GUI can be used which gives user power to choose options based upon the requirement.
✅  Run GUI
```
brew install python-tk
```
```
python3 whisper_gui.py
```

This command will bring up the gui:
1. Select which model you want to use(select higher moder for accurate and quick results)
2. Input a output filename, followed by .txt extention. 
   If no name is entered, RAT automatically generated a file name <timestamp>.txt.
3. Select number of threads you want to be executed in parallel, by default it is 4(min 4 required).
4. Click Listen button, RAT will start listening process via whisper.
5. Play any audio, RAT will pick it up from michrophone and will transcribe it in realtime. Transcribed output can be found in output file in output folder. 
Also some metrics related to audio can be found on the GUI itself.
6. Click stop to stop RAT from listening your audio.
7. Click on convert to JSON, if you also want to have a JSON file from your txt output file.

### 3. Configure SQUEAK

✅ 1. Go into genai_backend directory
```
cd genai_backend
```
✅ 2. Setup environment
```
python -m venv venv
venv\Scripts\activate # Windows
source venv/bin/activate # macOS/Linux

```
✅ 3. Install dependencies
```
pip install -r requirements.txt
```

✅ 4. Configure Environment Variables
Create a .env file in the root directory:
```
AZURE_OPENAI_KEY=<paste your azure_openai_key here without " ">
AZURE_OPENAI_ENDPOINT=https://hackfest25-openai-40.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT=gpt-4o-mini
```

✅ 5. Running the genai-backend
```
uvicorn main:app --reload
```
Or with explicit PYTHONPATH:
```
$env:PYTHONPATH = "."; uvicorn backend.main:app --reload # Powershell
# OR
PYTHONPATH=. uvicorn backend.main:app --reload # Bash/macOS
```

## 4. Configure React UI
1. Make sure you have node.js installed
2. Check node version by going into the terminal - Open cmd
```
    node -v
    npm -v
    cd frontend
    npm install (This installs the dependencies from package.json)
```
3. If you encounter an error like 'npm.ps1 cannot be loaded because running scripts is 
disabled on this system' Run:
```
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    npm run start
```

## 5. Test your application

```
The genai_backend runs on localhost:8000
The React UI runs on localhost:3000

```
Make sure you have your backend running to test the application from the UI.

### Roadmap to test and explore
There are two approaches to run the predictions using React UI:

1. Single Transcript Prediction
    - Upload a .txt file to run prediction for the entire transcript in one go.
    - Click on Predict Button.
    - The Model starts 'Predicting...'
    - You can see the prediction Result on the UI along with the time taken.


2. Sliding Window Evaluation
    - Generates a CSV file with weighted confidence across multiple windows of 1 min to full-length transcript chunks.
    - Upload a .txt file
    - Click on Test Sliding Window button
    - The prediction runs for sometime, exceutes for all windows
    - The output is a csv file that you can see in Downloads folder.


## Future Scope
- Integrate RAT and SQUEAK (Whisper C++ with GenAI model to develop an integrated solution)
- Deploy via Docker / Azure App Service
- Implement genre detection from transcript prediction

## License
MIT License

## Author
Developed by Media Maverick - Team MM for Hackfest 2025
