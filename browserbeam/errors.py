from __future__ import annotations

from typing import Any, Dict, Optional


class BrowserbeamError(Exception):
    """Base exception for all Browserbeam API errors."""

    def __init__(
        self,
        message: str,
        code: str = "",
        status_code: int = 0,
        context: Optional[Dict[str, Any]] = None,
        request_id: Optional[str] = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}
        self.request_id = request_id


class AuthenticationError(BrowserbeamError):
    """Raised on 401 — missing or invalid API key."""


class RateLimitError(BrowserbeamError):
    """Raised on 429 — rate limit exceeded."""

    def __init__(self, *args: Any, retry_after: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class QuotaExceededError(BrowserbeamError):
    """Raised on 429 — runtime quota exhausted."""

    def __init__(self, *args: Any, retry_after: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class SessionNotFoundError(BrowserbeamError):
    """Raised on 404 — session not found or expired."""


class EngineUnavailableError(BrowserbeamError):
    """Raised on 503 — browser engine temporarily unavailable."""

    def __init__(self, *args: Any, retry_after: Optional[int] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.retry_after = retry_after


class InvalidRequestError(BrowserbeamError):
    """Raised on 400 — invalid request body."""


class StepExecutionError(BrowserbeamError):
    """Raised when a step fails during execution (returned in the response body)."""

    def __init__(
        self,
        *args: Any,
        step_index: int = 0,
        action: str = "",
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.step_index = step_index
        self.action = action


def _raise_for_status(status_code: int, body: Dict[str, Any], headers: Dict[str, str]) -> None:
    error_data = body.get("error", {})
    code = error_data.get("code", "unknown")
    message = error_data.get("message", "Unknown error")
    context = error_data.get("context")
    request_id = headers.get("x-request-id")
    retry_after_raw = headers.get("retry-after")
    retry_after = int(retry_after_raw) if retry_after_raw else None

    kwargs: Dict[str, Any] = {
        "message": message,
        "code": code,
        "status_code": status_code,
        "context": context,
        "request_id": request_id,
    }

    if status_code == 401:
        raise AuthenticationError(**kwargs)
    elif status_code == 429:
        if code == "quota_exceeded":
            raise QuotaExceededError(**kwargs, retry_after=retry_after)
        raise RateLimitError(**kwargs, retry_after=retry_after)
    elif status_code == 404:
        raise SessionNotFoundError(**kwargs)
    elif status_code == 503:
        raise EngineUnavailableError(**kwargs, retry_after=retry_after)
    elif status_code == 400:
        raise InvalidRequestError(**kwargs)
    else:
        raise BrowserbeamError(**kwargs)
