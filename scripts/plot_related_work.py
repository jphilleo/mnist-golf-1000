"""Plot primary-source accuracy/size pairs; no inference or test-data access."""
import json, os
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR','/private/tmp/mnist-golf-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter
R=Path(__file__).resolve().parents[1]
D=json.loads((R/'results/related-work-points.json').read_text())
visible=[r for r in D['rows'] if r['test_accuracy_percent']>96 and r['bytes_for_plot']<=3000]
assert len(visible)==7
BG='#FAF8F3';INK='#172B35';GRAY='#6A7B82';TEAL='#007F73';GRID='#DDDFD8'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'text.color':INK,'axes.labelcolor':GRAY,'xtick.color':GRAY,'ytick.color':GRAY,'axes.edgecolor':GRID,'axes.spines.top':False,'axes.spines.right':False,'figure.facecolor':BG,'axes.facecolor':BG,'svg.fonttype':'none'})
fig=plt.figure(figsize=(14,8))
fig.text(.065,.94,'MNIST: accuracy and model size',fontsize=29,weight='bold')
ax=fig.add_axes([.085,.25,.85,.60])
ax.set_xlim(0,3000);ax.set_ylim(96,100)
ax.set_xticks(range(0,3001,500));ax.set_yticks([96,97,98,99,100])
ax.xaxis.set_major_formatter(FuncFormatter(lambda x,p:f'{x:,.0f}'))
ax.yaxis.set_major_formatter(FuncFormatter(lambda y,p:f'{y:g}%'))
ax.grid(color=GRID,linewidth=.65);ax.set_axisbelow(True)
ax.set_xlabel('Reported size (bytes)',labelpad=12);ax.set_ylabel('Test accuracy',labelpad=12)
# Prior reported Pareto frontier: lower size and higher accuracy are better.
prior=[r for r in visible if r['id']!='ours']
frontier=sorted([r for r in prior if not any(
 q['bytes_for_plot']<=r['bytes_for_plot'] and q['test_accuracy_percent']>=r['test_accuracy_percent']
 and (q['bytes_for_plot']<r['bytes_for_plot'] or q['test_accuracy_percent']>r['test_accuracy_percent'])
 for q in prior)],key=lambda r:r['bytes_for_plot'])
assert [r['id'] for r in frontier]==['kilobyte-1024','kilobyte-2048','miracle-small','scaling']
ax.plot([r['bytes_for_plot'] for r in frontier],[r['test_accuracy_percent'] for r in frontier],color=GRAY,alpha=.28,lw=2,zorder=2)
for row in visible:
 x,y=row['bytes_for_plot'],row['test_accuracy_percent']
 if row['id']=='ours':ax.scatter(x,y,marker='*',s=270,c=TEAL,edgecolors=BG,linewidths=.7,zorder=6)
 elif row['scope']=='code_and_model':ax.scatter(x,y,marker='s',s=70,c=GRAY,edgecolors=BG,linewidths=.7,zorder=4)
 else:ax.scatter(x,y,marker='o',s=75,facecolors=BG,edgecolors=GRAY,linewidths=1.5,zorder=4)
rows={r['id']:r for r in visible}
def note(id,label,position,color=GRAY,bold=False):
 r=rows[id]
 ax.annotate(label,(r['bytes_for_plot'],r['test_accuracy_percent']),xytext=position,textcoords='data',ha='left',va='center',fontsize=10.5,color=color,weight='bold' if bold else 'normal',bbox=dict(facecolor=BG,edgecolor='none',pad=2))
note('ours','Philleo-993\n993 B, 99.25%',(750,99.58),TEAL,True)
note('scaling','Scaling Discovery\n1,957 B, 99.41%',(1700,99.74))
note('tiny-repro','tiny_MNIST reproduction\n2,461 B, 99.40%',(2320,99.70))
note('miracle-small','MIRACLE\n≈1,520 B, 99.04%',(1420,98.78))
note('kilobyte-4096','Seed + learned code\n2,060 B, 98.60%',(2120,98.43))
note('kilobyte-2048','Seed + learned code\n1,036 B, 97.94%',(1090,97.76))
note('kilobyte-1024','Seed + learned code\n524 B, 96.41%',(570,96.40))
handles=[Line2D([],[],marker='*',color='none',markerfacecolor=TEAL,markeredgecolor=TEAL,markersize=14,label='This project: code + model data'),Line2D([],[],marker='s',color='none',markerfacecolor=GRAY,markeredgecolor=GRAY,markersize=8,label='Other code + model data'),Line2D([],[],marker='o',color='none',markerfacecolor=BG,markeredgecolor=GRAY,markersize=8,label='Model/weight payload only')]
handles.append(Line2D([],[],color=GRAY,alpha=.35,lw=2,label='Prior reported frontier'))
fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.075),frameon=False,ncol=2,fontsize=10.5,handletextpad=.5,columnspacing=1.6)
for ext in ('png','svg'):fig.savefig(R/'figures'/f'related-work.{ext}',dpi=400,facecolor=BG)
plt.close(fig)
print('Rendered one linear graph: 0–3,000 bytes and 96–100% accuracy.')
