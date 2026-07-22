"""Fig 2 - Thrust convergence history.
Reads the OpenFOAM forces function-object output directly, so the plot is
reproduced from the raw solver data. Column 1 (0-indexed) is total Fx.

Note: for this loaded, high-pitch propeller the steady frozen-rotor MRF does
NOT reach a fixed plateau - K_T drifts slowly upward at stable residuals,
which is the direct signature of the method's steady ceiling (see report S5).
"""
import numpy as np, matplotlib.pyplot as plt, sys

path = sys.argv[1] if len(sys.argv) > 1 else 'postProcessing/forces/0/force.dat'
d  = np.loadtxt(path, comments='#')
it, Fx = d[:, 0], d[:, 1]
KT = Fx / 878.0

# characterise the post-transient part (drift, not a plateau)
post = it >= 500
kt_lo, kt_hi = KT[post].min(), KT[post].max()

fig, ax = plt.subplots(figsize=(6.4, 4.0))
ax.plot(it, KT, color='#1f4e79', lw=0.8)
ax.axhline(0.489, color='#c00000', lw=1.3, label='SVA K$_T$ = 0.489')
ax.annotate('no steady plateau:\nslow upward drift at\nstable residuals\n(MRF ceiling)',
            xy=(it[-1], KT[post][-20:].mean()),
            xytext=(0.42, 0.62), textcoords='axes fraction',
            fontsize=8.5, color='#1f4e79',
            arrowprops=dict(arrowstyle='->', color='#1f4e79', lw=1))
ax.text(0.02, 0.96,
        f'post-transient K$_T$ spans {kt_lo:.2f} – {kt_hi:.2f}',
        transform=ax.transAxes, fontsize=8.5, va='top', color='#333333')
ax.set_xlabel('SIMPLE iteration')
ax.set_ylabel('K$_T$  (= F$_x$ / 878)')
ax.set_title('Thrust history — steady MRF does not converge to a plateau')
ax.grid(True, alpha=0.3)
ax.legend(frameon=False, fontsize=8.5, loc='lower right')
fig.tight_layout(); fig.savefig('fig2_convergence.png', dpi=150)
print(f'fig2 ok  post-transient K_T span [{kt_lo:.3f}, {kt_hi:.3f}]')
