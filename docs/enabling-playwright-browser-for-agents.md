# Enabling Playwright Browser for Claude Code Agents

## What This Is

A guide for any Claude Code agent to enable real browser automation via the Playwright MCP plugin. This gives you a full Chromium browser you can control programmatically — navigate pages, click elements, fill forms, take screenshots, and interact with web applications the way a human would.

## Why You Want This

### Without Playwright (Default)

By default, a Claude Code agent has:

- **WebFetch** — retrieves raw HTML/text from a URL (like `curl`). No JavaScript execution, no rendering, no interaction.
- **WebSearch** — returns search engine result summaries.

These tools break down on:
- JavaScript-rendered sites (SPAs, dashboards, data portals)
- Content behind login walls
- Dynamically loaded content (infinite scroll, "load more" buttons)
- Interactive elements (filters, dropdowns, date pickers)
- Sites that block non-browser requests

### With Playwright

You get a real Chromium browser that:
- Executes JavaScript, renders pages fully
- Maintains session state (cookies, auth, navigation history)
- Clicks, types, scrolls, drags, uploads files
- Takes screenshots and accessibility snapshots
- Handles dialogs, multiple tabs, network request monitoring

This unlocks: end-to-end testing of web apps, deep research on JS-heavy sites, multi-step authenticated workflows, visual verification of UI changes.

---

## How To Enable It

### Step 1: Understand the Architecture

Claude Code uses **MCP (Model Context Protocol) plugins** to extend its capabilities. Playwright is one such plugin. The plugin system works like this:

```
Claude Code Agent
    |
    +--> MCP Plugin System
            |
            +--> Playwright MCP Server (runs as a subprocess)
                    |
                    +--> Chromium Browser (headless)
```

The plugin is configured via `.mcp.json` files. There are two relevant locations:

1. **Source config** (plugin marketplace): `/root/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/playwright/.mcp.json`
2. **Cache config** (active runtime): `/root/.claude/plugins/cache/claude-plugins-official/playwright/<hash>/.mcp.json`

Both must match for the plugin to work correctly.

### Step 2: Install Playwright and Chromium

```bash
# Install the Playwright MCP package
npm install -g @playwright/mcp

# Install Playwright's bundled Chromium
npx playwright install chromium
```

**Why bundled Chromium?** See the "Critical Gotcha" section below.

### Step 3: Configure the MCP Plugin

Both `.mcp.json` files (source and cache) must contain:

```json
{
  "playwright": {
    "command": "npx",
    "args": ["@playwright/mcp@latest", "--browser", "chromium"]
  }
}
```

The key flag is `--browser chromium` — this tells the MCP server to use Playwright's bundled Chromium instead of system Chrome.

### Step 4: Restart Your Session

The MCP plugin system reads config at session start. After changing `.mcp.json`, you must restart the Claude Code session for the plugin to load.

### Step 5: Verify It Works

After restart, Playwright tools will appear in your available tools list with the prefix `mcp__plugin_playwright_playwright__browser_*`. Test by navigating to a simple page:

```
Tool: mcp__plugin_playwright_playwright__browser_navigate
URL: https://example.com
```

Then take a snapshot to confirm content loaded:

```
Tool: mcp__plugin_playwright_playwright__browser_snapshot
```

If you see the page content in the snapshot, the browser is working.

---

## Critical Gotcha: System Chrome vs Bundled Chromium

This is the problem we hit and the most important thing in this document.

### The Problem

In sandboxed environments (containers, cloud workstations, restricted VMs), the system-installed Chrome (`/opt/google/chrome/chrome` or similar) will crash on launch. The root cause:

- Chrome uses **AF_UNIX sockets** internally for its singleton lock mechanism (`process_singleton_posix.cc`)
- Sandboxed environments often **block AF_UNIX socket creation**
- Chrome crashes immediately with no useful error message

You'll see errors like:
- `Failed to launch browser`
- Chrome process exits with no output
- Socket-related errors in Chrome's internal logs

### The Fix

Use `--browser chromium` in the MCP config. This tells the Playwright MCP server to use **Playwright's bundled Chromium** instead of system Chrome. The bundled Chromium:

- Is downloaded by `npx playwright install chromium`
- Stored in Playwright's cache directory (typically `~/.cache/ms-playwright/`)
- Does not use the singleton lock mechanism that requires AF_UNIX sockets
- Launches with `chromiumSandbox: false` in headless mode, avoiding the conflict

