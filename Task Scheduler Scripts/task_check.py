# import os
# import datetime
# import time
# import pyodbc

# # ─── CONFIG ─────────────────────────────────────────────────────────────────────
# CONN_STR = (
#     "DRIVER={ODBC Driver 17 for SQL Server};"
#     "SERVER=RUSHI_PC\\SQLEXPRESS;"
#     "DATABASE=rushi_db;"
#     "Trusted_Connection=yes;"
# )

# DATE_FORMATS = [
#     '%Y-%m-%d', '%d-%m-%Y', '%m-%d-%Y',
#     '%Y%m%d',   '%d%m%Y',   '%m%d%Y',
# ]

# # ─── DB HELPERS ─────────────────────────────────────────────────────────────────
# def get_tasks_for_today():
#     conn = pyodbc.connect(CONN_STR)
#     cur  = conn.cursor()
#     cur.execute("""
#         SELECT id, path, arrival_time, last_checked_date, scheduled
#         FROM file_checks
#     """)
#     rows = cur.fetchall()
#     conn.close()

#     tasks = []
#     for row in rows:
#         tasks.append({
#             'id':               row.id,
#             'path':             row.path,
#             'arrival_time':     row.arrival_time,
#             'last_checked_date':row.last_checked_date,
#             'scheduled':        row.scheduled
#         })
#     return tasks

# def update_task_status(task_id, status, message):
#     conn = pyodbc.connect(CONN_STR)
#     cur  = conn.cursor()
#     cur.execute("""
#         UPDATE file_checks
#            SET last_checked_date = ?, status = ?, message = ?
#          WHERE id = ?
#     """, datetime.date.today(), status, message, task_id)
#     conn.commit()
#     conn.close()

# # ─── FILE CHECK ────────────────────────────────────────────────────────────────
# def check_for_today_file(path):
#     today     = datetime.date.today()
#     date_strs = [today.strftime(fmt) for fmt in DATE_FORMATS]

#     try:
#         filenames = os.listdir(path)
#     except Exception as e:
#         return False, f"ERROR: cannot access path: {e}"

#     for fname in filenames:
#         for d in date_strs:
#             if d in fname:
#                 return True, f"Found: {fname}"
#     return False, "No matching file with today's date"

# # ─── MAIN LOOP ─────────────────────────────────────────────────────────────────
# def main():
#     print("Bot started. Running every 1 min...")
#     while True:
#         now        = datetime.datetime.now()
#         today      = datetime.date.today()
#         today_name = today.strftime('%A')  # "Monday", "Tuesday", ...

#         tasks = get_tasks_for_today()
#         for task in tasks:
#             sched = task['scheduled'].lower()  # e.g. "daily" or "monday+friday"
#             if sched != 'daily' and today_name.lower() not in [d.strip() for d in sched.split('+')]:
#                 continue

#             task_time = datetime.datetime.combine(today, task['arrival_time'])
#             due_time  = task_time + datetime.timedelta(minutes=2)

#             if now >= due_time:
#                 if task['last_checked_date'] is None or task['last_checked_date'] < today:
#                     found, msg = check_for_today_file(task['path'])
#                     status     = "Present" if found else "Not present"
#                     update_task_status(task['id'], status, msg)
#                     print(f"[{now.strftime('%H:%M:%S')}] {task['path']}: {status} — {msg}")

#         time.sleep(60)

# if __name__ == "__main__":
#     main()


#-------------------------------------------------------------------------------------------------------------------------

# CODE TO GET TASKS FROM A SPECIFIC FOLDER

# import win32com.client

# def list_tasks_in_subfolder(subfolder_path):
#     """
#     subfolder_path: path under 'Task Scheduler Library', e.g. r"HP\\HPX Support"
#                     (no leading backslash)
#     Returns: list of task names in that folder.
#     """
#     # 1) Connect to the local Task Scheduler service
#     svc = win32com.client.Dispatch("Schedule.Service")
#     svc.Connect()

#     # 2) Start at the root folder (Task Scheduler Library)
#     folder = svc.GetFolder("\\")  

#     # 3) Drill down into each subfolder component
#     for part in subfolder_path.split("\\"):
#         folder = folder.GetFolder(part)

#     # 4) Fetch all tasks in that folder
#     tasks = folder.GetTasks(0)   # 0 = no flags

#     # 5) Collect and return their names (or any other property you like)
#     return [task.Name for task in tasks]

# if __name__ == "__main__":
#     # Example: you have Task Scheduler Library → HP → HPX Support
#     subfolder = r"Microsoft\Windows\Application Experience"
#     try:
#         tasks = list_tasks_in_subfolder(subfolder)
#         if tasks:
#             print(f"Tasks in '{subfolder}':")
#             for name in tasks:
#                 print("  ", name)
#         else:
#             print(f"No tasks found in '{subfolder}'.")
#     except Exception as e:
#         print(f"Error accessing folder '{subfolder}': {e}")



