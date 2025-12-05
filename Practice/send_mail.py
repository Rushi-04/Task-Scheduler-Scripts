import requests

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




send_email(t_mesge)