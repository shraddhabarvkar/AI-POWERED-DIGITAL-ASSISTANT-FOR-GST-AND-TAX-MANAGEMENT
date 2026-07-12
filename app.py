import streamlit as st
import os
import json
import pandas as pd
from PIL import Image
from datetime import datetime

from src.gst_extractor import GSTInvoiceExtractor
from src.utils import create_annotated_image, create_results_dataframe, save_results
from config import Config

# Page configuration
st.set_page_config(
    page_title="InvoiScope - GST Invoice Extractor",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1e88e5;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
    }
    .metric-card p {
        margin: 5px 0 0 0;
        font-size: 0.9rem;
    }
    .success-box {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .info-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 1px solid #bbdefb;
        color: #0d47a1;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .error-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'extraction_results' not in st.session_state:
    st.session_state.extraction_results = None
if 'processed_image_path' not in st.session_state:
    st.session_state.processed_image_path = None
if 'extractor' not in st.session_state:
    st.session_state.extractor = None

@st.cache_resource
def load_gst_extractor():
    """Load GST extractor with caching"""
    try:
        if not os.path.exists(Config.MODEL_PATH):
            st.error(f"❌ Model file not found at: {Config.MODEL_PATH}")
            st.info("Please place your trained YOLOv9c model in the 'models' directory.")
            return None
        return GSTInvoiceExtractor(Config.MODEL_PATH)
    except Exception as e:
        st.error(f"❌ Error loading model: {str(e)}")
        return None

def display_metrics(results):
    """Display extraction metrics"""
    summary = results.get('summary', {})
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_detections = summary.get('total_detections', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{total_detections}</h3>
            <p>Fields Detected</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_conf = summary.get('average_confidence', 0)
        st.markdown(f"""
        <div class="metric-card">
            <h3>{avg_conf:.3f}</h3>
            <p>Avg Confidence</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        quality = "High" if avg_conf >= 0.8 else "Medium" if avg_conf >= 0.6 else "Low"
        st.markdown(f"""
        <div class="metric-card">
            <h3>{quality}</h3>
            <p>Quality Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        processing_time = datetime.now().strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="metric-card">
            <h3>{processing_time}</h3>
            <p>Processed At</p>
        </div>
        """, unsafe_allow_html=True)

def display_categorized_results(results):
    """Display results in organized categories"""
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Invoice Details", 
        "🏢 Business Info", 
        "💰 Tax Information", 
        "📊 Complete Data"
    ])
    
    with tab1:
        st.subheader("📄 Invoice Metadata")
        invoice_data = results.get('invoice_metadata', {})
        
        if any(invoice_data.values()):
            for field_type, detections in invoice_data.items():
                if detections:
                    st.markdown(f"**{field_type.replace('_', ' ').title()}:**")
                    for detection in detections:
                        confidence = detection['confidence']
                        confidence_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
                        st.markdown(f"{confidence_emoji} `{detection['text_content']}` *({confidence:.3f})*")
        else:
            st.info("No invoice details detected")
    
    with tab2:
        st.subheader("🏢 Business Information")
        business_data = results.get('business_information', {})
        
        if any(business_data.values()):
            for field_type, detections in business_data.items():
                if detections:
                    st.markdown(f"**{field_type.replace('_', ' ').title()}:**")
                    for detection in detections:
                        confidence = detection['confidence']
                        confidence_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
                        st.markdown(f"{confidence_emoji} `{detection['text_content']}` *({confidence:.3f})*")
        else:
            st.info("No business information detected")
    
    with tab3:
        st.subheader("💰 Tax Breakdown")
        tax_data = results.get('tax_information', {})
        
        if any(tax_data.values()):
            tax_summary = []
            for field_type, detections in tax_data.items():
                for detection in detections:
                    confidence = detection['confidence']
                    confidence_emoji = "🟢" if confidence >= 0.8 else "🟡" if confidence >= 0.6 else "🔴"
                    tax_summary.append({
                        'Tax Type': field_type.upper(),
                        'Amount': detection['text_content'],
                        'Confidence': f"{confidence_emoji} {confidence:.3f}"
                    })
            
            if tax_summary:
                df_tax = pd.DataFrame(tax_summary)
                st.dataframe(df_tax, use_container_width=True)
        else:
            st.info("No tax information detected")
    
    with tab4:
        st.subheader("📊 Complete Extraction Data")
        df = create_results_dataframe(results)
        
        if not df.empty:
            st.dataframe(df, use_container_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv_data,
                    file_name=f"gst_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            
            with col2:
                json_data = json.dumps(results, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_data,
                    file_name=f"gst_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("No data to display")

def save_uploaded_file(uploaded_file):
    """Save uploaded file to local storage"""
    upload_dir = Config.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return file_path

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🔍 InvoiScope - GST Invoice Information Extractor</h1>', unsafe_allow_html=True)
    
    # Load extractor
    if not st.session_state.extractor:
        with st.spinner("🔄 Loading GST extraction model..."):
            st.session_state.extractor = load_gst_extractor()
    
    if not st.session_state.extractor:
        st.markdown('<div class="error-box">❌ Failed to load GST extraction model. Please check model file.</div>', unsafe_allow_html=True)
        st.stop()
    else:
        st.markdown('<div class="success-box">✅ GST Invoice Extractor loaded successfully!</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.1,
            max_value=1.0,
            value=Config.DEFAULT_CONFIDENCE,
            step=0.1,
            help="Minimum confidence score for field detection"
        )
        
        st.markdown("---")
        
        # Model info
        st.subheader("📊 Model Performance")
        perf = Config.MODEL_PERFORMANCE
        st.markdown(f"""
        **Architecture**: YOLOv9c Optimized  
        **mAP@0.5**: {perf['map50']}  
        **Precision**: {perf['precision']}  
        **Recall**: {perf['recall']}  
        **GST Fields**: {perf['num_classes']} types
        """)
        
        st.markdown("---")
        
        # Instructions
        st.subheader("📖 How to Use")
        st.markdown("""
        1. **📤 Upload** a GST invoice image
        2. **⚙️ Adjust** confidence threshold
        3. **🔍 Click** 'Extract GST Information'
        4. **📊 Review** extracted data
        5. **📥 Download** results
        """)
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📤 Upload GST Invoice")
        
        uploaded_file = st.file_uploader(
            "Choose an invoice image...",
            type=Config.ALLOWED_EXTENSIONS,
            help="Upload a clear GST invoice image"
        )
        
        if uploaded_file is not None:
            # Validate file size
            if len(uploaded_file.getvalue()) > Config.MAX_FILE_SIZE:
                st.error(f"❌ File too large! Maximum size: {Config.MAX_FILE_SIZE // (1024*1024)} MB")
                st.stop()
            
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Invoice", use_column_width=True)
            
            # Image info
            st.markdown(f"""
            <div class="info-box">
            <strong>📸 Image Details:</strong><br>
            📏 Size: {image.size[0]} x {image.size[1]} pixels<br>
            📁 File: {uploaded_file.name}<br>
            📊 Size: {len(uploaded_file.getvalue()) / 1024:.1f} KB<br>
            🎨 Format: {image.format}
            </div>
            """, unsafe_allow_html=True)
            
            # Save uploaded file
            upload_path = save_uploaded_file(uploaded_file)
            st.session_state.processed_image_path = upload_path
            
            # Extract button
            if st.button("🔍 Extract GST Information", type="primary", use_container_width=True):
                with st.spinner("🔄 Extracting GST information... Please wait..."):
                    try:
                        results = st.session_state.extractor.extract_gst_information(
                            upload_path, 
                            confidence_threshold=confidence_threshold
                        )
                        
                        if 'error' in results:
                            st.markdown(f'<div class="error-box">❌ Extraction failed: {results["error"]}</div>', unsafe_allow_html=True)
                        else:
                            st.session_state.extraction_results = results
                            st.success("✅ GST information extracted successfully!")
                            
                    except Exception as e:
                        st.markdown(f'<div class="error-box">❌ Error during extraction: {str(e)}</div>', unsafe_allow_html=True)
    
    with col2:
        st.subheader("📊 Extraction Results")
        
        if st.session_state.extraction_results:
            results = st.session_state.extraction_results
            
            # Display metrics
            display_metrics(results)
            
            # Show annotated image
            if st.session_state.processed_image_path:
                st.subheader("🖼️ Annotated Invoice")
                try:
                    annotated_img = create_annotated_image(
                        st.session_state.processed_image_path, 
                        results
                    )
                    if annotated_img:
                        st.image(annotated_img, caption="Detected GST Fields", use_column_width=True)
                except Exception as e:
                    st.warning(f"⚠️ Could not create annotated image: {str(e)}")
        else:
            st.markdown("""
            <div class="info-box">
            <h4>👆 Ready to Extract GST Information</h4>
            <p>Upload a GST invoice image and click 'Extract GST Information' to see results.</p>
            <ul>
                <li><strong>Supported formats:</strong> JPG, PNG, JPEG</li>
                <li><strong>Max file size:</strong> 10 MB</li>
                <li><strong>Processing time:</strong> 2-5 seconds</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
    
    # Detailed results
    if st.session_state.extraction_results:
        st.markdown("---")
        st.header("📋 Detailed Extraction Results")
        display_categorized_results(st.session_state.extraction_results)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem; padding: 1rem; background: #f8f9fa; border-radius: 10px;">
        <p>🔍 <strong>InvoiScope v1.0</strong> | YOLOv9c + OCR | Streamlit</p>
        <p>🎯 <strong>Performance:</strong> 74.1% mAP@0.5 | 85.4% Precision | 24 GST Fields</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
