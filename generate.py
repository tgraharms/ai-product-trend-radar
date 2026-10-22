"""Write today's daily brief with the Claude API and save it to briefs/.

Usage: ANTHROPIC_API_KEY=... python generate.py
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import anthropic

MODEL = os.environ.get("BRIEF_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = 16000
MAX_SEARCHES_PER_REQUEST = 20
MAX_CONTINUATIONS = 8
TZ = ZoneInfo("Asia/Kuala_Lumpur")

ROOT = Path(__file__).resolve().parent
BRIEFS = ROOT / "briefs"

# USD per million tokens (input, output), used only for the cost line in the run log.
PRICES = {
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
    "claude-haiku-5-5": (0.10, 0.50),
}
SEARCH_PRICE = 0.01  # $10 per 1,000 searches

REQUIRED_SECTIONS = ("## AI", "## TECH", "## CAREER")
MIN_ITEMS = 5


def fail(reason):
    """Stop the run. On GitHub Actions the reason also shows on the run page as an error."""
    if os.environ.get("GITHUB_ACTIONS"):
        one_line = reason.replace("%", "%25").replace("\r", " ").replace("\n", " ")
        print(f"::error title=Daily brief failed::{one_line}", flush=True)
    sys.exit(reason)


def build_prompt(today):
    template = (ROOT / "prompt.md").read_text(encoding="utf-8")
    return template.replace("{TODAY_LONG}", today.strftime("%A, %d %B %Y")).replace(
        "{TODAY_ISO}", today.isoformat()
    )


def ask_claude(prompt):
    """Run one research turn, resuming whenever the API pauses a long search loop."""
    client = anthropic.Anthropic(max_retries=4, timeout=900)
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": MAX_SEARCHES_PER_REQUEST}]
    messages = [{"role": "user", "content": prompt}]
    usage = {"input": 0, "output": 0, "searches": 0}
    texts = []

    for _ in range(MAX_CONTINUATIONS):
        response = client.messages.create(
            model=MODEL, max_tokens=MAX_TOKENS, messages=messages, tools=tools
        )
        u = response.usage
        usage["input"] += (u.input_tokens or 0) + (getattr(u, "cache_read_input_tokens", 0) or 0)
        usage["output"] += u.output_tokens or 0
        server = getattr(u, "server_tool_use", None)
        usage["searches"] += (getattr(server, "web_search_requests", 0) or 0) if server else 0

        texts.append("".join(block.text for block in response.content if block.type == "text"))

        if response.stop_reason != "pause_turn":
            break
        messages.append({"role": "assistant", "content": response.content})
    else:
        fail(f"Stopped after {MAX_CONTINUATIONS} paused turns without a finished brief.")

    if response.stop_reason == "max_tokens":
        fail("The brief was cut off at max_tokens.")
    return "".join(texts), usage


def extract_brief(text):
    start = text.rfind("# Daily Brief")
    return text[start:].strip() if start != -1 else None


def check_brief(brief):
    problems = []
    for header in REQUIRED_SECTIONS:
        if not re.search(rf"^{re.escape(header)}\s*$", brief, re.MULTILINE):
            problems.append(f"missing '{header}'")
    items = re.findall(r"^\[\d+\]\s*\S", brief, re.MULTILINE)
    if len(items) < MIN_ITEMS:
        problems.append(f"only {len(items)} items")
    return problems, len(items)


def save(brief, today):
    BRIEFS.mkdir(exist_ok=True)
    path = BRIEFS / f"{today.isoformat()}.md"
    path.write_text(brief + "\n", encoding="utf-8")
    write_index()
    return path


def write_index():
    """briefs/index.json lists every brief date, newest first. The page reads it to build the archive."""
    dates = sorted((p.stem for p in BRIEFS.glob("????-??-??.md")), reverse=True)
    (BRIEFS / "index.json").write_text(json.dumps({"briefs": dates}, indent=1) + "\n", encoding="utf-8")


def report(line):
    print(line)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write(line + "\n")


def main():
    if "--index-only" in sys.argv:
        write_index()
        return

    if not os.environ.get("ANTHROPIC_API_KEY"):
        fail("ANTHROPIC_API_KEY is empty. Add it under Settings > Secrets and variables > Actions > Repository secrets.")

    today = datetime.now(TZ).date()
    try:
        text, usage = ask_claude(build_prompt(today))
    except anthropic.APIStatusError as e:
        fail(f"Claude API returned {e.status_code}: {e.message}")
    except anthropic.APIError as e:
        fail(f"Claude API error: {e}")

    brief = extract_brief(text)
    if not brief:
        print(text[-3000:])
        fail("No brief found in Claude's reply.")

    problems, item_count = check_brief(brief)
    if problems:
        print(brief)
        fail("Brief failed checks: " + "; ".join(problems))

    path = save(brief, today)
    in_price, out_price = PRICES.get(MODEL, (0.0, 0.0))
    cost = usage["input"] / 1e6 * in_price + usage["output"] / 1e6 * out_price + usage["searches"] * SEARCH_PRICE
    report(
        f"Saved {path.relative_to(ROOT)}: {item_count} items, {usage['searches']} searches, "
        f"{usage['input']:,} input / {usage['output']:,} output tokens, about ${cost:.2f} on {MODEL}."
    )


if __name__ == "__main__":
    main()
