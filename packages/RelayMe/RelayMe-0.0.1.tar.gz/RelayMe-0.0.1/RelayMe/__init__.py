import logging
import smtplib
from email.message import EmailMessage


class EmailSender:
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger('EmailSender')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def send_email(self, subject, body, recipient, sender=None):
        email = EmailMessage()
        email['Subject'] = subject
        email['From'] = sender or self.config['sender']
        email['To'] = recipient
        email.set_content(body)

        try:
            with smtplib.SMTP(self.config['server'], self.config['port']) as smtp:
                if self.config.get('username') and self.config.get('password'):
                    smtp.login(self.config['username'],
                               self.config['password'])
                smtp.send_message(email)
            self.logger.info("Email sent successfully!")
        except smtplib.SMTPException as e:
            self.logger.error(f"Error sending email: {str(e)}")
