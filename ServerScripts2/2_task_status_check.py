# import win32com.client
# from datetime import datetime
# from tzlocal import get_localzone
# import requests      
  
# TARGET_FOLDERS = ["\\", "\\EDI Tasks"]
# SUCCESS_CODES = {0x0, 0xE0434352, 0x41301}

# EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
# EMAIL_SUBJECT = "Scheduled Task Status Report"
# # EMAIL_RECIPIENTS = ["borkarananta028@gmail.com"] # --- Testing
# EMAIL_RECIPIENTS = ["borkarananta028@gmail.com", "akumar@abchldg.com", "osvsethi@abchldg.com"]

# EXCLUDE_TASK_KEYWORDS = ["Adobe", "Microsoft", "OneDrive", "Hourly_taskchecker", "ITSPlatformSelfHealUtility", "TASK20240726010550", "User_Feed_Synchronization", "ZAKIPOINT DAILY", "ZAKIPOINT WEEKLY ELIGIBILITY"]
   
# def is_system_task(task_name):
#     return any(keyword.lower() in task_name.lower() for keyword in EXCLUDE_TASK_KEYWORDS)

# now_local = datetime.now(get_localzone())
# CUTOFF_TIME_STR = now_local.strftime("%H:%M")

# def get_localized_datetime(com_datetime):  
#     try:
#         if com_datetime:
#             return com_datetime.replace(tzinfo=None).astimezone(get_localzone())
#     except Exception:  
#         return None
#     return None

# def format_dt(dt):
#     return dt.strftime('%Y-%m-%d %H:%M:%S') if dt else 'N/A'
   
# def check_tasks():
#     scheduler = win32com.client.Dispatch("Schedule.Service")
#     scheduler.Connect()

#     cutoff_time = now_local.replace(
#         hour=int(CUTOFF_TIME_STR.split(":")[0]),
#         minute=int(CUTOFF_TIME_STR.split(":")[1]),
#         second=0, microsecond=0
#     )

#     print(f"[*] Checking Windows tasks that ran or were supposed to run before: {CUTOFF_TIME_STR}")

#     html_rows = []   
#     total_failed = 0

#     for folder_path in TARGET_FOLDERS:
#         folder = scheduler.GetFolder(folder_path)
#         tasks = folder.GetTasks(1)

#         for task in tasks:
#             if not task.Enabled:  
#                 continue
#             if folder_path == "\\" and is_system_task(task.Name):
#                 continue

#             task_name = task.Name
#             last_run = get_localized_datetime(task.LastRunTime)
#             last_result = task.LastTaskResult
#             last_result_hex = hex(last_result & 0xFFFFFFFF)
   
#             definition = task.Definition
#             triggers = definition.Triggers

#             should_have_run_today = False
#             start_boundary = None

#             for trigger in triggers:
#                 try:
#                     start_boundary = get_localized_datetime(trigger.StartBoundary)
#                     if start_boundary and start_boundary.date() == now_local.date():
#                         should_have_run_today = True
#                         break
#                 except:
#                     continue

#             if last_run and last_run.date() == now_local.date() and last_run <= cutoff_time:
#                 if (last_result & 0xFFFFFFFF) not in SUCCESS_CODES:
#                     total_failed += 1
#                     html_rows.append(f"""
#                         <tr>
#                             <td>{folder_path}</td>
#                             <td>{task_name}</td>
#                             <td>{format_dt(start_boundary)}</td>
#                             <td>{format_dt(last_run)}</td>
#                             <td>{last_result_hex}</td>
#                             <td><strong style='color:red;'>Failed</strong></td>
#                         </tr>
#                     """)
#             elif should_have_run_today and (not last_run or last_run.date() != now_local.date()):
#                 total_failed += 1
#                 html_rows.append(f"""
#                     <tr>
#                         <td>{folder_path}</td>
#                         <td>{task_name}</td>
#                         <td>{format_dt(start_boundary)}</td>
#                         <td>{format_dt(last_run)}</td>
#                         <td>{last_result_hex}</td>
#                         <td><strong style='color:orange;'>Missed</strong></td>
#                     </tr>
#                 """)

