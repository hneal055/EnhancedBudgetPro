class UnsupportedFormatError(Exception):
    """Raised when a script file has an unsupported format."""

class ParseError(Exception):
    """Raised when a loader returns malformed or invalid parsed data."""

class EngineError(Exception):
    """Raised for failures inside analysis or budget engines."""

class ExportError(Exception):
    """Raised when export step fails."""
