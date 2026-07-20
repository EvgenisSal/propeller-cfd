import os
import FreeCAD, Part, MeshPart
from FreeCAD import Vector

step_in    = os.environ["STEP_IN"]
stl_out    = os.environ["STL_OUT"]
deflection = float(os.environ["DEFLECTION"])
scale      = float(os.environ.get("SCALE", "1.0"))

# shaft extension, file units (mm)
x_start    = float(os.environ["SHAFT_X_START"])   # upstream end, past the inlet
x_join     = float(os.environ["SHAFT_X_JOIN"])    # inside the existing shaft
r_shaft    = float(os.environ["SHAFT_R"])

doc = FreeCAD.newDocument("fuse")
Part.insert(step_in, "fuse")

solids = [o.Shape for o in doc.Objects
          if hasattr(o, "Shape") and len(o.Shape.Solids) > 0]
if len(solids) != 1:
    raise SystemExit("expected exactly 1 solid, got %d" % len(solids))
prop = solids[0]
print("propeller volume: %.4g" % prop.Volume)

ext = Part.makeCylinder(r_shaft, x_join - x_start,
                        Vector(x_start, 0, 0), Vector(1, 0, 0))
print("extension volume: %.4g" % ext.Volume)

fused = prop.fuse(ext)
fused = fused.removeSplitter()      # merge coplanar faces from the seam

print("--- fused")
print("  solids :", len(fused.Solids), " faces:", len(fused.Faces))
print("  valid  :", fused.isValid(), " closed:", fused.isClosed())
print("  volume : %.4g" % fused.Volume)
bb = fused.BoundBox
print("  bbox   : X %.3f..%.3f  Y %.3f..%.3f  Z %.3f..%.3f" %
      (bb.XMin, bb.XMax, bb.YMin, bb.YMax, bb.ZMin, bb.ZMax))

if len(fused.Solids) != 1 or not fused.isClosed():
    raise SystemExit("fuse failed - not a single closed solid")

m = MeshPart.meshFromShape(Shape=fused,
                           LinearDeflection=deflection,
                           AngularDeflection=0.174533,
                           Relative=False)
print("triangles:", m.CountFacets)

if scale != 1.0:
    mat = FreeCAD.Matrix()
    mat.scale(scale, scale, scale)
    m.transform(mat)
    b = m.BoundBox
    print("bbox after scale: X %.4f..%.4f" % (b.XMin, b.XMax))

os.makedirs(os.path.dirname(stl_out), exist_ok=True)
m.write(stl_out)
print("written:", stl_out)
