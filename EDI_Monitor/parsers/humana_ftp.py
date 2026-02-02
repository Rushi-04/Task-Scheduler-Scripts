from datetime import datetime
from .base import TraceParser

class HumanaParser(TraceParser):
    def __init__(self, base_dir):
        super().__init__(base_dir)
        self.today_str = datetime.now().strftime("%Y%m%d")

    def find_file_in_line(self, line):
        # Detect today's file reference
        if self.today_str in line and "Humana_OEW_" in line:
            return "Humana_OEW_Matched" # logic indicates file presence
        return None

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\Humana
    prefix/ext not used (kept for interface consistency)
    """
    parser = HumanaParser(base_dir)
    found, success = parser.check()
    
    # Original returned "FINISHED" on success. 
    # Base check() returns the found object (string) if success is true.
    # If we found the file, return "FINISHED" to match old matching logic exactly, 
    # OR we can just return the found string which is fine too.
    if success and found:
        return "FINISHED", True
    
    return found, success
