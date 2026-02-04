import re
from datetime import datetime, timedelta
from .base import TraceParser

class MeiTeledocParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="trace.txt")
        # Pattern: MEITD_ + YYYYMMDD + .834
        # Example: MEITD_20260204.834
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Regex: prefix + (today|yesterday) + ext
        # Example: MEITD_(20260204|20260203)\.834
        self.pattern = re.compile(rf"{re.escape(prefix)}({t_str}|{y_str}){re.escape(ext)}", re.IGNORECASE)
        print(f"MeiTeledoc: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check MEI 834 TELEDOC in trace.txt
    """
    parser = MeiTeledocParser(base_dir, prefix, ext)
    return parser.check()
