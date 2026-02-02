import re
from utils import today_yymmdd
from .base import TraceParser

class Anthem521Parser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="log.txt")
        self.prefix = prefix
        self.ext = ext
        self.token = prefix + today_yymmdd()
        # Pre-compile regex for performance
        self.pattern = re.compile(rf"{self.token}\d+{self.ext}")

    def find_file_in_line(self, line):
        m = self.pattern.search(line)
        if m:
            print(f"Found file: {m.group()}")
            return m.group()
        return None

def check(base_dir, prefix, ext):
    print("Parsing ANTHEM 521 trace")
    # trace.txt might be passed as base_dir if the bug existed, but main.py sends os.path.dirname(exe_path)
    # The original code expected 'trace_path'. We'll assume main.py is sending the folder.
    
    parser = Anthem521Parser(base_dir, prefix, ext)
    found, finished = parser.check()
    
    return found, finished
