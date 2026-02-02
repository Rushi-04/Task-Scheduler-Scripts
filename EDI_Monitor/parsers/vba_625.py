import re
from datetime import datetime
from .base import TraceParser

class Vba625Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="trace.txt")
        # Pattern: vba + Digits + - + YYYYMMDD + .txt
        # Example: vba5397-20260202.txt
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # We match prefix (vba) + digits + hyphen + today_yyyymmdd + ext (.txt)
        self.pattern = re.compile(rf"{prefix}\d+-{today_yyyymmdd}{re.escape(ext)}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check 625 VBA 834 in trace.txt
    """
    parser = Vba625Parser(base_dir, prefix, ext)
    return parser.check()
