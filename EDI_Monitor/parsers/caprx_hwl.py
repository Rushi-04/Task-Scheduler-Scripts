import re
from datetime import datetime
from .base import TraceParser

class CaprxHwlParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        # Pattern: IronWorkers_Elig_ + YYYYMMDD + _HHMMSS + .txt
        # Example: IronWorkers_Elig_20260130_063002.txt
        
        today_str = datetime.now().strftime("%Y%m%d")
        # prefix should be "IronWorkers_Elig_"
        self.token = f"{prefix}{today_str}"
        # Matches IronWorkers_Elig_20260130...txt
        self.pattern = re.compile(rf"{self.token}.*{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check CAPRX HWL in log.txt
    """
    parser = CaprxHwlParser(base_dir, prefix, ext)
    return parser.check()
