# MiSTer Experimental Core Incubator

An opt-in distribution channel for unfinished, first-party, community, and AI-assisted MiSTer FPGA experiments.

> **Status: early public preview / work in progress.**
>
> The distribution pipeline is functional, but the submission tooling, project lifecycle, governance, and user-facing experience are still being developed. Experimental cores are not production-ready simply because they are available here.

**MiSTer Experimental is a community-run staging channel, not an official MiSTer-devel project and not a replacement for the MiSTer-devel distribution and review process.** Its purpose is to make experimental work easier to distribute, test, document, and mature before it is ready for wider distribution through the normal MiSTer ecosystem.

The goal is deliberately simple: **make it easy to publish experimental work without pretending that experimental work is production-ready.** A project can enter the incubator early, receive a consistent distribution path, gather testers, and mature over time. A mature project may then pursue whatever official MiSTer distribution path is appropriate; MiSTer Experimental does not decide or grant official inclusion.

## How it works

This repository uses MiSTer Downloader's custom-database mechanism rather than creating a second package format. The DB-Template workflow generates a Downloader database and drop-in `.ini`; users then run normal Downloader/update tooling. Repository paths are mirrored into the MiSTer filesystem, so paths intended for core collections use MiSTer's existing directory conventions.

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
MiSTer filesystem
```

The project deliberately keeps the **metadata/registry** separate from the **runtime payload**. Development files, review policy, and validation tooling are not installed onto the MiSTer.

More information:

- [MiSTer Downloader](https://github.com/MiSTer-devel/Downloader_MiSTer)
- [DB-Template_MiSTer](https://github.com/theypsilon/DB-Template_MiSTer)

## Current state

The incubator currently demonstrates both non-Arcade and Arcade experimental payloads:

- **Jinix Jupiter v0.2-rc1** — a non-Arcade experimental core distributed from its GitHub release.
- **Arcade-Psikyo 20260904** — an experimental Arcade project with five MRAs and a dated RBF, using an `_Arcade_Experimental` integration layout.

Jinix Jupiter is currently classified as `experimental` and is explicitly disclosed as **AI-assisted development**. Arcade-Psikyo is currently classified as `candidate` and is explicitly disclosed as **substantially AI-generated**.

Inclusion in this incubator does not imply official MiSTer endorsement, production stability, correctness, or hardware validation beyond what the individual project and its documentation actually claim.

For the first Arcade integration test, `Gunbird (World).mra` was installed through Downloader, recognized under `Arcade_Experimental`, and successfully launched using `Arcade-Psikyo_20260904.rbf` on real MiSTer hardware. The required `gunbird.zip` ROM set was supplied separately by the tester in the normal `games/mame/` location.

## Repository layout

### Non-Arcade cores

Non-Arcade projects may use the incubator namespace:

```text
_Experimental/
└── _ProjectName/
    ├── <Core>.rbf
    ├── <Core>.mra             # optional
    └── <other runtime files>  # optional
```

### Arcade cores

Arcade submissions retain MiSTer's native MRA/RBF relationship while using an Experimental root namespace:

```text
_Arcade_Experimental/
├── <game>.mra
└── cores/
    └── Arcade-Example_YYYYMMDD.rbf
