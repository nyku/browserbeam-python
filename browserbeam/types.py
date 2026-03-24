from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MarkdownContent:
    content: str = ""
    length: Optional[Dict[str, int]] = None


def _safe_init(cls, data: Dict[str, Any]):
    """Create a dataclass instance, ignoring any unknown fields."""
    import dataclasses
    known = {f.name for f in dataclasses.fields(cls)}
    return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class InteractiveElement:
    ref: str = ""
    tag: str = ""
    role: str = ""
    label: str = ""
    value: Optional[str] = None


@dataclass
class Changes:
    content_changed: bool = False
    content_delta: Optional[str] = None
    elements_added: List[Dict[str, Any]] = field(default_factory=list)
    elements_removed: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class ScrollState:
    y: int = 0
    height: int = 0
    viewport: int = 0
    percent: int = 0


@dataclass
class PageState:
    url: str = ""
    title: str = ""
    stable: bool = False
    markdown: Optional[MarkdownContent] = None
    interactive_elements: List[InteractiveElement] = field(default_factory=list)
    forms: List[Dict[str, Any]] = field(default_factory=list)
    changes: Optional[Changes] = None
    scroll: Optional[ScrollState] = None


@dataclass
class MediaItem:
    type: str = ""
    format: str = ""
    data: str = ""


@dataclass
class StepError:
    step: int = 0
    action: str = ""
    code: str = ""
    message: str = ""
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SessionEnvelope:
    session_id: str = ""
    expires_at: str = ""
    request_id: str = ""
    completed: int = 0
    page: Optional[PageState] = None
    media: List[MediaItem] = field(default_factory=list)
    extraction: Optional[Dict[str, Any]] = None
    blockers_dismissed: List[str] = field(default_factory=list)
    error: Optional[StepError] = None


@dataclass
class SessionInfo:
    session_id: str = ""
    status: str = ""
    started_at: str = ""
    ended_at: Optional[str] = None
    duration_seconds: Optional[int] = None
    expires_at: str = ""


@dataclass
class SessionListItem:
    session_id: str = ""
    status: str = ""
    started_at: str = ""


@dataclass
class SessionList:
    sessions: List[SessionListItem] = field(default_factory=list)
    has_more: bool = False
    next_cursor: Optional[str] = None


def _parse_page_state(data: Optional[Dict[str, Any]]) -> Optional[PageState]:
    if data is None:
        return None
    md_raw = data.get("markdown")
    markdown = _safe_init(MarkdownContent, md_raw) if isinstance(md_raw, dict) else None
    elements = [
        _safe_init(InteractiveElement, el) for el in (data.get("interactive_elements") or [])
    ]
    changes_raw = data.get("changes")
    changes = _safe_init(Changes, changes_raw) if isinstance(changes_raw, dict) else None
    scroll_raw = data.get("scroll")
    scroll = _safe_init(ScrollState, scroll_raw) if isinstance(scroll_raw, dict) else None
    return PageState(
        url=data.get("url", ""),
        title=data.get("title", ""),
        stable=data.get("stable", False),
        markdown=markdown,
        interactive_elements=elements,
        forms=data.get("forms") or [],
        changes=changes,
        scroll=scroll,
    )


def _parse_session_envelope(data: Dict[str, Any]) -> SessionEnvelope:
    page = _parse_page_state(data.get("page"))
    media = [_safe_init(MediaItem, m) for m in (data.get("media") or [])]
    error_raw = data.get("error")
    step_error = _safe_init(StepError, error_raw) if isinstance(error_raw, dict) else None
    return SessionEnvelope(
        session_id=data.get("session_id", ""),
        expires_at=data.get("expires_at", ""),
        request_id=data.get("request_id", ""),
        completed=data.get("completed", 0),
        page=page,
        media=media,
        extraction=data.get("extraction"),
        blockers_dismissed=data.get("blockers_dismissed") or [],
        error=step_error,
    )


def _parse_session_info(data: Dict[str, Any]) -> SessionInfo:
    return SessionInfo(
        session_id=data.get("session_id", ""),
        status=data.get("status", ""),
        started_at=data.get("started_at", ""),
        ended_at=data.get("ended_at"),
        duration_seconds=data.get("duration_seconds"),
        expires_at=data.get("expires_at", ""),
    )


def _parse_session_list(data: Dict[str, Any]) -> SessionList:
    items = [SessionListItem(**s) for s in (data.get("sessions") or [])]
    return SessionList(
        sessions=items,
        has_more=data.get("has_more", False),
        next_cursor=data.get("next_cursor"),
    )
