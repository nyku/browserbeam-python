from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from browserbeam._http import SyncHTTP, DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from browserbeam.session import Session
from browserbeam.types import (
    SessionEnvelope,
    SessionInfo,
    SessionList,
    _parse_session_envelope,
    _parse_session_info,
    _parse_session_list,
)


class _Sessions:
    """Sync interface for the /v1/sessions endpoints."""

    def __init__(self, http: SyncHTTP) -> None:
        self._http = http

    def create(
        self,
        *,
        url: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        timeout: Optional[int] = None,
        viewport: Optional[Dict[str, int]] = None,
        user_agent: Optional[str] = None,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
        proxy: Optional[str] = None,
        block_resources: Optional[List[str]] = None,
        auto_dismiss_blockers: Optional[bool] = None,
        cookies: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
    ) -> Session:
        """Create a browser session and return a :class:`Session` object."""
        body: Dict[str, Any] = {}
        if url is not None:
            body["url"] = url
        if steps is not None:
            body["steps"] = steps
        if timeout is not None:
            body["timeout"] = timeout
        if viewport is not None:
            body["viewport"] = viewport
        if user_agent is not None:
            body["user_agent"] = user_agent
        if locale is not None:
            body["locale"] = locale
        if timezone is not None:
            body["timezone"] = timezone
        if proxy is not None:
            body["proxy"] = proxy
        if block_resources is not None:
            body["block_resources"] = block_resources
        if auto_dismiss_blockers is not None:
            body["auto_dismiss_blockers"] = auto_dismiss_blockers
        if cookies is not None:
            body["cookies"] = cookies

        headers = {}
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key

        data = self._http._client.post(
            "/v1/sessions",
            json=body,
            headers=headers if headers else None,
        )
        if data.status_code >= 400:
            from browserbeam.errors import _raise_for_status
            h = {k.lower(): v for k, v in data.headers.items()}
            _raise_for_status(data.status_code, data.json(), h)
        envelope = _parse_session_envelope(data.json())
        return Session(envelope, self._http)

    def get(self, session_id: str) -> SessionInfo:
        """Get session status and metadata."""
        data = self._http.get(f"/v1/sessions/{session_id}")
        return _parse_session_info(data)

    def list(
        self,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        after: Optional[str] = None,
    ) -> SessionList:
        """List sessions with optional filtering and pagination."""
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        data = self._http.get("/v1/sessions", params=params if params else None)
        return _parse_session_list(data)

    def destroy(self, session_id: str) -> None:
        """Destroy a session and release browser resources."""
        self._http.delete(f"/v1/sessions/{session_id}")


class Browserbeam:
    """Sync Browserbeam API client.

    Usage::

        from browserbeam import Browserbeam

        client = Browserbeam(api_key="sk_live_...")

        session = client.sessions.create(url="https://example.com")
        session.click(ref="e1")
        result = session.extract(title="h1 >> text")
        print(result.extraction)
        session.close()
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        resolved_key = api_key or os.environ.get("BROWSERBEAM_API_KEY", "")
        if not resolved_key:
            raise ValueError(
                "No API key provided. Pass api_key= or set the BROWSERBEAM_API_KEY environment variable."
            )
        self._http = SyncHTTP(resolved_key, base_url=base_url, timeout=timeout)
        self.sessions = _Sessions(self._http)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()
