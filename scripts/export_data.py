"""Export data to CSV/JSON."""
import sys
import os
import json
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.student import Student
from models.risk_assessment import RiskAssessment

def export_students(output_file: str, db: Session):
    """Export students data."""
    students = db.query(Student).all()
    
    data = []
    for student in students:
        data.append({
            'id': student.id,
            'student_id': student.student_id,
            'name': student.name,
            'age': student.age,
            'email': student.email,
            'phone': student.phone,
            'school_id': student.school_id,
            'status': student.status
        })
    
    df = pd.DataFrame(data)
    
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.json'):
        df.to_json(output_file, orient='records', indent=2)
    
    print(f"Exported {len(data)} students to {output_file}")

def export_risk_assessments(output_file: str, db: Session):
    """Export risk assessments."""
    assessments = db.query(RiskAssessment).all()
    
    data = []
    for assessment in assessments:
        data.append({
            'id': assessment.id,
            'student_id': assessment.student_id,
            'risk_score': assessment.risk_score,
            'risk_level': assessment.risk_level,
            'calculated_at': assessment.calculated_at.isoformat() if assessment.calculated_at else None
        })
    
    df = pd.DataFrame(data)
    
    if output_file.endswith('.csv'):
        df.to_csv(output_file, index=False)
    elif output_file.endswith('.json'):
        df.to_json(output_file, orient='records', indent=2)
    
    print(f"Exported {len(data)} risk assessments to {output_file}")

def main():
    """Main export function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Export data to file')
    parser.add_argument('type', choices=['students', 'risk'], help='Data type to export')
    parser.add_argument('output', help='Output file path (.csv or .json)')
    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.type == 'students':
            export_students(args.output, db)
        elif args.type == 'risk':
            export_risk_assessments(args.output, db)
    finally:
        db.close()

if __name__ == "__main__":
    main()
