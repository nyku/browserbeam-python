# Changelog

All notable changes to the `browserbeam` Python SDK will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.0] - 2026-04-24

### Added

- `SessionInfo` includes optional `error_code` and `error_message` when a session ended in a **failed** state.
- `SessionListItem` includes optional `error_code` when present in the API response.
- Session `status` from the API can be `"failed"`; use `sessions.list(status="failed")` to list failed sessions.

### Changed

- `sessions.list` parsing uses safe field mapping so unknown API fields do not break list items.

## [0.4.0] - 2026-04-14

### Added

- Managed proxy support: `proxy` parameter now accepts a dict `{"kind": "datacenter"|"residential", "country": "us"|"auto"}` in addition to a BYO proxy URL string.
- AI-powered selectors: use `"ai >> description"` syntax in `extract` schemas to target elements by natural-language description.

### Changed

- All sessions now route through a datacenter proxy by default (country auto-detected from URL TLD). No configuration needed.
- Updated README with managed proxy examples, `user_agent` option, and AI selector examples.

## [0.3.0] - 2026-03-30

### Added

- `observe`: `mode` parameter — `"main"` (default) or `"full"`. Full mode returns markdown from all page sections (nav, aside, footer, etc.) organized by region headers.
- `observe`: `include_page_map` parameter — boolean to re-request the structural section map after the first auto-included observe.
- `MapEntry` dataclass: `section`, `selector`, `hint` describing each page landmark.
- `PageState.map`: optional list of `MapEntry` — the structural outline of page sections, auto-included on first observe.
- Both `Session` and `AsyncSession` updated with the new parameters.

## [0.2.0] - 2026-03-25

### Added

- `goto`: `wait_until` parameter for JavaScript-based wait conditions
- `fill`, `type`, `select`, `check`: `text` parameter for element targeting by visible text
- `scroll`: `text` and `label` parameters for element targeting
- `wait`: `until_js` parameter for JavaScript-based wait conditions (maps to API `until`)
- `upload`: `text` and `label` parameters for element targeting (signature changed from positional `ref` to keyword arguments)
- `execute_js`: `result_key` and `timeout` parameters
- `pdf`: `scale` and `margin` parameters

### Changed

- `upload` method signature changed from `upload(ref, files)` to `upload(files, *, ref=None, text=None, label=None)` — **breaking change**
- `execute_js` parameter renamed from `expression` to `code` — **breaking change**

## [0.1.0] - 2026-03-24

### Added

- Initial release
- Sync client (`Browserbeam`) and async client (`AsyncBrowserbeam`)
- Session management: `create`, `list`, `get`, `destroy`
- Navigation: `goto` with `wait_for` and `wait_timeout`
- Page observation: `observe` with `scope`, `format`, `include_links`, `max_text_length`
- Interactions: `click`, `fill`, `fill_form`
- Data extraction: `extract` with schema-based selectors
- Media: `screenshot`, `pdf`
- Scrolling: `scroll`, `scroll_collect`
- Waiting: `wait` with `ms`, `selector`, `text`, `timeout`
- Session lifecycle: `close`
- Typed errors: `BrowserbeamError`, `AuthenticationError`, `RateLimitError`, `NotFoundError`, `ValidationError`, `ServerError`

[0.4.0]: https://github.com/nyku/browserbeam-python/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/nyku/browserbeam-python/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/nyku/browserbeam-python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/nyku/browserbeam-python/releases/tag/v0.1.0
