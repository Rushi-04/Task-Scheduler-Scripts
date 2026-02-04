import re
from datetime import datetime, timedelta
from .base import TraceParser

class CareFirstAmoRetireeParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="Log.txt")
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Pattern: AMORET_834P_ + YYYYMMDD
        self.pattern = re.compile(rf"AMORET_834P_({t_str}|{y_str})", re.IGNORECASE)
        print(f"CareFirstAmoRetiree: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            # Try to grab the full filename: AMORET_834P_YYYYMMDD.HHMMSS.txt
            match_file = re.search(r"(AMORET_834P_\d{8}\.\d{6}\.txt)", line, re.IGNORECASE)
            if match_file:
                print(f"Found file: {match_file.group(1)}")
                return match_file.group(1)
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check AMO CareFirst Retiree in Log.txt
    """
    parser = CareFirstAmoRetireeParser(base_dir, prefix, ext)
    return parser.check()
