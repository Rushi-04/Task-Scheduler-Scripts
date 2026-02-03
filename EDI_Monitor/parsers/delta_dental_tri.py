import re
from datetime import datetime, timedelta
from utils import today_yymmdd
from .base import TraceParser

class DeltaDentalTriParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        self.prefix = prefix or "TRI"
        self.ext = ext or ".834"
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%y%m%d")
        y_str = yesterday.strftime("%y%m%d")
        
        # Matches prefix + (today|yesterday) + digits + ext
        # Regex: TRI(260203|260202)\d+\.834
        self.pattern = re.compile(rf"{self.prefix}({t_str}|{y_str})\d+{re.escape(self.ext)}", re.IGNORECASE)
        print(f"DeltaDentalTri: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check TRI 834 file in trace.txt
    """
    parser = DeltaDentalTriParser(base_dir, prefix, ext)
    return parser.check()
