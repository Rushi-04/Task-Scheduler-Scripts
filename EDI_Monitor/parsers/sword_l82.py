import re
from datetime import datetime, timedelta
from .base import TraceParser

class SwordL82Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="Log.txt")
        # Pattern: L82-Eligibility- + YYYYMMDD + .xls
        # Example: L82-Eligibility-20260204.xls
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Regex: prefix + (today|yesterday) + ext
        # Example: L82-Eligibility-(20260204|20260203)\.xls
        self.pattern = re.compile(rf"{prefix}({t_str}|{y_str}){re.escape(ext)}", re.IGNORECASE)
        print(f"SwordL82: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check Sword_L82 in Log.txt
    """
    parser = SwordL82Parser(base_dir, prefix, ext)
    return parser.check()
