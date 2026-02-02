import re
from utils import today_yymmdd
from .base import TraceParser

class AnthemGenericParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: Prefix + YYMMDD + Digits + Ext
        # Example: 480 + 260122 + 070008 + .834
        # Example: L82 + 260122 + 071041 + .834
        self.token = prefix + today_yymmdd()
        self.pattern = re.compile(rf"{self.token}\d+{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    """
    Generic Anthem parser Check.
    Requires prefix and ext to be set correctly in config.
    """
    parser = AnthemGenericParser(base_dir, prefix, ext)
    return parser.check()
