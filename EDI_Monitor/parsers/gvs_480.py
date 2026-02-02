import os
import re
from datetime import datetime


def check(trace_base_dir, prefix, ext):
    """
    trace_base_dir: C:\\Transfer_Programs\\GVS\\L480
    """

    logs_dir = os.path.join(trace_base_dir, "logs")
    if not os.path.isdir(logs_dir):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    # trace-GVS_260119052720.TXT
    pattern = re.compile(rf"trace-{prefix}_{today}\d+{ext}", re.IGNORECASE)

    matching_files = [
        f for f in os.listdir(logs_dir)
        if pattern.match(f)
    ]

    if not matching_files:
        return None, False

    # pick latest file (by name = timestamp-based)
    latest_file = sorted(matching_files)[-1]
    full_path = os.path.join(logs_dir, latest_file)

    with open(full_path, "r", errors="ignore") as f:
        content = f.read()

    if "Transfer request completed with status: Finished" in content:
        return latest_file, True

    return latest_file, False
