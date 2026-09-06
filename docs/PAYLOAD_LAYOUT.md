# MiSTer payload layout

MiSTer Experimental does not impose one runtime filesystem layout on every kind of core. The repository's metadata describes the **installed MiSTer paths**, and those paths must remain compatible with the platform's existing conventions.

## Non-Arcade cores

Non-Arcade cores may use the incubator namespace:

```text
_Experimental/_ProjectName/<artifact>
```

## Arcade cores

Arcade submissions use an `_Arcade*` root rather than nesting Arcade material under `_Experimental`.

The expected relationship is:

```text
_Arcade_Experimental/
├── <game>.mra
└── cores/
    └── Arcade-Example_YYYYMMDD.rbf
```

`Main_MiSTer` derives the Arcade root from the underscore-prefixed directory containing the MRA and then uses `<root>/cores` for the RBF. That behavior is visible in `support/arcade/mra_loader.cpp`. The standard MiSTer Arcade documentation also describes the MRA/RBF relationship as `/_Arcade/<game>.mra` and `/_Arcade/cores/<game>.rbf`.

Experimental therefore treats the upstream Arcade release naming/version as authoritative. It does not require an Experimental-specific semantic version.

The `_Arcade_Experimental` namespace is an **integration hypothesis that must be hardware-tested**. Do not describe it as officially supported by Main_MiSTer until the real MiSTer menu/loader path has been tested.
