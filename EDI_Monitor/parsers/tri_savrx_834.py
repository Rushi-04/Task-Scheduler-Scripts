import os
import re
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\SAVRX\\TRI
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")
    file_pattern = re.compile(rf"{prefix}{today}\d+{ext}", re.IGNORECASE)

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    finished_found = False
    found_file = None

    # scan bottom → top
    for line in reversed(lines):
        if not finished_found:
            if "Transfer request completed with status: Finished" in line:
                finished_found = True
        else:
            m = file_pattern.search(line)
            if m:
                found_file = m.group()
                return found_file, True

    return None, False
