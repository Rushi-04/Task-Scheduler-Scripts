import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\DELTA_DENTAL\\S98
    prefix/ext not required (kept for interface consistency)
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_today_block = False

    # scan bottom → top
    for line in reversed(lines):
        # detect today's SM98 file
        if today in line and "SM98_" in line:
            found_today_block = True

        if found_today_block and "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
