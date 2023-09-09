import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import sys
import os
import re
from os.path import basename


identity = "Cortext Report"
email = "temp email" #Replace Me


try:
    identity = sys.argv[1]
    email = sys.argv[2]
except Exception as e:
    print("Missing Identity or Email")
identity = re.sub("_"," ",identity)


html = "Error"


os.chdir('/home/ec2-user/cortext_io/cortext_io_db')



# output = "[\n"
#reader = open('000_cortext_io.html', 'r', newline='\n', encoding="utf-8")
with open('000_cortext_io.html', encoding="utf-8") as f:
    html = f.read()


sender_email = "smtp email" #smtp email
receiver_email = email
password = "smtp password" #smtp pass

message = MIMEMultipart("alternative")
message["Subject"] = identity
message["From"] = sender_email
message["To"] = receiver_email
message["BCC"] = "Temp Email" #Replace Me


# Create the plain-text and HTML version of your message


# Turn these into plain/html MIMEText objects
#part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
#message.attach(part1)
message.attach(part2)

with open("000_cortext_ssindex.png","rb") as fil:
    part3 = MIMEApplication(
            fil.read(),
            Name=basename("000_cortext_ssindex.png")
    )
part3['Content-Disposition'] = 'attachment; filename="%s"' % basename("000_cortext_ssindex.png")
message.attach(part3)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