#33333333333333333333333333333333333333333333333333333333333333333333333333333

# import win32com.client
# import datetime

# def list_tasks_in_subfolder(subfolder_path):
#     """
#     Returns a list of dicts, each with:
#       - Name
#       - Status
#       - Triggers (as human-readable strings)
#       - Next Run Time (formatted as 'DD-MM-YYYY HH:MM:SS')
#       - Last Run Time (formatted as 'DD-MM-YYYY HH:MM:SS')
#     """
#     svc = win32com.client.Dispatch("Schedule.Service")
#     svc.Connect()

#     # Navigate to the specified subfolder
#     folder = svc.GetFolder("\\")
#     for part in subfolder_path.split("\\"):
#         folder = folder.GetFolder(part)

#     tasks = folder.GetTasks(0)
#     out = []

#     # Map state codes to readable status
#     state_map = {
#         0: "Unknown",
#         1: "Disabled",
#         2: "Queued",
#         3: "Ready",
#         4: "Running"
#     }

#     # Helper to format datetime
#     def fmt(dt):
#         try:
#             if isinstance(dt, datetime.datetime):
#                 return dt.strftime("%d-%m-%Y %H:%M:%S")
#             return datetime.datetime.fromisoformat(str(dt)).strftime("%d-%m-%Y %H:%M:%S")
#         except:
#             return ""

#     for t in tasks:
#         status = state_map.get(t.State, f"State({t.State})")

#         # Build readable trigger descriptions
#         triggers = []
#         for trig in t.Definition.Triggers:
#             tb = trig.Type
#             sb = getattr(trig, "StartBoundary", "")
#             if tb == 1:
#                 desc = f"Time trigger @ {sb}"
#             elif tb == 3:
#                 desc = "On logon"
#             elif tb == 2:
#                 desc = "At system start"
#             else:
#                 desc = f"TriggerType({tb}) @ {sb}"
#             triggers.append(desc)

#         out.append({
#             "Name": t.Name,
#             "Status": status,
#             "Triggers": triggers,
#             "Next Run Time": fmt(t.NextRunTime),
#             "Last Run Time": fmt(t.LastRunTime)
#         })

#     return out

# if __name__ == "__main__":
#     # subfolder = r"Microsoft\Windows\Application Experience"  # <-- Change to your desired folder path
#     subfolder = r""  # <-- Change to your desired folder path
#     try:
#         tasks = list_tasks_in_subfolder(subfolder)
#         if tasks:
#             print(f"Tasks in '{subfolder}':\n")
#             for task in tasks:
#                 print("Name:           ", task["Name"])
#                 print("Status:         ", task["Status"])
#                 print("Triggers:       ", "; ".join(task["Triggers"]))
#                 print("Next Run Time:  ", task["Next Run Time"])
#                 print("Last Run Time:  ", task["Last Run Time"])
#                 print("-" * 50)
#         else:
#             print(f"No tasks found in '{subfolder}'.")
#     except Exception as e:
#         print(f"Error accessing folder '{subfolder}': {e}")


#4444444444444444444444444444444444444444444444444444444444444444444444444444444444  (Only Scheduled Today)

# import win32com.client
# import datetime

# def list_tasks_with_trigger_times_for_today(subfolder_path):
#     svc = win32com.client.Dispatch("Schedule.Service")
#     svc.Connect()

#     # Navigate to the specified subfolder
#     folder = svc.GetFolder("\\")
#     for part in subfolder_path.split("\\"):
#         if part.strip():
#             folder = folder.GetFolder(part)

#     tasks = folder.GetTasks(0)
#     out = []

#     trigger_type_map = {
#         1: "Daily",
#         2: "At system start",
#         3: "At logon",
#         4: "Weekly",
#         5: "Monthly",
#         6: "MonthlyDOW",
#         7: "On event",
#         8: "Registration",
#         9: "Boot trigger"
#     }

#     today = datetime.date.today()

#     for t in tasks:
#         try:
#             for trig in t.Definition.Triggers:
#                 # Parse trigger StartBoundary (if present)
#                 start_boundary = getattr(trig, "StartBoundary", "")
#                 trigger_type = trigger_type_map.get(trig.Type, f"TriggerType({trig.Type})")

#                 trigger_date = None
#                 trigger_time = ""
#                 if start_boundary:
#                     try:
#                         # Parse the StartBoundary string (format: 'YYYY-MM-DDTHH:MM:SS')
#                         dt = datetime.datetime.fromisoformat(start_boundary)
#                         trigger_date = dt.date()
#                         trigger_time = dt.strftime("%H:%M:%S")
#                     except Exception:
#                         trigger_time = "Invalid time format"

