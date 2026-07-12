import os
from pathlib import Path

class Config:
    # Base paths
    BASE_DIR = Path(__file__).parent
    
    # Model settings
    MODEL_PATH = BASE_DIR / "models" / "gst_invoice_yolov9c_optimal.pt"
    
    # Application settings
    APP_TITLE = "InvoiScope - GST Invoice Extractor"
    APP_ICON = "🔍"
    
    # Processing settings
    DEFAULT_CONFIDENCE = 0.5
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
    
    # Directory paths
    UPLOAD_DIR = BASE_DIR / "data" / "uploads"
    RESULTS_DIR = BASE_DIR / "data" / "results"
    TEMP_DIR = BASE_DIR / "data" / "temp"
    
    # OCR configurations
    OCR_CONFIGS = {
        'numbers': '--psm 7 -c tessedit_char_whitelist=0123456789',
        'alphanumeric': '--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz',
        'amounts': '--psm 7 -c tessedit_char_whitelist=0123456789₹.,- ',
        'dates': '--psm 7 -c tessedit_char_whitelist=0123456789/-.',
        'text': '--psm 7',
        'gst_number': '--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    }
    
    # Model performance metrics
    MODEL_PERFORMANCE = {
        'map50': '74.1%',
        'precision': '85.4%',
        'recall': '67.2%',
        'num_classes': 24
    }
    
    # Field type to OCR mapping
    FIELD_OCR_MAPPING = {
        'Invoice Number': 'alphanumeric',
        'Invoice Date': 'dates',
        'GST Number': 'gst_number',
        'Total Amount': 'amounts',
        'CGST': 'amounts',
        'SGST': 'amounts',
        'IGST': 'amounts',
        'Total GST': 'amounts',
        'TCS': 'amounts',
        'Compensation Cess': 'amounts'
    }
    
    # Create directories if they don't exist
    @classmethod
    def create_directories(cls):
        for dir_path in [cls.UPLOAD_DIR, cls.RESULTS_DIR, cls.TEMP_DIR]:
            os.makedirs(dir_path, exist_ok=True)
        # Create models directory
        os.makedirs(cls.BASE_DIR / "models", exist_ok=True)

# Initialize directories
Config.create_directories()
