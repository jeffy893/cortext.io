#!/usr/bin/env python3
"""
CORTEXT Email Notification System

This script sends an email notification with the CORTEXT analysis results to specified recipients.
It includes the HTML report and the StraightShooter index visualization as an attachment.
The script can accept command-line arguments for the document identity and recipient email.
"""

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys
import os
import re
from os.path import basename


# Default values for document identity and recipient email
# These will be used if no command-line arguments are provided
identity = "Cortext Report"
email = "temp email"  # TODO: Replace with a default email or remove hardcoded value


# Try to get document identity and recipient email from command-line arguments
try:
    identity = sys.argv[1]
    email = sys.argv[2]
except Exception as e:
    print("Missing Identity or Email")

# Format the identity for display in the email subject
# Replace underscores with spaces for better readability
identity = re.sub("_", " ", identity)


# Initialize HTML content variable
html = "Error"


# Change to the directory containing the CORTEXT output files
os.chdir('/home/ec2-user/cortext_io/cortext_io_db')


# Read the HTML report file
# This file contains the main CORTEXT analysis results
# output = "[\n"
#reader = open('000_cortext_io.html', 'r', newline='\n', encoding="utf-8")
with open('000_cortext_io.html', encoding="utf-8") as f:
    html = f.read()


# Email configuration
# TODO: Consider using environment variables or a config file for these credentials
sender_email = "smtp email"  # TODO: Replace with actual SMTP email
receiver_email = email
password = "smtp password"  # TODO: Replace with actual SMTP password or use secure storage

# Create a multipart message container
message = MIMEMultipart("alternative")
message["Subject"] = identity
message["From"] = sender_email
message["To"] = receiver_email
message["BCC"] = "Temp Email"  # TODO: Replace with actual BCC email or remove if not needed


# Create the HTML version of the email content
# Note: There was a commented-out plain text version that could be re-implemented if needed
part2 = MIMEText(html, "html")

# Add the HTML content to the email
# The email client will try to render the last part first
#message.attach(part1)
message.attach(part2)

# Attach the StraightShooter index visualization image
with open("000_cortext_ssindex.png", "rb") as fil:
    part3 = MIMEApplication(
            fil.read(),
            Name=basename("000_cortext_ssindex.png")
    )
# Set the attachment filename
part3['Content-Disposition'] = 'attachment; filename="%s"' % basename("000_cortext_ssindex.png")
message.attach(part3)

# Create secure connection with Gmail's SMTP server and send the email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )

# Note: This script has several security and code quality issues that should be addressed:
# 1. Hardcoded credentials (sender_email, password, BCC email)
# 2. No error handling for file operations or email sending
# 3. No confirmation of successful email delivery
# 4. No logging of email activity
# 5. No validation of email addresses
