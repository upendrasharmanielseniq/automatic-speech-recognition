import React from 'react';
import './TranscriptResult.css';

const TranscriptResult = ({ result }) => {
  if (!result) return null;

  const { title, type, season, episode, language, confidence } = result;

  return (
    <div className="result-card">
      <div className="result-header">
        <h2>{title || 'Unknown Title'}</h2>
      </div>
      <div className="result-details">
        {type === 'TV Show' && (
          <>
            <p><strong>Season:</strong> {season}</p>
            <p><strong>Episode:</strong> {episode}</p>
          </>
        )}
        <p><strong>Language:</strong> {language}</p>
        <p><strong>Confidence:</strong> {confidence}</p>
      </div>
    </div>
  );
};

export default TranscriptResult;
