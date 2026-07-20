import os, math
import Mesh

m = Mesh.Mesh(os.environ["STL_IN"])
pts = [(p.x, p.y, p.z) for p in m.Points]

xs = [p[0] for p in pts]
xmin, xmax = min(xs), max(xs)
n = 40
w = (xmax - xmin) / n
best = [0.0] * n

for x, y, z in pts:
    i = min(int((x - xmin) / w), n - 1)
    r = math.hypot(y, z)
    if r > best[i]:
        best[i] = r

print("x_lo      x_hi      r_max")
for i in range(n):
    lo = xmin + i * w
    print("%8.4f  %8.4f  %8.4f  %s" %
          (lo, lo + w, best[i], "#" * int(best[i] * 200)))
