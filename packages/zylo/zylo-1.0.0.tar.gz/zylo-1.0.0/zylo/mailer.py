import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Mailer:
    def __init__(self):
        self.config = {
            'SMTP': '',
            'SMTP_PORT': 587,
            'SENDER_EMAIL': '',
            'SENDER_PASSWORD': '',
            'SSL': False,
            'DEFAULT_SENDER': '',
            'SSL_SECURITY': False
        }

    def send_email(self, recipient, subject=None, body=None, cc=None, bcc=None, attachments=None):
        smtp_server = self.config['SMTP']
        smtp_port = self.config['SMTP_PORT']
        sender_email = self.config['SENDER_EMAIL']
        sender_password = self.config['SENDER_PASSWORD']
        use_ssl = self.config['SSL']
        default_sender = self.config['DEFAULT_SENDER']
        ssl_security = self.config['SSL_SECURITY']

        if not smtp_server or not sender_email or not sender_password:
            return 'SMTP server, sender email, or sender password not provided.'

        message = MIMEMultipart()
        message['From'] = default_sender if default_sender else sender_email
        message['To'] = recipient
        message['Subject'] = subject if subject else ''

        if cc:
            message['Cc'] = cc
            recipient = [recipient] + cc.split(',')

        if bcc:
            message['Bcc'] = bcc
            recipient = recipient + bcc.split(',')

        if body:
            body_type = 'html' if '<' in body and '>' in body else 'plain'
            message.attach(MIMEText(body, body_type))

        if attachments:
            for attachment in attachments:
                try:
                    with open(attachment, 'rb') as file:
                        attachment_part = MIMEText(file.read(), 'plain')
                        attachment_part.add_header('Content-Disposition', 'attachment', filename=attachment)
                        message.attach(attachment_part)
                except FileNotFoundError:
                    return f'Attachment "{attachment}" not found.'

        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                if use_ssl:
                    server.starttls()

                if ssl_security:
                    server.ehlo()
                    server.esmtp_features['auth'] = 'LOGIN'

                server.login(sender_email, sender_password)
                server.sendmail(sender_email, recipient, message.as_string())
                server.quit()

            return 'Email sent successfully!'
        except smtplib.SMTPAuthenticationError:
            return 'Authentication error: Please check your email credentials.'
        except smtplib.SMTPException as e:
            return f'An error occurred while sending the email: {str(e)}'
        except Exception as e:
            return f'An unexpected error occurred: {str(e)}'

