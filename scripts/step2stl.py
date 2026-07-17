import os
import FreeCAD, Part, MeshPart

step_in    = os.environ["STEP_IN"]
stl_out    = os.environ["STL_OUT"]
deflection = float(os.environ["DEFLECTION"])
scale      = float(os.environ.get("SCALE", "1.0"))

doc = FreeCAD.newDocument("conv")
Part.insert(step_in, "conv")

# keep only real solids - empty compounds poison the bounding box
shapes = [o.Shape for o in doc.Objects
          if hasattr(o, "Shape") and len(o.Shape.Solids) > 0]
print("solids kept:", len(shapes))
if not shapes:
    raise SystemExit("no solids found")

comp = Part.makeCompound(shapes)
bb = comp.BoundBox
print("bbox (file units): %.3f x %.3f x %.3f" % (bb.XLength, bb.YLength, bb.ZLength))

m = MeshPart.meshFromShape(Shape=comp,
                           LinearDeflection=deflection,
                           AngularDeflection=0.174533,
                           Relative=False)
print("triangles:", m.CountFacets)

if scale != 1.0:
    mat = FreeCAD.Matrix()
    mat.scale(scale, scale, scale)
    m.transform(mat)
    b = m.BoundBox
    print("bbox after scale: %.4f x %.4f x %.4f" % (b.XLength, b.YLength, b.ZLength))

os.makedirs(os.path.dirname(stl_out), exist_ok=True)
m.write(stl_out)
print("written:", stl_out)
