# Cycle Foot

An open-source, 3D-printable **cycling foot for lower-limb prosthetics**. It
clamps onto a standard 30 mm pylon tube in place of a regular prosthetic
foot and gives you a cleat mount directly under the pylon, so you can clip into
clipless bike pedals. A separate printed sole with a grip pattern lets you
walk short distances off the bike.

Designed by an amputee, for amputees, in [FreeCAD](https://www.freecad.org/).
It supports SPD and Crank Brothers cleats and is sized so Össur Total Knee
users can still unlock the knee. See the [design history](docs/design-history.md)
for the requirements and what each version taught us.
Fully parametric: adjust the dimensions to fit your own leg and setup.

> ## ⚠️ Safety notice — read before use
>
> This is a **homemade, unregulated prosthetic component**. It is **not** a
> certified medical device and has not been tested to ISO 10328 or any other
> prosthetic standard. A failure while riding can cause serious injury.
>
> - Talk to your prosthetist before using it, and have them check the fit and
>   alignment.
> - Inspect the part for cracks, layer separation or loose hardware **before
>   every ride**. Replace it at the first sign of damage.
> - Start with low-intensity riding and build up gradually.
> - Print quality, material and settings strongly affect strength. A part
>   printed by you is only as good as your print.
>
> You use this design entirely at your own risk. See the disclaimer of
> warranty and limitation of liability in [LICENSE](LICENSE), section 6.

## Repository layout

| Path | Contents |
| --- | --- |
| `cad/cycle_foot.FCStd` | **Source model** (FreeCAD 1.x, current version v3.7). Edit this one. |
| `exports/step/` | STEP files for each part, for use in other CAD software |
| `exports/stl/` | STL files ready to slice and print |
| `docs/design-history.md` | Requirements, load cases and lessons learned from every revision |
| `tools/export.py` | Script that regenerates `exports/` from the source model |

## Previous versions

Each design revision is a tagged commit (`v0` … `v3.7`) with its STEP and STL
exports, so you can download or compare any earlier version from the
[tags page](https://github.com/ZacVawter/cycle_foot/tags). Run
`git log --stat` to see how the design evolved, and read
[docs/design-history.md](docs/design-history.md) for why it changed.

## Parts

| Part | File | Notes |
| --- | --- | --- |
| Foot | `exports/stl/cycle_foot-foot.stl` | Pylon clamp, gusset, and cleat mount. Structural part. |
| Sole | `exports/stl/cycle_foot-sole.stl` | Walking shell with grip pattern and mud ramp |

### Hardware

- Threaded inserts for the clamp and cleat bolts, sized for E-Z LOK tapered
  thin-wall inserts (dimensions in the model's `Parameters` spreadsheet):
  - DV-M40-TH (M4 × 0.7)
  - DV-M30-TH (M3 × 0.5)
  - Dimensional drawing: <https://www.ezlok.com/assets/documents/dimensional_drawings/DimDwg_Ultra_Tapered.pdf>
- M4 / M3 bolts for the pylon clamp
- A cleat compatible with your pedals, with its bolts

## Customising for your leg

Open `cad/cycle_foot.FCStd` and edit the **`Parameters`** spreadsheet. The whole
model updates from these values:

| Alias | Default | Meaning |
| --- | --- | --- |
| `pilon_dia` | 30 mm | Pylon tube diameter |
| `pilon_to_cleat` | 70 mm | Pylon centreline to cleat centreline |
| `cleat_to_toe` | 25 mm | Cleat centreline to toe |
| `cleat_to_top_clamp` | 89.5 mm | Cleat centreline to top clamp |
| `cleat_to_bottom_clamp` | 92 mm | Cleat centreline to bottom clamp |
| `clamp_top_bolt` | 47 mm | Height of top clamp bolt |
| `clamp_mid_bolt` | 27 mm | Height of middle clamp bolt |
| `clamp_bottom_bolt` | 7.5 mm | Height of bottom clamp bolt |

After editing, regenerate the print files:

```sh
freecadcmd tools/export.py      # Snap install: freecad.cmd tools/export.py
```

The model also has a FEM analysis (CalculiX), with a fixed constraint and a
500 N load, that you can re-run after changing the geometry.

## Printing

<!-- TODO: add the material, printer type, layer height, infill/walls and
     print orientation that have been tested on the road. -->

Earlier versions were made from ABS and machined Delrin (see the
[design history](docs/design-history.md)). Print the **Foot** with high wall
and infill counts. It carries your full weight while pedalling, and the design
target is 1500 N at the cleat with a 2× safety factor.

## Contributing

Ride reports, fit changes, photos and design improvements are welcome. Open an
issue or a pull request. If you change the geometry, please commit the updated
`cad/cycle_foot.FCStd` **and** re-run `tools/export.py` so the STEP/STL files
match the source.

## License

Copyright © 2023–2026 Zac Vawter.

This hardware design is licensed under the **CERN Open Hardware Licence Version
2 – Strongly Reciprocal** ([CERN-OHL-S-2.0](LICENSE)). You may use, study,
modify, make and sell products from it. If you distribute a modified version
(or products made from one), you must release your modified source under the
same licence.

Source location: <https://github.com/ZacVawter/cycle_foot>

The software in `tools/` is covered by the same licence.
