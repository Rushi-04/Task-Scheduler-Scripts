import re
from datetime import datetime, timedelta
from .base import TraceParser

class CareFirstAmoSamParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="Log.txt")
        # Pattern: (AMORET_|AMO_)834P_ + YYYYMMDD + . + HHMMSS + .txt
        # Example success in log: Opening remote file "/ABC/AMO_834P_20260204.072235.txt"
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # We look for "834P_" followed by today or yesterday
        # This covers both AMO_834P_ and AMORET_834P_
        self.pattern = re.compile(rf"834P_({t_str}|{y_str})", re.IGNORECASE)
        print(f"CareFirstAmoSam: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        if self.pattern.search(line):
            # Extract the full file name if possible (prefix + 834P_ + date + . + time + ext)
            match_file = re.search(r"((?:AMORET_|AMO_)834P_\d{8}\.\d{6}\.txt)", line, re.IGNORECASE)
            if match_file:
                print(f"Found file: {match_file.group(1)}")
                return match_file.group(1)
            
            # Fallback to a simpler match if the full one fails but pattern is there
            m = self.pattern.search(line)
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check AMO CareFirst SAM (Active & Retiree) in Log.txt
    """
    parser = CareFirstAmoSamParser(base_dir, prefix, ext)
    return parser.check()
