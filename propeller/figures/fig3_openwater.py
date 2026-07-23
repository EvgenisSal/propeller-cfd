"""Fig 3 - Open-water coefficients at J = 0.8, CFD vs SVA.
Standard open-water axes: K_T, 10*K_Q, eta_O. CFD bars carry the
oscillation range as error bars; SVA are the Potsdam experimental values.
"""
import matplotlib.pyplot as plt, numpy as np

labels = ['K$_T$', '10·K$_Q$', r'$\eta_O$']
cfd_mean = [1.007, 2.206, 0.581]
cfd_lo   = [0.943, 2.071, 0.577]
cfd_hi   = [1.058, 2.311, 0.584]
sva      = [0.489, 1.22, 0.525]

x = np.arange(len(labels)); w = 0.36
err = [np.array(cfd_mean)-np.array(cfd_lo), np.array(cfd_hi)-np.array(cfd_mean)]

fig, ax = plt.subplots(figsize=(6.0, 4.0))
ax.bar(x-w/2, cfd_mean, w, yerr=err, capsize=4, color='#1f4e79',
       label='CFD (steady MRF, 277k cells)')
ax.bar(x+w/2, sva, w, color='#c00000', label='SVA experiment')
for i,(c,s) in enumerate(zip(cfd_mean,sva)):
    ax.text(i-w/2, c+0.09, f'{c:.2f}', ha='center', fontsize=8)
    ax.text(i+w/2, s+0.03, f'{s:.2f}', ha='center', fontsize=8)
ax.set_xticks(x); ax.set_xticklabels(labels)
ax.set_ylabel('coefficient value')
ax.set_title('Open-water performance at J = 0.8')
ax.grid(True, axis='y', alpha=0.3); ax.legend(frameon=False, fontsize=8.5)
fig.tight_layout(); fig.savefig('fig3_openwater.png', dpi=150)
print('fig3 ok')
