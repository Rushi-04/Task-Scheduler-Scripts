import win32com.client
import os
import requests
from datetime import datetime, timedelta

EMAIL_TO = "borkarananta028@gmail.com"
EMAIL_API_URL = "http://104.153.122.230:8127/send-email"

# FOLDERS = ["DevTasks", "Microsoft\\Windows\\Application Experience"]
# FOLDERS = ["Microsoft\\Windows\\Device Information"]
FOLDERS = ["Microsoft\\Windows\\Customer Experience Improvement Program"]
# FOLDERS = ["HP\\HPX Support"]
CHECKER_SCRIPT = r"E:\OneSmarter Files\Automation\File_Check_Bot\Task Scheduler Scripts\task_checker.py"  # Change this to your actual checker script path

def send_email(html_body):
    payload = {
        "email": EMAIL_TO,
        "subject": "Scheduled Tasks for Today",
        "body": html_body
    }
    try:
        res = requests.post(EMAIL_API_URL, data=payload)
        print("Email sent:", res.status_code)
    except Exception as e:
        print("Failed to send email:", str(e))

def format_html(tasks):
    if not tasks:
        return "<p><strong>No scheduled tasks found for today.</strong></p>"

    html = """
    <html><body><h2>Scheduled Tasks for Today</h2><table border='1' cellspacing='0' cellpadding='5'>
    <tr><th>Task Name</th><th>Scheduled Time</th></tr>
    """
    for task in tasks:
        html += f"<tr><td>{task['Path']}</td><td>{task['Time']}</td></tr>"
    html += "</table></body></html>"
    return html

# def schedule_checker(task_path, expected_time):
#     try:
#         # Ensure expected_time is local naive datetime
#         if expected_time.tzinfo:
#             expected_time = expected_time.astimezone().replace(tzinfo=None)

#         # Calculate check time correctly
#         check_time = expected_time + timedelta(minutes=30)
#         now = datetime.now()

#         if check_time <= now:
#             print(f"[!] Skipping {task_path} – check time {check_time} in the past.")
#             return

#         check_time_str = check_time.strftime("%H:%M")
#         date_str = check_time.strftime("%d/%m/%Y")

#         task_name = f"Check_{task_path.split('\\')[-1].replace(' ', '_')}_{check_time.strftime('%H%M')}"

#         checker_cmd = (
#                 f'powershell -Command \\"python \'{CHECKER_SCRIPT}\' \'{task_path}\' \'{expected_time.isoformat()}\' \'{task_name}\'\\"'
#             )
#             # Escape PowerShell command
#             # checker_cmd = (
#             #     f'powershell -Command \\"python \'{CHECKER_SCRIPT}\' \'{task_path}\' \'{expected_time.isoformat()}\'\\"'
#             # )

#             # checker_cmd = (
#             #     f'powershell -Command \\"python \'{CHECKER_SCRIPT}\' \'{task_path}\' \'{expected_time.isoformat()}\' \'{task_name}\'\\"'
#             # )

#         print(f"[+] Scheduling checker for {task_path} at {check_time_str} on {date_str}")
#         print(f"Command: schtasks /Create /TN \"{task_name}\" /TR \"{checker_cmd}\" /SC ONCE /ST {check_time_str} /SD {date_str} /F")

#         result = os.system(
#             f'schtasks /Create /TN "{task_name}" /TR "{checker_cmd}" /SC ONCE /ST {check_time_str} /SD {date_str} /F'
#         )

#         if result != 0:
#             print(f"[!] ❌ Failed to schedule task: {task_name}")
#         else:
#             print(f"[✔] Scheduled: {task_name}")

#     except Exception as e:
#         print(f"[!] Exception while scheduling {task_path}: {e}")

def schedule_checker(task_path, expected_time):
    try:
        if expected_time.tzinfo:
            expected_time = expected_time.astimezone().replace(tzinfo=None)

        check_time = expected_time + timedelta(minutes=30)
        now = datetime.now()

        if check_time <= now:
            print(f"[!] Skipping {task_path} – check time {check_time} is in the past.")
            return

        # Format strings for schtasks
        check_time_str = check_time.strftime("%H:%M")
        date_str = check_time.strftime("%d/%m/%Y")
        expected_str = expected_time.strftime("%Y-%m-%dT%H:%M:%S")

        task_name = f"Check_{task_path.split('\\')[-1].replace(' ', '_')}_{check_time.strftime('%H%M')}"

        # checker_cmd = (
        #     f'powershell -Command "python \\"{CHECKER_SCRIPT}\\" \\"{task_path}\\" \\"{expected_str}\\" \\"{task_name}\\""'
        # )
        checker_cmd = (
            f'powershell -Command \\"python \'{CHECKER_SCRIPT}\' \'{task_path}\' \'{expected_str}\' \'{task_name}\'\\"'
            )

        print(f"[+] Scheduling checker for {task_path} at {check_time_str} on {date_str}")
        print(f"Command: schtasks /Create /TN \"{task_name}\" /TR \"{checker_cmd}\" /SC ONCE /ST {check_time_str} /SD {date_str} /F")

        result = os.system(
            f'schtasks /Create /TN "{task_name}" /TR "{checker_cmd}" /SC ONCE /ST {check_time_str} /SD {date_str} /F'
        )

        if result != 0:
            print(f"[!] ❌ Failed to schedule task: {task_name}")
        else:
            print(f"[✔] Scheduled: {task_name}")

    except Exception as e:
        print(f"[!] Exception while scheduling {task_path}: {e}")

def main():
    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()

    today = datetime.today().date()
    scheduled_today = []

    for folder_path in FOLDERS:
        # folder = svc.GetFolder("\\")
        # for part in folder_path.split("\\"):
        #     if part.strip():
        #         folder = folder.GetFolder(part)
        try:
            folder = svc.GetFolder(f"\\{folder_path}")
        except Exception as e:
            print(f"[!] Failed to access folder: {folder_path} – {e}")
            continue

        for task in folder.GetTasks(0):
            if not task.Enabled:
                continue

            # next_run = task.NextRunTime
            # if next_run.tzinfo:
            #     next_run = next_run.astimezone().replace(tzinfo=None)

            next_run = task.NextRunTime
            if next_run.year < 2000:
                continue

            
            if next_run.date() == today:
                full_path = f"{folder_path}\\{task.Name}"
                scheduled_today.append({"Path": full_path, "Time": next_run.strftime("%I:%M %p")})
                schedule_checker(full_path, next_run)
            else:
                print(f"[i] Skipped {task.Name} – NextRunTime = {next_run}")

    html = format_html(scheduled_today)
    send_email(html)

if __name__ == "__main__":
    main()
