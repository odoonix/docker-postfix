#!/usr/bin/env python3
import smtplib
import ssl

smtp_server = "localhost"
port = 1587  # For starttls
sender_email = "my@example.org"
password = ""

# Create a secure SSL context
context = ssl.create_default_context()
sender = 'mostafa.barmshory@example.org'
receivers = ['mostafa.barmshory@gmail.com']
message = """From: Mostafa Barmshory <mostafa.barmshory@example.org>
To: Mostafa Barmshory <mostafa.barmshory@gmail.com>
Subject: SMTP email example


This is a test message.
"""
# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port, timeout=10)
    server.ehlo()  # Can be omitted
    # server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted
    # server.login(sender_email, password)
    # TODO: Send email here
    server.sendmail(sender, receivers, message) 
except Exception as e:
    # Print any error messages to stdout
    print(e)
