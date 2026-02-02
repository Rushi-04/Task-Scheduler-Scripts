import re
from datetime import datetime
from .base import TraceParser

class PeboHealthcomb625Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: CP1021_834_ + YYYYMMDD + .txt
        # Example: CP1021_834_20260122.txt
        
        today_str = datetime.now().strftime("%Y%m%d")
        # prefix should be "CP1021_834_" passed from config
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
    base_dir: C:\\Transfer_Programs\\PEBO_HEALTHCOMB\\P625
    """
    parser = PeboHealthcomb625Parser(base_dir, prefix, ext)
    return parser.check()
