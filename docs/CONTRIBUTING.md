# Contributing to MiSTer Experimental

The incubator is intentionally friendly to unfinished work. You do not need a production-quality core to propose a project; you do need to be honest about its current state.

## Before submitting

Verify that the project builds, boots (or otherwise runs) on the hardware you claim to support, and document known limitations.

Choose one stable install directory:

```text
_Experimental/_ProjectName/
```

Keep the project directory name stable once published.

## Pull request contents

A useful submission PR should include:

- the metadata entry in `metadata/cores.json`;
- the project payload under `_Experimental/_ProjectName/`, or an `external_files.csv` entry if the artifact is hosted elsewhere;
- build/reproduction information;
- hardware and SDRAM requirements;
- known limitations;
- AI-assistance disclosure, if applicable.

## Review

Reviewers are checking distribution safety and testability first, not whether the project is polished. A project can be accepted while still being crude or incomplete.

A project can be removed from the incubator for security problems, license problems, broken/disappeared artifacts, path conflicts, abandoned maintenance, or material misrepresentation of its status.
