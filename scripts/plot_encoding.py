import os,json
from pathlib import Path
# Uses the standard Matplotlib cache directory.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
rows=json.loads((R/'results/figure-data.json').read_text())['encoding_variants']
BG='#FAF8F3';INK='#172B35';MUTED='#66747A';TEAL='#007F73';GRID='#DCDDD5'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'text.color':INK,'axes.labelcolor':MUTED,'xtick.color':MUTED,'ytick.color':MUTED,'axes.edgecolor':GRID,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':BG,'axes.facecolor':BG,'svg.fonttype':'none'})
fig=plt.figure(figsize=(13,6.4))
fig.text(.065,.89,'Encoding size',size=26,weight='bold')
fig.text(.065,.82,'Alternative encodings of the same checkpoint',size=12,color=MUTED)
ax=fig.add_axes([.36,.17,.52,.54])
for i,r in enumerate(rows):
 ax.plot([990,r['bytes']],[i,i],color=GRID,lw=2)
 ax.scatter(r['bytes'],i,s=100,color=TEAL if i==5 else '#7B8C90',zorder=3)
 ax.text(r['bytes']+.45,i,f"{r['bytes']:,} B",va='center',fontsize=11,weight='bold' if i==5 else 'normal')
ax.set_yticks(range(6),[r['label'] for r in rows],fontsize=11);ax.invert_yaxis();ax.set_ylim(5.6,-.6)
ax.set_xlim(990,1014);ax.set_xticks([990,995,1000,1005,1010]);ax.grid(axis='x',color=GRID,ls=':',alpha=.7);ax.set_axisbelow(True);ax.tick_params(axis='y',length=0,pad=12)
ax.spines['left'].set_visible(False);ax.set_xlabel('Compressed file size (bytes)',labelpad=12)
for ext in ('png','svg'):fig.savefig(R/'figures'/f'encoding.{ext}',dpi=300,facecolor=BG)
