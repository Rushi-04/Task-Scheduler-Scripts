import os

class TraceParser:
    def __init__(self, base_dir, success_marker="Transfer request completed with status: Finished", trace_filename="trace.txt"):
        self.base_dir = base_dir
        self.success_marker = success_marker
        self.trace_filename = trace_filename

    def get_trace_path(self):
        """Constructs the full path to the trace file."""
        return os.path.join(self.base_dir, self.trace_filename)

    def find_file_in_line(self, line):
        """
        Override this method in subclasses to extract a filename from a line.
        Return the filename string if found, otherwise None.
        """
        return None

    def check(self):
        """
        Scans the trace file (from bottom to top) for the success marker and optionally a matching file.
        Returns:
            found_file (str or None): The found filename, "FINISHED" if no file looked for but success found, or None.
            finished (bool): True if the success marker was found.
        """
        path = self.get_trace_path()
        if not os.path.exists(path):
            return None, False

        try:
            with open(path, "r", errors="ignore") as f:
                lines = f.readlines()
        except Exception as e:
            print(f"Error reading trace file {path}: {e}")
            return None, False

        found_file = None
        finished = False

        # Scan from bottom to top as we are usually interested in the latest run
        for line in reversed(lines):
            # Check for success marker
            if self.success_marker in line:
                finished = True
            
            # Check for file match if not already found
            if not found_file:
                found_file = self.find_file_in_line(line)
            
            # Optimization: If we found both, we can stop (unless we need to ensure they are from the same "run" block)
            # For now, simple scanning is usually sufficient for these sequential log files.
            if found_file and finished:
                break

        # If the subclass doesn't implement find_file_in_line (returns None),
        # but the process finished successfully, we return "FINISHED" to indicate success.
        if found_file is None and finished:
            # We assume if successful and no specific file was looked for (or found), 
            # the status itself is the "result".
            # Check if subclass actually intended to find a file?
            # heuristic: if find_file_in_line is base implementation, return "FINISHED"
            if self.find_file_in_line.__func__ == TraceParser.find_file_in_line:
                 found_file = "FINISHED"

        return found_file, finished
