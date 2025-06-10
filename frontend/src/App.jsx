import { useState } from 'react';
import ListenButton from './components/ListenButton';
import PredictButton from './components/PredictButton';
import TranscriptDisplay from './components/TranscriptDisplay';
import BatchUploader from './components/BatchUploader';
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
      <div
        className="container min-vh-100 bg-light py-5"
        style={{
          background: "linear-gradient(to bottom right, #0d3f8, #faffff)",
        }}
      >
        <header className="text-center mb-5">
          <img
            src="/assets/RAT_SQUEAK.jpeg"
            alt="Rat Squeak Logo"
            className="img-fluid rounded-circle shadow mb-3"
            style={{ width: "250px", height: "auto", objectFit: "cover" }}
          />
          <h2 className="fs-5 text-secondary fst-italic">
            Real-time Insight Engine
          </h2>
          <h3 className="fs-5 text-secondary fst-italic">
            From Sound to Sense
          </h3>
        </header>

        <section className="mb-5">
          <h3 className="h5 fw-semibold text-dark mb-3">
            Predict from Single Transcript File
          </h3>
          <div className="mb-3">
            <ListenButton onTxtFileReceived={handleTxtFile} />
          </div>
          <div className="d-flex justify-content-center mb-3">
            <PredictButton onPredict={handlePredict} isDisabled={!txtFile} />
          </div>
          <TranscriptDisplay result={prediction} metadata={metadata} />
          {loading && (
            <p className="text-center text-primary mt-3">Predicting...</p>
          )}
        </section>

        <section>
          <h3 className="h5 fw-semibold text-dark mb-3">
            Bulk Prediction from Multiple Transcript Files
          </h3>
          <BatchUploader />
        </section>
      </div>
    );
};

export default App;