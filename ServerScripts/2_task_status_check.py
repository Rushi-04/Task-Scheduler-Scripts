import win32com.client
from datetime import datetime
from tzlocal import get_localzone
import requests    

TARGET_FOLDERS = ["DevTasks", "EDI Tasks"]
SUCCESS_CODES = {0x0, 0xE0434352, 0x41301} 
# CUTOFF_TIME_STR = "09:05"  # HH:MM  --->   CHANGE THIS 
now_local = datetime.now(get_localzone())
CUTOFF_TIME_STR = now_local.strftime("%H:%M")

EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
EMAIL_SUBJECT = "Scheduled Task Status Report"
EMAIL_RECIPIENTS = ["borkarananta028@gmail.com", "akumar@abchldg.com"]
# EMAIL_RECIPIENTS = ["borkarananta028@gmail.com"] #--- Testing


def get_localized_datetime(com_datetime):  
    try:
        if com_datetime:
            return com_datetime.replace(tzinfo=None).astimezone(get_localzone())
    except Exception:  
        return None
    return None

def format_dt(dt):
    return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else 'N/A'


def check_tasks():
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()

    cutoff_time = now_local.replace(hour=int(CUTOFF_TIME_STR.split(":")[0]),
                                minute=int(CUTOFF_TIME_STR.split(":")[1]),
                                second=0, microsecond=0)

    

    print(f"[*] Checking Windows tasks that ran before: {CUTOFF_TIME_STR}")

    html_rows = []
    total_failed = 0

    for folder_path in TARGET_FOLDERS:
        folder = scheduler.GetFolder(folder_path)
        tasks = folder.GetTasks(1)

        for task in tasks:
            if not task.Enabled:
                continue

            last_run = get_localized_datetime(task.LastRunTime)
            last_result = task.LastTaskResult
            last_result_hex = hex(last_result & 0xFFFFFFFF)

            if last_run and last_run.date() == now_local.date() and last_run <= cutoff_time:
                if (last_result & 0xFFFFFFFF) not in SUCCESS_CODES:
                    total_failed += 1
                    html_rows.append(f"""
                        <tr>
                            <td>{folder_path}</td>
                            <td>{task.Name}</td>
                            <td>N/A</td>
                            <td>{format_dt(last_run)}</td>
                            <td>{last_result_hex}</td>
                            <td>Failed</td>
                        </tr>
                    """)

    
    if total_failed > 0:
        html_table = f"""
        <html>
        <body>
        <p>Hi,</p>
        <p>The following tasks failed before <strong>{CUTOFF_TIME_STR}</strong> today:</p>
        <table border="1" cellpadding="6" cellspacing="0">
            <tr>
                <th>Folder</th>
                <th>Task Name</th>
                <th>Scheduled Time</th>
                <th>Last Run Time</th>
                <th>Result Code</th>
                <th>Status</th>
            </tr>
            {''.join(html_rows)}
        </table>
        <p>Total Failed: <strong>{total_failed}</strong></p>
        </body>
        </html>
        """
    else:
        html_table = f"<p>All tasks successfully executed before {CUTOFF_TIME_STR}.</p>"

    
    for recipient in EMAIL_RECIPIENTS:
        payload = {
            "email": recipient,
            "subject": EMAIL_SUBJECT,
            "body": html_table
        }

        try:
            response = requests.post(EMAIL_API_URL, data=payload)
            if response.status_code == 200:
                print(f"[+] Email sent successfully to {recipient}")
            else:
                print(f"[!] Failed to send email to {recipient}. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"[!] Error sending email to {recipient}: {e}")


if __name__ == "__main__":
    check_tasks()