```

The `_Arcade_Experimental` layout has now been **verified on real MiSTer hardware**. MiSTer recognizes it as an Arcade collection, Downloader installs the associated MRA/RBF payloads without errors, and `Gunbird (World)` has been successfully launched through the associated dated RBF after supplying the required local MAME ROM set. This verifies the layout on the tested MiSTer configuration; it is not a claim of official MiSTer-devel support.

### Authoring-only files

```text
.github/                  # CI / database generation / submission validation
docs/                     # project policy and contributor docs
examples/                 # templates only
metadata/                 # registry metadata; not installed
scripts/                  # development/updater/validation helpers; not installed
external_files.csv        # external payload declarations; not installed itself
```

Repository-only files are excluded from the generated Downloader database so users receive the intended MiSTer payloads rather than the repository's development infrastructure.

See [`docs/PAYLOAD_LAYOUT.md`](docs/PAYLOAD_LAYOUT.md) for the current payload-layout policy.

## Submission lifecycle

Projects move through a human-reviewed lifecycle:

```text
experimental -> developing -> candidate -> graduated
```

**Experimental** means the project may be incomplete, inaccurate, unstable, or missing features. It must still be buildable/distributable enough for someone else to test it.

**Developing** means there is active development and the project has a maintainer responding to issues and documenting known problems.

**Candidate** means the project is substantially functional and is being evaluated for maturity and wider distribution.

**Graduated** means the project is mature enough that its maintainer can pursue the normal MiSTer distribution ecosystem or another appropriate long-term home. Graduation is not an official MiSTer-devel approval and is not granted automatically by this repository.

A project may remain experimental indefinitely, be archived, or move backward in status if circumstances warrant it.

**Graduation is a human decision, not an automated quality score.**

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

AI assistance is **not** an automatic rejection criterion. AI use is treated as provenance information; review focuses on the resulting project, its maintainability, its documentation, its behavior, and the submitter's ability to support it responsibly.

## Review, trust, and security

Experimental artifacts should be treated as **untrusted software/hardware descriptions**, not as automatically safe merely because they are distributed through this repository.

MiSTer Experimental does not claim that an FPGA bitstream can be proven free of malicious behavior by repository validation alone. Instead, maintainers should establish provenance and apply review appropriate to the submission, including as practical:

- checking the source and release provenance;
- verifying artifact hashes and sizes;
- reviewing build and distribution information;
- testing the advertised artifact on the stated hardware when practical;
- checking that installation paths do not overwrite unrelated MiSTer content; and
- documenting known limitations and unresolved concerns.

Binary-only submissions may require additional scrutiny because their behavior cannot be inspected from source in the same way as a reproducible build.

The repository's automated validation is a consistency and integrity check, not a substitute for human review or a security audit.

The experimental channel is not a place to silently replace production cores, distribute known malware, or ship arbitrary installation scripts.

Prefer ordinary MiSTer payload files (`.rbf`, `.mra`, configuration/data files, documentation) installed through Downloader. Arbitrary per-core shell installers should not be required.

## Maintainers and governance

MiSTer Experimental is intentionally designed to avoid becoming dependent on a single person.

During the early public-preview stage, the repository has an initial maintainer who operates the infrastructure and can perform emergency administration. The long-term goal is a **small team of trusted maintainers/reviewers** with shared access, documented responsibilities, and an auditable review process.

The project should not rely on the continued availability of one maintainer. As the maintainer team grows, the repository should move toward:

- multiple trusted reviewers for ordinary submissions;
- shared responsibility for database publication and emergency removal;
- documented handoff procedures;
- protected branches with required human review and automated validation; and
- clear procedures for handling an inactive maintainer or a compromised artifact.

The repository's branch protections and CI are safeguards, but administrative bypass may still be necessary during the public-preview stage. That exception should be reduced as shared maintainership becomes practical.

## What we will not do

MiSTer Experimental will not attempt to replace MiSTer-devel, establish itself as an alternative official distribution authority, or decide unilaterally which projects belong in the official MiSTer ecosystem.

It also will not silently replace production cores, distribute known malware, or require arbitrary installation scripts.

Experimental projects remain responsible for their own code, licensing, documentation, and maintenance. MiSTer Experimental provides a staging and distribution mechanism; it does not become the upstream maintainer of every project it hosts.

## Naming rules

For non-Arcade projects, the incubator namespace is:

```text
_Experimental/_ProjectName/
```

For Arcade projects, the current experimental namespace is:

```text
_Arcade_Experimental/
```

Use stable, descriptive names because installed paths become part of the MiSTer filesystem and should not be changed casually.

See [`docs/PAYLOAD_LAYOUT.md`](docs/PAYLOAD_LAYOUT.md) for the current Arcade and non-Arcade layout rules.

## Metadata

`metadata/cores.json` is a registry for human-facing project information. It is deliberately separate from the Downloader database.

The registry records status, maintainer, source, license, platform, artifact information, and notes. It is not itself installed on MiSTer.

Artifact declarations distinguish between repository-hosted payloads and externally hosted payloads. External artifacts are checked against `external_files.csv`; repository artifacts are expected to exist at their declared installed paths and are validated locally.

## Testing philosophy

The incubator should make the **cost of trying an idea low**, while keeping its status obvious. A project does not need to pretend to be finished before people can test it.

Before accepting a project into the channel, maintainers should at minimum verify that:

1. The advertised artifact downloads or is present at the declared repository path.
2. The artifact is placed at the intended MiSTer path.
3. The project boots or otherwise behaves as documented on the stated hardware, when hardware testing is practical.
4. Known limitations are documented.
5. The submission does not overwrite unrelated MiSTer paths.
6. The artifact provenance and maintainer contact are clear enough for follow-up.

The current CI validates project metadata, checks the relationship between metadata and `external_files.csv`, rejects undeclared files under declared payload roots, parses repository MRAs, and verifies declared artifact size and SHA-256 values where supplied or externally retrievable.

Passing automated validation does **not** mean that a core is endorsed or production-ready.

## Downloader experience

MiSTer Experimental is intended to use the normal MiSTer Downloader experience rather than requiring users to maintain a collection of unrelated custom repositories.

The desired user experience is:

- Experimental projects can be selected independently rather than forcing users to install the entire channel.
- Unselected Experimental projects can eventually be removed cleanly, including their associated payload files where Downloader semantics allow it.
- Experimental projects remain visibly separated from mature/official content.

These behaviors depend partly on what the existing Downloader database format and client can express. They are therefore tracked as product goals rather than claimed as fully implemented features today.

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

After the database is added, normal Downloader/update tooling processes it alongside other configured databases.

## Pull requests and review

New submissions are expected to go through a pull request.

The repository currently has:

- A pull-request submission template.
- Automated metadata and artifact validation.
- CODEOWNERS-based review routing.
- Protected `main` with required validation and review, while retaining a limited administrator bypass during the early public-preview stage.

Passing automated validation does **not** mean that a core is endorsed or production-ready. Human review is still required.

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
- [x] Establish an experimental `_Arcade_Experimental` MRA/RBF integration layout and publish it through the custom database.
- [x] Add automated metadata validation.
- [x] Add pull-request submission workflow.
- [x] Add maintainer review checklist and repository review policy.
- [x] Add artifact size and SHA-256 verification.
- [x] Add the first genuine experimental core submission: Jinix Jupiter v0.2-rc1.
- [x] Add the first Arcade integration test project: Arcade-Psikyo 20260904.
- [x] Verify an Arcade MRA successfully launches through the associated dated RBF on real MiSTer hardware.
- [x] Protect `main` with required validation and human review.

### In progress

- [ ] Simplify the contributor submission format so project metadata does not have to be maintained in multiple places.
- [ ] Finish the standalone `update_experimental` UX.
- [ ] Add clearer installed/status information for Experimental projects.
- [ ] Add richer lifecycle tooling for `experimental`, `developing`, `candidate`, and `graduated` states.
- [ ] Harden CI against untrusted pull-request code and artifacts.
- [x] Test the `_Arcade_Experimental` layout on real MiSTer hardware and document the observed loader behavior.
- [ ] Improve selective install/removal behavior so users can manage Experimental projects individually.

### Future

- [ ] Add maintainers/reviewers beyond the initial maintainer.
- [ ] Add automated project/release checks beyond the current artifact validation.
- [ ] Establish a documented graduation handoff process for projects moving into the normal MiSTer ecosystem.
- [ ] Establish a documented emergency-removal and compromised-maintainer procedure.
- [ ] Evaluate whether Experimental can eventually serve as a community staging layer feeding projects toward other MiSTer distribution paths without becoming a competing official authority.

## License

The updater, validation scripts, and other project-specific tooling are MIT-licensed unless a component explicitly states otherwise.

Individual experimental cores retain their own licenses and distribution terms.
