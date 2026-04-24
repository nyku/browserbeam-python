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

# Extract with CSS, AI, and JS selectors combined
result = session.extract(
    products=[{
        "_parent": ".product-card",
        "_limit": 3,
        "name": "h2 >> text",                          # CSS selector
        "price": ".price >> text",                     # CSS selector
        "url": "a >> href",                            # CSS attribute
        "rating": "ai >> the star rating out of 5",    # AI selector
        "in_stock": "js >> el.querySelector('.stock')?.textContent.includes('In stock')",  # JS
    }]
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
    user_agent="Mozilla/5.0 ...",  # omit for automatic rotation
    locale="en-US",
    timezone="America/New_York",
    block_resources=["image", "font"],
    auto_dismiss_blockers=True,
    timeout=300,
)
```

### Proxies

All sessions use a datacenter proxy by default (country auto-detected from the URL's TLD). No configuration needed. To customize:

```python
# Use a residential proxy for a specific country
session = client.sessions.create(
    url="https://example.com",
    proxy={"kind": "residential", "country": "us"},
)

# Or bring your own proxy (overrides managed proxy)
session = client.sessions.create(
    url="https://example.com",
    proxy="http://user:pass@proxy:8080",
)
```

## Available Methods

| Method | Description |
|--------|-------------|
| `session.goto(url)` | Navigate to a URL |
| `session.observe()` | Get page state as markdown. Supports `mode="full"` for all sections. |
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

## Page Map & Full Mode

The first `observe` call automatically includes a `page.map` — a lightweight structural outline of the page's landmark regions (header, nav, main, aside, footer) with CSS selectors and descriptive hints. Use it to discover what content is available outside the main area.

```python
res = session.observe()
for entry in res.page.map:
    print(f"{entry.section}: {entry.hint}")
# nav: Home · Docs · Pricing
# main: Getting started with Browserbeam...
# aside: Related posts · Popular tags
```

To re-request the map on subsequent calls:

```python
session.observe(include_page_map=True)
```

When you need content from **all** page sections (sidebars, footer links, nav items), use `mode="full"`. The response markdown is organized by region headers:

```python
full = session.observe(mode="full", max_text_length=20_000)
print(full.page.markdown.content)
# ## [nav]
# Home · Docs · Pricing
# ## [main]
# ...article content...
# ## [aside]
# Related posts · ...
```

Both parameters work identically with `AsyncSession`.

## Session Management

Filter by `status`: `"active"`, `"closed"`, or `"failed"`. Failed sessions ended with a fatal error; `get` returns `error_code` and `error_message`.

```python
sessions = client.sessions.list(status="active")
failed = client.sessions.list(status="failed")

info = client.sessions.get("ses_abc123")
if info.status == "failed":
    print(info.error_code, info.error_message)

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
