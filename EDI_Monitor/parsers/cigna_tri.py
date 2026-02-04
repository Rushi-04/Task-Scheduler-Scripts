import re
from datetime import datetime, timedelta
from .base import TraceParser

class CignaTriParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="trace.txt")
        # Pattern: XO16000__xo10001i. + HHMMSS + . + MMDDYY + .txt
        # Example: XO16000__xo10001i.142810.020426.txt
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%m%d%y")
        y_str = yesterday.strftime("%m%d%y")
        
        # Regex: prefix + time(6 digits) + (today|yesterday) + ext
        # Example: XO16000__xo10001i\.\d{6}\.(020426|020326)\.txt
        self.pattern = re.compile(rf"{re.escape(prefix)}\d{{6}}\.({t_str}|{y_str}){re.escape(ext)}", re.IGNORECASE)
        print(f"CignaTri: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check CIGNA TRI in trace.txt
    """
    # prefix from log: "XO16000__xo10001i."
    parser = CignaTriParser(base_dir, prefix, ext)
    return parser.check()