#     if total_failed > 0:
#         html_table = f"""
#         <html>
#         <body>
#         <p>Hi,</p>
#         <p>The following tasks either <strong>failed</strong> or did not execute before <strong>{CUTOFF_TIME_STR}</strong> today:</p>
#         <table border="1" cellpadding="6" cellspacing="0">
#             <tr>
#                 <th>Folder</th>
#                 <th>Task Name</th>
#                 <th>Scheduled Time</th>
#                 <th>Last Run Time</th>
#                 <th>Result Code</th>
#                 <th>Status</th>
#             </tr>
#             {''.join(html_rows)}
#         </table>
#         <p>Total Issues Detected: <strong>{total_failed}</strong></p>
#         </body>
#         </html>
#         """
#     else:
#         html_table = f"<p> All tasks executed successfully before {CUTOFF_TIME_STR} today.</p>"

#     for recipient in EMAIL_RECIPIENTS:
#         payload = {
#             "email": recipient,
#             "subject": EMAIL_SUBJECT,
#             "body": html_table
#         }

#         try:
#             response = requests.post(EMAIL_API_URL, data=payload)
#             if response.status_code == 200:
#                 print(f"[+] Email sent successfully to {recipient}")
#             else:
#                 print(f"[!] Failed to send email to {recipient}. Status: {response.status_code}, Response: {response.text}")
#         except Exception as e:
#             print(f"[!] Error sending email to {recipient}: {e}")

# if __name__ == "__main__":
#     check_tasks()


##### 2.

import win32com.client
from datetime import datetime
from tzlocal import get_localzone
import requests


TARGET_FOLDERS = ["\\", "\\EDI Tasks"]
SUCCESS_CODES = {0x0, 0xE0434352, 0x41301}
# SUCCESS_CODES = {0x0, 0x1, 0xE0434352, 0x41301}

EMAIL_API_URL = "http://104.153.122.230:8127/send-email"
EMAIL_SUBJECT = "Scheduled Task Status Report"
EMAIL_RECIPIENTS = ["borkarananta028@gmail.com", "akumar@abchldg.com", "osvsethi@abchldg.com"]
# EMAIL_RECIPIENTS = ["borkarananta028@gmail.com"] # Testing

EXCLUDE_TASK_KEYWORDS = [
    "Adobe", "Microsoft", "OneDrive", "Hourly_taskchecker",
    "ITSPlatformSelfHealUtility", "TASK20240726010550",
    "User_Feed_Synchronization", "ZAKIPOINT DAILY",
    "ZAKIPOINT WEEKLY ELIGIBILITY"
]

EXPECTED_DISABLED_TASKS = [
    "CBC p42", "Claim Monitoring Alert", "Daily Failed Scheduled Tasks Report",
    "One Time Reboot", "taskt-anthem_retention_account_automation.xml",
    "taskt-anthem_retention_account_automation_Echo.xml",
    "taskt-anthem_standard_account_automation.xml",
    "taskt-anthem_standard_account_automation_Echo.xml",
    "taskt-IpSwitchCommand - MagellanMonthlyTask.xml",
    "taskt-IpSwitchCommand.xml",
    "taskt-WEXHealthCloudAutomation_0.xml",
    "taskt-WEXHealthCloudAutomation_1.xml",
    "UHC TRI", "TRI 834 EMPIRERX", "P42 WGS 834", "OCU ANTHEM 834 TO WGS",
    "MIRA 834 TRUSTMARK", "HWL 834 EMPIRX", "ESI Express Script"
]

def is_system_task(task_name):
    return any(keyword.lower() in task_name.lower() for keyword in EXCLUDE_TASK_KEYWORDS)

