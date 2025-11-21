class AIClientError(Exception):
    """Raised when AI client cannot fetch a response."""


class AIResponseValidationError(Exception):
    """Raised when AI response is malformed or missing items."""
