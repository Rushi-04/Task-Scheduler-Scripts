from .base import TraceParser

def check(base_dir, prefix, ext):
    """
    Generic parser entry point.
    Use this for any task where you just need to check if 'trace.txt' 
    contains the standard success marker.
    
    prefix and ext are ignored but kept for compatibility.
    """
    parser = TraceParser(base_dir)
    return parser.check()
