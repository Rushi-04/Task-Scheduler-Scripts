import re
from datetime import datetime, timedelta
from .base import TraceParser

class AmoCareFirstActiveParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="Log.txt")
        # Pattern: AMO_834P_ + YYYYMMDD + . + HHMMSS + (anything)
        # Example success line: Opening remote file "/IN/AMO_834P_20260204.072235.txt.gpg"
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Match prefix + date. We don't stick strictly to the end extension here 
        # because it might be .txt.gpg or just .txt in various logs.
        self.pattern = re.compile(rf"{prefix}({t_str}|{y_str})", re.IGNORECASE)
        print(f"AmoCareFirstActive: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        if self.pattern.search(line):
            # Try to grab the full filename from the log line
            # It usually looks like AMO_834P_YYYYMMDD.HHMMSS.txt.gpg
            m = re.search(rf"({self.pattern.pattern}\.\d{{6}}.*?\.gpg)", line, re.IGNORECASE)
            if m:
                print(f"Found file: {m.group(1)}")
                return m.group(1)
            # Fallback
            sub = self.pattern.search(line)
            return sub.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check AMO CareFirst Active in Log.txt
    """
    parser = AmoCareFirstActiveParser(base_dir, prefix, ext)
    return parser.check()