now_local = datetime.now(get_localzone())
CUTOFF_TIME_STR = now_local.strftime("%H:%M")

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

    cutoff_time = now_local.replace(
        hour=int(CUTOFF_TIME_STR.split(":")[0]),
        minute=int(CUTOFF_TIME_STR.split(":")[1]),
        second=0, microsecond=0
    )

    print(f"[*] Checking Windows tasks that ran or were supposed to run before: {CUTOFF_TIME_STR}")

    html_rows = []
    total_failed = 0
    unexpected_disabled = []  

    for folder_path in TARGET_FOLDERS:
        folder = scheduler.GetFolder(folder_path)
        tasks = folder.GetTasks(1)

        for task in tasks:
            task_name = task.Name

            
            if folder_path == "\\" and is_system_task(task_name):
                continue

            # If disabled, check if unexpected
            if not task.Enabled:
                if task_name not in EXPECTED_DISABLED_TASKS:
                    unexpected_disabled.append(task_name)
                continue  # Disabled tasks don't go into fail check

            last_run = get_localized_datetime(task.LastRunTime)
            last_result = task.LastTaskResult
            last_result_hex = hex(last_result & 0xFFFFFFFF)

            definition = task.Definition
            triggers = definition.Triggers

            should_have_run_today = False
            start_boundary = None

            for trigger in triggers:
                try:
                    start_boundary = get_localized_datetime(trigger.StartBoundary)
                    if start_boundary and start_boundary.date() == now_local.date():
                        should_have_run_today = True
                        break
                except:
                    continue

            if last_run and last_run.date() == now_local.date() and last_run <= cutoff_time:
                if (last_result & 0xFFFFFFFF) not in SUCCESS_CODES:
                    total_failed += 1
                    html_rows.append(f"""
                        <tr>
                            <td>{folder_path}</td>
                            <td>{task_name}</td>
                            <td>{format_dt(start_boundary)}</td>
                            <td>{format_dt(last_run)}</td>
                            <td>{last_result_hex}</td>
                            <td><strong style='color:red;'>Failed</strong></td>
                        </tr>
                    """)
            elif should_have_run_today and (not last_run or last_run.date() != now_local.date()):
                total_failed += 1
                html_rows.append(f"""
                    <tr>
                        <td>{folder_path}</td>
                        <td>{task_name}</td>
                        <td>{format_dt(start_boundary)}</td>
                        <td>{format_dt(last_run)}</td>
                        <td>{last_result_hex}</td>
                        <td><strong style='color:orange;'>Missed</strong></td>
                    </tr>
                """)

    if total_failed > 0:
        html_table = f"""
        <html>
        <body>
        <p>Hi,</p>
        <p>The following tasks either <strong>failed</strong> or did not execute before <strong>{CUTOFF_TIME_STR}</strong> today:</p>
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
        <p>Total Issues Detected: <strong>{total_failed}</strong></p>
        """
    else:
        html_table = f"""
        <html>
        <body>
        <p>Hi,</p>
        <p>All tasks executed successfully before <strong>{CUTOFF_TIME_STR}</strong> today.</p>
        """

   
    html_table += "<hr><p><strong>⚠ Disabled Task Alert:</strong></p><ul>"
    if unexpected_disabled:
        for task in unexpected_disabled:
            html_table += f"<li>{task} task is disabled.</li>"
    else:
        html_table += "<li>No other task disabled.</li>"
    html_table += "</ul></body></html>"


    for recipient in EMAIL_RECIPIENTS:
        payload = {
            "email": recipient,
            "subject": EMAIL_SUBJECT,
            "body": html_table
        }

        try:
            response = requests.post(EMAIL_API_URL, data=payload)
            if response.status_code == 200:
                print(f"Email sent successfully to {recipient}")
            else:
                print(f"Failed to send email to {recipient}. Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            print(f"Error sending email to {recipient}: {e}")

if __name__ == "__main__":
    check_tasks()
