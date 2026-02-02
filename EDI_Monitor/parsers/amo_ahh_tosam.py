import re
from datetime import datetime
from .base import TraceParser

class AmoAhhToSamParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        # Override to check ToSAMLog.txt instead of trace.txt
        super().__init__(base_dir, trace_filename="ToSAMLog.txt")
        
        # Pattern: AHH_ABC_Elig_ToAMO_ + YYMMDD + HHMMSS + .TXT
        # Example: AHH_ABC_Elig_ToAMO_260130104111.TXT
        # Date is 260130 (YYMMDD), time is 104111
        
        today_yymmdd = datetime.now().strftime("%y%m%d")
        
        # We need to construct the regex.
        # Prefix is typically "AHH_ABC_Elig_ToAMO_"
        self.token = f"{prefix}{today_yymmdd}"
        
        # Matches: [token] + [6 digits for time] + [ext]
        # Example regex: AHH_ABC_Elig_ToAMO_260130\d{6}\.TXT
        self.pattern = re.compile(rf"{self.token}\d{{6}}{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Check AMO AHH ToSAM in ToSAMLog.txt
    """
    parser = AmoAhhToSamParser(base_dir, prefix, ext)
    return parser.check()
