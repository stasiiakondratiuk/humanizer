#!/usr/bin/env python3
"""Eval runner for the humanizer skill.

Checks that a humanized output removed the AI/slop markers (`banned`)
while keeping the essential facts (`keep`). Pure stdlib, UTF-8.

Examples:
    python check.py --list
    python check.py --validate
    python check.py --selftest
    python check.py --id ru-03 --text "Делаем сайты и настраиваем рекламу."
    python check.py --id en-02 --output out.txt
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASES_PATH = os.path.join(HERE, "cases.jsonl")


def load_cases():
    cases = []
    with open(CASES_PATH, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                cases.append(json.loads(line))
            except json.JSONDecodeError as e:
                sys.exit(f"cases.jsonl line {i}: invalid JSON: {e}")
    return cases


def check_output(case, output):
    """Return (banned_still_present, facts_missing) — both lists, case-insensitive."""
    out = output.lower()
    still_banned = [b for b in case.get("banned", []) if b.lower() in out]
    missing_keep = [k for k in case.get("keep", []) if k.lower() not in out]
    return still_banned, missing_keep


def cmd_list(cases):
    for c in cases:
        print(f"{c['id']:8} [{c['lang']}] {c.get('tests', '')}")
    print(f"\n{len(cases)} cases")
    return True


def cmd_validate(cases):
    ok = True
    seen = set()
    required = ("id", "lang", "input", "banned", "keep", "reference")
    for c in cases:
        cid = c.get("id", "?")
        for k in required:
            if k not in c:
                print(f"[FAIL] {cid}: missing field '{k}'")
                ok = False
        if cid in seen:
            print(f"[FAIL] duplicate id '{cid}'")
            ok = False
        seen.add(cid)
        for arr in ("banned", "keep"):
            if not isinstance(c.get(arr), list):
                print(f"[FAIL] {cid}: '{arr}' must be a list")
                ok = False
    print("OK - cases.jsonl is well-formed" if ok else "VALIDATION FAILED")
    return ok


def cmd_selftest(cases):
    """Every gold reference must itself pass its own banned/keep checks."""
    passed = 0
    for c in cases:
        sb, mk = check_output(c, c["reference"])
        if sb or mk:
            print(f"[FAIL] {c['id']}: reference has banned {sb} / missing keep {mk}")
        else:
            passed += 1
    print(f"\n{passed}/{len(cases)} gold references are clean")
    return passed == len(cases)


def cmd_check(cases, cid, output):
    case = next((c for c in cases if c["id"] == cid), None)
    if not case:
        sys.exit(f"no case with id '{cid}' (try --list)")
    sb, mk = check_output(case, output)
    print(f"case {cid} [{case['lang']}] - {case.get('tests', '')}")
    if sb:
        print(f"  [FAIL] still contains banned markers: {sb}")
    if mk:
        print(f"  [FAIL] missing required facts: {mk}")
    if not sb and not mk:
        print("  [PASS] no banned markers, all facts kept")
    print(f"  gold reference: {case['reference']}")
    return not sb and not mk


def main():
    # Windows consoles default to cp1252 and choke on Cyrillic / dashes.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description="Humanizer eval runner")
    p.add_argument("--list", action="store_true", help="list all cases")
    p.add_argument("--validate", action="store_true", help="validate cases.jsonl structure")
    p.add_argument("--selftest", action="store_true", help="check that gold references are clean")
    p.add_argument("--id", help="case id to check an output against")
    p.add_argument("--output", help="path to a file with the humanized output")
    p.add_argument("--text", help="humanized output as a string")
    a = p.parse_args()

    cases = load_cases()

    if a.list:
        sys.exit(0 if cmd_list(cases) else 1)
    if a.validate:
        sys.exit(0 if cmd_validate(cases) else 1)
    if a.selftest:
        sys.exit(0 if cmd_selftest(cases) else 1)
    if a.id:
        out = a.text
        if a.output:
            with open(a.output, encoding="utf-8") as f:
                out = f.read()
        if out is None:
            sys.exit("provide --output FILE or --text STRING")
        sys.exit(0 if cmd_check(cases, a.id, out) else 1)

    p.print_help()


if __name__ == "__main__":
    main()
