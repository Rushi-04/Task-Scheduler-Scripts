import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\ANTHEM_WGS\\834_Pgms\\HWL
    prefix/ext kept for interface consistency
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    today = datetime.now().strftime("%y%m%d")

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_today = False

    # scan from bottom upwards
    for line in reversed(lines):
        # detect today's HWL file
        if f"HWL{today}" in line:
            found_today = True

        if found_today and "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
