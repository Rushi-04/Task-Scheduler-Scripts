import re
from datetime import datetime
from .base import TraceParser

class MntBankPospayParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        # Pattern: MEIMTB_ + YYYYMMDD + .txt
        # Example: MEIMTB_20260129.txt
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # Token: MEIMTB_20260129
        self.token = f"{prefix}{today_yyyymmdd}"
        
        # Exact match pattern
        self.pattern = re.compile(rf"{self.token}{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check MNT BANK POSITIVE PAY in log.txt
    """
    parser = MntBankPospayParser(base_dir, prefix, ext)
    return parser.check()
