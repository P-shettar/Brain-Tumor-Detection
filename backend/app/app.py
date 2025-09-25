from flask import Flask, request, jsonify
from flask_cors import CORS
from ultralytics import YOLO
from PIL import Image
import io
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Load your YOLO model
model = None

def load_model():
    global model
    try:
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../yolov8s.pt'))
        logger.info(f"Loading model from: {model_path}")
        logger.info(f"Model file exists: {os.path.exists(model_path)}")
        
        # Load model using ultralytics package
        model = YOLO(model_path)
        logger.info("Model loaded successfully")
        
        # Test the model
        test_image = Image.new('RGB', (100, 100), color='red')
        results = model.predict(test_image)
        logger.info("Model test passed")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy", 
        "model_loaded": model is not None,
        "model_path": os.path.abspath(os.path.join(os.path.dirname(__file__), '../../yolov8s.pt'))
    })

@app.route('/api/detect', methods=['POST'])
def detect_tumor():
    try:
        logger.info("Detection request received")
        
        if 'image' not in request.files:
            logger.error("No image file in request")
            return jsonify({"error": "No image provided"}), 400
        
        image_file = request.files['image']
        logger.info(f"Image received: {image_file.filename}")
        
        # Read image
        image_data = image_file.read()
        if len(image_data) == 0:
            logger.error("Empty image data")
            return jsonify({"error": "Empty image file"}), 400
            
        image = Image.open(io.BytesIO(image_data))
        logger.info(f"Image opened: {image.size}, mode: {image.mode}")
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
            logger.info("Image converted to RGB")
        
        # Check if model is loaded
        if model is None:
            logger.error("Model not loaded")
            return jsonify({"error": "Model not loaded"}), 500
        
        # Perform detection
        logger.info("Starting detection...")
        results = model.predict(image)
        logger.info("Detection completed")
        
        # Process results
        detections = []
        if len(results) > 0:
            result = results[0]
            if result.boxes is not None:
                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    confidence = box.conf[0].item()
                    class_id = int(box.cls[0].item())
                    
                    detections.append({
                        "bbox": [float(x1), float(y1), float(x2), float(y2)],
                        "confidence": float(confidence),
                        "class": class_id
                    })
                logger.info(f"Found {len(detections)} detections")
            else:
                logger.info("No detections found")
        else:
            logger.info("No results returned")
        
        return jsonify({
            "detections": detections,
            "success": True,
            "image_size": image.size
        })
        
    except Exception as e:
        logger.error(f"Error in detection: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        load_model()
        logger.info("Starting server on http://0.0.0.0:8000")
        app.run(host='0.0.0.0', port=8000, debug=True)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")