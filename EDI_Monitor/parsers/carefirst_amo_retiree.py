import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\CAREFIRST\\AMO_Ret
    """

    log_path = os.path.join(base_dir, "Log.txt")
    if not os.path.isfile(log_path):
        return None, False

    today = datetime.now().strftime("%Y%m%d")

    with open(log_path, "r", errors="ignore") as f:
        lines = f.readlines()

    found_today = False

    # scan from bottom (latest run)
    for line in reversed(lines):
        # Detect today's renamed file
        if today in line and "AMORET_834P_" in line:
            found_today = True

        if found_today and "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
