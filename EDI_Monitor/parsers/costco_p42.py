import re
from datetime import datetime
from .base import TraceParser

class CostcoP42Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: NVPSL_elig- + YYYYMMDD + .txt
        # Example: NVPSL_elig-20260122.txt
        
        today_str = datetime.now().strftime("%Y%m%d")
        # prefix should be "NVPSL_elig-" passed from config
        self.token = f"{prefix}{today_str}"
        self.pattern = re.compile(rf"{self.token}{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\COSTCO\\P42
    """
    parser = CostcoP42Parser(base_dir, prefix, ext)
    return parser.check()
