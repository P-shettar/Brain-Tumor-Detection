import React, { useState } from 'react';
import Navbar from './components/Navbar';
import Upload from './components/Upload';
import Results from './components/Results';
import { detectTumor } from './api';
import './App.css';

function App() {
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setIsLoading(true);
    setError(null);
    setResults(null);

    try {
      const detectionResults = await detectTumor(file);
      setResults(detectionResults);
    } catch (err) {
      setError(err.message);
      console.error('Detection error:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
  };

  return (
    <div className="App">
      <Navbar />
      
      <div className="container">
        <div className="header">
          <h1>Brain Tumor Detection System</h1>
          <p>Upload an MRI scan to detect and classify brain tumors using AI</p>
        </div>

        <div className="card">
          {!results ? (
            <>
              <Upload 
                onFileUpload={handleFileUpload} 
                isLoading={isLoading}
              />
              
              {error && (
                <div className="alert error">
                  <h4>❌ Error</h4>
                  <p>{error}</p>
                  <button onClick={() => setError(null)} className="btn">
                    Try Again
                  </button>
                </div>
              )}
            </>
          ) : (
            <>
              <Results results={results} />
              <div className="action-buttons">
                <button onClick={handleReset} className="btn">
                  Analyze Another MRI
                </button>
              </div>
            </>
          )}
        </div>

        <div className="info-section">
          <h3>About Brain Tumor Detection</h3>
          <div className="info-grid">
            <div className="info-card">
              <h4>🧠 Tumor Types Detected</h4>
              <ul>
                <li><strong>Glioma:</strong> Tumors that originate in the brain's glial cells</li>
                <li><strong>Meningioma:</strong> Tumors arising from the meninges</li>
                <li><strong>Pituitary:</strong> Tumors in the pituitary gland</li>
                <li><strong>No Tumor:</strong> Healthy brain scans</li>
              </ul>
            </div>
            <div className="info-card">
              <h4>⚡ How It Works</h4>
              <ol>
                <li>Upload an MRI scan in common image formats</li>
                <li>AI model analyzes the image using YOLOv8</li>
                <li>Get instant results with tumor locations and confidence scores</li>
                <li>Download or share the results with healthcare professionals</li>
              </ol>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;