"""Notification service for email and SMS."""
from typing import Optional
from twilio.rest import Client as TwilioClient
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings
from utils.logger import setup_logger

logger = setup_logger()


class NotificationService:
    """Service for sending notifications."""
    
    def __init__(self):
        """Initialize notification services."""
        self.twilio_client = None
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            try:
                self.twilio_client = TwilioClient(
                    settings.TWILIO_ACCOUNT_SID,
                    settings.TWILIO_AUTH_TOKEN
                )
            except Exception as e:
                logger.warning(f"Failed to initialize Twilio: {str(e)}")
    
    async def send_sms(self, to: str, message: str) -> bool:
        """Send SMS notification."""
        if not self.twilio_client:
            logger.warning("Twilio not configured, skipping SMS")
            return False
        
        try:
            self.twilio_client.messages.create(
                body=message,
                from_=settings.TWILIO_PHONE_NUMBER,
                to=to
            )
            logger.info(f"SMS sent to {to}")
            return True
        except Exception as e:
            logger.error(f"Error sending SMS: {str(e)}")
            return False
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html_body: Optional[str] = None
    ) -> bool:
        """Send email notification."""
        if not settings.EMAIL_USER or not settings.EMAIL_PASSWORD:
            logger.warning("Email not configured, skipping email")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = settings.EMAIL_USER
            msg['To'] = to
            
            # Add plain text
            msg.attach(MIMEText(body, 'plain'))
            
            # Add HTML if provided
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            
            # Send email
            with smtplib.SMTP(settings.EMAIL_SMTP_HOST, settings.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent to {to}")
            return True
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    async def notify_risk_alert(
        self,
        student_name: str,
        risk_level: str,
        contact_email: Optional[str] = None,
        contact_phone: Optional[str] = None
    ):
        """Send risk alert notification."""
        message = f"Alert: {student_name} has been flagged as {risk_level} risk for dropout. Please review their profile."
        
        if contact_email:
            await self.send_email(
                contact_email,
                f"Risk Alert: {student_name}",
                message
            )
        
        if contact_phone:
            await self.send_sms(contact_phone, message)


# Global instance
notification_service = NotificationService()
