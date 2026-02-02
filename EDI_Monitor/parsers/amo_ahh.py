from .base import TraceParser

class AmoAhhParser(TraceParser):
    def __init__(self, base_dir, success_marker="Receive completed successfully."):
        super().__init__(base_dir, trace_filename="Log.txt", success_marker=success_marker)

    # def find_file_in_line(self, line):
    #     return None

def check(base_dir, prefix, ext):
    """
    AMO AHH Eligibility Check.
    Checks Log.txt for 'Receive completed successfully.'
    """
    parser = AmoAhhParser(base_dir)
    return parser.check()
