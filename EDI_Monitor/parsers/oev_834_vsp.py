import os
from datetime import datetime


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\VSP\\834_Pgms\\OEW
    prefix/ext not used (kept for interface consistency)
    """

    trace_path = os.path.join(base_dir, "trace.txt")
    if not os.path.isfile(trace_path):
        return None, False

    with open(trace_path, "r", errors="ignore") as f:
        lines = f.readlines()

    # Look for latest SUCCESS block
    for line in reversed(lines):
        if "Transfer request completed with status: Finished" in line:
            return "FINISHED", True

    return None, False
