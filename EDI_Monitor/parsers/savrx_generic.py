import re
from utils import today_yymmdd
from .base import TraceParser

class SavrxGenericParser(TraceParser):
    def __init__(self, base_dir, prefix, ext, trace_filename="trace.txt"):
        super().__init__(base_dir, trace_filename=trace_filename)
        # Pattern: Prefix + YYMMDD + Digits + Ext
        # Example: OEWEDI_260119162000.pgp
        self.token = prefix + today_yymmdd()
        self.pattern = re.compile(rf"{self.token}\d+{ext}", re.IGNORECASE)

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext, trace_filename="trace.txt"):
    """
    Generic SAVRX parser.
    """
    parser = SavrxGenericParser(base_dir, prefix, ext, trace_filename=trace_filename)
    return parser.check()
