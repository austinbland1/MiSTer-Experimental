# MiSTer Experimental Core Incubator

An opt-in distribution channel for unfinished, first-party, community, and AI-assisted MiSTer FPGA experiments.

> **Status: early public preview / work in progress.**
>
> The distribution pipeline is functional, but the submission tooling, project lifecycle, and user-facing experience are still being developed. Experimental cores are not production-ready simply because they are available here.

The goal is deliberately simple: **make it easy to publish experimental work without pretending that experimental work is production-ready.** A project can enter the incubator early, receive a consistent distribution path, gather testers, and graduate when it is mature enough for the normal MiSTer ecosystem.

## How it works

This repository uses MiSTer Downloader's custom-database mechanism rather than creating a second package format. The DB-Template workflow generates `db/db.json.zip` and a drop-in Downloader `.ini`; users then run normal `update`/Downloader tooling. Repository paths are mirrored into the MiSTer filesystem, so paths intended to be core directories use MiSTer's `_`-prefixed directory convention.

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

More information:

- [MiSTer Downloader](https://github.com/MiSTer-devel/Downloader_MiSTer)
- [DB-Template_MiSTer](https://github.com/theypsilon/DB-Template_MiSTer)

## Current state

The first genuine project in the incubator is **Jinix Jupiter v0.2-rc1**.

It is distributed from its GitHub release through `external_files.csv`, installed by MiSTer Downloader, exposed under the MiSTer `Experimental` menu, and has been tested on real MiSTer hardware.

```text
_Experimental/
└── _JinixJupiter/
    └── JinixJupiter_v0.2-rc1.rbf
```

Jinix Jupiter is currently classified as `experimental` and is explicitly disclosed as **AI-assisted development**. Inclusion in this incubator does not imply official MiSTer endorsement, production stability, or correctness.

## Repository layout

```text
_Experimental/
└── _<CoreName>/              # actual MiSTer payloads; core directories start with _
    ├── <Core>.rbf
    ├── <Core>.mra             # optional
    └── <other runtime files>  # optional

authoring-only files:
├── .github/                  # CI / database generation / submission validation
├── docs/                     # project policy and contributor docs
├── examples/                 # templates only
├── metadata/                 # registry metadata; not installed
└── scripts/                  # development/updater/validation helpers; not installed

external_files.csv            # external payloads; not installed itself
```

Repository-only files are excluded from the generated Downloader database so users receive the intended MiSTer payloads rather than the repository's development infrastructure.

## Submission lifecycle

Every project starts as `experimental`.

```text
experimental -> developing -> candidate -> graduated
```

**Experimental** means the core may be incomplete, inaccurate, unstable, or missing features. It must still be buildable/distributable enough for someone else to test it.

**Developing** means there is active development and the project has a maintainer responding to issues and documenting known problems.

**Candidate** means the core is substantially functional and is being evaluated for graduation.

**Graduated** means the incubator maintainers believe it belongs in the normal MiSTer distribution ecosystem and the project has a maintainer prepared to support it there.

A project may remain experimental indefinitely, be archived, or move backward in status if circumstances warrant it.

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

The `_` prefix is intentional: MiSTer's menu uses `_`-prefixed core directories when scanning for core collections.

## Metadata

`metadata/cores.json` is a registry for human-facing project information. It is deliberately separate from the Downloader database.

The registry records status, maintainer, source, license, platform, SDRAM requirements, artifact information, and notes. It is not itself installed on MiSTer.

## Testing philosophy

The incubator should make the **cost of trying an idea low**, while keeping its status obvious. A project does not need to pretend to be finished before people can test it.

Before accepting a project into the channel, maintainers should at minimum verify that:

1. The advertised artifact downloads.
2. The artifact is placed at the intended MiSTer path.
3. The project boots or otherwise behaves as documented on the stated hardware.
4. Known limitations are documented.
5. The submission does not overwrite unrelated MiSTer paths.

The current CI also validates project metadata, checks the relationship between metadata and `external_files.csv`, rejects undeclared files under `_Experimental/`, and verifies declared artifact size and SHA-256 values against the published artifact.

## Database

The generated database is published at:

```text
https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip
```

The generated drop-in configuration is published under the `db` branch as well.

MiSTer Downloader supports custom databases and drop-in `.ini` database files. A generated drop-in `.ini` can be placed at the root of the MiSTer SD card, or the database can be added manually to `/media/fat/downloader.ini`:

```ini
[austinbland1/MiSTer-Experimental]
db_url = https://raw.githubusercontent.com/austinbland1/MiSTer-Experimental/db/db.json.zip
```

After the database is added, normal `update`/Downloader tooling processes it alongside other configured databases.

## Pull requests and review

New submissions are expected to go through a pull request.

The repository currently has:

- A pull-request submission template.
- Automated metadata and artifact validation.
- CODEOWNERS-based review routing.
- Protected `main` with required validation and review.

Passing automated validation does **not** mean that a core is endorsed or production-ready. Human review is still required.

Because the repository is currently maintained by a single maintainer, the branch protection configuration still permits an administrator bypass. This is intentional for the early public-preview stage and should be tightened as the maintainer team grows.

## Development

The database-generation workflow runs automatically on pushes to `main` and can also be dispatched manually from GitHub Actions.

The validation workflow runs on pushes and pull requests. It is intended to catch malformed metadata, inconsistent project declarations, undeclared experimental files, and artifact integrity mismatches before a submission can be merged.

The repository uses MiSTer Downloader's existing database format rather than inventing a new package format. For custom database behavior and external-file handling, see the [MiSTer Downloader](https://github.com/MiSTer-devel/Downloader_MiSTer) and [DB-Template_MiSTer](https://github.com/theypsilon/DB-Template_MiSTer) projects.

## `update_experimental`

`scripts/update_experimental.sh` is intended to provide a dedicated entry point for managing the Experimental channel without replacing MiSTer Downloader itself.

The current implementation is still an MVP. The underlying distribution mechanism is already functional; the script's user experience and lifecycle management are still being refined.

## Roadmap

### Completed

- [x] Prove custom Downloader database generation.
- [x] Prove a real RBF can be delivered through the database.
- [x] Establish the `_Experimental/_ProjectName` directory convention.
- [x] Add automated metadata validation.
- [x] Add pull-request submission workflow.
- [x] Add maintainer review checklist and repository review policy.
- [x] Add artifact size and SHA-256 verification.
- [x] Add the first genuine experimental core submission: Jinix Jupiter v0.2-rc1.
- [x] Protect `main` with required validation and human review.

### In progress

- [ ] Simplify the contributor submission format so project metadata does not have to be maintained in multiple places.
- [ ] Finish the standalone `update_experimental` UX.
- [ ] Add clearer installed/status information for Experimental projects.
- [ ] Add richer lifecycle tooling for `experimental`, `developing`, `candidate`, and `graduated` states.
- [ ] Harden CI against untrusted pull-request code and artifacts.

### Future

- [ ] Add maintainers/reviewers beyond the initial maintainer.
- [ ] Add automated project/release checks beyond the current artifact validation.
- [ ] Establish a documented graduation handoff process for projects moving into the normal MiSTer ecosystem.

## License

The updater, validation scripts, and other project-specific tooling are MIT-licensed unless a component explicitly states otherwise.

Individual experimental cores retain their own licenses and distribution terms.
