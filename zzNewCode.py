import os
import re
import win32com.client
from datetime import datetime
import requests
import traceback

# ---------------- CONFIG ---------------- #

TARGET_FOLDER = r"\EDI Tasks"
TARGET_TASK_NAME = "521 ANTHEM 834 WGS"
FILE_PREFIX = "521"

EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
EMAIL_RECIPIENTS = [
    "borkarrushi028@gmail.com"
]

# ---------------------------------------- #


def send_failure_email(reason, details=""):
    print("[INFO] Sending failure email...")
    subject = f"❌ EDI Task Failed: {TARGET_TASK_NAME}"

    body = f"""
    <html>
    <body>
        <p><strong>Task:</strong> {TARGET_TASK_NAME}</p>
        <p><strong>Date:</strong> {datetime.now().strftime('%Y-%m-%d')}</p>
        <p><strong>Failure Reason:</strong></p>
        <p style="color:red;">{reason}</p>
        <pre>{details}</pre>
    </body>
    </html>
    """

    for recipient in EMAIL_RECIPIENTS:
        try:
            payload = {
                "email": recipient,
                "subject": subject,
                "body": body
            }
            response = requests.post(EMAIL_API_URL, data=payload)
            print(f"[INFO] Email API response for {recipient}: {response.status_code}")
        except Exception as e:
            print(f"[ERROR] Failed to send email to {recipient}: {e}")


def get_task_exe_path():
    print("[INFO] Connecting to Task Scheduler...")
    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()

    print(f"[INFO] Accessing folder: {TARGET_FOLDER}")
    folder = scheduler.GetFolder(TARGET_FOLDER)
    tasks = folder.GetTasks(0)

    for task in tasks:
        print(f"[DEBUG] Found task: {task.Name}")
        if task.Name == TARGET_TASK_NAME:
            print(f"[INFO] Target task found: {task.Name}")
            for action in task.Definition.Actions:
                if action.Type == 0:  # EXEC action
                    print(f"[INFO] EXE path found: {action.Path}")
                    return action.Path

    print("[ERROR] Target task not found in Task Scheduler.")
    return None


def locate_trace_file(base_dir):
    print(f"[INFO] Looking for trace.txt in: {base_dir}")

    trace_path = os.path.join(base_dir, "trace.txt")
    logs_trace_path = os.path.join(base_dir, "logs", "trace.txt")

    if os.path.exists(trace_path):
        print(f"[INFO] trace.txt found: {trace_path}")
        return trace_path

    if os.path.exists(logs_trace_path):
        print(f"[INFO] trace.txt found in logs folder: {logs_trace_path}")
        return logs_trace_path

    print("[ERROR] trace.txt not found in base or logs directory.")
    return None


def check_trace_for_today_success(trace_path):
    today_token = FILE_PREFIX + datetime.now().strftime("%y%m%d")
    print(f"[INFO] Checking trace for today's token: {today_token}")

    filename_pattern = re.compile(rf"{today_token}\d+\.834")

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    print(f"[INFO] Total lines read from trace.txt: {len(lines)}")

    found_file = None
    finished = False

    for i in range(len(lines) - 1, -1, -1):
        line = lines[i]

        if not found_file:
            match = filename_pattern.search(line)
            if match:
                found_file = match.group()
                print(f"[INFO] Found today's file: {found_file}")
                continue

        if found_file and "Transfer request completed with status: Finished" in line:
            finished = True
            print("[INFO] Found successful completion status.")
            break

    return found_file, finished


def main():
    print("=" * 60)
    print("[INFO] Starting EDI 521 trace verification script")
    print(f"[INFO] Run time: {datetime.now()}")
    print("=" * 60)

    try:
        exe_path = get_task_exe_path()
        if not exe_path:
            print("[ERROR] Executable path could not be resolved.")
            send_failure_email("Executable path not found in Task Scheduler.")
            return

        if not os.path.exists(exe_path):
            print(f"[ERROR] EXE path does not exist on disk: {exe_path}")
            send_failure_email("Executable path does not exist on server.", exe_path)
            return

        base_dir = os.path.dirname(exe_path)
        trace_path = locate_trace_file(base_dir)

        if not trace_path:
            send_failure_email("trace.txt not found.", base_dir)
            return

        found_file, success = check_trace_for_today_success(trace_path)

        if not found_file:
            print("[ERROR] No upload detected for today.")
            send_failure_email(
                "No upload detected for today in trace file.",
                f"Expected prefix: {FILE_PREFIX + datetime.now().strftime('%y%m%d')}"
            )
            return

        if not success:
            print("[ERROR] Upload detected but not finished.")
            send_failure_email(
                "Upload started but did NOT finish successfully.",
                f"File detected: {found_file}"
            )
            return

        print("[SUCCESS] Task executed successfully. No action needed.")

    except Exception as e:
        print("[FATAL] Unexpected error occurred.")
        print(traceback.format_exc())
        send_failure_email("Script crashed unexpectedly.", str(e))


if __name__ == "__main__":
    main()
