import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\DELTA_DENTAL\\TRI_County
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_today = False

    # scan bottom → top
    for line in reversed(lines):
        # detect today's TRI file
        if today in line and "TRI" in line:
            found_today = True

        if found_today and "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
