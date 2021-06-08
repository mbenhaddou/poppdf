"""
    Define exceptions specific to poppdf
"""


class PopplerNotInstalledError(Exception):
    """Happens when poppdf is not installed"""

    pass


class PDFInfoNotInstalledError(PopplerNotInstalledError):
    """Happens when pdfinfo is not installed"""

    pass


class PDFPageCountError(Exception):
    """Happens when the pdfinfo was unable to retrieve the page count"""

    pass


class PDFSyntaxError(Exception):
    """Syntax error was thrown during rendering"""

    pass


class PDFPopplerTimeoutError(Exception):
    """Timeout when pdf convert image."""

    pass
