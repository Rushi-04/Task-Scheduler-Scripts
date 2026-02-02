from .base import TraceParser

class VspTricountyParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        super().__init__(base_dir, trace_filename="trace.txt")
        # User implies a file pattern ending in 8011956
        # Example: MPUT ...*8011956
        # Since we don't have a success sample showing the exact filename,
        # we will rely on the base class checking for "Finished".
        # If we need to match the file later, we can implement find_file_in_line matching .*8011956
        pass

    # def find_file_in_line(self, line):
    #     if "8011956" in line and self.ext in line:
    #         return "Found"
    #     return None

def check(base_dir, prefix, ext):
    parser = VspTricountyParser(base_dir, prefix, ext)
    return parser.check()
