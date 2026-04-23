#!/usr/bin/env python3
"""Check all hyperlinks in docs/ markdown files for broken URLs."""

import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
URL_PATTERN = re.compile(r'https?://[^\s)>\]"]+')
TIMEOUT = 15
REPORT_PATH = os.environ.get("LINK_CHECK_REPORT")


def extract_urls(filepath):
    """Extract all HTTP(S) URLs from a markdown file."""
    text = filepath.read_text(encoding="utf-8")
    return [(url.rstrip(".,;:"), filepath) for url in URL_PATTERN.findall(text)]


def check_url(url):
    """Check a single URL, trying HEAD then falling back to GET."""
    headers = {"User-Agent": "ado2gh-link-checker/1.0"}
    for method in ("HEAD", None):
        try:
            req = urllib.request.Request(url, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                return (url, resp.status, None)
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code == 405:
                continue
            return (url, e.code, str(e.reason))
        except Exception as e:
            return (url, None, str(e))
    return (url, None, "All request methods failed")


def main():
    md_files = list(DOCS_DIR.glob("**/*.md"))
    if not md_files:
        print("No markdown files found in docs/.")
        return 0

    url_sources = {}
    for f in md_files:
        for url, source in extract_urls(f):
            url_sources.setdefault(url, []).append(source)

    if not url_sources:
        print("No URLs found.")
        return 0

    print(f"Checking {len(url_sources)} unique URL(s) from {len(md_files)} file(s)...\n")

    failures = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(check_url, url): url for url in url_sources}
        for future in as_completed(futures):
            url, status, error = future.result()
            if status and 200 <= status < 400:
                print(f"  ✓ {status} {url}")
            else:
                sources = [str(s.relative_to(DOCS_DIR.parent)) for s in url_sources[url]]
                failures.append((url, status, error, sources))
                print(f"  ✗ {status or 'ERR'} {url} — {error}")

    if failures:
        print(f"\n{'=' * 60}")
        print(f"FAILED: {len(failures)} broken link(s)\n")
        for url, status, error, sources in failures:
            print(f"  {url}")
            print(f"    Status: {status or 'N/A'} — {error}")
            print(f"    Found in: {', '.join(sources)}\n")

        if REPORT_PATH:
            write_report(failures)

        return 1

    print(f"\nAll {len(url_sources)} link(s) OK.")
    return 0


def write_report(failures):
    """Write a markdown-formatted report of broken links."""
    lines = [
        f"The weekly link check found **{len(failures)} broken link(s)**.\n",
        "| URL | Status | Found in |",
        "|-----|--------|----------|",
    ]
    for url, status, error, sources in failures:
        status_text = str(status) if status else "ERR"
        sources_text = ", ".join(f"`{s}`" for s in sources)
        lines.append(f"| {url} | {status_text} | {sources_text} |")

    Path(REPORT_PATH).write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
