#!/usr/bin/env python3
"""Render the Flask app into a directory suitable for GitHub Pages."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from app import app


REPOSITORY_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = REPOSITORY_ROOT / "docs"
DEFAULT_DOMAIN = "paperquilts.art"


def route_output_path(route: str) -> Path:
    clean_route = route.strip("/")
    if not clean_route:
        return OUTPUT_DIR / "index.html"
    return OUTPUT_DIR / clean_route / "index.html"


def export_html_routes(base_url: str) -> None:
    client = app.test_client()

    for rule in sorted(app.url_map.iter_rules(), key=lambda current: current.rule):
        if rule.endpoint == "static" or rule.arguments or "GET" not in rule.methods:
            continue

        response = client.get(rule.rule, base_url=base_url)
        if response.status_code >= 400:
            raise RuntimeError(f"Failed to render {rule.rule}: {response.status_code}")

        destination = route_output_path(rule.rule)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(response.get_data(as_text=True), encoding="utf-8")


def copy_static_assets() -> None:
    shutil.copytree(REPOSITORY_ROOT / "static", OUTPUT_DIR / "static")


def write_metadata(domain: str | None) -> None:
    (OUTPUT_DIR / ".nojekyll").write_text("", encoding="utf-8")
    if domain:
        (OUTPUT_DIR / "CNAME").write_text(f"{domain}\n", encoding="utf-8")


def reset_output_dir() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render the Flask app into static files for GitHub Pages."
    )
    parser.add_argument(
        "--domain",
        default=DEFAULT_DOMAIN,
        help="Custom domain to write into docs/CNAME. Use an empty string to skip it.",
    )
    parser.add_argument(
        "--base-url",
        default=f"https://{DEFAULT_DOMAIN}",
        help="Base URL to use while rendering routes.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    domain = args.domain.strip() or None

    reset_output_dir()
    export_html_routes(args.base_url)
    copy_static_assets()
    write_metadata(domain)

    print(f"Static site generated in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
