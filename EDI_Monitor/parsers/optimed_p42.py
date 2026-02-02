import re
from datetime import datetime
from .base import TraceParser

class OptimedP42Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="transfer.log")
        # Pattern: P42_ELG_ + YYYYMMDD + .csv
        # Example: P42_ELG_20260130.csv
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # Token: P42_ELG_20260130
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
    Check OPTIMED P42 in transfer.log
    """
    parser = OptimedP42Parser(base_dir, prefix, ext)
    return parser.check()
