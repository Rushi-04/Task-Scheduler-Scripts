import re
from datetime import datetime
from .base import TraceParser

class LyraElgOewParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.log")
        # Pattern: 4thdistricthealthfund_ + YYYYMMDD + ...
        # Example: 4thdistricthealthfund_20260202.csv.pgp
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # Token: 4thdistricthealthfund_20260202
        self.token = f"{prefix}{today_yyyymmdd}"
        
        # Match anything after the date, usually .csv or .csv.pgp
        # Regex: 4thdistricthealthfund_20260202.*\.csv
        self.pattern = re.compile(rf"{self.token}", re.IGNORECASE)

    def find_file_in_line(self, line):
        # We look for "Uploading local file" lines or success lines containing the file
        if "Uploading local file" in line or "Transfer request" in line:
            m = self.pattern.search(line)
            if m:
                # Basic check: if the token is found, we assume it's the right file
                print(f"Found file token: {m.group()}")
                return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check LYRA ELG OEW in log.log
    """
    parser = LyraElgOewParser(base_dir, prefix, ext)
    return parser.check()
