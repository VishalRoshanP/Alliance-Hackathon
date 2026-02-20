"""Backup database."""
import sys
import os
import shutil
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import settings

def backup_database():
    """Backup SQLite database."""
    db_path = settings.DATABASE_URL.replace('sqlite:///', '')
    
    if not os.path.exists(db_path):
        print(f"Database file not found: {db_path}")
        return
    
    # Create backup directory
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = os.path.join(backup_dir, f"women_education_{timestamp}.db")
    
    # Copy database file
    shutil.copy2(db_path, backup_path)
    
    print(f"Database backed up to: {backup_path}")

if __name__ == "__main__":
    backup_database()
