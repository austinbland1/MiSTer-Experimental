#!/usr/bin/env python3

import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "metadata" / "cores.json"
EXTERNAL = ROOT / "external_files.csv"

VALID_STATUSES = {"experimental", "developing", "candidate", "graduated"}
VALID_AI = {
    "No AI assistance",
    "AI-assisted development",
    "Substantially AI-generated",
    "Other"
}

def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)

def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)

if not METADATA.exists():
    fail("metadata/cores.json does not exist")

if not EXTERNAL.exists():
    fail("external_files.csv does not exist")

try:
    data = json.loads(METADATA.read_text())
except json.JSONDecodeError as exc:
    fail(f"metadata/cores.json is invalid JSON: {exc}")

cores = data.get("cores")
if not isinstance(cores, list):
    fail("metadata/cores.json must contain a 'cores' array")

seen_slugs = set()

for core in cores:
    required = [
        "name",
        "slug",
        "status",
        "release",
        "source_repository",
        "release_url",
        "asset",
        "path",
        "author",
        "license",
        "ai_assistance"
    ]

    for key in required:
        if not core.get(key):
            fail(f"{core.get('name', '<unnamed>')}: missing '{key}'")

    slug = core["slug"]
    if slug in seen_slugs:
        fail(f"duplicate slug: {slug}")
    seen_slugs.add(slug)

    if core["status"] not in VALID_STATUSES:
        fail(f"{slug}: invalid status '{core['status']}'")

    if core["ai_assistance"] not in VALID_AI:
        fail(f"{slug}: invalid ai_assistance '{core['ai_assistance']}'")

    if not valid_url(core["source_repository"]):
        fail(f"{slug}: invalid source_repository URL")

    if not valid_url(core["release_url"]):
        fail(f"{slug}: invalid release_url URL")

    path = core["path"]
    if not path.startswith("_Experimental/_"):
        fail(f"{slug}: path must start with _Experimental/_")

    if not path.lower().endswith(".rbf"):
        fail(f"{slug}: path must end in .rbf")

    if ".." in Path(path).parts:
        fail(f"{slug}: path must not contain '..'")

    if "rbf_sha256" in core:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", core["rbf_sha256"]):
            fail(f"{slug}: invalid RBF SHA-256")

    if "rbf_size_bytes" in core:
        if not isinstance(core["rbf_size_bytes"], int) or core["rbf_size_bytes"] <= 0:
            fail(f"{slug}: invalid rbf_size_bytes")

text = EXTERNAL.read_text().strip().splitlines()

if len(text) < 2:
    fail("external_files.csv has no project entries")

header = text[0]
if not header.lower().startswith("path in mister"):
    fail("external_files.csv has an unexpected header")

for line_no, line in enumerate(text[1:], start=2):
    if not line.strip():
        continue

    fields = [field.strip() for field in line.split(",")]
    if len(fields) < 2:
        fail(f"external_files.csv line {line_no}: fewer than 2 fields")

    path, url = fields[0], fields[1]

    if not path.startswith("_Experimental/_"):
        fail(f"external_files.csv line {line_no}: invalid MiSTer path")

    if not path.lower().endswith(".rbf"):
        fail(f"external_files.csv line {line_no}: artifact is not an RBF")

    if not valid_url(url):
        fail(f"external_files.csv line {line_no}: invalid URL")

print(f"Validation OK: {len(cores)} metadata project(s)")
