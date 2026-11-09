# Cycle Foot: Design Notes

This file is for people who want to modify the design, re-run the analysis, or
understand why it looks the way it does. To **print and fit** the foot, the
[README](README.md) has everything you need.

- [Repository layout](#repository-layout)
- [Parts](#parts)
- [Design parameters](#design-parameters)
- [Structural analysis (FEA)](#structural-analysis-fea)
- [Requirements](#requirements)
- [Previous learnings](#previous-learnings)
- [Previous versions](#previous-versions)

## Repository layout

| Path | Contents |
| --- | --- |
| `cad/cycle_foot.FCStd` | **Source model** (FreeCAD 1.x, current version v3.7), including the FEA setup. Edit this one. |
| `exports/step/` | STEP files for each part, for use in other CAD software |
| `exports/stl/` | STL files ready to slice and print |
| `docs/images/` | Renderings and photos |
| `tools/export.py` | Script that regenerates `exports/` from the source model |

## Parts

| Part | File | Notes |
| --- | --- | --- |
| Foot | `exports/stl/cycle_foot-foot.stl` | Pylon clamp, gusset and cleat mount. Structural part. |
| Sole | `exports/stl/cycle_foot-sole.stl` | TPU walking shell with Z-grip pattern and mud ramp |

## Design parameters

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

The insert pocket sizes (`insert_m4_*`, `insert_m3_*`) come from the E-Z LOK
tapered insert drawings and are also in the spreadsheet.

After editing, regenerate the print files:

```sh
freecadcmd tools/export.py      # Snap install: freecad.cmd tools/export.py
```

**After any geometry or material change, re-run the FEA below** before you
print and ride.

## Structural analysis (FEA)

The model includes a FreeCAD FEM analysis (`Analysis` in the model tree). It is
set up so you can re-run it after changing the design or the material.

### Load case

The design load comes from the bicycle pedal static strength test in
**ISO 4210-8**, which applies **1500 N** to the pedal. The 2023 edition allows
the force on clipless pedals to be applied through a cleat, which is how load
enters this foot. With the **2× safety factor** from the requirements, the
analysis applies **3000 N**.

### Setup

| Item | Setting |
| --- | --- |
| Solver | CalculiX (`SolverCcxTools`), linear static |
| Mesh | Gmsh (`FEMMeshGmsh`), 2nd-order tetrahedra with straight sides (`SecondOrderLinear` = true), min. element size 0.6 mm (~22k elements, ~38k nodes) |
| Material | `PEHT` material object: Young's modulus 2.18 GPa (316,182 psi), Poisson's ratio 0.36 |
| Fixed constraint | `ConstraintFixed`: the pylon bore (`Face38` and `Face16`, the two halves of the 30 mm bore) |
| Load | `ConstraintForce`: **3000 N** upward on the cleat pad (`Face86`, the underside of the foot bed under the cleat) |

The modulus is close to Bambu PA6-CF's published Z-direction (between-layer)
value of 2.17 GPa. A single isotropic modulus is a simplification. A printed
part is anisotropic, and choosing a low modulus does not by itself make the
predicted stresses conservative.

### Results (v3.7, 3000 N): indicative only

| Region | Max von Mises | Max tension (principal) |
| --- | --- | --- |
| Foot bed, at the edge of the rear cleat insert hole (overall peak) | 58 MPa | — |
| Foot bed, away from holes and constraints | — | 19 MPa (underside, between cleat and pylon) |
| Gusset | 31 MPa | 14 MPa |
| Pylon clamp | 18 MPa | 13 MPa |
| **Whole part** | **58 MPa** | **21 MPa** |

Max displacement: 2.5 mm.

**How to read this.** These results are **indicative, not a demonstrated
safety factor**. They are most useful for showing where stress concentrates
and for comparing design changes against each other.

For reference only: the peak tension (21 MPa) and peak von Mises stress
(58 MPa) are below the published specimen strengths of the filaments used
(Bambu PAHT-CF, 64 MPa between layers; PA6-CF, 102 MPa in-plane). But specimen
strengths do not transfer directly to a printed part, and an isotropic solid
model cannot establish the safety margin of an anisotropic printed part.

The von Mises peak is at the edge of a cleat insert hole, which is modelled as
empty. How the brass insert changes the stress there depends on its contact
and loading, which are not modelled.

**Limits.** The model treats the part as solid and isotropic. A real print has
80%+ infill, different strength between and along layers, layer-bonding
variation from print to print, and brass inserts. It checks one static load
case. Impacts and fatigue from repeated pedal strokes are not modelled. The
riding record in the [README](README.md) is real-world experience from one
rider and one setup, not a substitute for testing.

### Validation

Because the analysis is only indicative, **validate representative printed
assemblies** with appropriate testing before relying on them. That means parts
printed in the same material, with the same settings and orientation, and
fitted with the same inserts, bolts, shoe shield and cleat. For example:

- **Static test:** load the assembly through a cleat clipped into a pedal, as
  in the ISO 4210-8 pedal static strength test (1500 N), and check for
  cracking, permanent deformation or insert pull-out.
- **Fatigue test:** apply repeated pedalling-level loads for many cycles, and
  inspect for cracks, especially around the cleat inserts, the gusset and the
  pylon clamp.

Test results, or more detailed analysis, are very welcome as contributions.

### Re-running after a change

1. Open `cad/cycle_foot.FCStd` and switch to the **FEM** workbench.
2. **Material change:** edit the `PEHT` material object and enter the new
   filament's Young's modulus and Poisson's ratio from its technical data
   sheet. Use the Z-direction values if they are given.
3. **Geometry change:** double-click `ConstraintFixed` and `ConstraintForce`
   and check that they still highlight the pylon bore and the cleat pad.
   FreeCAD refers to faces by number (`Face38`, `Face86` …), and these numbers
   can shift when the geometry changes, which silently moves the constraints.
4. **Always regenerate the mesh** (double-click `FEMMeshGmsh` and apply).
   FreeCAD does not do this automatically. A stale mesh still solves, but its
   results belong to the old geometry.
5. Double-click `SolverCcxTools`, then write the input file and run CalculiX.
6. Open `Pipeline_CCX_Results` and view the von Mises and max principal
   stress. Look at **where** the peaks are, not just their values, and compare
   them with the results above.

> **Watch the force units.** FreeCAD 1.x stores forces in mN internally
> (`mm·kg/s²`). A force entered in an older FreeCAD as a plain number such as
> `500` (meaning newtons) is read by 1.x as **0.5 N**. Always type the unit,
> for example `3000 N`. To check, open `ConstraintForce` and confirm it shows
> `3000 N` (or `3000000 mm·kg/s²`).

## Requirements

Converted from the original design notes (Oct 2023 – May 2026).

### Product requirement

Provide a prosthetic foot for mountain biking and cycling that weighs less than
a normal prosthetic foot with a cycling shoe, and less than a human foot.

### Technical requirements

These are the current "live" requirements, built up from what each revision
taught us.

#### Pylon-to-cleat interface

- Supported cleat styles:
  - Crank Brothers
  - SPD
- Side-to-side clearance: **40 mm**
- Rib height: **7 mm** (measured from a few shoes)
- Cleat mounting holes:
  - M5 cleat bolts into M5 heat-set inserts (the original notes said M4)
  - Centre-to-centre: **14 mm**
- Toe to hole centreline: **25 mm**
  - V1 used 15 mm. That was enough for Crank Brothers Egg Beaters but not for
    SPD. Even the Egg Beaters barely fit, and the material at the edge started
    deforming after a few rides.

#### Dimensions

- Pylon diameter: **30 mm**
- Pylon centreline to cleat centreline: **70 mm**
  - V1 used 60 mm, which caused the problem described below.
  - This distance matters for users of the **Össur Total Knee**. If it is too
    short, the rider can't create a large enough moment to unlock the knee.

#### Loads

- **Z (vertical axis)**
  - The bicycle pedal static strength test (ISO 4210-8, called up by the
    requirements in ISO 4210-2) applies **1500 N** to the centre of the pedal.
    This is the minimum design test load at the cleat.
  - Safety factor: **2×**
- **Toe torsional axis**
  - Some torsional compliance in the toe can be useful. It lets the rider's hip
    move sideways away from the bike without unclipping the cleat from the
    pedal.
  - Rough experimental data suggests about **80 N·m**.

#### Materials

- The foot will sometimes hit the bicycle, for example in a tip-over or a minor
  crash.
  - Keeping point-impact forces low limits damage to carbon frames.
  - For example, sharp aluminium corners create very large forces on impact.
  - **This is a very important requirement.** A carbon frame costs thousands,
    and a single impact can compromise its structural integrity. This is why
    the Sole is TPU.

#### Weight

Keep weight as low as possible once the other requirements are met. If weight
didn't matter, you could just put a cycling shoe on a prosthetic foot.

| Reference | Weight |
| --- | --- |
| Human foot | ~1 kg |
| Prosthetic foot | ~0.5 kg |
| Cycling shoe | ~0.35 kg |
| **Cycle foot V1** (cleat included) | **0.2 kg** |

## Previous learnings

### V0.1 – V0.5: ABS prototypes

Different thicknesses and shapes of ABS, cut with a hacksaw and a drill. ABS
was chosen because it was easy to get and work with.

- Many of the requirements above came from these prototypes.
- **The vertical load path is critical.** Get it wrong and the part breaks.
- **The side ribs are critical.** They carry load into the pedal so it doesn't
  all go through the cleat. That allows some side-to-side movement, with the
  ribs taking a large share of the load, without unclipping.
- The pylon-to-cleat distance determines whether the rider can unlock their
  knee.

### V1: machined Delrin

Lessons learned:

- The cleat-to-toe distance has to be long enough for the rider to clip in
  easily.
- Ideally the cleat mounting holes use the standard centre-to-centre spacing,
  so standard mounting hardware fits.
- Lengthen the pylon-to-cleat distance slightly (5–10 mm) to make unlocking the
  knee easier.
- Add a 3D-printed **lower wear plate** that covers the whole bottom of the
  foot:
  - The surface that wears from walking can be replaced.
  - The ribs can be a different material with some compliance for clipping
    in, similar to a cycling shoe sole.
- Ideally use threaded inserts installed from the top, with a "shelf" to sit
  on, for the cleat bolts to screw into.

### V2: threaded inserts and a separate sole

- Uses tapered brass heat-set inserts:
  - Cleat: M5 inserts, [McMaster-Carr 94180A361](https://www.mcmaster.com/94180A361/)
  - M3 inserts, [McMaster-Carr 94180A333](https://www.mcmaster.com/94180A333/)
    (probably for the sole bolt-on holes, removed in V3.7; unused in V3.7)
  - [E-Z LOK manufacturer spec sheet](https://www.ezlok.com/assets/documents/dimensional_drawings/DimDwg_Ultra_Tapered.pdf)
- Introduced the separate printed sole (the wear plate suggested after V1).

### V3 – V3.7: parametric FreeCAD model

The original notes stop at V2. The V3.x summaries below come from the CAD
files, apart from V3.7, which the designer described directly.

- **V3** (Oct 2023): small adjustment to the foot geometry.
- **V3.1** (Nov 2023): rebuilt around a `Parameters` spreadsheet (pylon
  diameter, pylon-to-cleat, cleat-to-toe), with pockets sized for E-Z LOK
  tapered inserts.
- **V3.5** (Nov 2023): added a three-bolt pylon tube clamp and M3 inserts, and
  remodelled the sole. Followed by adjustments for 3D printing.
- **V3.6** (Jan 2024): revised sole.
- **V3.7** (May 2026, current):
  - Removed the sole bolt-on holes
  - Strengthened the tube clamp
  - Made the tube clamp slot a printable feature
  - Added more Z-shaped grip patterns to the sole
  - FEA re-run at 3000 N (1500 N × 2) on a fresh mesh; see
    [Structural analysis](#structural-analysis-fea)

Printed in Bambu PAHT-CF and PA6-CF (current build) and ridden since
December 2023. See the [README](README.md) for the riding record.

## Previous versions

Each design revision is a tagged commit (`v0` … `v3.7`) with its STEP and STL
exports, so you can download or compare any earlier version from the
[tags page](https://github.com/ZacVawter/cycle_foot/tags). Run
`git log --stat` to see how the design evolved.
