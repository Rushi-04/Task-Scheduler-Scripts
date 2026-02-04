import re
from datetime import datetime, timedelta
from .base import TraceParser

class MeiGenericParser(TraceParser):
    def __init__(self, base_dir, prefix, ext, trace_filename="trace.txt"):
        super().__init__(base_dir, trace_filename=trace_filename)
        # Pattern: [prefix] + (YYYYMMDD | YYYYMMDD-1) + [ext]
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%Y%m%d")
        y_str = yesterday.strftime("%Y%m%d")
        
        # Regex: prefix + (today|yesterday) + ext
        self.pattern = re.compile(rf"{re.escape(prefix)}({t_str}|{y_str}){re.escape(ext)}", re.IGNORECASE)
        print(f"MeiGeneric: Searching for pattern: {self.pattern.pattern} in {trace_filename}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Generic MEI parser Check.
    Detects if it should use log.txt or trace.txt if not specified, 
    but defaults to trace.txt.
    """
    # For Cancer task, user specified log.txt
    # We can handle this by checking which one exists or just trusting the pattern
    import os
    trace_file = "trace.txt"
    if not os.path.exists(os.path.join(base_dir, trace_file)):
        if os.path.exists(os.path.join(base_dir, "log.txt")):
            trace_file = "log.txt"
            
    parser = MeiGenericParser(base_dir, prefix, ext, trace_filename=trace_file)
    return parser.check()
