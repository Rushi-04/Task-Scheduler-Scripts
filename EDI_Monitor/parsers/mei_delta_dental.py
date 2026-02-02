import re
from datetime import datetime
from .base import TraceParser

class MeiDeltaDentalParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: 05589newmaryland_ + YYYYMMDD + _<Digits> + .txt
        # Example: 05589newmaryland_20260122_01.txt
        
        today_str = datetime.now().strftime("%Y%m%d")
        # prefix should be "05589newmaryland_" passed from config
        self.token = f"{prefix}{today_str}"
        self.pattern = re.compile(rf"{self.token}_\d+{ext}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\DELTA_DENTAL\\MEI
    """
    parser = MeiDeltaDentalParser(base_dir, prefix, ext)
    return parser.check()