### What Does NOT Work

- `--launch-options` flag — does not exist in `@playwright/mcp`, despite what documentation or other agents may suggest
- System Chrome with `--no-sandbox` — still crashes due to the socket issue
- Setting `CHROME_FLAGS` environment variables — MCP server doesn't read them

---

## Available Tools Once Enabled

After enabling, you get these tools (all prefixed with `mcp__plugin_playwright_playwright__`):

| Tool | Purpose |
|------|---------|
| `browser_navigate` | Go to a URL |
| `browser_snapshot` | Get accessibility tree of current page (preferred over screenshots for reading content) |
| `browser_take_screenshot` | Capture visual screenshot |
| `browser_click` | Click an element by ref ID |
| `browser_fill_form` | Fill in form fields |
| `browser_type` | Type text character by character |
| `browser_press_key` | Press keyboard keys (Enter, Tab, etc.) |
| `browser_hover` | Hover over an element |
| `browser_drag` | Drag and drop |
| `browser_select_option` | Select from dropdown menus |
| `browser_file_upload` | Upload files to file inputs |
| `browser_handle_dialog` | Accept/dismiss browser dialogs |
| `browser_evaluate` | Run arbitrary JavaScript in the page |
| `browser_run_code` | Run Playwright code directly |
| `browser_console_messages` | Read browser console output |
| `browser_network_requests` | Monitor network traffic |
| `browser_tabs` | Manage browser tabs |
| `browser_navigate_back` | Go back in history |
| `browser_wait_for` | Wait for elements or conditions |
| `browser_resize` | Change viewport size |
| `browser_close` | Close the browser |
| `browser_install` | Install browsers |

### Important: Tool Loading

These are **deferred tools**. Before you can call any of them, you must first load them using `ToolSearch`:

```
ToolSearch query: "select:mcp__plugin_playwright_playwright__browser_navigate"
```

Only after loading can you call the tool directly.

---

## Usage Patterns

### Basic Page Reading
```
1. browser_navigate -> URL
2. browser_snapshot -> read the accessibility tree
```

### Interacting with a Page
```
1. browser_navigate -> URL
2. browser_snapshot -> find element ref IDs
3. browser_click -> ref=e5 (click a button)
4. browser_snapshot -> verify result
```

### Form Submission
```
1. browser_navigate -> URL
2. browser_snapshot -> find form fields
3. browser_click -> ref=e10 (focus input)
4. browser_fill_form -> ref=e10, value="text"
5. browser_click -> ref=e15 (submit button)
6. browser_snapshot -> verify submission result
```

### End-to-End Testing
```
1. browser_navigate -> your app's URL
2. browser_snapshot -> verify page loaded
3. Interact with elements (click, type, fill)
4. browser_snapshot -> verify expected state changes
5. browser_console_messages -> check for JS errors
6. browser_network_requests -> verify API calls
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Tools not appearing | Plugin not loaded | Check `.mcp.json` config, restart session |
| Browser crash on navigate | System Chrome being used | Ensure `--browser chromium` in config |
| `npx playwright install chromium` fails | Network restriction | Check internet access, proxy settings |
| Snapshot returns empty | Page hasn't loaded yet | Add `browser_wait_for` before snapshot |
| "Target closed" errors | Browser crashed mid-session | Navigate again to restart the browser |
| Config changes not taking effect | Stale cache | Update BOTH source and cache `.mcp.json` |

---

## File Locations Reference

| File | Path |
|------|------|
| Source plugin config | `/root/.claude/plugins/marketplaces/claude-plugins-official/external_plugins/playwright/.mcp.json` |
| Cache plugin config | `/root/.claude/plugins/cache/claude-plugins-official/playwright/<hash>/.mcp.json` |
| Bundled Chromium | `~/.cache/ms-playwright/chromium-*/chrome-linux/chrome` |
| MCP plugin logs | Check session console output |

---

## Summary

1. Install: `npx playwright install chromium`
2. Configure: Set `--browser chromium` in both `.mcp.json` files
3. Restart: Session must be restarted for config to load
4. Verify: Navigate to a test URL, take a snapshot
5. Use: Load tools via `ToolSearch` before calling them

The critical lesson: **always use Playwright's bundled Chromium, not system Chrome**, especially in sandboxed environments. The singleton lock socket issue is the most common failure mode and has no workaround other than using the bundled browser.
