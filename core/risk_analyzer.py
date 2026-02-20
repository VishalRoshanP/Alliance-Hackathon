"""Risk analysis and scoring engine."""
from typing import Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from models.student import Student
from models.attendance import AttendanceRecord
from models.fee import FeeRecord
from models.health import HealthRecord
from models.academic import AcademicRecord
from models.risk_assessment import RiskAssessment
from utils.constants import (
    RISK_LOW, RISK_MEDIUM, RISK_HIGH, RISK_CRITICAL,
    RISK_SCORE_LOW, RISK_SCORE_MEDIUM, RISK_SCORE_HIGH
)
from utils.logger import setup_logger

logger = setup_logger()


class RiskAnalyzer:
    """Analyzes student risk for dropout."""
    
    @staticmethod
    def calculate_risk_score(db: Session, student_id: int) -> Dict:
        """Calculate comprehensive risk score for a student."""
        try:
            student = db.query(Student).filter(Student.id == student_id).first()
            if not student:
                raise ValueError(f"Student {student_id} not found")
            
            # Analyze different factors
            attendance_score = RiskAnalyzer.analyze_attendance(db, student_id)
            financial_score = RiskAnalyzer.analyze_financial_stress(db, student_id)
            academic_score = RiskAnalyzer.analyze_academic_performance(db, student_id)
            health_score = RiskAnalyzer.analyze_health_issues(db, student_id)
            
            # Weighted calculation
            risk_score = (
                attendance_score['score'] * 0.25 +
                financial_score['score'] * 0.20 +
                academic_score['score'] * 0.20 +
                health_score['score'] * 0.15 +
                (100 if student.status == "at_risk" else 0) * 0.10 +
                (50 if student.status == "dropped_out" else 0) * 0.10
            )
            
            # Determine risk level
            if risk_score < RISK_SCORE_LOW:
                risk_level = RISK_LOW
            elif risk_score < RISK_SCORE_MEDIUM:
                risk_level = RISK_MEDIUM
            elif risk_score < RISK_SCORE_HIGH:
                risk_level = RISK_HIGH
            else:
                risk_level = RISK_CRITICAL
            
            return {
                'risk_score': round(risk_score, 2),
                'risk_level': risk_level,
                'factors': {
                    'attendance': attendance_score,
                    'financial': financial_score,
                    'academic': academic_score,
                    'health': health_score
                }
            }
        except Exception as e:
            logger.error(f"Error calculating risk score: {str(e)}")
            raise
    
    @staticmethod
    def analyze_attendance(db: Session, student_id: int) -> Dict:
        """Analyze attendance patterns."""
        try:
            # Get attendance records for last 90 days
            cutoff_date = datetime.now().date() - timedelta(days=90)
            records = db.query(AttendanceRecord).filter(
                AttendanceRecord.student_id == student_id,
                AttendanceRecord.date >= cutoff_date
            ).all()
            
            if not records:
                return {'score': 0, 'attendance_rate': 100, 'days_absent': 0}
            
            total_days = len(records)
            absent_days = sum(1 for r in records if r.status == "absent")
            attendance_rate = ((total_days - absent_days) / total_days) * 100 if total_days > 0 else 100
            
            # Calculate risk score (lower attendance = higher risk)
            if attendance_rate >= 80:
                score = 0
            elif attendance_rate >= 60:
                score = 30
            elif attendance_rate >= 40:
                score = 60
            elif attendance_rate >= 20:
                score = 80
            else:
                score = 100
            
            return {
                'score': score,
                'attendance_rate': round(attendance_rate, 2),
                'days_absent': absent_days,
                'total_days': total_days
            }
        except Exception as e:
            logger.error(f"Error analyzing attendance: {str(e)}")
            return {'score': 0, 'attendance_rate': 100, 'days_absent': 0}
    
    @staticmethod
    def analyze_financial_stress(db: Session, student_id: int) -> Dict:
        """Analyze financial stress."""
        try:
            fee_records = db.query(FeeRecord).filter(
                FeeRecord.student_id == student_id,
                FeeRecord.status.in_(["pending", "overdue"])
            ).all()
            
            if not fee_records:
                return {'score': 0, 'total_pending': 0, 'months_overdue': 0}
            
            total_pending = sum(r.amount_due - r.amount_paid for r in fee_records)
            max_months_overdue = max((r.months_overdue for r in fee_records), default=0)
            
            # Calculate risk score
            score = 0
            if total_pending > 50000:
                score += 50
            elif total_pending > 25000:
                score += 30
            elif total_pending > 10000:
                score += 15
            
            if max_months_overdue >= 6:
                score += 50
            elif max_months_overdue >= 3:
                score += 30
            elif max_months_overdue >= 1:
                score += 15
            
            score = min(score, 100)
            
            return {
                'score': score,
                'total_pending': total_pending,
                'months_overdue': max_months_overdue,
                'fee_records_count': len(fee_records)
            }
        except Exception as e:
            logger.error(f"Error analyzing financial stress: {str(e)}")
            return {'score': 0, 'total_pending': 0, 'months_overdue': 0}
    
    @staticmethod
    def analyze_academic_performance(db: Session, student_id: int) -> Dict:
        """Analyze academic performance."""
        try:
            records = db.query(AcademicRecord).filter(
                AcademicRecord.student_id == student_id
            ).order_by(AcademicRecord.exam_date.desc()).limit(10).all()
            
            if not records:
                return {'score': 0, 'average_percentage': 0, 'trend': 'stable'}
            
            percentages = [r.percentage for r in records if r.percentage]
            if not percentages:
                return {'score': 0, 'average_percentage': 0, 'trend': 'stable'}
            
            avg_percentage = sum(percentages) / len(percentages)
            
            # Check trend (declining performance is risky)
            trend = 'stable'
            if len(percentages) >= 2:
                recent_avg = sum(percentages[:len(percentages)//2]) / (len(percentages)//2)
                older_avg = sum(percentages[len(percentages)//2:]) / (len(percentages) - len(percentages)//2)
                if recent_avg < older_avg - 10:
                    trend = 'declining'
                elif recent_avg > older_avg + 10:
                    trend = 'improving'
            
            # Calculate risk score
            score = 0
            if avg_percentage < 40:
                score = 80
            elif avg_percentage < 50:
                score = 60
            elif avg_percentage < 60:
                score = 40
            elif avg_percentage < 70:
                score = 20
            
            if trend == 'declining':
                score += 20
            
            score = min(score, 100)
            
            return {
                'score': score,
                'average_percentage': round(avg_percentage, 2),
                'trend': trend,
                'records_count': len(records)
            }
        except Exception as e:
            logger.error(f"Error analyzing academic performance: {str(e)}")
            return {'score': 0, 'average_percentage': 0, 'trend': 'stable'}
    
    @staticmethod
    def analyze_health_issues(db: Session, student_id: int) -> Dict:
        """Analyze health issues."""
        try:
            records = db.query(HealthRecord).filter(
                HealthRecord.student_id == student_id,
                HealthRecord.resolved_date.is_(None)  # Unresolved issues
            ).all()
            
            if not records:
                return {'score': 0, 'issues_count': 0, 'critical_issues': 0}
            
            critical_count = sum(1 for r in records if r.severity == "critical")
            high_count = sum(1 for r in records if r.severity == "high")
            affects_attendance = sum(1 for r in records if r.affects_attendance)
            
            # Calculate risk score
            score = 0
            if critical_count > 0:
                score += 60
            if high_count > 0:
                score += 30
            if affects_attendance > 0:
                score += 20
            
            score = min(score, 100)
            
            return {
                'score': score,
                'issues_count': len(records),
                'critical_issues': critical_count,
                'high_issues': high_count,
                'affects_attendance': affects_attendance > 0
            }
        except Exception as e:
            logger.error(f"Error analyzing health issues: {str(e)}")
            return {'score': 0, 'issues_count': 0, 'critical_issues': 0}
    
    @staticmethod
    def predict_dropout_probability(
        db: Session,
        student_id: int,
        timeframe_days: int = 180
    ) -> float:
        """Predict probability of dropout within timeframe."""
        risk_assessment = RiskAnalyzer.calculate_risk_score(db, student_id)
        risk_score = risk_assessment['risk_score']
        
        # Simple probability calculation based on risk score
        # Higher risk score = higher probability
        probability = risk_score / 100
        
        return round(probability, 4)


# Global instance
risk_analyzer = RiskAnalyzer()
