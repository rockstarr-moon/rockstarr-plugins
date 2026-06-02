#!/usr/bin/env python3
"""Extract JSON-LD schema from cached HTML.

Usage:
    python3 extract_schema.py /tmp/audit-example                 # list @types per page
    python3 extract_schema.py /tmp/audit-example --full          # full JSON dump
    python3 extract_schema.py /tmp/audit-example --type RealEstateAgent  # show specific type

Helps catalogue what schema exists across the site and surface anomalies
(missing LocalBusiness, stray Person name, broken FAQ markup, etc.).
"""

import argparse
import json
import os
import re
import sys


def extract_blobs(html):
    return re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.IGNORECASE | re.DOTALL,
    )


def parse_blob(blob):
    try:
        data = json.loads(blob.strip())
        graph = data.get("@graph", [data]) if isinstance(data, dict) else data
        return graph if isinstance(graph, list) else [graph]
    except Exception:
        return []


def main():
    p = argparse.ArgumentParser()
    p.add_argument("dir", help="Directory of cached HTML files")
    p.add_argument("--full", action="store_true", help="Dump full JSON for every block")
    p.add_argument("--type", help="Show only blocks matching this @type (e.g. RealEstateAgent)")
    args = p.parse_args()

    files = sorted(f for f in os.listdir(args.dir) if f.endswith(".html"))
    for f in files:
        path = os.path.join(args.dir, f)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        blobs = extract_blobs(html)
        types = []
        for b in blobs:
            for d in parse_blob(b):
                if not isinstance(d, dict):
                    continue
                t = d.get("@type")
                tlabel = t if isinstance(t, str) else (",".join(t) if t else "?")
                types.append(tlabel)
                if args.type:
                    # Match if requested type is anywhere in the @type
                    if isinstance(t, str) and t == args.type:
                        print(f"\n=== {f}: {tlabel} ===")
                        print(json.dumps(d, indent=2))
                    elif isinstance(t, list) and args.type in t:
                        print(f"\n=== {f}: {tlabel} ===")
                        print(json.dumps(d, indent=2))
        if args.type:
            continue
        if args.full:
            print(f"\n=== {f} ===")
            for b in blobs:
                for d in parse_blob(b):
                    print(json.dumps(d, indent=2))
        else:
            print(f"{f}: {sorted(set(types))}")


if __name__ == "__main__":
    sys.exit(main() or 0)
