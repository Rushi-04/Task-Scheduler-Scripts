import win32com.client
import os

def get_task_exe_path(folder_path, task_name):
    print(f"Reading Task Scheduler: {task_name}")

    scheduler = win32com.client.Dispatch("Schedule.Service")
    scheduler.Connect()

    folder = scheduler.GetFolder(folder_path)
    for task in folder.GetTasks(0):
        if task.Name == task_name:
            for action in task.Definition.Actions:
                if action.Type == 0:
                    print(f"EXE/BAT path: {action.Path}")
                    return action.Path

    print("Task not found in scheduler")
    return None


def locate_trace_file(base_dir):
    candidates = [
        os.path.join(base_dir, "trace.txt"),
        os.path.join(base_dir, "logs", "trace.txt")
    ]

    for p in candidates:
        if os.path.exists(p):
            print(f"trace.txt found: {p}")
            return p

    print("trace.txt not found")
    return None
