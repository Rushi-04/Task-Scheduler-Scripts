import re
from utils import today_yymmdd
from .base import TraceParser

class SavrxOewParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir)
        # Pattern: OEWEDI_ + YYMMDD + <Digits> + .pgp
        # Example: OEWEDI_260119162000.pgp
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
    base_dir: C:\\Transfer_Programs\\SAVRX\\OEW
    """
    parser = SavrxOewParser(base_dir, prefix, ext)
    return parser.check()
