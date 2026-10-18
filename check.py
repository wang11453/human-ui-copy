#!/usr/bin/env python3
"""human-ui-copy checker.

Checks only the mechanical items from SKILL.md, and respects the skill's own
whitelist through page profiles. Everything that needs a human is reported as
WARN and never fails the run.

Usage:
    python check.py <file-or-dir> [--profile generic|game|tool|marketing] [--json]

Profiles
    generic    default. Prose separators and numeric claims are MUST/WARN as usual.
    game       odds tables and prize numbers are house style: separators become
               WARN, numeric claims are skipped.
    tool       a task page: separators are MUST, numeric claims WARN.
    marketing  structure rules do not apply; separators WARN, claims WARN.

Ignoring a line
    Put `hui-check: ignore` in a comment on that line (HTML/JS/CSS comments all work).

Exit codes: 0 = no MUST failures, 1 = at least one MUST failure, 2 = usage error.
Stdlib only. Works on Windows, macOS and Linux.
"""

import argparse
import json
import os
import re
import sys

SKIP_DIRS = {
    ".git", "node_modules", "dist", "build", ".next", ".nuxt", "coverage",
    "vendor", "__pycache__", ".venv", "venv", "target",
    # fixtures and demo pages are deliberately full of tells; scan them explicitly
    "tests", "examples",
}
WEB_EXT = {".html", ".htm", ".js", ".mjs", ".cjs", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".css", ".md"}

RE_CONSOLE = re.compile(r"console\.(log|debug|info|warn)\s*\(")
RE_DEBUGGER = re.compile(r"^\s*debugger\s*;?\s*$", re.M)
RE_MIDDOT = re.compile(r"[^\s·]\s*·\s*[^\s·]")
RE_ABS_PATH = re.compile(r"([A-Za-z]:\\[^\s\"'<>)]+|/Users/[^\s\"'<>)]+|/home/[^\s\"'<>)]+)")
# claim-shaped only: a "+", a k/M/万/亿 unit, or a high percentage.
# Plain counts ("6 个工具") are content, not claims — flagging them is a false positive.
# Off unless --claims is passed: content that states real numbers (member counts, prices)
# has no "source" to cite, so the check is only useful when explicitly asked for.
RE_CLAIM_NUM = re.compile(
    r"\b\d[\d,.]*\s*(?:k|K|M|万|亿)\b"
    r"|\b\d[\d,.]*\s*\+"
    r"|\b(?:9\d(?:\.\d+)?|100)\s*%"
)
RE_SOURCE = re.compile(r"(href=|cite=|<a\s|data-source|来源|source:|\[\d+\])", re.I)
RE_IGNORE = re.compile(r"hui-check:\s*ignore", re.I)

STATE_WORDS = ("empty", "loading", "error", "skeleton", "空态", "加载", "错误", "正在启动", "初始化")

BLOCK_RE = re.compile(r"<(script|style|textarea|pre|code)\b[^>]*>.*?</(script|style|textarea|pre|code)>", re.S | re.I)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
QUOTED_RE = re.compile(r"「[^」\n]*」|“[^”\n]*”")
STYLE_ATTR_RE = re.compile(r"style\s*=\s*(?:\"[^\"]*\"|'[^']*')", re.I)
TAG_RE = re.compile(r"<[^>]*>", re.S)
MINIFIED_LINE = 400  # lines longer than this are almost always bundled code

# severity per profile: "must" | "warn" | "off"
PROFILES = {
    "generic":   {"console": "must", "debugger": "must", "middot": "must", "path": "must", "claims": "warn"},
    "game":      {"console": "must", "debugger": "must", "middot": "warn", "path": "must", "claims": "off"},
    "tool":      {"console": "must", "debugger": "must", "middot": "must", "path": "must", "claims": "warn"},
    "marketing": {"console": "must", "debugger": "must", "middot": "warn", "path": "must", "claims": "warn"},
}


