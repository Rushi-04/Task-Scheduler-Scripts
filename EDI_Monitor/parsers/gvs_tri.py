from .base import TraceParser

class GVSTRIParser(TraceParser):
    def __init__(self, base_dir, prefix, ext):
        # User specified "log.txt" in the base folder.
        # Sample shows "Upload complete." as the success indicator.
        super().__init__(base_dir, trace_filename="log.txt", success_marker="Upload complete.")

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\GVS\\TRI
    """
    parser = GVSTRIParser(base_dir, prefix, ext)
    return parser.check()
