#!/usr/bin/env python3
"""Regression test for check.py.

Loads check.py as a module, runs it on tests/fixtures/bad-page.html, and compares
the rule counts against tests/expected.json.

    python tests/run_tests.py
"""

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load_checker():
    spec = importlib.util.spec_from_file_location("hui_check", os.path.join(ROOT, "check.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def counts(findings):
    out = {}
    for _, _, rule, _ in findings:
        out[rule] = out.get(rule, 0) + 1
    return out


def main():
    checker = load_checker()
    fixture = os.path.join(HERE, "fixtures", "bad-page.html")
    expected = json.load(open(os.path.join(HERE, "expected.json"), encoding="utf-8"))

    must, warn, _ = checker.check_file(fixture, os.path.dirname(fixture), claims=True)
    must_counts, warn_counts = counts(must), counts(warn)

    failures = []
    for rule, want in expected.get("must", {}).items():
        got = must_counts.get(rule, 0)
        if got != want:
            failures.append("must  %-32s want %d got %d" % (rule, want, got))
    for rule, want in expected.get("warn_min", {}).items():
        got = warn_counts.get(rule, 0)
        if got < want:
            failures.append("warn  %-32s want >=%d got %d" % (rule, want, got))

    # line numbers must survive block stripping: a <style> block before the tell
    # used to shift every reported line (877 was reported as 222 on a long page).
    import tempfile

    html = "<style>\n.a{}\n.b{}\n</style>\n<p>ok</p>\n<p>甲 · 乙</p>\n"
    fd, tmp = tempfile.mkstemp(suffix=".html")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(html)
        lmust, _, _ = checker.check_file(tmp, tmp, "generic")
        want = html.split("\n").index("<p>甲 · 乙</p>") + 1
        got = lmust[0][1] if lmust else None
        if got != want:
            failures.append("line    reported line %s, expected %s "
                            "(block stripping must keep newlines)" % (got, want))
    finally:
        os.unlink(tmp)

    print("fixture:", os.path.relpath(fixture, ROOT))
    print("must counts:", must_counts)
    print("warn counts:", warn_counts)
    if failures:
        print("\nFAIL")
        for f in failures:
            print("  " + f)
        return 1
    print("\nPASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
