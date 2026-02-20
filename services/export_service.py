"""Data export service."""
import pandas as pd
import json
from typing import List, Dict
from datetime import datetime
from utils.logger import setup_logger

logger = setup_logger()


class ExportService:
    """Service for exporting data."""
    
    @staticmethod
    def export_to_csv(data: List[Dict], filename: str = None) -> str:
        """Export data to CSV file."""
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logger.info(f"Data exported to {filename}")
        return filename
    
    @staticmethod
    def export_to_json(data: List[Dict], filename: str = None) -> str:
        """Export data to JSON file."""
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Data exported to {filename}")
        return filename
    
    @staticmethod
    def export_to_excel(data: List[Dict], filename: str = None, sheet_name: str = "Data") -> str:
        """Export data to Excel file."""
        if not filename:
            filename = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, sheet_name=sheet_name)
        logger.info(f"Data exported to {filename}")
        return filename


# Global instance
export_service = ExportService()
