import re
from datetime import datetime
from .base import TraceParser

class AmoCareFirstActiveParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="Log.txt")
        # Pattern: AMO_834P_ + YYYYMMDD + . + HHMMSS + .txt
        # Example: AMO_834P_20260128.072303.txt
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # Token: AMO_834P_20260128
        self.token = f"{prefix}{today_yyyymmdd}"
        
        # Regex to match token + dot + time + ext
        # self.token includes the prefix "AMO_834P_"
        self.pattern = re.compile(rf"{self.token}\.\d{{6}}{re.escape(ext)}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check AMO CareFirst Active in Log.txt
    """
    parser = AmoCareFirstActiveParser(base_dir, prefix, ext)
    return parser.check()
