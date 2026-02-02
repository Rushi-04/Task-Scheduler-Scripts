import os
import re
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\ANTHEM_WGS\\834_Pgms\\TRI
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")
    file_pattern = re.compile(rf"{prefix}{today}\d+{ext}", re.IGNORECASE)

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_file = None
    finished = False

    for line in reversed(lines):
        if not found_file:
            m = file_pattern.search(line)
            if m:
                found_file = m.group()
        elif "Transfer request completed with status: Finished" in line:
            finished = True
            break

    return found_file, finished
