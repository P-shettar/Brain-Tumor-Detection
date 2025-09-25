import React from 'react';

const Results = ({ results }) => {
  if (!results) return null;

  const { original_image, processed_image, detections, stats } = results;

  const getTumorColor = (tumorType) => {
    const colors = {
      glioma: '#ff6b6b',
      meningioma: '#4ecdc4',
      pituitary: '#45b7d1',
      notumor: '#96ceb4'
    };
    return colors[tumorType] || '#666';
  };

  return (
    <div className="results-section">
      <h3>Detection Results</h3>
      
      <div className="results-grid">
        <div className="image-container">
          <h4>Original MRI</h4>
          <img src={`data:image/jpeg;base64,${original_image}`} alt="Original MRI" />
        </div>
        
        <div className="image-container">
          <h4>Processed MRI</h4>
          <img src={`data:image/jpeg;base64,${processed_image}`} alt="Processed MRI with Detections" />
        </div>
      </div>

      {detections && detections.length > 0 ? (
        <div className="detection-results">
          <h4>Detected Tumors</h4>
          <div className="detections-list">
            {detections.map((detection, index) => (
              <div 
                key={index} 
                className="detection-item"
                style={{ borderLeftColor: getTumorColor(detection.class) }}
              >
                <div className="detection-header">
                  <span className="tumor-type">
                    {detection.class.charAt(0).toUpperCase() + detection.class.slice(1)}
                  </span>
                  <span className="confidence">
                    {(detection.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="confidence-bar">
                  <div 
                    className="confidence-fill"
                    style={{ width: `${detection.confidence * 100}%` }}
                  ></div>
                </div>
                <div className="detection-coords">
                  Location: ({detection.bbox.x.toFixed(1)}, {detection.bbox.y.toFixed(1)}) | 
                  Size: {detection.bbox.width.toFixed(1)}×{detection.bbox.height.toFixed(1)}
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="no-detections">
          <div className="alert success">
            <h4>✅ No Tumors Detected</h4>
            <p>The MRI scan appears to be clear of detectable tumors.</p>
          </div>
        </div>
      )}

      {stats && (
        <div className="stats-section">
          <h4>Analysis Statistics</h4>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Processing Time:</span>
              <span className="stat-value">{stats.processing_time}ms</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Image Size:</span>
              <span className="stat-value">{stats.image_size}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Detections:</span>
              <span className="stat-value">{stats.detection_count}</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Results;