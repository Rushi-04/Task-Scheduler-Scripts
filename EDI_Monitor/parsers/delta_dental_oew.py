import re
from datetime import datetime, timedelta
from .base import TraceParser

class DeltaDentalOEWParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Handle cases where prefix/ext might be empty in config
        self.prefix = prefix or "4DIBEW"
        self.ext = ext or ".pgp"
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Pattern: 4DIBEW + (YYYYMMDD | YYYYMMDD-1) + Digits + .pgp
        # Regex: 4DIBEW(20260204|20260203)\d+\.pgp
        self.pattern = re.compile(rf"{self.prefix}({t_str}|{y_str})\d+{re.escape(self.ext)}", re.IGNORECASE)
        print(f"DeltaDentalOEW: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check OEW 834 file in trace.txt
    """
    parser = DeltaDentalOEWParser(base_dir, prefix, ext)
    return parser.check()