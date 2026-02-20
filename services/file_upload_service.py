"""File upload handling service."""
import pandas as pd
import os
from typing import Dict, List, Optional
from fastapi import UploadFile
from config import settings
from utils.logger import setup_logger

logger = setup_logger()


class FileUploadService:
    """Service for handling file uploads."""
    
    @staticmethod
    async def save_upload_file(file: UploadFile) -> str:
        """Save uploaded file and return path."""
        os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(settings.UPLOAD_DIR, file.filename)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"File saved: {file_path}")
        return file_path
    
    @staticmethod
    async def parse_csv(file_path: str) -> List[Dict]:
        """Parse CSV file and return list of dictionaries."""
        try:
            df = pd.read_csv(file_path)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error parsing CSV: {str(e)}")
            raise
    
    @staticmethod
    async def parse_excel(file_path: str, sheet_name: Optional[str] = None) -> List[Dict]:
        """Parse Excel file and return list of dictionaries."""
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return df.to_dict('records')
        except Exception as e:
            logger.error(f"Error parsing Excel: {str(e)}")
            raise
    
    @staticmethod
    def validate_student_data(data: List[Dict]) -> tuple[List[Dict], List[str]]:
        """Validate student data and return valid records and errors."""
        valid_records = []
        errors = []
        
        required_fields = ['student_id', 'name']
        
        for idx, record in enumerate(data, 1):
            record_errors = []
            for field in required_fields:
                if field not in record or not record[field]:
                    record_errors.append(f"Missing {field}")
            
            if record_errors:
                errors.append(f"Row {idx}: {', '.join(record_errors)}")
            else:
                valid_records.append(record)
        
        return valid_records, errors


# Global instance
file_upload_service = FileUploadService()
