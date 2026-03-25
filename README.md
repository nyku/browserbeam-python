# Browserbeam Python SDK

Official Python SDK for the [Browserbeam API](https://browserbeam.com) — browser automation built for AI agents.

## Installation

```bash
pip install browserbeam
```

## Quick Start

```python
from browserbeam import Browserbeam

client = Browserbeam(api_key="sk_live_...")

session = client.sessions.create(url="https://example.com")

# Page state is available immediately
print(session.page.title)
print(session.page.interactive_elements)

# Interact with the page
session.click(ref="e1")

# Extract structured data
result = session.extract(
    title="h1 >> text",
    links=["a >> href"]
)
print(result.extraction)

# Close when done
session.close()
```

## Async Support

```python
from browserbeam import AsyncBrowserbeam

client = AsyncBrowserbeam(api_key="sk_live_...")

session = await client.sessions.create(url="https://example.com")
await session.click(ref="e1")
result = await session.extract(title="h1 >> text")
print(result.extraction)
await session.close()
```

## Configuration

```python
client = Browserbeam(
    api_key="sk_live_...",       # or set BROWSERBEAM_API_KEY env var
    base_url="https://api.browserbeam.com",  # default
    timeout=120.0,               # request timeout in seconds
)
```

## Session Options

```python
session = client.sessions.create(
    url="https://example.com",
    viewport={"width": 1280, "height": 720},
    locale="en-US",
    timezone="America/New_York",
    proxy="http://user:pass@proxy:8080",
    block_resources=["image", "font"],
    auto_dismiss_blockers=True,
    timeout=300,
)
```

## Available Methods

| Method | Description |
|--------|-------------|
| `session.goto(url)` | Navigate to a URL |
| `session.observe()` | Get page state as markdown |
| `session.click(ref=)` | Click an element by ref, text, or label |
| `session.fill(value, ref=)` | Fill an input field |
| `session.type(value, label=)` | Type text character by character |
| `session.select(value, label=)` | Select a dropdown option |
| `session.check(label=)` | Toggle a checkbox |
| `session.scroll(to="bottom")` | Scroll the page |
| `session.scroll_collect()` | Scroll and collect all content |
| `session.screenshot()` | Take a screenshot |
| `session.extract(**schema)` | Extract structured data |
| `session.fill_form(fields, submit=)` | Fill and submit a form |
| `session.wait(ms=)` | Wait for time, selector, or text |
| `session.pdf()` | Generate a PDF |
| `session.execute_js(code)` | Run JavaScript |
| `session.close()` | Close the session |

## Session Management

```python
# List active sessions
sessions = client.sessions.list(status="active")

# Get session info
info = client.sessions.get("ses_abc123")

# Destroy a session
client.sessions.destroy("ses_abc123")
```

## Error Handling

```python
from browserbeam import Browserbeam, RateLimitError, SessionNotFoundError

client = Browserbeam()

try:
    session = client.sessions.create(url="https://example.com")
except RateLimitError as e:
    print(f"Rate limited. Retry after {e.retry_after}s")
except SessionNotFoundError as e:
    print(f"Session not found: {e.message}")
```

## Documentation

Full API documentation at [browserbeam.com/docs](https://browserbeam.com/docs/).

## License

MIT
