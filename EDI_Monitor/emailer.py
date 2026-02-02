import requests
from datetime import datetime
from config import EMAIL_API_URL, EMAIL_RECIPIENTS

def send_failure_email(task_name, reason, details=""):
    print("Sending failure email...")

    subject = f"EDI Task Failed: {task_name}"

    body = f"""
    <html>
    <body>
        <h3>EDI Task Failure</h3>
        <p><b>Task:</b> {task_name}</p>
        <p><b>Date:</b> {datetime.now().strftime('%Y-%m-%d')}</p>
        <p><b>Reason:</b></p>
        <p style="color:red;">{reason}</p>
        <pre>{details}</pre>
    </body>
    </html>
    """

    for r in EMAIL_RECIPIENTS:
        try:
            requests.post(EMAIL_API_URL, data={
                "email": r,
                "subject": subject,
                "body": body
            })
            print(f"Email sent to {r}")
        except Exception as e:
            print(f"Email failed for {r}: {e}")
