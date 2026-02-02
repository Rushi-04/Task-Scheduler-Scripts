import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\ANTHEM_WGS\\834_Pgms\\S98
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_today_block = False

    # Scan from bottom (latest run first)
    for line in reversed(lines):
        # Detect today's S98 file reference
        if today in line and "S98" in line:
            found_today_block = True

        if found_today_block and "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
