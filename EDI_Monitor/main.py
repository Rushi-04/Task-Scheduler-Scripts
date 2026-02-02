# import os
# import importlib
# from config import TASKS
# from task_reader import get_task_exe_path, locate_trace_file
# from emailer import send_failure_email

# print("=" * 70)
# print("EDI TASK MONITOR STARTED")
# print("=" * 70)

# for task in TASKS:
#     print("\n" + "-" * 60)
#     print(f"-- Checking task: {task['task_name']}")

#     exe_path = get_task_exe_path(task["task_folder"], task["task_name"])
#     if not exe_path or not os.path.exists(exe_path):
#         send_failure_email(task["task_name"], "Executable path not found")
#         continue

#     base_dir = os.path.dirname(exe_path)
#     trace_path = locate_trace_file(base_dir)
#     if not trace_path:
#         send_failure_email(task["task_name"], "trace.txt not found", base_dir)
#         continue

#     parser = importlib.import_module(f"parsers.{task['parser']}")
#     found, success = parser.check(
#         trace_path,
#         task["file_prefix"],
#         task["file_extension"]
#     )

#     if not found:
#         send_failure_email(task["task_name"], "No file generated today")
#     elif not success:
#         send_failure_email(task["task_name"], "File upload incomplete", found)
#     else:
#         print(f" {task['task_name']} SUCCESS")

# print("\n All tasks checked")




import os
import importlib
from config import TASKS
from task_reader import get_task_exe_path
from emailer import send_failure_email
from utils import is_task_due

print("=" * 70)
print("EDI TASK MONITOR STARTED")
print("=" * 70)

for task in TASKS:
    print("\n" + "-" * 60)
    print(f"Checking task: {task['task_name']}")

    due, reason = is_task_due(task["schedule"])
    if not due:
        print(f"Skipping task: {reason}")
        continue

    exe_path = get_task_exe_path(task["task_folder"], task["task_name"])
    if not exe_path or not os.path.exists(exe_path):
        send_failure_email(task["task_name"], "Executable path not found")
        continue

    base_dir = os.path.dirname(exe_path)

    parser = importlib.import_module(f"parsers.{task['parser']}")
    found, success = parser.check(
        base_dir,
        task["file_prefix"],
        task["file_extension"]
    )

    if not found:
        send_failure_email(task["task_name"], "Today's file not found")
    elif not success:
        send_failure_email(task["task_name"], "File upload incomplete", found)
    else:
        print(f"{task['task_name']} SUCCESS")

print("\nAll eligible tasks checked")



