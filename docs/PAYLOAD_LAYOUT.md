# MiSTer payload layout

MiSTer Experimental does not impose one runtime filesystem layout on every kind of core. The repository's metadata describes the **installed MiSTer paths**, and those paths must remain compatible with the platform's existing conventions.

## Non-Arcade cores

Non-Arcade cores may use the incubator namespace:

```text
_Experimental/_ProjectName/<artifact>
```

## Arcade cores

Arcade submissions use an `_Arcade*` root rather than nesting Arcade material under `_Experimental`.

The verified relationship is:

```text
_Arcade_Experimental/
├── <game>.mra
└── cores/
    └── Arcade-Example_YYYYMMDD.rbf
```

The MRA retains its normal `<rbf>` core identity, while the RBF may use the upstream Arcade project's date-based release filename. The current `Arcade-Psikyo` integration demonstrates this with `Arcade-Psikyo_20260904.rbf` and MRAs declaring `<rbf>Arcade-Psikyo</rbf>`.

## Verification status

The `_Arcade_Experimental` namespace has been **verified on real MiSTer hardware** using the current public-preview database. The test established that:

1. MiSTer recognizes `_Arcade_Experimental` as an Arcade collection.
2. Downloader installs the associated five MRAs and the dated RBF without errors.
3. `Gunbird (World).mra` successfully selects and launches the associated `Arcade-Psikyo_20260904.rbf`.
4. The game successfully runs when the required `gunbird.zip` ROM set is supplied separately in the normal `games/mame/` location.

This verifies the current layout on the tested MiSTer configuration. It does **not** imply that `_Arcade_Experimental` is an official MiSTer-devel namespace or that every future MiSTer version will preserve the same behavior without further testing.

## Naming and versioning

Experimental does not require an Experimental-specific semantic version for Arcade RBFs. The upstream Arcade project's release naming/versioning should remain authoritative where practical. The Experimental layer provides the installation namespace; it should not unnecessarily fork upstream artifact naming conventions.
