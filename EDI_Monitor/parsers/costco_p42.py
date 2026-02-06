import os
from datetime import datetime, timedelta

def check(base_dir, prefix, ext):
    """
    Check Costco ELG P42 by looking for the generated file in the 'Files' subdirectory.
    It does NOT parse the trace/log file, but verifies the artifact existence directly.
    
    base_dir: C:\\Transfer_Programs\\COSTCO\\P42
    Target: base_dir\\Files\\NVPSL_elig-YYYYMMDD.txt
    """
    
    files_dir = os.path.join(base_dir, "Files")
    
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    
    # Construct expected filenames
    # prefix is "NVPSL_elig-"
    # ext is ".txt"
    fname_today = f"{prefix}{today.strftime('%Y%m%d')}{ext}"
    fname_yesterday = f"{prefix}{yesterday.strftime('%Y%m%d')}{ext}"
    
    path_today = os.path.join(files_dir, fname_today)
    path_yesterday = os.path.join(files_dir, fname_yesterday)
    
    print(f"Checking for files in: {files_dir}")
    
    # Check Today's file
    if os.path.exists(path_today):
        print(f"Found today's file: {path_today}")
        return path_today, True
        
    # Check Yesterday's file (flexible match)
    if os.path.exists(path_yesterday):
         print(f"Found yesterday's file: {path_yesterday}")
         return path_yesterday, True
         
    print(f"File not found. Checked: {fname_today}, {fname_yesterday}")
    return None, False
