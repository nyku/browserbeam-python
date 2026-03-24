from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from browserbeam.types import SessionEnvelope, _parse_session_envelope

if TYPE_CHECKING:
    from browserbeam._http import SyncHTTP, AsyncHTTP


class Session:
    """A browser session with convenience methods for each step type.

    Returned by ``client.sessions.create()``::

        session = client.sessions.create(url="https://example.com")
        session.click(ref="e1")
        result = session.extract(title="h1 >> text")
        print(result.extraction)
        session.close()
    """

    def __init__(self, envelope: SessionEnvelope, http: SyncHTTP) -> None:
        self._http = http
        self._update(envelope)

    def _update(self, envelope: SessionEnvelope) -> None:
        self.session_id = envelope.session_id
        self.expires_at = envelope.expires_at
        self.request_id = envelope.request_id
        self.completed = envelope.completed
        self.page = envelope.page
        self.media = envelope.media
        self.extraction = envelope.extraction
        self.blockers_dismissed = envelope.blockers_dismissed
        self.error = envelope.error
        self._last = envelope

    @property
    def last_response(self) -> SessionEnvelope:
        return self._last

    def act(self, steps: List[Dict[str, Any]]) -> SessionEnvelope:
        """Execute one or more steps on this session."""
        data = self._http.post(f"/v1/sessions/{self.session_id}/act", json={"steps": steps})
        envelope = _parse_session_envelope(data)
        self._update(envelope)
        return envelope

    def goto(self, url: str, *, wait_for: Optional[str] = None, wait_timeout: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {"url": url}
        if wait_for is not None:
            params["wait_for"] = wait_for
        if wait_timeout is not None:
            params["wait_timeout"] = wait_timeout
        return self.act([{"goto": params}])

    def observe(
        self,
        *,
        scope: Optional[str] = None,
        format: Optional[str] = None,
        include_links: Optional[bool] = None,
        max_text_length: Optional[int] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if scope is not None:
            params["scope"] = scope
        if format is not None:
            params["format"] = format
        if include_links is not None:
            params["include_links"] = include_links
        if max_text_length is not None:
            params["max_text_length"] = max_text_length
        return self.act([{"observe": params}])

    def click(
        self,
        *,
        ref: Optional[str] = None,
        text: Optional[str] = None,
        label: Optional[str] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if ref is not None:
            params["ref"] = ref
        if text is not None:
            params["text"] = text
        if label is not None:
            params["label"] = label
        return self.act([{"click": params}])

    def fill(
        self,
        value: str,
        *,
        ref: Optional[str] = None,
        label: Optional[str] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if ref is not None:
            params["ref"] = ref
        if label is not None:
            params["label"] = label
        return self.act([{"fill": params}])

    def type(
        self,
        value: str,
        *,
        label: Optional[str] = None,
        ref: Optional[str] = None,
        delay: Optional[int] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        if delay is not None:
            params["delay"] = delay
        return self.act([{"type": params}])

    def select(
        self,
        value: str,
        *,
        label: Optional[str] = None,
        ref: Optional[str] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        return self.act([{"select": params}])

    def check(
        self,
        *,
        label: Optional[str] = None,
        ref: Optional[str] = None,
        checked: Optional[bool] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        if checked is not None:
            params["checked"] = checked
        return self.act([{"check": params}])

    def scroll(
        self,
        *,
        to: Optional[str] = None,
        direction: Optional[str] = None,
        amount: Optional[int] = None,
        times: Optional[int] = None,
        ref: Optional[str] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if to is not None:
            params["to"] = to
        if direction is not None:
            params["direction"] = direction
        if amount is not None:
            params["amount"] = amount
        if times is not None:
            params["times"] = times
        if ref is not None:
            params["ref"] = ref
        return self.act([{"scroll": params}])

    def scroll_collect(
        self,
        *,
        max_scrolls: Optional[int] = None,
        wait_ms: Optional[int] = None,
        timeout_ms: Optional[int] = None,
        max_text_length: Optional[int] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if max_scrolls is not None:
            params["max_scrolls"] = max_scrolls
        if wait_ms is not None:
            params["wait_ms"] = wait_ms
        if timeout_ms is not None:
            params["timeout_ms"] = timeout_ms
        if max_text_length is not None:
            params["max_text_length"] = max_text_length
        return self.act([{"scroll_collect": params}])

    def screenshot(
        self,
        *,
        full_page: Optional[bool] = None,
        format: Optional[str] = None,
        quality: Optional[int] = None,
        selector: Optional[str] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if full_page is not None:
            params["full_page"] = full_page
        if format is not None:
            params["format"] = format
        if quality is not None:
            params["quality"] = quality
        if selector is not None:
            params["selector"] = selector
        return self.act([{"screenshot": params}])

    def wait(
        self,
        *,
        ms: Optional[int] = None,
        selector: Optional[str] = None,
        text: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if ms is not None:
            params["ms"] = ms
        if selector is not None:
            params["selector"] = selector
        if text is not None:
            params["text"] = text
        if timeout is not None:
            params["timeout"] = timeout
        return self.act([{"wait": params}])

    def extract(self, **schema: Any) -> SessionEnvelope:
        """Extract structured data. Pass the extraction schema as keyword arguments::

            session.extract(title="h1 >> text", products=[{"_parent": ".card", "name": "h2 >> text"}])
        """
        return self.act([{"extract": schema}])

    def fill_form(
        self,
        fields: Dict[str, str],
        *,
        submit: bool = False,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {"fields": fields}
        if submit:
            params["submit"] = True
        return self.act([{"fill_form": params}])

    def upload(self, ref: str, files: List[str]) -> SessionEnvelope:
        return self.act([{"upload": {"ref": ref, "files": files}}])

    def pdf(
        self,
        *,
        format: Optional[str] = None,
        landscape: Optional[bool] = None,
        print_background: Optional[bool] = None,
    ) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if format is not None:
            params["format"] = format
        if landscape is not None:
            params["landscape"] = landscape
        if print_background is not None:
            params["print_background"] = print_background
        return self.act([{"pdf": params}])

    def execute_js(self, expression: str) -> SessionEnvelope:
        return self.act([{"execute_js": {"expression": expression}}])

    def close(self) -> SessionEnvelope:
        return self.act([{"close": {}}])


class AsyncSession:
    """Async version of :class:`Session`."""

    def __init__(self, envelope: SessionEnvelope, http: AsyncHTTP) -> None:
        self._http = http
        self._update(envelope)

    def _update(self, envelope: SessionEnvelope) -> None:
        self.session_id = envelope.session_id
        self.expires_at = envelope.expires_at
        self.request_id = envelope.request_id
        self.completed = envelope.completed
        self.page = envelope.page
        self.media = envelope.media
        self.extraction = envelope.extraction
        self.blockers_dismissed = envelope.blockers_dismissed
        self.error = envelope.error
        self._last = envelope

    @property
    def last_response(self) -> SessionEnvelope:
        return self._last

    async def act(self, steps: List[Dict[str, Any]]) -> SessionEnvelope:
        data = await self._http.post(f"/v1/sessions/{self.session_id}/act", json={"steps": steps})
        envelope = _parse_session_envelope(data)
        self._update(envelope)
        return envelope

    async def goto(self, url: str, *, wait_for: Optional[str] = None, wait_timeout: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {"url": url}
        if wait_for is not None:
            params["wait_for"] = wait_for
        if wait_timeout is not None:
            params["wait_timeout"] = wait_timeout
        return await self.act([{"goto": params}])

    async def observe(self, *, scope: Optional[str] = None, format: Optional[str] = None, include_links: Optional[bool] = None, max_text_length: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if scope is not None:
            params["scope"] = scope
        if format is not None:
            params["format"] = format
        if include_links is not None:
            params["include_links"] = include_links
        if max_text_length is not None:
            params["max_text_length"] = max_text_length
        return await self.act([{"observe": params}])

    async def click(self, *, ref: Optional[str] = None, text: Optional[str] = None, label: Optional[str] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if ref is not None:
            params["ref"] = ref
        if text is not None:
            params["text"] = text
        if label is not None:
            params["label"] = label
        return await self.act([{"click": params}])

    async def fill(self, value: str, *, ref: Optional[str] = None, label: Optional[str] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if ref is not None:
            params["ref"] = ref
        if label is not None:
            params["label"] = label
        return await self.act([{"fill": params}])

    async def type(self, value: str, *, label: Optional[str] = None, ref: Optional[str] = None, delay: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        if delay is not None:
            params["delay"] = delay
        return await self.act([{"type": params}])

    async def select(self, value: str, *, label: Optional[str] = None, ref: Optional[str] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {"value": value}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        return await self.act([{"select": params}])

    async def check(self, *, label: Optional[str] = None, ref: Optional[str] = None, checked: Optional[bool] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if label is not None:
            params["label"] = label
        if ref is not None:
            params["ref"] = ref
        if checked is not None:
            params["checked"] = checked
        return await self.act([{"check": params}])

    async def scroll(self, *, to: Optional[str] = None, direction: Optional[str] = None, amount: Optional[int] = None, times: Optional[int] = None, ref: Optional[str] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if to is not None:
            params["to"] = to
        if direction is not None:
            params["direction"] = direction
        if amount is not None:
            params["amount"] = amount
        if times is not None:
            params["times"] = times
        if ref is not None:
            params["ref"] = ref
        return await self.act([{"scroll": params}])

    async def scroll_collect(self, *, max_scrolls: Optional[int] = None, wait_ms: Optional[int] = None, timeout_ms: Optional[int] = None, max_text_length: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if max_scrolls is not None:
            params["max_scrolls"] = max_scrolls
        if wait_ms is not None:
            params["wait_ms"] = wait_ms
        if timeout_ms is not None:
            params["timeout_ms"] = timeout_ms
        if max_text_length is not None:
            params["max_text_length"] = max_text_length
        return await self.act([{"scroll_collect": params}])

    async def screenshot(self, *, full_page: Optional[bool] = None, format: Optional[str] = None, quality: Optional[int] = None, selector: Optional[str] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if full_page is not None:
            params["full_page"] = full_page
        if format is not None:
            params["format"] = format
        if quality is not None:
            params["quality"] = quality
        if selector is not None:
            params["selector"] = selector
        return await self.act([{"screenshot": params}])

    async def wait(self, *, ms: Optional[int] = None, selector: Optional[str] = None, text: Optional[str] = None, timeout: Optional[int] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if ms is not None:
            params["ms"] = ms
        if selector is not None:
            params["selector"] = selector
        if text is not None:
            params["text"] = text
        if timeout is not None:
            params["timeout"] = timeout
        return await self.act([{"wait": params}])

    async def extract(self, **schema: Any) -> SessionEnvelope:
        return await self.act([{"extract": schema}])

    async def fill_form(self, fields: Dict[str, str], *, submit: bool = False) -> SessionEnvelope:
        params: Dict[str, Any] = {"fields": fields}
        if submit:
            params["submit"] = True
        return await self.act([{"fill_form": params}])

    async def upload(self, ref: str, files: List[str]) -> SessionEnvelope:
        return await self.act([{"upload": {"ref": ref, "files": files}}])

    async def pdf(self, *, format: Optional[str] = None, landscape: Optional[bool] = None, print_background: Optional[bool] = None) -> SessionEnvelope:
        params: Dict[str, Any] = {}
        if format is not None:
            params["format"] = format
        if landscape is not None:
            params["landscape"] = landscape
        if print_background is not None:
            params["print_background"] = print_background
        return await self.act([{"pdf": params}])

    async def execute_js(self, expression: str) -> SessionEnvelope:
        return await self.act([{"execute_js": {"expression": expression}}])

    async def close(self) -> SessionEnvelope:
        return await self.act([{"close": {}}])
