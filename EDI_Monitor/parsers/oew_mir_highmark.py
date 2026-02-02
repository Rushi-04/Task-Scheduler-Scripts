import re
from datetime import datetime
from .base import TraceParser

class OewMirHighmarkParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        # Pattern: MIROUT.D + YYMMDD + .T + HHMMSS
        # Example: MIROUT.D260130.T150001
        
        today_yymmdd = datetime.now().strftime("%y%m%d")
        
        # prefix should be "MIROUT.D"
        self.token = f"{prefix}{today_yymmdd}"
        
        # Matches: [token] + .T + [digits]
        # We make the extension optional or part of the pattern logic since it varies
        # But here valid matches look like: MIROUT.D260130.T150001
        self.pattern = re.compile(rf"{self.token}\.T\d+", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check OEW MIR Highmark in log.txt
    """
    parser = OewMirHighmarkParser(base_dir, prefix, ext)
    return parser.check()
