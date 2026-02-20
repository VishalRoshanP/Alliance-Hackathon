"""Import resources from JSON/CSV files."""
import sys
import os
import json
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.resource import Resource

def import_from_json(file_path: str, db: Session):
    """Import resources from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            resources_data = json.load(f)
        
        count = 0
        for resource_data in resources_data:
            existing = db.query(Resource).filter(Resource.title == resource_data['title']).first()
            if not existing:
                resource = Resource(**resource_data)
                db.add(resource)
                count += 1
        
        db.commit()
        print(f"Imported {count} resources from {file_path}")
    except Exception as e:
        print(f"Error importing from JSON: {str(e)}")
        db.rollback()

def import_from_csv(file_path: str, db: Session):
    """Import resources from CSV file."""
    try:
        df = pd.read_csv(file_path)
        count = 0
        
        for _, row in df.iterrows():
            resource_data = row.to_dict()
            existing = db.query(Resource).filter(Resource.title == resource_data.get('title')).first()
            if not existing:
                resource = Resource(**resource_data)
                db.add(resource)
                count += 1
        
        db.commit()
        print(f"Imported {count} resources from {file_path}")
    except Exception as e:
        print(f"Error importing from CSV: {str(e)}")
        db.rollback()

def main():
    """Main import function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import resources from file')
    parser.add_argument('file', help='Path to JSON or CSV file')
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.file.endswith('.json'):
            import_from_json(args.file, db)
        elif args.file.endswith('.csv'):
            import_from_csv(args.file, db)
        else:
            print("Unsupported file format. Use .json or .csv")
    finally:
        db.close()

if __name__ == "__main__":
    main()
