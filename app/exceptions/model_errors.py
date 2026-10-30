class ModelError(Exception):
    """base exception for model-related errors"""

    def __init__(
            self,
            code: str,
            message: str,
    ):
        self.code = code
        self.message = message

        super().__init__(self.message)


class ModelAuthenticationError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_AUTHENTICATION_FAILED",
            message="Model authentication failed.",
        )

class ModelRateLimitError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_RATE_LIMITED",
            message="Model request rate limit exceeded"
        )

class ModelTimeoutError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_TIMEOUT",
            message="Model request timed out.",
        )


class ModelConnectionError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_CONNECTION_FAILED",
            message="Unable to connect to the model service.",
        )


class ModelAPIError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_API_ERROR",
            message="Model service returned an error.",
        )


class ModelEmptyResponseError(ModelError):
    def __init__(self):
        super().__init__(
            code="MODEL_EMPTY_RESPONSE",
            message="Model returned an empty response.",
        )