import os
import re
import datetime
from email.mime.text import MIMEText
import requests 


FOLDER_PATH = r"C:\Bicc\Capario_HICN_Processing\Files\backup"

FILE_PATTERN_PREFIX = "COBA_AMBEN_QUERY_RESPONSE_"   # constant part
FILE_PATTERN_REGEX = r"COBA_AMBEN_QUERY_RESPONSE_(\d{12})\.txt"

# Email Config loads from .env file
# SMTP_SERVER = os.getenv("SMTP_SERVER")
# SMTP_PORT = int(os.getenv("SMTP_PORT"))
# EMAIL_FROM = os.getenv("EMAIL_FROM")
# EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
# EMAIL_TO = os.getenv("EMAIL_TO")

"""
# FUNCTION TO SEND EMAIL Old METhOD
def send_email(message):
    msg = MIMEText(message)
    msg["Subject"] = "Missing Monthly File Alert"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("Email sending failed:", e)
"""


mail_api = "http://104.153.122.230:8127/send-email"
mails = ["borkarananta028@gmail.com"]

def send_email(body):
    for mail in mails:
        payload = {
            "email": mail,
            "subject": "Missing Monthly File Alerts",
            "body": body
        }

        response = requests.post(mail_api, data=payload)
        if response.status_code == 200:
            print(f" Email sent successfully to {mail}")
        else:
            print(f" Failed to send email to {mail}. Status: {response.status_code}, Response: {response.text}")


def check_monthly_file():

    # Get current year & month in YYMM format
    now = datetime.datetime.now()
    current_month_prefix = now.strftime("%y%m")   # e.g., 2510

    file_found = False

    # Check files in folder
    for filename in os.listdir(FOLDER_PATH):
        if filename.startswith(FILE_PATTERN_PREFIX) and filename.endswith(".txt"):
            
            match = re.match(FILE_PATTERN_REGEX, filename)
            if match:
                yymmddhhmmss = match.group(1)

                
                if yymmddhhmmss.startswith(current_month_prefix):
                    print("File found for current month:", filename)
                    file_found = True
                    break

    if not file_found:
        message = f"No file found for current month ({current_month_prefix}) in backup folder."
        print(message)
        send_email(message)  


if __name__ == "__main__":
    check_monthly_file()
