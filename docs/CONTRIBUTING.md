# Contributing to MiSTer Experimental

MiSTer Experimental is an opt-in incubator for unfinished, experimental,
community, and AI-assisted MiSTer FPGA projects.

## Submission requirements

Every project must provide:

- A clear project name and maintainer.
- A public source repository.
- A specific reproducible release artifact.
- A declared software/hardware license.
- A documented MiSTer destination path.
- Required hardware and SDRAM requirements, when applicable.
- A description of known limitations.
- A disclosure of AI assistance:
  - none
  - AI-assisted development
  - substantially AI-generated
  - other, with explanation

Projects should use:

    _Experimental/_ProjectName/

and core directories must retain the leading `_` so MiSTer's menu recognizes them.

## Review

A pull request is required for new projects and significant release changes.

Automation checks metadata and repository structure first.
Human review then evaluates functionality, reproducibility, documentation,
licensing, and whether the artifact belongs in the experimental channel.
