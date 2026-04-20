from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Union

from browserbeam._http import AsyncHTTP, DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from browserbeam.session import AsyncSession
from browserbeam.types import (
    SessionEnvelope,
    SessionInfo,
    SessionList,
    _parse_session_envelope,
    _parse_session_info,
    _parse_session_list,
)


class _AsyncSessions:
    """Async interface for the /v1/sessions endpoints."""

    def __init__(self, http: AsyncHTTP) -> None:
        self._http = http

    async def create(
        self,
        *,
        url: Optional[str] = None,
        steps: Optional[List[Dict[str, Any]]] = None,
        timeout: Optional[int] = None,
        viewport: Optional[Dict[str, int]] = None,
        user_agent: Optional[str] = None,
        locale: Optional[str] = None,
        timezone: Optional[str] = None,
        proxy: Optional[Union[str, Dict[str, Any]]] = None,
        block_resources: Optional[List[str]] = None,
        auto_dismiss_blockers: Optional[bool] = None,
        cookies: Optional[List[Dict[str, Any]]] = None,
        idempotency_key: Optional[str] = None,
    ) -> AsyncSession:
        """Create a browser session and return an :class:`AsyncSession` object."""
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

        response = await self._http._client.post(
            "/v1/sessions",
            json=body,
            headers=headers if headers else None,
        )
        if response.status_code >= 400:
            from browserbeam.errors import _raise_for_status
            h = {k.lower(): v for k, v in response.headers.items()}
            _raise_for_status(response.status_code, response.json(), h)
        envelope = _parse_session_envelope(response.json())
        return AsyncSession(envelope, self._http)

    async def get(self, session_id: str) -> SessionInfo:
        data = await self._http.get(f"/v1/sessions/{session_id}")
        return _parse_session_info(data)

    async def list(
        self,
        *,
        status: Optional[str] = None,
        limit: Optional[int] = None,
        after: Optional[str] = None,
    ) -> SessionList:
        params: Dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        if limit is not None:
            params["limit"] = limit
        if after is not None:
            params["after"] = after
        data = await self._http.get("/v1/sessions", params=params if params else None)
        return _parse_session_list(data)

    async def destroy(self, session_id: str) -> None:
        await self._http.delete(f"/v1/sessions/{session_id}")


class AsyncBrowserbeam:
    """Async Browserbeam API client.

    Usage::

        from browserbeam import AsyncBrowserbeam

        client = AsyncBrowserbeam(api_key="sk_live_...")

        session = await client.sessions.create(url="https://example.com")
        await session.click(ref="e1")
        result = await session.extract(title="h1 >> text")
        print(result.extraction)
        await session.close()
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
        self._http = AsyncHTTP(resolved_key, base_url=base_url, timeout=timeout)
        self.sessions = _AsyncSessions(self._http)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()
