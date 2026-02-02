import os
import re
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\SAVRX\\480
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")
    pattern = re.compile(rf"{prefix}{today}\d+{ext}", re.IGNORECASE)

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found = None
    finished = False

    for line in reversed(lines):
        if not found:
            m = pattern.search(line)
            if m:
                found = m.group()
                print(f"Found file: {found}")
        elif "Transfer request completed with status: Finished" in line:
            finished = True
            break

    return found, finished
