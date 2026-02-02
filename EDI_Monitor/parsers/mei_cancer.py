import re
from datetime import datetime
from .base import TraceParser

class MeiCancerParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        # Use log.txt as the trace filename
        super().__init__(base_dir, trace_filename="log.txt")
        
        # Pattern: MEI_CANCER_CLAIMS_ + YYYYMMDD + .xls
        # Sample shows: MEI_CANCER_CLAIMS_20260122.xls (no extra digits in sample, but regex is safer)
        today_str = datetime.now().strftime("%Y%m%d")
        self.token = f"{prefix}{today_str}"
        self.pattern = re.compile(rf"{self.token}.*{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\CANCER\\CLAIMS\\MEI
    """
    parser = MeiCancerParser(base_dir, prefix, ext)
    return parser.check()
