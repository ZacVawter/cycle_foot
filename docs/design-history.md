# Design History & Requirements

Requirements and lessons learned across every revision of the cycle foot.
Converted from the original Google Doc design notes (Oct 2023 – May 2026).

## Product requirement

Provide a prosthetic foot for mountain biking and cycling that weighs less than
a normal prosthetic foot with a cycling shoe, and less than a human foot.

## Technical requirements

These are the current "live" requirements, built up from what each revision
taught us.

### Pylon-to-cleat interface

- Supported cleat styles:
  - Crank Brothers
  - SPD
- Side-to-side clearance: **40 mm**
- Rib height: **7 mm** (measured from a few shoes)
- Cleat mounting through-holes:
  - Diameter: M4 bolt
  - Centre-to-centre: **14 mm**
- Toe to hole centreline: **25 mm**
  - V1 used 15 mm. That was enough for Crank Brothers Egg Beaters but not for
    SPD. Even the Egg Beaters barely fit, and the material at the edge started
    deforming after a few rides.

### Dimensions

- Pylon diameter: **30 mm**
- Pylon centreline to cleat centreline: **70 mm**
  - V1 used 60 mm, which caused the problem described below.
  - This distance matters for users of the **Össur Total Knee**. If it is too
    short, the rider can't create a large enough moment to unlock the knee.

### Loads

- **Z (vertical axis)**
  - The ISO 4210-2 test standard specifies **1500 N** applied to the centre of
    the pedal. This is the minimum design test load at the cleat.
  - Safety factor: **2×**
- **Toe torsional axis**
  - Some torsional compliance in the toe can be useful. It lets the rider's hip
    move sideways away from the bike without unclipping the cleat from the
    pedal.
  - Rough experimental data suggests about **80 N·m**.

### Materials

- The foot will sometimes hit the bicycle, for example in a tip-over or a minor
  crash.
  - Keeping point-impact forces low limits damage to carbon frames.
  - For example, sharp aluminium corners create very large forces on impact.
  - **This is a very important requirement.** A carbon frame costs thousands,
    and a single impact can compromise its structural integrity.
- Materials tested so far:
  - Rev 0: ABS, chosen because it was easy to get and work with
  - Rev 1: Delrin (acetal)

### Weight

Keep weight as low as possible once the other requirements are met. If weight
didn't matter, you could just put a cycling shoe on a prosthetic foot.

| Reference | Weight |
| --- | --- |
| Human foot | ~1 kg |
| Prosthetic foot | ~0.5 kg |
| Cycling shoe | ~0.35 kg |
| **Cycle foot V1** (cleat included) | **0.2 kg** |

## Versions & lessons learned

### V0.1 – V0.5: ABS prototypes

Different thicknesses and shapes of ABS, cut with a hacksaw and a drill.

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

- Uses heat-set threaded inserts:
  - M4 bolts (cleat): [McMaster-Carr 94180A361](https://www.mcmaster.com/94180A361/)
  - M4 tapered heat-set inserts for plastic:
    [McMaster-Carr category](https://www.mcmaster.com/products/threaded-inserts/for-use-in~plastic-1/tapered-heat-set-inserts-for-plastic-7/thread-type~metric/)
    (link may be broken).
    [E-Z LOK manufacturer spec sheet](https://www.ezlok.com/assets/documents/dimensional_drawings/DimDwg_Ultra_Tapered.pdf)
  - M3 bolts: [McMaster-Carr 94180A333](https://www.mcmaster.com/94180A333/)
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

Every version is tagged in git (`v0` – `v3.7`) with its STEP/STL exports.
