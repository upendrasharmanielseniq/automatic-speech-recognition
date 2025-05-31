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
        <div className="container">
            <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
            🎬 Content Classifier
            </h1>
            <ListenButton
                // onAudioSelect={handleAudioSelect}
                onTxtFileReceived={handleTxtFile }
                // onListen={handleListen}
            />
            <div className="flex justify-center mt-4">
                <PredictButton onPredict={handlePredict} isDisabled={!txtFile} />
            </div>
           <TranscriptDisplay result={prediction} metadata={metadata}/>
            {loading && <p className="text-center mt-4 text-blue-600">Predicting...</p>}
            <BatchUploader />
        </div>
    );
};

export default App;