import re
from datetime import datetime
from .base import TraceParser

class KeyBankPosPayParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="upload_log.log")
        # Pattern: ARP_L82_ + YYYYMMDD + HHMMSS + .KBARM.ARMOH
        # Example: ARP_L82_20260130070000.KBARM.ARMOH
        
        today_yyyymmdd = datetime.now().strftime("%Y%m%d")
        
        # Token: ARP_L82_20260130
        self.token = f"{prefix}{today_yyyymmdd}"
        
        # Matches: [token] + [6 digits for time] + [ext]
        # Example regex: ARP_L82_20260130\d{6}\.KBARM\.ARMOH
        # Note: 'ext' passed from config should probably be ".KBARM.ARMOH"
        self.pattern = re.compile(rf"{self.token}\d{{6}}{re.escape(ext)}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check KeyBank Positive Pay in upload_log.log
    """
    parser = KeyBankPosPayParser(base_dir, prefix, ext)
    return parser.check()
