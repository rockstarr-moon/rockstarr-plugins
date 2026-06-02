#!/usr/bin/env python3
"""Extract on-page SEO signals from a folder of cached HTML files.

Usage:
    python3 extract_on_page.py /tmp/audit-example
    python3 extract_on_page.py /tmp/audit-example --json   # machine-readable

For each .html file in the directory, prints title, meta description, canonical,
robots meta, H1 list, H2 list, image alt counts, internal/external link counts,
and JSON-LD schema types. Use this to find outliers — pages with missing/long
titles, weird H2 hierarchies, bad alt patterns, missing schema.
"""

import argparse
import json
import os
import re
import sys


def extract(html, host=None):
    title = re.search(r"<title[^>]*>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    title = title.group(1).strip() if title else ""
    desc = re.search(
        r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    desc = desc.group(1).strip() if desc else ""
    canonical = re.search(
        r'<link\s+rel=["\']canonical["\']\s+href=["\'](.*?)["\']', html, re.IGNORECASE
    )
    canonical = canonical.group(1).strip() if canonical else ""
    robots = re.search(
        r'<meta\s+name=["\']robots["\']\s+content=["\'](.*?)["\']', html, re.IGNORECASE
    )
    robots = robots.group(1).strip() if robots else ""

    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", html, re.IGNORECASE | re.DOTALL)
    h2s = re.findall(r"<h2[^>]*>(.*?)</h2>", html, re.IGNORECASE | re.DOTALL)
    h1s = [re.sub(r"<[^>]+>", "", h).strip() for h in h1s]
    h2s = [re.sub(r"<[^>]+>", "", h).strip() for h in h2s]

    imgs = re.findall(r"<img\s[^>]*>", html, re.IGNORECASE)
    n_img = len(imgs)
    n_empty_alt = sum(1 for i in imgs if re.search(r'alt=["\']\s*["\']', i, re.IGNORECASE))
    n_no_alt = sum(1 for i in imgs if not re.search(r"alt=", i, re.IGNORECASE))

    # Link classification
    links = re.findall(r'<a\s[^>]*href=["\']([^"\']+)["\']', html, re.IGNORECASE)
    n_internal = 0
    n_external = 0
    for l in links:
        if l.startswith("/") or (host and host in l):
            n_internal += 1
        elif l.startswith("http"):
            n_external += 1

    # JSON-LD schema types
    blobs = re.findall(
        r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.IGNORECASE | re.DOTALL,
    )
    ld_types = []
    for b in blobs:
        try:
            data = json.loads(b.strip())
            graph = data.get("@graph", [data]) if isinstance(data, dict) else data
            if not isinstance(graph, list):
                graph = [graph]
            for d in graph:
                if isinstance(d, dict):
                    t = d.get("@type")
                    if t:
                        ld_types.append(t if isinstance(t, str) else ",".join(t))
        except Exception:
            ld_types.append("PARSE_ERROR")

    return {
        "title": title,
        "title_len": len(title),
        "desc": desc,
        "desc_len": len(desc),
        "canonical": canonical,
        "robots": robots,
        "h1_count": len(h1s),
        "h1s": h1s,
        "h2_count": len(h2s),
        "h2s_first10": h2s[:10],
        "schema_types": ld_types,
        "imgs_total": n_img,
        "imgs_empty_alt": n_empty_alt,
        "imgs_no_alt": n_no_alt,
        "links_internal": n_internal,
        "links_external": n_external,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("dir", help="Directory of cached HTML files")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    p.add_argument("--host", help="Host name for internal-link classification (e.g. example.com)")
    args = p.parse_args()

    files = sorted(f for f in os.listdir(args.dir) if f.endswith(".html"))
    all_data = {}
    for f in files:
        path = os.path.join(args.dir, f)
        with open(path, encoding="utf-8", errors="ignore") as fh:
            html = fh.read()
        data = extract(html, host=args.host)
        all_data[f] = data

    if args.json:
        print(json.dumps(all_data, indent=2))
        return

    for f, d in all_data.items():
        print(f"\n=== {f} ===")
        print(f"  TITLE [{d['title_len']}]: {d['title']}")
        print(f"  DESC  [{d['desc_len']}]: {d['desc'][:160]}")
        print(f"  CANON: {d['canonical']}")
        print(f"  ROBOTS: {d['robots']}")
        print(f"  H1 ({d['h1_count']}): {d['h1s']}")
        print(f"  H2 ({d['h2_count']}): {d['h2s_first10']}")
        print(f"  SCHEMA: {d['schema_types']}")
        print(
            f"  IMGS: total={d['imgs_total']} empty_alt={d['imgs_empty_alt']} no_alt={d['imgs_no_alt']}"
        )
        print(f"  LINKS: internal={d['links_internal']} external={d['links_external']}")


if __name__ == "__main__":
    sys.exit(main() or 0)
