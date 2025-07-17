import win32com.client
import sys
import os
from datetime import datetime
import requests

EMAIL_TO = "borkarananta028@gmail.com"
EMAIL_API_URL = "http://104.153.122.230:8127/send-email"

def send_failure_email(task_path, last_run, result_code):
    subject = f"❌ Task Failed or Did Not Run: {task_path}"
    html_body = f"""
    <html><body>
    <h3>Task Failed or Missed</h3>
    <p><strong>Task:</strong> {task_path}</p>
    <p><strong>Last Run Time:</strong> {last_run}</p>
    <p><strong>Last Result Code:</strong> {result_code}</p>
    </body></html>
    """
    
    payload = {
        "email": EMAIL_TO,
        "subject": subject,
        "body": html_body
    }
    
    try:
        response = requests.post(EMAIL_API_URL, data=payload)
        print(f"Email sent for failed task: {task_path}")
    except Exception as e:
        print(f"Failed to send email for {task_path}: {e}")

def delete_task(task_name):
    try:
        result = os.system(f'schtasks /Delete /TN "{task_name}" /F')
        if result == 0:
            print(f"🗑️ Deleted task: {task_name}")
        else:
            print(f"⚠️ Failed to delete task: {task_name}")
    except Exception as e:
        print(f"Exception while deleting task: {e}")

def main():
    if len(sys.argv) != 4:
        print("Usage: task_checker.py <TaskPath> <ExpectedRunTime> <SelfTaskName>")
        return

    task_path = sys.argv[1]
    expected_time = datetime.fromisoformat(sys.argv[2])
    self_task_name = sys.argv[3]

    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()

    folder = svc.GetFolder("\\")
    for part in task_path.split("\\")[:-1]:
        if part.strip():
            folder = folder.GetFolder(part)

    task_name = task_path.split("\\")[-1]
    task = folder.GetTask(task_name)

    last_run = task.LastRunTime
    result_code = task.LastTaskResult

    if last_run < expected_time:
        send_failure_email(task_path, last_run, "Did Not Run")
    elif result_code != 0:
        send_failure_email(task_path, last_run, f"Failed (Code: {result_code})")
    else:
        print(f"✅ {task_path} ran successfully at {last_run}")

    delete_task(self_task_name)

if __name__ == "__main__":
    main()
