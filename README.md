# 🔍 InvoiScope - GST Invoice Information Extractor

**InvoiScope** is an intelligent GST invoice information extraction system powered by YOLOv9c object detection and OCR technology. Extract key information from GST invoices with high accuracy and confidence through an intuitive web interface.

## 📋 Table of Contents
- [Features](#-features)
- [Demo](#-demo)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Supported GST Fields](#-supported-gst-fields)
- [Technical Architecture](#-technical-architecture)
- [Configuration](#-configuration)
- [Model Performance](#-model-performance)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- **🎯 High Accuracy Detection**: 74.1% mAP@0.5 with 85.4% precision using optimized YOLOv9c
- **📊 Comprehensive Field Extraction**: 24 different GST invoice fields across 3 categories
- **🖼️ Visual Annotations**: Interactive annotated images showing detected fields with bounding boxes
- **📱 Modern Web Interface**: Clean, responsive Streamlit interface with real-time processing
- **📥 Multiple Export Formats**: Download results as CSV or JSON with timestamps
- **⚡ Fast Processing**: 2-5 seconds per invoice with optimized inference pipeline
- **🔧 Configurable Confidence**: Adjustable confidence thresholds for different use cases
- **📈 Performance Metrics**: Real-time confidence scores and quality assessments
- **🎨 Categorized Results**: Organized display of invoice metadata, business info, and tax details


### Key Capabilities:
- Upload GST invoice images (JPG, PNG, JPEG)
- Real-time field detection and text extraction
- Interactive confidence threshold adjustment
- Categorized results display with visual indicators
- Downloadable extraction reports

## 🚀 Installation

### Prerequisites
- **Python**: 3.8 or higher
- **Tesseract OCR**: Required for text extraction
- **System Memory**: Minimum 4GB RAM recommended
- **Storage**: ~2GB for dependencies and model files

### Step 1: Clone Repository
```bash
git clone https://github.com/ayush2635/Invoiscope.git
cd Invoiscope
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Tesseract OCR

**Windows:**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install and add to PATH
3. Verify: `tesseract --version`

**macOS:**
```bash
brew install tesseract
```

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

### Step 5: Model Setup
1. Place your trained YOLOv9c model file in the `models/` directory
2. Rename it to: `gst_invoice_yolov9c_optimal.pt`
3. Ensure the file path matches: `models/gst_invoice_yolov9c_optimal.pt`

### Step 6: Verify Installation
```bash
python -c "import streamlit, cv2, pytesseract; print('All dependencies installed successfully!')"
```

## 🔧 Usage

### Starting the Application
```bash
streamlit run app.py
```

The application will be available at: **http://localhost:8501**

### Basic Workflow
1. **📤 Upload Invoice**: 
   - Drag and drop or click to select a GST invoice image
   - Supported formats: JPG, PNG, JPEG (max 10MB)

2. **⚙️ Configure Settings**:
   - Adjust confidence threshold (0.1 - 1.0)
   - Higher values = more precise but fewer detections
   - Lower values = more detections but potentially less accurate

3. **🔍 Extract Information**:
   - Click "Extract GST Information" button
   - Processing typically takes 2-5 seconds

4. **📊 Review Results**:
   - View categorized extraction results
   - Check annotated image with bounding boxes
   - Review confidence scores and quality metrics

5. **📥 Export Data**:

   - Download results as CSV for spreadsheet analysis
   - Download as JSON for programmatic use
   - Files include timestamps for organization

### Advanced Usage

#### Batch Processing
```python
from src.gst_extractor import GSTInvoiceExtractor

extractor = GSTInvoiceExtractor("models/gst_invoice_yolov9c_optimal.pt")

# Process multiple invoices
invoice_paths = ["invoice1.jpg", "invoice2.png", "invoice3.jpeg"]
results = []

for path in invoice_paths:
    result = extractor.extract_gst_information(path, confidence_threshold=0.6)
    results.append(result)
```

#### Custom OCR Configuration
```python
# Modify config.py for custom OCR settings
OCR_CONFIGS = {
    'custom_field': '--psm 7 -c tessedit_char_whitelist=ABCDEF0123456789',
    # Add your custom configurations
}
```

## 📁 Project Structure

```
Invoiscope/
├── 📁 .streamlit/              # Streamlit configuration
│   └── config.toml             # App settings and themes
├── 📁 assets/                  # Static assets
│   └── style.css               # Custom CSS styles
├── 📁 data/                    # Data directories
│   ├── 📁 uploads/             # Uploaded invoice images
│   ├── 📁 results/             # Processing results and exports
│   └── 📁 temp/                # Temporary processing files
├── 📁 models/                  # Machine learning models
│   └── gst_invoice_yolov9c_optimal.pt  # YOLOv9c trained model
├── 📁 src/                     # Source code modules
│   ├── gst_extractor.py        # Main extraction logic and YOLO integration
│   ├── ocr_processor.py        # OCR processing and text cleaning
│   ├── utils.py                # Utility functions and visualization
│   └── __init__.py             # Package initialization
├── 📁 venv/                    # Virtual environment (created after setup)
├── 📄 app.py                   # Main Streamlit application
├── 📄 config.py                # Configuration settings and constants
├── 📄 requirements.txt         # Python dependencies
├── 📄 README.md                # This documentation
└── 📄 .gitignore               # Git ignore rules
```

### Key Files Description

- **`app.py`**: Main Streamlit application with UI components and user interactions
- **`config.py`**: Central configuration file with paths, settings, and OCR configurations
- **`src/gst_extractor.py`**: Core extraction logic using YOLOv9c for field detection
- **`src/ocr_processor.py`**: OCR processing with field-specific text cleaning and validation
- **`src/utils.py`**: Utility functions for visualization, data formatting, and file operations

## 🎯 Supported GST Fields

InvoiScope can extract **24 different types** of GST invoice fields organized into three main categories:

### 📄 Invoice Metadata (7 fields)
- **Invoice Number**: Unique invoice identifier
- **Invoice Date**: Date of invoice generation
- **Due Date**: Payment due date
- **PO Number**: Purchase order reference
- **Total Amount**: Final payable amount
- **Taxable Amount**: Amount before tax calculation
- **Bill Number**: Alternative billing reference

### 🏢 Business Information (8 fields)
- **Supplier/Merchant Name**: Vendor business name
- **Supplier Address**: Complete vendor address
- **Supplier GST Number**: Vendor GST registration number
- **Buyer Name**: Customer/buyer business name
- **Buyer Address**: Customer address details
- **Buyer GST Number**: Customer GST registration
- **Contact Information**: Phone numbers, emails
- **Business Registration Details**: Additional business identifiers

### 💰 Tax Information (9 fields)
- **CGST**: Central Goods and Services Tax
- **SGST**: State Goods and Services Tax
- **IGST**: Integrated Goods and Services Tax
- **UTGST**: Union Territory GST
- **Total GST**: Combined GST amount
- **TCS**: Tax Collected at Source
- **TDS**: Tax Deducted at Source
- **Compensation Cess**: Additional cess amount
- **Tax Rate**: Applicable tax percentage

### Field Detection Confidence
- **🟢 High Confidence**: ≥ 80% (Highly reliable)
- **🟡 Medium Confidence**: 60-79% (Generally reliable)
- **🔴 Low Confidence**: < 60% (Requires verification)

## 🏗️ Technical Architecture

### System Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│  Image Upload &  │───▶│   YOLOv9c       │
│   (Frontend)    │    │   Preprocessing  │    │   Detection     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Results &     │◀───│  Data Processing │◀───│   OCR Text      │
│   Visualization │    │   & Formatting   │    │   Extraction    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Core Components

#### 1. **YOLOv9c Object Detection**
- **Model**: Custom-trained YOLOv9c optimized for GST invoices
- **Input**: Invoice images (JPG, PNG, JPEG)
- **Output**: Bounding boxes with field classifications and confidence scores
- **Performance**: 74.1% mAP@0.5, 85.4% precision

#### 2. **OCR Processing Pipeline**
- **Engine**: Tesseract OCR with custom configurations
- **Preprocessing**: Image enhancement, scaling, noise reduction
- **Field-Specific Processing**: Different OCR settings for numbers, dates, text
- **Post-processing**: Text cleaning, validation, and formatting

#### 3. **Data Processing & Categorization**
- **Structured Output**: JSON format with categorized fields
- **Confidence Scoring**: Per-field confidence assessment
- **Data Validation**: Format checking and error handling
- **Export Generation**: CSV and JSON export capabilities

### Technology Stack

| Component | Technology | Version | Purpose |
|-----------|------------|---------|---------|
| **Object Detection** | YOLOv9c (Ultralytics) | 8.1.34 | Field detection and localization |
| **OCR Engine** | Tesseract (pytesseract) | 0.3.10 | Text extraction from detected regions |
| **Web Framework** | Streamlit | 1.29.0 | User interface and web application |
| **Image Processing** | OpenCV | 4.8.1.78 | Image preprocessing and manipulation |
| **Deep Learning** | PyTorch | 2.1.0 | Neural network inference |
| **Data Processing** | Pandas | 2.1.3 | Data manipulation and export |
| **Visualization** | Matplotlib | 3.8.2 | Result visualization and annotations |

## ⚙️ Configuration

### Main Configuration (`config.py`)

```python
# Model Settings
MODEL_PATH = "models/gst_invoice_yolov9c_optimal.pt"
DEFAULT_CONFIDENCE = 0.5

# File Processing
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']

# OCR Configurations
OCR_CONFIGS = {
    'numbers': '--psm 7 -c tessedit_char_whitelist=0123456789',
    'amounts': '--psm 7 -c tessedit_char_whitelist=0123456789₹.,- ',
    'dates': '--psm 7 -c tessedit_char_whitelist=0123456789/-.',
    'gst_number': '--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
}
```

### Streamlit Configuration (`.streamlit/config.toml`)

```toml
[theme]
primaryColor = "#1e88e5"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"

[server]
maxUploadSize = 10
enableCORS = false
```

### Environment Variables

```bash
# Optional: Set Tesseract path if not in system PATH
export TESSERACT_CMD="/usr/local/bin/tesseract"

# Optional: Set custom model path
export GST_MODEL_PATH="/path/to/your/model.pt"
```

## 📊 Model Performance

### Training Metrics
- **Dataset**: 2,500+ annotated GST invoices
- **Training Time**: 48 hours on NVIDIA RTX 3080
- **Validation Split**: 80/20 train/validation

### Performance Metrics
| Metric | Value | Description |
|--------|-------|-------------|
| **mAP@0.5** | 74.1% | Mean Average Precision at IoU 0.5 |
| **mAP@0.5:0.95** | 52.3% | Mean Average Precision across IoU thresholds |
| **Precision** | 85.4% | True Positive / (True Positive + False Positive) |
| **Recall** | 67.2% | True Positive / (True Positive + False Negative) |
| **F1-Score** | 75.2% | Harmonic mean of precision and recall |

### Processing Performance
- **Average Processing Time**: 2.8 seconds per invoice
- **Memory Usage**: ~1.2GB during inference
- **Supported Image Sizes**: 640x640 to 2048x2048 pixels
- **Batch Processing**: Up to 10 images simultaneously

### Field-Specific Accuracy
| Field Category | Precision | Recall | F1-Score |
|----------------|-----------|--------|----------|
| Invoice Metadata | 88.2% | 71.5% | 79.0% |
| Business Information | 82.1% | 65.8% | 73.0% |
| Tax Information | 86.7% | 64.3% | 73.8% |

## 📚 API Reference

### GSTInvoiceExtractor Class

```python
from src.gst_extractor import GSTInvoiceExtractor

# Initialize extractor
extractor = GSTInvoiceExtractor(model_path="models/gst_invoice_yolov9c_optimal.pt")

# Extract information
results = extractor.extract_gst_information(
    image_path="path/to/invoice.jpg",
    confidence_threshold=0.5
)
```

#### Methods

##### `extract_gst_information(image_path, confidence_threshold=0.5)`
Extracts GST information from an invoice image.

**Parameters:**
- `image_path` (str): Path to the invoice image file
- `confidence_threshold` (float): Minimum confidence score (0.1-1.0)

**Returns:**
```python
{
    "invoice_metadata": {
        "invoice_number": [{"field_type": str, "text_content": str, "confidence": float, "bbox": list}],
        # ... other fields
    },
    "business_information": { /* ... */ },
    "tax_information": { /* ... */ },
    "summary": {
        "total_detections": int,
        "average_confidence": float,
        "extraction_timestamp": str
    }
}
```

### OCRProcessor Class

```python
from src.ocr_processor import OCRProcessor

# Initialize OCR processor
ocr = OCRProcessor()

# Extract text from image region
text = ocr.extract_text(image_region, field_type="amounts")
```

### Utility Functions

```python
from src.utils import create_annotated_image, create_results_dataframe

# Create annotated image
annotated_img = create_annotated_image(image_path, gst_data)

# Create results DataFrame
df = create_results_dataframe(gst_data)
```

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **Model File Not Found**
```
Error: Model file not found at: models/gst_invoice_yolov9c_optimal.pt
```
**Solution:**
- Ensure the model file is placed in the `models/` directory
- Check file name matches exactly: `gst_invoice_yolov9c_optimal.pt`
- Verify file permissions and accessibility

#### 2. **Tesseract Not Found**
```
TesseractNotFoundError: tesseract is not installed or it's not in your PATH
```
**Solution:**
- Install Tesseract OCR for your operating system
- Add Tesseract to your system PATH
- On Windows, verify installation path in environment variables

#### 3. **Memory Issues**
```
RuntimeError: CUDA out of memory
```
**Solution:**
- Reduce image size before processing
- Process images one at a time instead of batches
- Use CPU inference if GPU memory is limited:
```python
# Force CPU usage
import torch
torch.cuda.is_available = lambda: False
```

#### 4. **Poor OCR Results**
**Symptoms:** Extracted text is garbled or incorrect
**Solutions:**
- Ensure invoice images are high resolution (minimum 300 DPI)
- Check image quality - avoid blurry or low-contrast images
- Adjust confidence threshold to filter low-quality detections
- Verify proper lighting and minimal skew in scanned documents

#### 5. **Streamlit Port Issues**
```
Error: Port 8501 is already in use
```
**Solution:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8501 | xargs kill -9
```

### Performance Optimization

#### For Better Accuracy:
1. **Image Quality**: Use high-resolution, well-lit images
2. **Confidence Tuning**: Start with 0.6-0.7 for better precision
3. **Image Preprocessing**: Ensure minimal skew and good contrast

#### For Faster Processing:
1. **Image Resizing**: Resize large images to 1024x1024 maximum
2. **Batch Processing**: Process multiple invoices in sequence
3. **Model Optimization**: Use TensorRT or ONNX for production deployment

### Debug Mode

Enable debug logging for troubleshooting:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run extraction with detailed logs
results = extractor.extract_gst_information(image_path, confidence_threshold=0.5)
```

## 🤝 Contributing

We welcome contributions to improve InvoiScope! Here's how you can help:

### Development Setup

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Install development dependencies**:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. **Make your changes**
5. **Run tests**:
   ```bash
   python -m pytest tests/
   ```
6. **Submit a pull request**

### Contribution Areas

- **🐛 Bug Fixes**: Report and fix issues
- **✨ New Features**: Add support for new invoice formats
- **📚 Documentation**: Improve documentation and examples
- **🧪 Testing**: Add test cases and improve coverage
- **🎨 UI/UX**: Enhance the user interface
- **⚡ Performance**: Optimize processing speed and accuracy

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Add docstrings for all functions and classes
- Include unit tests for new features

### Reporting Issues

When reporting issues, please include:
- Python version and operating system
- Complete error messages and stack traces
- Sample invoice images (with sensitive data removed)
- Steps to reproduce the issue

## 📄 License

This project is licensed under the **MIT License**.

### MIT License Summary
- ✅ Commercial use allowed
- ✅ Modification allowed
- ✅ Distribution allowed
- ✅ Private use allowed
- ❌ No warranty provided
- ❌ No liability assumed

## 🙏 Acknowledgments

- **Ultralytics**: For the excellent YOLOv9 implementation
- **Tesseract OCR**: For robust text extraction capabilities
- **Streamlit**: For the intuitive web framework
- **OpenCV**: For comprehensive image processing tools
- **Contributors**: Thanks to all contributors who helped improve this project

## 📞 Support & Contact

- **📧 Email**: naman2634@gmail.com
- **🐛 Issues**: [GitHub Issues](https://github.com/ayush2635/Invoiscope/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/ayush2635/Invoiscope/discussions)
- **📖 Documentation**: [Wiki](https://github.com/ayush2635/Invoiscope/wiki)


---

<div align="center">

**🔍 InvoiScope** - Making GST invoice processing intelligent and efficient!

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Powered by YOLOv9](https://img.shields.io/badge/Powered%20by-YOLOv9-blue.svg)](https://github.com/ultralytics/ultralytics)
[![Built with Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red.svg)](https://streamlit.io/)

⭐ **Star this repository if you find it helpful!** ⭐

</div>