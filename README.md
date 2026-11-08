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
> - **CRITICAL: Print quality, material and settings strongly affect
>   strength. A part printed by you is only as good as your print.** Follow
>   [Printing & setup](#printing--setup) exactly.
>
> You use this design entirely at your own risk. See the disclaimer of
> warranty and limitation of liability in [LICENSE](LICENSE), section 6.

## Printing & setup

### Material

Print the **Foot** in a carbon-fibre-filled nylon. Both of these are
acceptable:

| Filament | Tensile strength (X–Y) | Data sheet |
| --- | --- | --- |
| Bambu Lab **PAHT-CF** | 88 ± 7 MPa | [TDS](https://cdn.shopify.com/s/files/1/0380/5149/files/Bambu_PAHT-CF_Technical_Data_Sheet.pdf) |
| Bambu Lab **PA6-CF** (current build) | 102 ± 7 MPa | [TDS](https://polyalkemi.no/wp-content/uploads/2024/01/Bambu_PA6-CF_Technical_Data_Sheet-v2.pdf) |

Broadly, **any filament with a printed-part tensile strength of roughly
85 MPa or more (X–Y) should work**. Check the manufacturer's technical data
sheet for printed specimens, not the raw filament. Do **not** use plain PLA or
PETG for the Foot.

Nylon absorbs moisture, which weakens the print. Dry the filament before
printing, following the manufacturer's data sheet, and print from a dry box.

### Print settings

| Setting | Value |
| --- | --- |
| Infill | **80% or more** |
| Orientation | Foot bed flat on the build plate, or tilted up to **20° toe-up** |

Why this orientation: 3D-printed parts are weakest where one layer joins the
next. With the foot bed flat, the pylon clamp's hoop stress (from tightening
the clamp bolts) and the load spread across the foot bed both run *along*
the layers. A tilt of up to 20° toe-up has also been tested.

The **Sole** is not structural and can be printed in a tougher, more flexible
material.

### Installing the heat-set inserts

The Foot uses tapered brass heat-set inserts. The holes are already shaped to
fit them, so no drilling is needed.

| Location | Qty | Insert | McMaster-Carr |
| --- | --- | --- | --- |
| Cleat mount | 2 | M5 × 0.8, tapered | [94180A361](https://www.mcmaster.com/94180A361/) |
| Pylon clamp | 2 | M4 × 0.7, 7.9 mm long, tapered | [94180A353](https://www.mcmaster.com/94180A353/) |

The pocket sizes also match E-Z LOK tapered inserts
([dimensional drawing](https://www.ezlok.com/assets/documents/dimensional_drawings/DimDwg_Ultra_Tapered.pdf)).

1. Let the print cool completely. Clear any stringing or debris from the
   holes.
2. Fit a soldering iron with a heat-set insert tip that matches the thread
   size, and set it to about your filament's printing temperature.
3. Put the insert in the hole, small end down, and check that it is square.
   Install the **cleat inserts from the top of the foot bed**, so they sit on
   the shelf and the cleat pulls them *into* the part rather than out of it.
4. Press down gently and let the heat do the work. Don't force it. Stop when
   the insert is flush with the surface.
5. While the plastic is still soft, take the iron away and press the insert
   flat with something cool and flat, such as the side of a wrench, to keep
   it square. Hold it for a few seconds.
6. Let it cool fully. Then test-fit each bolt by hand before the final
   assembly.

### Bolts and assembly

| Item | Qty | Notes |
| --- | --- | --- |
| M4 × 20 mm socket head cap screw | 2 | Pylon clamp. Passes through the 4.3 mm clearance holes into the M4 inserts. |
| Cleat and M5 cleat bolts | 1 set | SPD or Crank Brothers, as supplied with your pedals |
| Crankbrothers MTB Shoe Shields | 1 | Thin metal plate fitted between the cleat and the print |

1. Fit a **Crankbrothers Shoe Shield** between the cleat and the foot bed. It
   protects the printed surface from the cleat digging in and wearing it
   away. You may need slightly longer cleat bolts to allow for its thickness.
   Check that each bolt engages the full length of its insert.
2. Bolt the cleat on through the shield into the M5 inserts.
3. Slide the Foot onto the pylon and tighten the two M4 clamp bolts evenly.
   Check that the foot can't rotate on the pylon before you ride.

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

Hardware (inserts, bolts, cleat) is listed under
[Printing & setup](#printing--setup).

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
