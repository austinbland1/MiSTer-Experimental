# MiSTer Experimental Core Incubator

An opt-in distribution channel for unfinished, first-party, community, and AI-assisted MiSTer FPGA experiments.

The project uses MiSTer Downloader's existing custom-database mechanism. The incubator adds project metadata, submission rules, testing expectations, and a graduation path instead of creating a second package format.

## Current pipeline test

The repository now uses a real third-party MiSTer RBF as the pipeline test:

`_Experimental/TestCore/InputTest_20260810.rbf`

The bitstream is published by `MiSTer-devel/InputTest_MiSTer` and is referenced through `external_files.csv`; it is not an Experimental project submission. The InputTest core is GPL-3.0.

The file is referenced as an external database asset rather than copied into this repository, so the project does not redistribute the binary itself.

This verifies the complete pipeline:

`GitHub main -> GitHub Actions -> db branch -> MiSTer Downloader -> MiSTer SD card -> RBF`

## Database

The DB-Template workflow generates the database at:

`https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip`

It also generates a drop-in Downloader configuration on the `db` branch. The template mirrors repository paths into the MiSTer filesystem. Our workflow additionally sets `FINDER_IGNORE` so repository-only directories (`db`, `examples`, `metadata`, and `scripts`) are excluded from the install database. The only current database payload is the test RBF supplied through `external_files.csv`. citeturn674328view0turn770949view0

## Manual Downloader integration

Add this to `/media/fat/downloader.ini`:

```ini
[austinbland1/MiSTer-Experimental]
db_url = https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip
```

MiSTer Downloader supports custom databases and drop-in `.ini` database files; after the database is added, normal `update` or Downloader runs will process it alongside other configured databases. citeturn337034view0turn674328view0

## Experimental updater

`scripts/update_experimental.sh` is intended to install/refresh the project's drop-in database and then invoke the normal MiSTer Downloader. It does not replace `downloader.ini`.

The current MVP assumes Downloader is at `/media/fat/Scripts/downloader.sh`, matching the official Downloader repository layout. citeturn337034view0

## Repository-only metadata

`metadata/cores.json` is not consumed directly by Downloader. It describes each incubator project: status, maintainer, source, hardware requirements, and notes.

## Security model

Experimental cores are untrusted artifacts. Submissions should prefer ordinary files that Downloader installs rather than arbitrary per-core shell installers. A contributor remains responsible for the code they publish, including AI-assisted code.

## Project states

`experimental -> developing -> candidate -> graduated`

Graduation is a human review decision based on reproducibility, documented behavior, testing, stability, and a maintainer willing to support the project outside the incubator.

## Roadmap

1. Verify the test payload downloads correctly.
2. Add a real experimental core with a reproducible release artifact.
3. Add automated metadata validation.
4. Add contributor submission and review workflow.
5. Add clearer installed/status UX to `update_experimental`.
