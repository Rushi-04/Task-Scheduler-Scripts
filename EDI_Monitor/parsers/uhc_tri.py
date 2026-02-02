import os


def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\UHC\\TRI
    """

    log_path = os.path.join(base_dir, "process.log")
    if not os.path.isfile(log_path):
        return None, False

    with open(log_path, "r", errors="ignore") as f:
        lines = f.readlines()

    # Find the LAST run start
    start_index = None
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("Start:"):
            start_index = i
            break

    if start_index is None:
        return None, False

    run_block = lines[start_index:]

    success_markers = [
        "SUCCESSFUL",
        "1 file(s) copied",
        "1 file(s) moved"
    ]

    for line in run_block:
        if any(marker in line for marker in success_markers):
            return "SUCCESS", True

    return None, False
