# MiSTer Experimental Core Incubator

An opt-in distribution channel for unfinished, first-party, community, and AI-assisted MiSTer FPGA experiments.

The goal is deliberately simple: **make it easy to publish experimental work without pretending that experimental work is production-ready.** A project can enter the incubator early, receive a consistent distribution path, gather testers, and graduate when it is mature enough for the normal MiSTer ecosystem.

## How it works

This repository uses MiSTer Downloader's custom-database mechanism rather than creating a second package format. The DB-Template workflow generates `db/db.json.zip` and a drop-in Downloader `.ini`; users then run normal `update`/Downloader tooling. Repository paths are mirrored into the MiSTer filesystem, so paths intended to be core directories use MiSTer's `_`-prefixed directory convention. citeturn650381view0turn650381view1

The experimental channel therefore looks like:

```text
GitHub repository
      |
      v
GitHub Actions -> custom Downloader database
      |
      v
MiSTer Downloader
      |
      v
/media/fat/_Experimental/
```

## Current pipeline test

The repository contains one pipeline test entry using the upstream `MiSTer-devel/InputTest_MiSTer` bitstream:

```text
_Experimental/
└── _TestCore/
    └── InputTest_20260810.rbf
```

The RBF is referenced through `external_files.csv`; it is not copied into this repository. It exists only to validate the distribution pipeline. It is **not** an incubator submission.

## Repository layout

```text
_Experimental/
└── _<CoreName>/              # actual MiSTer payloads; core directories start with _
    ├── <Core>.rbf
    ├── <Core>.mra             # optional
    └── <other runtime files>  # optional

authoring-only files:
├── .github/                  # CI / database generation
├── docs/                     # project policy and contributor docs
├── examples/                 # templates only
├── metadata/                 # registry metadata; not installed
└── scripts/                  # development/updater helpers; not installed

external_files.csv            # external payloads; not installed itself
```

## Submission lifecycle

Every project starts as `experimental`.

```text
experimental -> developing -> candidate -> graduated
```

**Experimental** means the core may be incomplete, inaccurate, unstable, or missing features. It must still be buildable/distributable enough for someone else to test it.

**Developing** means there is active development and the project has a maintainer responding to issues and documenting known problems.

**Candidate** means the core is substantially functional and is being evaluated for graduation.

**Graduated** means the incubator maintainers believe it belongs in the normal MiSTer distribution ecosystem and the project has a maintainer prepared to support it there.

Graduation is a human decision, not an automated quality score.

## Submission requirements

A submission should provide:

- A public source repository or otherwise reproducible source.
- A clear license compatible with distribution of the source and any included artifacts.
- A maintainer/contact.
- The target platform and hardware requirements.
- Known limitations and current status.
- Build instructions or a reproducible build process.
- ROM/BIOS requirements, when applicable.
- SDRAM requirements, when applicable.
- A statement describing AI assistance, when AI tools were used.

AI assistance is **not** a rejection criterion. The incubator cares about whether the resulting project is usable, reviewable, and responsibly maintained.

## What we will not do

The experimental channel is not a place to silently replace production cores, distribute known malware, or ship arbitrary installation scripts.

Prefer ordinary MiSTer payload files (`.rbf`, `.mra`, configuration/data files, documentation) installed through Downloader. Arbitrary per-core shell installers should not be required.

Experimental artifacts are untrusted. Users should understand that installing an experimental core is different from installing a mature core from the main distribution.

## Naming rules

The top-level directory is:

```text
_Experimental/
```

Each core/project gets its own `_`-prefixed directory:

```text
_Experimental/_ProjectName/
```

Do not use spaces in project directory names. Use a stable, descriptive name because the path becomes part of the installed MiSTer filesystem and should not be changed casually.

## Metadata

`metadata/cores.json` is a registry for human-facing project information. It is deliberately separate from the Downloader database.

The registry records status, maintainer, source, license, platform, SDRAM requirements, and notes. It is not itself installed on MiSTer.

## Testing philosophy

The incubator should make the **cost of trying an idea low**, while keeping its status obvious. A project does not need to pretend to be finished before people can test it.

Before accepting a project into the channel, maintainers should at minimum verify that:

1. The advertised artifact downloads.
2. The artifact is placed at the intended MiSTer path.
3. The project boots or otherwise behaves as documented on the stated hardware.
4. Known limitations are documented.
5. The submission does not overwrite unrelated MiSTer paths.

## Database

The generated database is published at:

```text
https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip
```

The generated drop-in configuration is published under the `db` branch as well. DB-Template documents both the generated database URL and the drop-in `.ini` mechanism. citeturn650381view0

## Development

The database-generation workflow runs automatically on pushes to `main` and can also be dispatched manually from GitHub Actions.

The workflow excludes authoring-only directories from the install database. This prevents repository infrastructure such as `metadata/`, `docs/`, `examples/`, and `scripts/` from appearing on users' MiSTers.

## Roadmap

- [x] Prove custom Downloader database generation.
- [x] Prove a real RBF can be delivered through the database.
- [x] Establish the `_Experimental/_ProjectName` directory convention.
- [ ] Add automated metadata validation.
- [ ] Add pull-request submission workflow.
- [ ] Add maintainer review checklist.
- [ ] Finish the standalone `update_experimental` UX.
- [ ] Add the first genuine experimental core submission.
