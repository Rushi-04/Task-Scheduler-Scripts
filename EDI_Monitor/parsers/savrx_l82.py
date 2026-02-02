from .savrx_generic import SavrxGenericParser

def check(base_dir, prefix, ext):
    """
    L82 834 SAVRX Check.
    Uses run.log instead of trace.txt.
    """
    parser = SavrxGenericParser(base_dir, prefix, ext, trace_filename="run.log")
    return parser.check()
