import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.smtp_username = settings.SMTP_USERNAME
        self.smtp_password = settings.SMTP_PASSWORD
        self.sender_email = settings.SMTP_USERNAME
        self.recipient_email = "info@trumpetwinsouls.sl.com"  # Your email address

    async def send_contact_email(self, name: str, email: str, message: str) -> bool:
        """
        Send a contact form email
        
        Args:
            name: Sender's name
            email: Sender's email
            message: The message content
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{name} <{self.sender_email}>"
            msg['To'] = self.recipient_email
            msg['Reply-To'] = email
            msg['Subject'] = f"New Contact Form Submission from {name}"
            
            # Create the email body
            body = f"""
            You have received a new message from your website contact form.
            
            Name: {name}
            Email: {email}
            
            Message:
            {message}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Create SMTP session
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
