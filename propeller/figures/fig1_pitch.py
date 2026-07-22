"""Fig 1 - Blade pitch verification.
Measured P/D (from the STL geometry, via pitch_verify.py) vs the VP1304
design value at r/R = 0.7. Confirms the imported geometry is at design pitch.
"""
import matplotlib.pyplot as plt

r_R      = [0.5, 0.7, 0.9]      # radial stations analysed
PoD_meas = [1.59, 1.65, 1.57]   # measured mean over all 5 blades
PoD_design_07 = 1.635           # SVA design value at 0.7R

fig, ax = plt.subplots(figsize=(5.2, 4.0))
ax.plot(r_R, PoD_meas, 'o-', color='#1f4e79', lw=1.8, ms=7,
        label='Measured from STL (5-blade mean)')
ax.plot(0.7, PoD_design_07, 's', color='#c00000', ms=9,
        label='SVA design, 0.7R (1.635)')
ax.annotate(f'measured 1.65\ndesign 1.635\n(+1.1%)',
            xy=(0.7, 1.65), xytext=(0.735, 1.60),
            fontsize=8.5, color='#333333')
ax.set_xlabel('r / R')
ax.set_ylabel('P / D')
ax.set_title('Blade pitch verification')
ax.set_xlim(0.45, 0.95); ax.set_ylim(1.45, 1.75)
ax.grid(True, alpha=0.3); ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout(); fig.savefig('fig1_pitch.png', dpi=150)
print('fig1 ok')
