import logging
import smtplib
from email.message import EmailMessage


class SenderConfig:
    def __init__(self, config):
        self.config = {key.lower(): value for key, value in config.items()}
        self.logger = logging.getLogger('Sending Email')
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

    def send_email(self, body, recipients, subject=None, header=None, footer=None, sender=None):
        email = EmailMessage()
        email['Subject'] = subject or self.config['subject']
        email['From'] = sender or self.config['sender']
        email['To'] = recipients
        head = (header or self.config['header']) + "\n\n"
        foot = "\n\n" + (footer or self.config['footer'])
        message = str(head + body + foot)
        email.set_content(message)

        try:
            with smtplib.SMTP(self.config['server'], self.config['port']) as smtp:
                if self.config.get('username') and self.config.get('password'):
                    smtp.login(self.config['username'],
                               self.config['password'])
                smtp.send_message(email)
            self.logger.info("Email sent successfully!")
        except smtplib.SMTPException as e:
            self.logger.error(f"Error sending email: {str(e)}")
