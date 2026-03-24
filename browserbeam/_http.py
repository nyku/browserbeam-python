from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from browserbeam.errors import _raise_for_status

DEFAULT_BASE_URL = "https://api.browserbeam.com"
DEFAULT_TIMEOUT = 120.0


class SyncHTTP:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.Client(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "browserbeam-python/0.1.0",
            },
            timeout=timeout,
        )

    def close(self) -> None:
        self._client.close()

    def request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        response = self._client.request(method, path, **kwargs)
        if response.status_code == 204:
            return {}
        body = response.json()
        if response.status_code >= 400:
            headers = {k.lower(): v for k, v in response.headers.items()}
            _raise_for_status(response.status_code, body, headers)
        return body

    def post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("POST", path, json=json or {})

    def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self.request("GET", path, params=params)

    def delete(self, path: str) -> Dict[str, Any]:
        return self.request("DELETE", path)


class AsyncHTTP:
    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "browserbeam-python/0.1.0",
            },
            timeout=timeout,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        response = await self._client.request(method, path, **kwargs)
        if response.status_code == 204:
            return {}
        body = response.json()
        if response.status_code >= 400:
            headers = {k.lower(): v for k, v in response.headers.items()}
            _raise_for_status(response.status_code, body, headers)
        return body

    async def post(self, path: str, *, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.request("POST", path, json=json or {})

    async def get(self, path: str, *, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return await self.request("GET", path, params=params)

    async def delete(self, path: str) -> Dict[str, Any]:
        return await self.request("DELETE", path)
