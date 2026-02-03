import re
from datetime import datetime, timedelta
from .base import TraceParser

class AnthemGenericParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: Prefix + (YYMMDD | YYMMDD-1) + Digits + Ext
        
        today = datetime.now()
        yesterday = today - timedelta(days=1)
        
        t_str = today.strftime("%y%m%d")
        y_str = yesterday.strftime("%y%m%d")
        
        # Regex: prefix + (today|yesterday) + digits + ext
        # We use re.escape(ext) for safety.
        self.pattern = re.compile(rf"{prefix}({t_str}|{y_str})\d+{re.escape(ext)}", re.IGNORECASE)
        print(f"AnthemGeneric: Searching for pattern: {self.pattern.pattern}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Generic Anthem parser Check.
    """
    parser = AnthemGenericParser(base_dir, prefix, ext)
    return parser.check()
