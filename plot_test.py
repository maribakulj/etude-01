import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
from test_noyau import harmonic, music_box, roughness, fusion, rs, cents, JUST

def curves(spec, bw=1.0, w=25.0):
    C=np.array([-roughness(spec,r,bw_scale=bw) for r in rs])
    P=np.array([ fusion(spec,r,w_cents=w)      for r in rs])
    Cn=(C-C.min())/(C.max()-C.min()); Pn=P/P.max()
    return Cn,Pn

fig,ax=plt.subplots(2,1,figsize=(11,7),sharex=True)
for a,(spec,lab) in zip(ax,[(harmonic(),'Timbre harmonique'),(music_box(),'Boîte à musique (1:6.27:17.55:…)')]):
    Cn,Pn=curves(spec)
    a.plot(cents,Cn,color='#2a6f97',lw=1.6,label='C — consonance (−rugosité)')
    a.plot(cents,Pn,color='#c1121f',lw=1.6,label='Φ — fusion (coïncidence)')
    for nm,c in JUST.items():
        a.axvline(c,color='0.85',lw=0.8,zorder=0)
        a.text(c,1.02,nm,ha='center',va='bottom',fontsize=7,color='0.5')
    a.set_title(lab,fontsize=11,loc='left'); a.set_ylabel('normalisé'); a.set_ylim(0,1.08)
    a.legend(fontsize=8,loc='upper left')
ax[1].set_xlabel('intervalle (cents) — unisson → octave')
plt.tight_layout(); plt.savefig('/home/claude/out/courbes.png',dpi=130)
print("ok")
