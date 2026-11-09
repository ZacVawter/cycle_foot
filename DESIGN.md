# Cycle Foot: Design Notes

This file is for people who want to modify the design, re-run the analysis, or
understand why it looks the way it does. To **print and fit** the foot, the
[README](README.md) has everything you need.

- [Repository layout](#repository-layout)
- [Parts](#parts)
- [Customising for your leg](#customising-for-your-leg)
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

### Current setup

| Item | Setting |
| --- | --- |
| Solver | CalculiX (`SolverCcxTools`), linear static |
| Mesh | Gmsh (`FEMMeshGmsh`), 2nd-order tetrahedra, min. element size 0.6 mm (~31k elements, ~54k nodes) |
| Material | `PEHT` material object: Young's modulus 2.18 GPa (316,182 psi), Poisson's ratio 0.36 |
| Fixed constraint | `ConstraintFixed`, two faces of the `Toe_Anchors` feature |
| Load | `ConstraintForce`, **500 N** normal to one face of the `Toe_Anchors` feature |

The modulus is close to Bambu PA6-CF's published Z-direction (between-layer)
value of 2.17 GPa. That is a conservative choice, because the Z direction is
the weakest direction of a print.

### Last recorded results (v3.7, 500 N load)

| Result | Value |
| --- | --- |
| Max von Mises stress | 83 MPa |
| Max displacement | 2.0 mm |

Peak stresses in a linear analysis often sit at the edges of fixed faces or at
sharp corners, and are partly an artefact of the model there. Look at where the
peak is, not only at its value, and compare the stress in the main load paths
(gusset, pylon clamp, foot bed) with the material's strength.

### Re-running after a change

1. Open `cad/cycle_foot.FCStd` and switch to the **FEM** workbench.
2. **Material change:** edit the `PEHT` material object and enter the new
   filament's Young's modulus and Poisson's ratio from its technical data
   sheet. Use the Z-direction values if they are given.
3. **Geometry change:** double-click `ConstraintFixed` and `ConstraintForce`
   and check that they still highlight the intended faces. FreeCAD refers to
   faces by number (`Face38`, `Face86` …), and these numbers can shift when
   the geometry changes, which silently moves the constraints.
4. Right-click `FEMMeshGmsh` and regenerate the mesh.
5. Double-click `SolverCcxTools`, then write the input file and run CalculiX.
6. Open `Pipeline_CCX_Results` and view the von Mises stress and
   displacement. Compare them with the results above.

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
  - The ISO 4210-2 test standard specifies **1500 N** applied to the centre of
    the pedal. This is the minimum design test load at the cleat.
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
  - FEA re-run for the current geometry

Printed in Bambu PAHT-CF and PA6-CF (current build) and ridden since
December 2023. See the [README](README.md) for the riding record.

## Previous versions

Each design revision is a tagged commit (`v0` … `v3.7`) with its STEP and STL
exports, so you can download or compare any earlier version from the
[tags page](https://github.com/ZacVawter/cycle_foot/tags). Run
`git log --stat` to see how the design evolved.
