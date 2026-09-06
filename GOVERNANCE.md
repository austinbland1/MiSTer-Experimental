# Governance

MiSTer Experimental is a community-run staging and distribution channel for experimental MiSTer projects. It is **not an official MiSTer-devel project** and does not replace the MiSTer-devel distribution or review process.

The purpose of this document is to make the project's decision-making, review, and continuity expectations explicit as the project grows beyond a single maintainer.

## Principles

MiSTer Experimental should be:

- **Independent but interoperable.** It should work with existing MiSTer tooling where practical without presenting itself as an alternative official distribution authority.
- **Reviewable.** Automated checks should enforce consistency and integrity, while human review remains responsible for project acceptance and higher-risk decisions.
- **Transparent.** Project status, artifact provenance, licensing, AI assistance, known limitations, and important review decisions should be documented.
- **Reversible.** Experimental inclusion should be easy to suspend or remove when an artifact becomes unsafe, broken, abandoned, or otherwise unsuitable for continued distribution.
- **Maintainable.** The infrastructure should not depend permanently on one person's availability.

## Roles

### Maintainers

Maintainers operate the repository and its distribution infrastructure. Their responsibilities include:

- reviewing submissions and changes to project metadata;
- maintaining CI, database generation, and repository policy;
- coordinating emergency removal of problematic artifacts;
- protecting access to publishing infrastructure and repository administration; and
- documenting significant operational decisions.

During the early public-preview period, the project may have a single primary maintainer. This is a temporary operating condition, not the desired long-term governance model.

### Reviewers

Reviewers are trusted contributors who participate in submission review and other project decisions. A reviewer does not need unrestricted administrative access to the repository.

The long-term goal is to have multiple trusted reviewers so that ordinary submissions do not depend on one person acting alone.

### Contributors / submitters

Project authors and other contributors may propose new cores, metadata, documentation, and infrastructure changes through the repository's normal contribution process. Submission does not imply acceptance.

## Submission and review

A new project should enter the repository through a pull request or another auditable review mechanism appropriate to the repository's current configuration.

Before publication, maintainers/reviewers should establish, as practical:

1. clear project ownership or maintainer contact;
2. source and release provenance;
3. a valid license;
4. accurate artifact paths and metadata;
5. disclosure of AI assistance when AI tools were used;
6. documented known limitations and hardware requirements;
7. artifact integrity information such as size and SHA-256 where available; and
8. evidence of testing appropriate to the project's maturity and claims.

Automated validation is required where the repository's CI provides it, but passing CI is not equivalent to human approval, hardware validation, or official MiSTer-devel endorsement.

### Review depth

Review depth should be proportional to risk and maturity.

A straightforward source-backed experimental core may only need basic provenance, metadata, path, and functional checks. Binary-only artifacts, unusual installation behavior, unclear provenance, or submissions with elevated risk should receive additional scrutiny.

The project does not claim that an FPGA bitstream can be proven harmless solely through source inspection, hashing, or automated validation. Review establishes reasonable provenance and consistency; it does not provide a security guarantee.

## Approval model

As the maintainer team grows, ordinary new-project submissions should preferably receive review from **at least two trusted maintainers/reviewers** before publication.

The review requirement may initially be relaxed when the project has too few maintainers to make two-person review practical. Such exceptions should be treated as temporary and should be documented in the pull request or relevant project record.

Changes that materially affect the publishing pipeline, trust model, artifact validation, or branch protections should receive additional review whenever practical.

## Project lifecycle

MiSTer Experimental uses the following lifecycle states:

```text
experimental -> developing -> candidate -> graduated
```

These states describe the project's maturity **within MiSTer Experimental**. They do not confer official MiSTer-devel status.

A project may also be archived or returned to an earlier state when appropriate.

### Experimental

The project may be incomplete, unstable, inaccurate, or missing features, but it must be distributable enough for others to test.

### Developing

The project has active development, a maintainer responding to issues, and enough documentation to support continued testing.

### Candidate

The project is substantially functional and is being evaluated for maturity and wider distribution.

### Graduated

The project has reached a maturity level where its maintainer can pursue an appropriate long-term distribution path. Graduation is not official MiSTer-devel approval and does not guarantee inclusion there.

## Artifact trust and security

Experimental artifacts must be treated as untrusted.

Maintainers should prefer ordinary MiSTer payloads distributed through Downloader and should avoid requiring arbitrary per-core installation scripts.

For each published artifact, maintainers should preserve enough provenance to answer:

- What project produced this artifact?
- Which upstream source or release does it correspond to?
- Who is responsible for maintaining it?
- Where can the source or release be inspected?
- What artifact was actually published?
- What integrity information is available?

When practical, artifact hashes and sizes should be recorded and checked automatically.

Known malicious artifacts, compromised releases, or artifacts that materially violate repository policy should be removed or disabled promptly.

## Emergency removal

A maintainer may temporarily remove or disable an artifact without waiting for the normal review cycle when there is a credible reason to believe that continued distribution presents a significant security, integrity, licensing, or operational risk.

Emergency action should be followed by an auditable record describing, at an appropriate level of detail:

- what was removed or disabled;
- why action was taken;
- when it occurred; and
- what follow-up review is required.

Emergency removal does not permanently ban a project. Reinstatement should require a documented review of the underlying issue.

## Maintainer succession and continuity

The project should not depend permanently on a single maintainer.

As the project grows, maintainers should establish:

- at least two trusted people familiar with the repository and publishing workflow;
- shared knowledge of CI, database publication, and branch protections;
- documented access and handoff procedures;
- a way to revoke access when a maintainer leaves the project; and
- a procedure for recovering control if a maintainer becomes unavailable or an account is compromised.

The long-term objective is for no single person to be indispensable to routine project operation.

## Repository and branch protection

The source repository should use protected branches and required automated validation wherever practical.

Administrative bypasses may be necessary during the early public-preview period for infrastructure recovery or other exceptional situations. Such bypasses should remain limited and should not be treated as a substitute for normal review.

As the maintainer team grows, the project should reduce reliance on administrative bypasses and strengthen multi-person review and recovery procedures.

## Relationship to MiSTer-devel

MiSTer Experimental does not speak for MiSTer-devel and does not grant official MiSTer-devel inclusion.

A project hosted here may later pursue submission to MiSTer-devel or another appropriate distribution channel. The decision to accept such a project into an official ecosystem belongs to the maintainers of that ecosystem.

MiSTer Experimental's role is to provide a staging path in which experimental work can be distributed to interested testers, receive feedback, and mature without requiring the project to be presented as production-ready.

## Changes to this policy

This document may evolve as the project gains maintainers and practical experience.

Changes to governance should be made through the normal repository review process and should be written so that contributors can understand what changed and why.
