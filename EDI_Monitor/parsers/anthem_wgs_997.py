import re
from datetime import datetime, timedelta
from .base import TraceParser

class AnthemWgs997Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        # Pattern: FA + YYYYMMDD + ... + .835
        # Example: FA2026012915004014046517.835
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Regex: prefix + (today|yesterday) + anything + ext
        # Example: FA(20260203|20260202).*\.835
        # We use re.escape(ext) to handle the dot safely.
        self.pattern = re.compile(rf"{prefix}({t_str}|{y_str}).*{re.escape(ext)}", re.IGNORECASE)
        print(f"AnthemWgs997: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check 997 Recon Download Anthem_WGS in log.txt
    """
    parser = AnthemWgs997Parser(base_dir, prefix, ext)
    return parser.check()