#                 # Filter: only include if trigger is today (based on StartBoundary date)
#                 if trigger_date == today:
#                     out.append({
#                         "Name": t.Name,
#                         "Time in Trigger": trigger_time,
#                         "Status": trigger_type
#                     })
#                 elif not start_boundary:
#                     # Handle triggers that don't use StartBoundary (e.g., on boot/logon)
#                     # We'll include them if they are system-based and may run anytime
#                     if trig.Type in [2, 3, 9]:  # System start, logon, boot
#                         out.append({
#                             "Name": t.Name,
#                             "Time in Trigger": "N/A",
#                             "Status": trigger_type
#                         })

#         except Exception as e:
#             continue  # Skip any tasks with malformed triggers

#     return out

# # ---------------------------- MAIN ----------------------------

# if __name__ == "__main__":
#     subfolder = r""  # Change this to subfolder path if needed
#     try:
#         tasks = list_tasks_with_trigger_times_for_today(subfolder)
#         if tasks:
#             print(f"Tasks running today in '{subfolder or 'Root'}':\n")
#             for task in tasks:
#                 print("Task Name:       ", task["Name"])
#                 print("Time in Trigger: ", task["Time in Trigger"])
#                 print("Status:          ", task["Status"])
#                 print("-" * 50)
#         else:
#             print("No tasks scheduled to run today.")
#     except Exception as e:
#         print(f"Error: {e}")


#55555555555555555555555555555555555555555555555555555555555555555555555555555 (All tasks then today scheduled tasks)
import win32com.client
import datetime

def get_valid_tasks(subfolder_path):
    svc = win32com.client.Dispatch("Schedule.Service")
    svc.Connect()

    
    folder = svc.GetFolder("\\")
    for part in subfolder_path.split("\\"):
        if part.strip():
            folder = folder.GetFolder(part)

    tasks = folder.GetTasks(0)
    today = datetime.datetime.today()
    weekday = today.weekday()  # Monday = 0, Sunday = 6
    day_of_month = today.day
    month = today.month

    all_enabled_tasks = []
    today_tasks = []

    trigger_type_map = {
        1: "Time",
        2: "At system start",
        3: "At logon",
        4: "Weekly",
        5: "Monthly",
        6: "MonthlyDOW",
        7: "On event",
        8: "On registration",
        9: "Boot trigger"
    }

    state_map = {
        0: "Unknown",
        1: "Disabled",
        2: "Queued",
        3: "Ready",
        4: "Running"
    }

    for t in tasks:
        if t.State == 1: 
            continue

        try:
            for trig in t.Definition.Triggers:
                trigger_type = trigger_type_map.get(trig.Type, f"Type({trig.Type})")
                time_part = "N/A"
                should_run_today = False

                if hasattr(trig, "StartBoundary"):
                    try:
                        dt = datetime.datetime.fromisoformat(trig.StartBoundary)
                        time_part = dt.strftime("%H:%M:%S")
                    except:
                        time_part = "Invalid time"

                if trig.Type == 1: 
                    should_run_today = True

                elif trig.Type == 4:
                    if hasattr(trig, "DaysOfWeek"):
                        if trig.DaysOfWeek & (1 << weekday):
                            should_run_today = True

                elif trig.Type == 5: 
                    if hasattr(trig, "DaysOfMonth") and hasattr(trig, "MonthsOfYear"):
                        if (trig.DaysOfMonth & (1 << (day_of_month - 1))) and (trig.MonthsOfYear & (1 << (month - 1))):
                            should_run_today = True

                elif trig.Type == 6:
                    if hasattr(trig, "DaysOfWeek") and hasattr(trig, "MonthsOfYear"):
                        if (trig.DaysOfWeek & (1 << weekday)) and (trig.MonthsOfYear & (1 << (month - 1))):
                            should_run_today = True

                elif trig.Type in [2, 3, 9]:
                    should_run_today = True
                    time_part = "N/A"

                task_info = {
                    "Name": t.Name,
                    "Time in Trigger": time_part,
                    "Status": trigger_type
                }

                all_enabled_tasks.append(task_info)
                if should_run_today:
                    today_tasks.append(task_info)
        except Exception as e:
            continue

    return all_enabled_tasks, today_tasks

if 1:
    # subfolder = r"DevTasks" 
    subfolder = r"" # --- Testing  

    all_tasks, today_tasks = get_valid_tasks(subfolder)

    print("All Enabled Tasks:-\n")
    if all_tasks:
        for task in all_tasks:
            print("Task Name:       ", task["Name"])
            print("Time in Trigger: ", task["Time in Trigger"])
            print("Status:          ", task["Status"])
            print("-" * 50)
    else:
        print("No enabled tasks found.\n")

    print("Tasks Scheduled for Today:-\n")
    if today_tasks:
        for task in today_tasks:
            print("Task Name:       ", task["Name"])
            print("Time in Trigger: ", task["Time in Trigger"])
            print("Status:          ", task["Status"])
            print("-" * 50)
    else:
        print("No tasks scheduled to run today.")
