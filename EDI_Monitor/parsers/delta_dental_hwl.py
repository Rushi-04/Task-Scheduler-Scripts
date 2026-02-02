from .base import TraceParser

def check(base_dir, prefix, ext):
    """
    base_dir: C:\\Transfer_Programs\\DELTA_DENTAL\\HWL
    """
    # Simple check for success marker only
    parser = TraceParser(base_dir)
    return parser.check()
