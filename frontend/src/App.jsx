import React, { useState } from 'react';
import ListenButton from './components/ListenButton';
import PredictButton from './components/PredictButton';
import TranscriptDisplay from './components/TranscriptDisplay';
import { uploadTranscript } from './services/api';
import './App.css';

const App = () => {
    const [file, setFile] = useState(null);
    const [result, setResult] = useState(null);

    const handleFileSelect = (selectedFile) => {
        setFile(selectedFile);
        setResult(null);
    };
   
const handlePredict = async () => {
    if (!file) return;
    try {
        const res = await uploadTranscript(file);
        setResult(res.data);
    } catch (err) {
        console.error("Prediction failed:", err);
        setResult({ error: "Prediction failed. Check backend." });
    }
};

    return (
        <div className="container">
            <h1 className="text-2xl font-bold text-center mb-6 text-gray-800">
            🎬 Content Classifier
            </h1>
            <ListenButton onFileSelect={handleFileSelect} />
            <div className="flex justify-center mt-4">
            <PredictButton onPredict={handlePredict} isDisabled={!file} />
            </div>
            <TranscriptDisplay result={result} />
        </div>
    );
};

export default App;