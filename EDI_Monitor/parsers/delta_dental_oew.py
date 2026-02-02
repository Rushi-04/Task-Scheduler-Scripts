import re
from .base import TraceParser
from utils import today_yymmdd 

class DeltaDentalOEWParser(TraceParser):
    def find_file_in_line(self, line):
        # We look for lines like: Uploading local file "...4DIBEW20260121004000.pgp"
        # Pattern: 4DIBEW + YYYYMMDD + Any Digits + .pgp
        # today_yymmdd() returns YYMMDD, so we might need '20'+YYMMDD if the format is YYYY
        
        # NOTE: The log shows '20260121' (YYYYMMDD). 
        # If today_yymmdd() returns '260121', we need to adjust or use datetime directly.
        
        # Assuming we want to match strictly:
        # P.S. If you just want to find ANY file starting with 4DIBEW that was uploaded:
        if "4DIBEW" in line and ".pgp" in line and "Uploading local file" in line:
             # Extract just the filename if needed, or return the whole line
             # Simple regex to grab the filename:
             m = re.search(r"4DIBEW\d+\.pgp", line)
             if m:
                 return m.group()
        return None

def check(base_dir, prefix, ext):
    return DeltaDentalOEWParser(base_dir).check()