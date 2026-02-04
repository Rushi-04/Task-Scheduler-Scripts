import re
from .base import TraceParser

class VspGenericParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="trace.txt")
        self.prefix = prefix
        self.ext = ext
        # Pattern to find the file in the MPUT or similar line
        # Example: MPUT D:\Transfers\VSP\834s\S98\*.TXT
        # We can look for the wildcard asterisk as a proxy for the file attempt
        if self.prefix:
            self.pattern = re.compile(rf"{re.escape(self.prefix)}.*{re.escape(self.ext)}", re.IGNORECASE)
        else:
            self.pattern = re.compile(rf"\*.*{re.escape(self.ext)}", re.IGNORECASE)

    def find_file_in_line(self, line):
        # In VSP logs, the filename isn't usually shown in the 'Opening remote file' line in trace.txt
        # But we can look for the command that initiated it
        if "MPUT" in line:
            m = self.pattern.search(line)
            if m:
                # Return 'UPLOADED' or similar since we found the pattern
                return "UPLOADED"
        return None

def check(base_dir, prefix, ext):
    """
    Generic VSP parser Check.
    """
    parser = VspGenericParser(base_dir, prefix, ext)
    return parser.check()
