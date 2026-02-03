import re
from utils import today_yymmdd
from .base import TraceParser

class DeltaDentalTriParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Handle cases where prefix/ext might be empty in config
        self.prefix = prefix or "TRI"
        self.ext = ext or ".834"
        
        td = today_yymmdd()
        # Pattern: TRI + YYMMDD + Digits + .834
        self.pattern = re.compile(rf"{self.prefix}{td}\d+{re.escape(self.ext)}", re.IGNORECASE)

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
