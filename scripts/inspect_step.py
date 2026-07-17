import os
import FreeCAD, Part

doc = FreeCAD.newDocument("insp")
Part.insert(os.environ["STEP_IN"], "insp")

for o in doc.Objects:
    if not hasattr(o, "Shape"):
        continue
    s = o.Shape
    bb = s.BoundBox
    print("---")
    print("  label   :", o.Label)
    print("  type    :", s.ShapeType)
    print("  solids  :", len(s.Solids), " faces:", len(s.Faces))
    print("  valid   :", s.isValid(), " closed:", s.isClosed() if s.Solids else "n/a")
    print("  bbox    : %.4g x %.4g x %.4g" % (bb.XLength, bb.YLength, bb.ZLength))
    try:
        print("  volume  : %.4g" % s.Volume)
    except Exception as e:
        print("  volume  : FAILED")
