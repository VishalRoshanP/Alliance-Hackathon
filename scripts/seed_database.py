"""Seed database with initial data."""
import sys
import os
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from models.database import init_db, get_db, SessionLocal
from models.school import School
from models.resource import Resource

def seed_schools(db: Session):
    """Seed schools data."""
    try:
        with open('data/seed_data/sample_schools.json', 'r', encoding='utf-8') as f:
            schools_data = json.load(f)
        
        for school_data in schools_data:
            # Check if school already exists
            existing = db.query(School).filter(School.code == school_data['code']).first()
            if not existing:
                school = School(**school_data)
                db.add(school)
        
        db.commit()
        print(f"Seeded {len(schools_data)} schools")
    except Exception as e:
        print(f"Error seeding schools: {str(e)}")
        db.rollback()

def seed_resources(db: Session):
    """Seed resources data."""
    try:
        with open('data/seed_data/resources.json', 'r', encoding='utf-8') as f:
            resources_data = json.load(f)
        
        count = 0
        for resource_data in resources_data:
            # Check if resource already exists
            existing = db.query(Resource).filter(Resource.title == resource_data['title']).first()
            if not existing:
                resource = Resource(**resource_data)
                db.add(resource)
                count += 1
        
        db.commit()
        print(f"Seeded {count} resources")
    except Exception as e:
        print(f"Error seeding resources: {str(e)}")
        db.rollback()

def main():
    """Main seeding function."""
    print("Initializing database...")
    init_db()
    
    print("Seeding data...")
    db = SessionLocal()
    try:
        seed_schools(db)
        seed_resources(db)
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    main()
