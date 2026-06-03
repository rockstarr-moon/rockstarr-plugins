#!/usr/bin/env python3
"""Pull the live blog-post URLs from a client's sitemap.

Shares the Googlebot user-agent approach with rockstarr-content's
seo-site-audit (fetch_site.py), but scoped to one job: enumerate the
blog POST URLs so the master-list audit can diff them against what's
tracked in _publish.log / the master list.

Usage:
    python3 fetch_sitemap.py https://example.com/
    python3 fetch_sitemap.py https://example.com/ --json

Walks /sitemap.xml (or /sitemap_index.xml), follows nested
`post-sitemap*.xml` children, and prints one normalized blog URL per
line. Skips page-, project-, testimonial-, and other non-post sitemaps
(those are pages/case-studies/landing pages, not blog posts).
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"

# Child sitemaps that hold blog POSTS. WordPress/Yoast/RankMath split
# posts into post-sitemap.xml / post-sitemap1.xml / post-sitemap2.xml ...
POST_SITEMAP_RE = re.compile(r"post-sitemap\d*\.xml", re.IGNORECASE)
# Non-post sitemaps to ignore.
SKIP_SITEMAP_RE = re.compile(
    r"(page|project|testimonial|category|author|product|tag|attachment)-sitemap",
    re.IGNORECASE,
)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="ignore")
    except urllib.error.HTTPError as e:
        return e.code, ""
    except Exception:
        return 0, ""


def locs(xml):
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", xml, re.IGNORECASE | re.DOTALL)


def normalize(u):
    u = u.strip()
    u = re.sub(r"^https?://", "", u)
    u = re.sub(r"^www\.", "", u)
    u = re.sub(r"/$", "", u)
    return u.lower()


def main():
    p = argparse.ArgumentParser()
    p.add_argument("base", help="Site root URL, e.g. https://example.com/")
    p.add_argument("--json", action="store_true", help="Emit JSON instead of one-URL-per-line")
    args = p.parse_args()

    base = args.base.rstrip("/") + "/"
    host = normalize(base)

    # Find the sitemap index.
    index_xml = ""
    for path in ("sitemap.xml", "sitemap_index.xml"):
        status, body = fetch(urllib.parse.urljoin(base, path))
        if status == 200 and "<loc>" in body.lower():
            index_xml = body
            break

    if not index_xml:
        sys.stderr.write("WARN: no readable sitemap at /sitemap.xml or /sitemap_index.xml\n")
        # Some sites have a flat sitemap with URLs directly — fall through with empty index.

    child_sitemaps = [u for u in locs(index_xml) if u.lower().endswith(".xml")]
    post_sitemaps = [u for u in child_sitemaps if POST_SITEMAP_RE.search(u) and not SKIP_SITEMAP_RE.search(u)]

    blog_urls = set()

    if post_sitemaps:
        for sm in post_sitemaps:
            status, body = fetch(sm)
            for u in locs(body):
                if u.lower().endswith(".xml"):
                    continue
                if host in normalize(u) and normalize(u) != host:
                    blog_urls.add(u.strip())
    else:
        # No post-specific child sitemap. Treat any non-.xml <loc> in the
        # index as a candidate (flat sitemap), excluding the bare homepage.
        for u in locs(index_xml):
            if u.lower().endswith(".xml"):
                continue
            if host in normalize(u) and normalize(u) != host:
                blog_urls.add(u.strip())

    ordered = sorted(blog_urls)
    if args.json:
        print(json.dumps({"count": len(ordered), "blog_urls": ordered}, indent=2))
    else:
        for u in ordered:
            print(u)
        sys.stderr.write("\n{} blog URLs found.\n".format(len(ordered)))


if __name__ == "__main__":
    sys.exit(main() or 0)
