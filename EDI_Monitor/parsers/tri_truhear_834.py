import os
import re
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\TruHear\\TRI
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    # TRI260113064545.834
    pattern = re.compile(rf"{prefix}{today}\d+{ext}", re.IGNORECASE)

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_file = None

    for line in reversed(lines):
        if not found_file:
            match = pattern.search(line)
            if match:
                found_file = match.group()
        elif "Transfer request completed with status: Finished" in line:
            return found_file, True

    return found_file, False
