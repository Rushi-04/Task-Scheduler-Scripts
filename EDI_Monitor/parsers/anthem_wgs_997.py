import re
from datetime import datetime
from .base import TraceParser

class AnthemWgs997Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        # Pattern: FA + YYYYMMDD + ... + .835
        # Example: FA2026012915004014046517.835
        
        today_str = datetime.now().strftime("%Y%m%d")
        # prefix is likely "FA"
        self.token = f"{prefix}{today_str}"
        self.pattern = re.compile(rf"{self.token}.*{ext}", re.IGNORECASE)

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
