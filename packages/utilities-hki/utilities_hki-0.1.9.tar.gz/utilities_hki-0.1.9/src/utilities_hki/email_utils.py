"""
Email utility functions.
Copyright (C) 2022 Humankind Investments
"""

from datetime import date
import smtplib, os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email(content, subject, receiver, credentials):
    """
    Send an email alert.

    Parameters
    ----------
    content : str
        Content of the email to send.
    subject : str
        Subject of the email to send.
    receiver : str
        Email to send the alert to.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    for key in ['sender', 'password', 'port']:
        assert key in credentials, f"credentials must have a key for {key}"
    
    sender = credentials['sender']
    passw = credentials['password']
    port = credentials['port']
    
    msg = MIMEText(content)
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.add_header('Content-Type', 'text/html')

    server = smtplib.SMTP('smtp.' + sender.split('@')[1], port)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(sender, passw)
    # server.sendmail(sender, receiver, msg.as_string())
    server.send_message(msg)
    server.quit()


def wrotetoday(platform, receivers, content, credentials):
    """
    Send an email notification that a script succeeded.

    Parameters
    ----------
    platform : str
        Name of the platform.
    receivers : list of str
        List of emails to send the alert to.
    content : str
        Content of the email alert.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    subject = '[%s] finished writing %s' % (platform, date.today())

    if isinstance(receivers, list):
        receivers= ", ".join(receivers)
        send_email(content, subject, receivers, credentials)
    elif isinstance(receivers, str):
        send_email(content, subject, receivers, credentials)
    else:
        raise TypeError("receivers must be a str or list")

            
def error_alert(platform, receivers, filename, credentials):
    """
    Send an email alert that a script failed.

    Parameters
    ----------
    platform : str
        Name of the platform to be included in the subject line.
    receivers : list of str
        List of emails to send the alert to.
    filename : str
        Name of the script which ran into the error.
    credentials : dict
        Provides the credentials for sender, password, and port.
    """
    
    subject = '[ERROR] %s failed %s' % (platform, date.today())
    content = "{} did not run successfully. <br> Check log".format(filename)
    if isinstance(receivers, list):
        receivers= ", ".join(receivers)
        send_email(content, subject, receivers, credentials)
    elif isinstance(receivers, str):
        send_email(content, subject, receivers, credentials)
    else:
        raise TypeError("receivers must be a str or list")


def send_email_with_attachment(content, subject, receiver, credentials, attachment_paths):
    """
    Send an email alert.

    Parameters
    ----------
    content : str
        Content of the email to send.
    subject : str
        Subject of the email to send.
    receiver : str
        Email to send the alert to.
    credentials : dict
        Provides the credentials for sender, password, and port.
    attachment_paths : list
        List of file path(s) for the attachment(s)
    """
    
    for key in ['sender', 'password', 'port']:
        assert key in credentials, f"credentials must have a key for {key}"
    
    if not isinstance(attachment_paths, list):
        attachment_paths= [attachment_paths]
        
    sender = credentials['sender']
    passw = credentials['password']
    port = credentials['port']
    
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = subject
    msg.attach(MIMEText(content, _subtype='html'))
    msg.add_header('Content-Type', 'text/html')
        
    for path in attachment_paths:
        # Get the file name
        attachment_name = os.path.basename(path)
    
        # Read the attachment file
        with open(path, "rb") as file:
            attachment_part = MIMEApplication(
                file.read(),
                Name=attachment_name
            )
        attachment_part.add_header(
            "Content-Disposition",
            f"attachment; filename= {attachment_name}",
        )
    
        # Add the attachment to the message
        msg.attach(attachment_part)

    with smtplib.SMTP('smtp.' + sender.split('@')[1], port) as server:
        server.starttls()
        server.login(sender, passw)
        server.send_message(msg)
