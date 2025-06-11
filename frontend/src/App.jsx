import { useState } from 'react';
import ListenButton from './components/ListenButton';
import PredictButton from './components/PredictButton';
import TranscriptDisplay from './components/TranscriptDisplay';
// import BatchUploader from './components/BatchUploader';
import SlidingWindow from './components/SlidingWindow';
import { uploadTranscript } from './services/api';
// import { triggerListening } from './services/api';
import './App.css';

const App = () => {
    // const [mp3File, setMp3File] = useState(null);
    const [txtFile, setTxtFile] = useState(null);
    const [prediction, setPrediction] = useState(null);
    // const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [metadata, setMetadata] = useState(null);

    // const handleAudioSelect = (file) => {
    //     setMp3File(file);
    // };

    const handleTxtFile  = (file) => {
        setTxtFile(file);
        setPrediction(null);
        setMetadata(null);
    };

    //  const handleListen = async () => {
    //     if (!mp3File) return;
    //     setLoading(true);
    //     try {
    //         // const res = await triggerListening(mp3File);
    //         alert('Transcript generated successfully. Please upload the generated .txt to proceed.');
    //     } catch (err) {
    //         alert('Listening failed. Check C++ backend.');
    //         console.error(err);
    //     } finally {
    //         setLoading(false);
    //     }
    // };
   
const handlePredict = async () => {
    if (!txtFile) return;
    setLoading(true);
    try {
        const res = await uploadTranscript(txtFile);
        setPrediction(res.data);
    } catch (err) {
        console.error("Prediction failed:", err);
        setPrediction({ error: "Prediction failed. Check backend." });
    } finally {
            setLoading(false);
    }
};

return (
  <div className="container row py-5">
    <header className="text-center mb-5">
      <img
        src="/assets/RAT_SQUEAK.jpeg"
        alt="Rat Squeak Logo"
        className="img-fluid rounded-circle shadow mb-3"
        style={{ width: "200px", objectFit: "cover" }}
      />
      <h2 className="text-muted fst-italic tagline-glow">
        From Sound to Sense
      </h2>
    </header>

    <div className="row row-cols-1 row-cols-md-3 g-4">
      {/* Single Transcript Prediction */}
      <div className="row d-flex justify-content-center">
        <div className="co-md-6">
          <div className="card h-100 card-hover shadow-sm">
            <div className="card-body">
              <h5 className="card-title">
                <i className="bi bi-file-earmark-text"></i> Single Transcript
                Prediction
              </h5>
              <ListenButton onTxtFileReceived={handleTxtFile} />
              <PredictButton onPredict={handlePredict} isDisabled={!txtFile} />
              {loading && <p className="text-primary mt-3">Predicting...</p>}
              <TranscriptDisplay result={prediction} metadata={metadata} />
            </div>
          </div>
        </div>
      </div>

      {/* Batch Transcript Prediction */}
      {/* <div className="col">
        <div className="card h-100 card-hover h-100 shadow-sm">
          <div className="card-body">
            <h5 className="card-title">
              <i className="bi bi-upload"></i> Batch Transcript Prediction
            </h5>
            <BatchUploader />
          </div>
        </div>
      </div> */}

      {/* Sliding Window Evaluation */}
      <div className="col">
        <div className="card h-100 card-hover h-100 shadow-sm">
          <div className="card-body">
            <h5 className="card-title">
              <i className="bi bi-clock-history"></i> Sliding Window Evaluation
            </h5>
            <SlidingWindow />
          </div>
        </div>
      </div>
    </div>
  </div>
);

};

export default App;