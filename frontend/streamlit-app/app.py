import streamlit as st
import requests
import base64
from PIL import Image
import io
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Brain Tumor Detection",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        background-color: #f0f2f6;
    }
    .tumor-detected {
        border-left: 5px solid #ff4b4b;
    }
    .no-tumor {
        border-left: 5px solid #00d4aa;
    }
    .confidence-bar {
        height: 10px;
        background-color: #e0e0e0;
        border-radius: 5px;
        margin: 5px 0;
    }
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #ff4b4b, #ffa34b);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🧠 Brain Tumor Detection System</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info(
        "This AI-powered system detects and classifies brain tumors from MRI scans "
        "using YOLOv8 deep learning model. Upload an MRI image to get started."
    )
    
    st.sidebar.title("Supported Tumor Types")
    st.sidebar.write("- **Glioma**: Tumors in glial cells")
    st.sidebar.write("- **Meningioma**: Tumors in meninges")
    st.sidebar.write("- **Pituitary**: Pituitary gland tumors")
    st.sidebar.write("- **No Tumor**: Healthy scans")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("Upload MRI Scan")
        
        uploaded_file = st.file_uploader(
            "Choose an MRI image",
            type=['jpg', 'jpeg', 'png', 'bmp', 'gif'],
            help="Supported formats: JPG, JPEG, PNG, BMP, GIF"
        )
        
        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded MRI Scan", use_column_width=True)
            
            if st.button("Analyze MRI", type="primary"):
                with st.spinner("Analyzing MRI for tumors..."):
                    try:
                        # Send to backend
                        files = {"file": uploaded_file.getvalue()}
                        response = requests.post(
                            "http://localhost:8000/api/detect",
                            files=files,
                            timeout=60
                        )
                        
                        if response.status_code == 200:
                            results = response.json()
                            display_results(results, col2)
                        else:
                            st.error("Error processing image. Please try again.")
                            
                    except requests.exceptions.RequestException as e:
                        st.error(f"Backend service unavailable: {e}")
    
    with col2:
        if 'results' not in st.session_state:
            st.header("Detection Results")
            st.info("Upload an MRI image and click 'Analyze MRI' to see results here.")
        else:
            display_results(st.session_state.results, col2)

def display_results(results, col):
    col.header("Detection Results")
    
    # Display processed image
    if 'processed_image' in results:
        processed_img = base64.b64decode(results['processed_image'])
        image = Image.open(io.BytesIO(processed_img))
        col.image(image, caption="Processed Image with Detections", use_column_width=True)
    
    # Display detections
    if results.get('detections'):
        for i, detection in enumerate(results['detections']):
            with col.container():
                st.markdown(f"""
                <div class="result-box tumor-detected">
                    <h4>Detection #{i+1}</h4>
                    <p><strong>Type:</strong> {detection['class'].title()}</p>
                    <p><strong>Confidence:</strong> {detection['confidence']:.1%}</p>
                    <div class="confidence-bar">
                        <div class="confidence-fill" style="width: {detection['confidence']*100}%"></div>
                    </div>
                    <p><strong>Location:</strong> ({detection['bbox']['x']:.1f}, {detection['bbox']['y']:.1f})</p>
                    <p><strong>Size:</strong> {detection['bbox']['width']:.1f} × {detection['bbox']['height']:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        col.markdown("""
        <div class="result-box no-tumor">
            <h4>✅ No Tumors Detected</h4>
            <p>The MRI scan appears to be clear of detectable tumors.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Display statistics
    if results.get('stats'):
        col.subheader("Analysis Statistics")
        stats = results['stats']
        col.metric("Processing Time", f"{stats.get('processing_time', 0)}ms")
        col.metric("Image Size", stats.get('image_size', 'N/A'))
        col.metric("Detections Found", stats.get('detection_count', 0))

if __name__ == "__main__":
    main()