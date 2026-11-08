"""Regenerate STEP and STL exports from the FreeCAD source model.

Usage (from the repo root):
    freecadcmd tools/export.py        # or: freecad.cmd tools/export.py (snap)

Recomputes cad/cycle_foot.FCStd and writes:
    exports/step/cycle_foot-<part>.step
    exports/stl/cycle_foot-<part>.stl
"""
import os
import FreeCAD
import Mesh
import MeshPart

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SOURCE = os.path.join(ROOT, "cad", "cycle_foot.FCStd")

# Object label in the model -> output file stem
PARTS = {
    "Foot": "cycle_foot-foot",
    "Sole": "cycle_foot-sole",
}

doc = FreeCAD.openDocument(SOURCE)
doc.recompute()

for label, stem in PARTS.items():
    objs = doc.getObjectsByLabel(label)
    if not objs:
        raise SystemExit(f"Object labelled '{label}' not found in {SOURCE}")
    shape = objs[0].Shape
    if shape.isNull() or not shape.isValid():
        raise SystemExit(f"'{label}' has an invalid shape after recompute")

    step_path = os.path.join(ROOT, "exports", "step", stem + ".step")
    stl_path = os.path.join(ROOT, "exports", "stl", stem + ".stl")
    os.makedirs(os.path.dirname(step_path), exist_ok=True)
    os.makedirs(os.path.dirname(stl_path), exist_ok=True)

    shape.exportStep(step_path)
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02,
                                  AngularDeflection=0.0872665, Relative=False)
    mesh.write(stl_path)
    print(f"{label}: volume {shape.Volume/1000:.1f} cm^3, "
          f"{mesh.CountFacets} facets -> {os.path.relpath(stl_path, ROOT)}")

FreeCAD.closeDocument(doc.Name)
