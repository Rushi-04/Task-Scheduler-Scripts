import win32com.client
from datetime import datetime
import requests
from email.utils import format_datetime

# === Configuration ===
EMAIL_TO = "borkarananta028@gmail.com"
EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
CUTOFF_TIME = "16:00"  # Hardcoded time before which to check tasks
SUCCESS_CODES = [0x0, 0xE0434352, 0x41301]

# === Only these folders will be scanned ===
FOLDERS_TO_CHECK = ["Microsoft\\Windows\\Application Experience"]

def get_cutoff_time():
    today = datetime.today().date()
    return datetime.strptime(f"{today} {CUTOFF_TIME}", "%Y-%m-%d %H:%M")

def build_html_table(results):
    rows = ""
    for res in results:
        status_color = "#d4edda" if res['Status'] == "Success" else "#f8d7da"
        rows += f"""
        <tr style="background-color: {status_color};">
            <td>{res['TaskPath']}</td>
            <td>{res['LastRunTime']}</td>
            <td>{res['ResultCode']}</td>
            <td>{res['Status']}</td>
        </tr>"""
    
    return f"""
    <html>
    <body>
    <h3>🧾 Windows Task Execution Report – {datetime.today().strftime("%Y-%m-%d")}</h3>
    <table border="1" cellpadding="6" cellspacing="0">
        <tr style="background-color: #dee2e6;">
            <th>Task Path</th>
            <th>Last Run Time</th>
            <th>Result Code</th>
            <th>Status</th>
        </tr>
        {rows}
    </table>
    </body>
    </html>
    """

def send_email_report(html_table):
    payload = {
        "email": EMAIL_TO,
        "subject": "📋 Task Execution Report",
        "body": html_table
    }
    try:
        r = requests.post(EMAIL_API_URL, data=payload)
        print(f"[✔] Email sent, status: {r.status_code}")
    except Exception as e:
        print(f"[✖] Failed to send email: {e}")

def collect_task_statuses():
    results = []
    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()

    for folder_path in FOLDERS_TO_CHECK:
        try:
            folder = svc.GetFolder(folder_path)
        except Exception as e:
            print(f"[!] Failed to access folder: {folder_path} – {e}")
            continue

        for task in folder.GetTasks(0):
            print(f"\n[+] Scanning Task: {task.Path}") #-- Debugging
            try:
                if not task.Enabled:
                    print(f"    ↪ Skipped (Disabled)") #-- Debugging
                    continue
                # if task.State != 1:  # 1 = Ready
                #     print(f"    ↪ Skipped (Not Ready, State = {task.State})") #-- Debugging
                #     continue
                
                matched_trigger = False
                for trigger in task.Definition.Triggers:
                    if trigger.Type != 1:  # Only time-based triggers  -- #-- Debugging
                        continue
                    
                    next_run = task.NextRunTime
                    print(f"    ↪ NextRunTime: {next_run}")  #-- Debugging
                    
                    if not next_run:
                        print("    ↪ Skipped (No NextRunTime)")  #-- Debugging
                        continue
                    
                    next_run_local = next_run.astimezone()  # Convert to local time
                    cutoff_time = get_cutoff_time()
                    
                    print(f"    ↪ NextRunTime (local): {next_run_local}")  # Debug
                    
                     # Compare with today and cutoff
                    if next_run_local.date() == datetime.today().date() and next_run_local <= cutoff_time():
                        result_code = task.LastTaskResult
                        status = "Success" if result_code in SUCCESS_CODES else "Failed"
                        results.append({
                            "TaskPath": task.Path,
                            "LastRunTime": format_datetime(task.LastRunTime),
                            "ResultCode": hex(result_code),
                            "Status": status
                        })
                        print(f"    ↪ ✅ Included (Scheduled before cutoff)") #-- Debugging
                        matched_trigger = True  #-- Debugging
                        break
                    else:
                        print("    ↪ Skipped (Not scheduled before cutoff or not today)") #-- Debugging
                        
                if not matched_trigger:
                    print("    ↪ No valid time-based trigger matched.")   #-- Debugging
                        
            except Exception as e:
                print(f"[!] Error checking task {task.Name}: {e}")

    return results

def main():
    print("[*] Checking Windows tasks scheduled before:", get_cutoff_time().strftime("%H:%M"))
    task_results = collect_task_statuses()

    if task_results:
        html = build_html_table(task_results)
        send_email_report(html)
    else:
        print("[i] No tasks matched the criteria.")

if __name__ == "__main__":
    main()



#########################################################################################

