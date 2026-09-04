#!/usr/bin/env python3

import csv
import hashlib
import json
import re
import sys
import urllib.request
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
METADATA = ROOT / "metadata" / "cores.json"
EXTERNAL = ROOT / "external_files.csv"

VALID_STATUSES = {
    "experimental",
    "developing",
    "candidate",
    "graduated",
}

VALID_AI = {
    "No AI assistance",
    "AI-assisted development",
    "Substantially AI-generated",
    "Other",
}

EXPERIMENTAL_ROOT = "_Experimental"


def fail(message: str) -> None:
    print(f"ERROR: {message}")
    sys.exit(1)


def valid_url(value: str) -> bool:
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def sha256_url(url: str) -> tuple[str, int]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "MiSTer-Experimental-Validator/1.0"},
    )

    digest = hashlib.sha256()
    size = 0

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break

                digest.update(chunk)
                size += len(chunk)

    except Exception as exc:
        fail(f"unable to download artifact: {url} ({exc})")

    return digest.hexdigest(), size


# ------------------------------------------------------------
# Load metadata
# ------------------------------------------------------------

if not METADATA.exists():
    fail("metadata/cores.json does not exist")

if not EXTERNAL.exists():
    fail("external_files.csv does not exist")

try:
    metadata = json.loads(METADATA.read_text())
except json.JSONDecodeError as exc:
    fail(f"metadata/cores.json is invalid JSON: {exc}")

cores = metadata.get("cores")

if not isinstance(cores, list):
    fail("metadata/cores.json must contain a 'cores' array")


# ------------------------------------------------------------
# Parse metadata
# ------------------------------------------------------------

metadata_by_path: dict[str, dict] = {}
metadata_slugs: set[str] = set()

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
        "ai_assistance",
    ]

    for key in required:
        if not core.get(key):
            fail(f"{core.get('name', '<unnamed>')}: missing '{key}'")

    slug = core["slug"]

    if slug in metadata_slugs:
        fail(f"duplicate slug: {slug}")

    metadata_slugs.add(slug)

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
        fail(
            f"{slug}: path must start with "
            f"_Experimental/_ProjectName/"
        )

    if not path.lower().endswith(".rbf"):
        fail(f"{slug}: path must end in .rbf")

    path_parts = Path(path).parts

    if ".." in path_parts:
        fail(f"{slug}: path must not contain '..'")

    if len(path_parts) != 3:
        fail(
            f"{slug}: path must be exactly "
            "_Experimental/_ProjectName/file.rbf"
        )

    if not path_parts[1].startswith("_"):
        fail(f"{slug}: project directory must start with '_'")

    if not re.fullmatch(
        r"_Experimental/_[^/]+/[^/]+\.rbf",
        path
    ):
        fail(f"{slug}: invalid experimental core path '{path}'")

    if path in metadata_by_path:
        fail(f"duplicate metadata path: {path}")

    metadata_by_path[path] = core

    if "rbf_sha256" in core:
        if not re.fullmatch(r"[0-9a-fA-F]{64}", core["rbf_sha256"]):
            fail(f"{slug}: invalid RBF SHA-256")

    if "rbf_size_bytes" in core:
        if (
            not isinstance(core["rbf_size_bytes"], int)
            or core["rbf_size_bytes"] <= 0
        ):
            fail(f"{slug}: invalid rbf_size_bytes")


# ------------------------------------------------------------
# Parse external_files.csv
# ------------------------------------------------------------

external_by_path: dict[str, dict] = {}

with EXTERNAL.open(newline="") as handle:
    reader = csv.DictReader(handle, skipinitialspace=True)

    if not reader.fieldnames:
        fail("external_files.csv has no header")

    if "Path in MiSTer" not in reader.fieldnames:
        fail("external_files.csv is missing 'Path in MiSTer' column")

    if "URL" not in reader.fieldnames:
        fail("external_files.csv is missing 'URL' column")

    for line_no, row in enumerate(reader, start=2):
        path = (row.get("Path in MiSTer") or "").strip()
        url = (row.get("URL") or "").strip()

        if not path:
            fail(f"external_files.csv line {line_no}: empty path")

        if not url:
            fail(f"external_files.csv line {line_no}: empty URL")

        if path in external_by_path:
            fail(
                f"external_files.csv line {line_no}: "
                f"duplicate path '{path}'"
            )

        if not path.startswith("_Experimental/_"):
            fail(
                f"external_files.csv line {line_no}: "
                f"path outside _Experimental: {path}"
            )

        if not re.fullmatch(
            r"_Experimental/_[^/]+/[^/]+\.rbf",
            path
        ):
            fail(
                f"external_files.csv line {line_no}: "
                f"invalid core path '{path}'"
            )

        if not valid_url(url):
            fail(
                f"external_files.csv line {line_no}: "
                f"invalid URL '{url}'"
            )

        external_by_path[path] = {
            "url": url,
            "line": line_no,
        }


# ------------------------------------------------------------
# Cross-check metadata <-> external_files.csv
# ------------------------------------------------------------

metadata_paths = set(metadata_by_path)
external_paths = set(external_by_path)

missing_external = metadata_paths - external_paths

if missing_external:
    for path in sorted(missing_external):
        fail(
            f"metadata entry has no external_files.csv entry: {path}"
        )

undeclared_metadata = external_paths - metadata_paths

if undeclared_metadata:
    for path in sorted(undeclared_metadata):
        fail(
            f"external_files.csv entry has no metadata entry: {path}"
        )


# ------------------------------------------------------------
# Inspect actual repository contents
# ------------------------------------------------------------

tracked_experimental = []

for path in ROOT.rglob("*"):
    if not path.is_file():
        continue

    relative = path.relative_to(ROOT).as_posix()

    if relative.startswith(EXPERIMENTAL_ROOT + "/"):
        tracked_experimental.append(relative)

unexpected_files = [
    path
    for path in tracked_experimental
    if path not in external_paths
]

if unexpected_files:
    for path in sorted(unexpected_files):
        fail(
            f"undeclared file under _Experimental: {path}\n"
            "Every experimental artifact must be declared in "
            "external_files.csv and metadata/cores.json."
        )


# ------------------------------------------------------------
# Verify each published artifact
# ------------------------------------------------------------

for path, core in metadata_by_path.items():
    entry = external_by_path[path]
    url = entry["url"]

    print(f"Checking artifact: {core['name']}")
    print(f"  URL: {url}")

    actual_sha256, actual_size = sha256_url(url)

    expected_sha256 = core.get("rbf_sha256")
    expected_size = core.get("rbf_size_bytes")

    if expected_sha256:
        if actual_sha256.lower() != expected_sha256.lower():
            fail(
                f"{core['slug']}: SHA-256 mismatch\n"
                f"  expected: {expected_sha256}\n"
                f"  actual:   {actual_sha256}"
            )

    if expected_size:
        if actual_size != expected_size:
            fail(
                f"{core['slug']}: artifact size mismatch\n"
                f"  expected: {expected_size}\n"
                f"  actual:   {actual_size}"
            )

    print(f"  SHA-256: {actual_sha256}")
    print(f"  Size:    {actual_size} bytes")


print()
print(
    f"Validation OK: {len(cores)} project(s), "
    f"{len(external_paths)} artifact(s)"
)
