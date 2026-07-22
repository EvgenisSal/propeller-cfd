"""Fig 4 - K_T across the mesh and near-wall interventions.
Visual companion to the exclusion table: every mesh/near-wall change left
K_T far above the experiment, i.e. the offset is not discretisation-driven.
"""
import matplotlib.pyplot as plt, numpy as np

cfg = ['coarse\nnutk\n(12% cov.)', '79% cov.\nnutk',
       '79% cov.\nSpalding', 'refined 277k\n+ farfield BC']
KT  = [0.985, 0.90, 0.87, 0.82]

fig, ax = plt.subplots(figsize=(6.2, 4.0))
ax.plot(range(len(cfg)), KT, 'o-', color='#1f4e79', lw=1.8, ms=8)
ax.axhline(0.489, color='#c00000', lw=1.3, label='SVA K$_T$ = 0.489')
for i,k in enumerate(KT):
    ax.text(i, k+0.012, f'{k:.2f}', ha='center', fontsize=8.5)
ax.set_xticks(range(len(cfg))); ax.set_xticklabels(cfg, fontsize=8)
ax.set_ylabel('K$_T$')
ax.set_title('K$_T$ is insensitive to mesh / near-wall refinement')
ax.set_ylim(0.42, 1.05)
ax.grid(True, axis='y', alpha=0.3); ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout(); fig.savefig('fig4_campaign.png', dpi=150)
print('fig4 ok')