def strip_code(html):
    """Blank out blocks and spans that legitimately contain literal tells."""
    out = BLOCK_RE.sub(lambda m: " " * len(m.group(0)), html)
    out = INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), out)
    out = QUOTED_RE.sub(lambda m: " " * len(m.group(0)), out)
    out = STYLE_ATTR_RE.sub(lambda m: " " * len(m.group(0)), out)
    # visible text only: attribute values (SVG filter x="-50%", style, class) are not prose
    out = TAG_RE.sub(lambda m: " " * len(m.group(0)), out)
    return out


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def iter_files(root):
    if os.path.isfile(root):
        if os.path.splitext(root)[1].lower() in WEB_EXT:
            yield root
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            low = name.lower()
            if low.endswith((".min.js", ".min.css")):
                continue
            if os.path.splitext(name)[1].lower() in WEB_EXT:
                yield os.path.join(dirpath, name)


def ignored(lines, lineno):
    if not (0 < lineno <= len(lines)):
        return False
    if RE_IGNORE.search(lines[lineno - 1]):
        return True
    # bundled/minified code lives on enormous single lines; never a page's own tell
    return len(lines[lineno - 1]) > MINIFIED_LINE


def check_file(path, root, profile="generic", claims=False):
    with open(path, encoding="utf-8", errors="replace") as fh:
        raw = fh.read()
    text = strip_code(raw)
    lines = raw.split("\n")
    rel = os.path.relpath(path, root) if os.path.isdir(root) else os.path.basename(path)
    sev = PROFILES[profile]

    must, warn = [], []

    def add(rule, level, lineno, evidence):
        if ignored(lines, lineno):
            return
        if level == "must":
            must.append((rel, lineno, rule, evidence))
        elif level == "warn":
            warn.append((rel, lineno, rule, evidence))

    for m in RE_CONSOLE.finditer(raw):
        add("console residue", sev["console"], line_of(raw, m.start()), m.group(0))
    for m in RE_DEBUGGER.finditer(raw):
        add("debugger statement", sev["debugger"], line_of(raw, m.start()), m.group(0).strip())

    for m in RE_MIDDOT.finditer(text):
        snippet = text[max(0, m.start() - 24):m.end() + 24].replace("\n", " ").strip()
        add("middot separator in prose", sev["middot"], line_of(text, m.start()), snippet)

    for m in RE_ABS_PATH.finditer(raw):
        add("absolute path", sev["path"], line_of(raw, m.start()), m.group(0))

    if claims:
        for m in RE_CLAIM_NUM.finditer(text):
            around = text[max(0, m.start() - 200):m.end() + 200]
            if not RE_SOURCE.search(around):
                add("number without a visible source", sev["claims"], line_of(text, m.start()), m.group(0).strip())

    lowered = text.lower()

    # Documentation quotes the tells it bans. In .md files every finding is a note.
    if path.lower().endswith(".md"):
        warn = must + warn
        must = []

    return must, warn, lowered


def main():
    ap = argparse.ArgumentParser(description="human-ui-copy checker (mechanical items only)")
    ap.add_argument("target", help="file or directory to scan")
    ap.add_argument("--profile", choices=sorted(PROFILES), default="generic",
                    help="page type; controls whitelist-aware severity")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    ap.add_argument("--claims", action="store_true",
                    help="also flag claim-shaped numbers with no visible source (noisy: off by default)")
    args = ap.parse_args()

    if not os.path.exists(args.target):
        print("target not found: %s" % args.target, file=sys.stderr)
        return 2

    files = list(iter_files(args.target))
    all_must, all_warn = [], []

    for path in files:
        must, warn, _ = check_file(path, args.target, args.profile, claims=args.claims)
        all_must.extend(must)
        all_warn.extend(warn)

    if args.json:
        print(json.dumps({
            "target": args.target,
            "profile": args.profile,
            "files": len(files),
            "must": [{"file": f, "line": l, "rule": r, "evidence": e} for f, l, r, e in all_must],
            "warn": [{"file": f, "line": l, "rule": r, "evidence": e} for f, l, r, e in all_warn],
            "ok": not all_must,
        }, ensure_ascii=False, indent=2))
    else:
        if not args.quiet:
            for f, l, r, e in all_must:
                print("MUST  %s:%s  %s  |  %s" % (f, l, r, e[:90]))
            for f, l, r, e in all_warn:
                print("WARN  %s:%s  %s  |  %s" % (f, l, r, e[:90]))
        print("\nprofile %s · filed %d  must %d  warn %d" % (args.profile, len(files), len(all_must), len(all_warn)))

    return 0 if not all_must else 1


if __name__ == "__main__":
    sys.exit(main())
