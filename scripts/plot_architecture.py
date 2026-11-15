import os,json
from pathlib import Path
# Uses the standard Matplotlib cache directory.
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,Rectangle
from matplotlib.colors import LinearSegmentedColormap
import numpy as np
R=Path(__file__).resolve().parents[1];O=R/'figures';d=json.loads((R/'results/network-activations.json').read_text())
BG='#FAF8F3';INK='#172B35';TEAL='#007F73';GRAY='#657981';GRID='#D8DFD9';GOLD='#B67D27'
plt.rcParams.update({'font.family':'DejaVu Sans','text.color':INK,'figure.facecolor':BG,'axes.facecolor':BG,'svg.fonttype':'none'})
cm=LinearSegmentedColormap.from_list('response',['#F0F1EB','#8BC9B6',TEAL,'#133B42'])
f=plt.figure(figsize=(18,24))
def text(x,y,s,size=13,bold=False,color=INK,ha='left',va='baseline'):
 f.text(x,y,s,fontsize=size,weight='bold' if bold else 'normal',color=color,ha=ha,va=va,linespacing=1.5)
def line(x1,y1,x2,y2,color=GRID,lw=1):f.add_artist(plt.Line2D([x1,x2],[y1,y2],transform=f.transFigure,color=color,lw=lw))
def arrow(x1,y1,x2,y2,color=TEAL):f.add_artist(FancyArrowPatch((x1,y1),(x2,y2),transform=f.transFigure,arrowstyle='-|>',mutation_scale=18,lw=1.8,color=color))
def tile(rect,a,cmap='gray_r',vmax=1):
 ax=f.add_axes(rect);ax.imshow(a,cmap=cmap,vmin=0,vmax=vmax,interpolation='nearest');ax.set_axis_off();return ax
def phase(y,num,title,desc):
 text(.045,y,str(num),22,True,TEAL);text(.08,y,title,22,True);text(.08,y-.026,desc,12.5,color=GRAY)
text(.045,.966,'How 993 bytes recognize a handwritten digit',28,True)
text(.045,.937,'One image, four phases. The pictures and scores below come from the frozen model.',14,color=GRAY)
# Phase 1: image -> learned convolution -> eight maps.
phase(.895,1,'Turn pixels into eight response maps','Each filter scans 3 × 3 patches and responds to a different learned pattern.')
tile([.06,.765,.105,.07875],d['image'])
text(.1125,.749,'28 × 28 grayscale pixels',11,color=GRAY,ha='center')
arrow(.18,.807,.345,.807)
text(.262,.833,'8 learned filters',13,True,ha='center')
text(.262,.782,'Same filters at every position',10.5,color=GRAY,ha='center')
st=d['all_stages'][0]
for i,a in enumerate(st['values']):tile([.37+(i%4)*.065,.807-(i//4)*.048,.055,.04125],a,cm,st['maximum'])
text(.495,.741,'8 maps, each 28 × 28',11,color=GRAY,ha='center')
text(.695,.831,'These are eight responses to one image.',13,True)
text(.695,.807,'Each square keeps the image’s layout.\nDarker areas show where a filter\nresponds more strongly.',12,color=GRAY,va='top')
line(.045,.72,.955,.72)
# Phase 2: show both updates and each pool explicitly on a consistent channel.
phase(.694,2,'Update twice, shrink, then do it again','The four updates reuse one set of weights. Shrinking reduces the number of positions to process.')
xs=[.06,.245,.43,.615,.80];stageids=[0,2,3,5,6]
for x,idx,label in zip(xs,stageids,['28 × 28','28 × 28','14 × 14','14 × 14','7 × 7']):
 st=d['all_stages'][idx];tile([x,.566,.10,.075],st['values'][2],cm,st['maximum']);text(x+.05,.552,label,12,True,ha='center')
for j,lab in enumerate(['Update twice','Shrink','Update twice','Shrink']):
 arrow(xs[j]+.112,.606,xs[j+1]-.012,.606);text((xs[j]+.1+xs[j+1])/2,.65,lab,12,True,ha='center')
text(.06,.526,'What an update does',13,True)
text(.06,.508,'Mix information from all eight maps, add it to the existing maps,\nand replace negative values with zero. Do this twice.',12,color=GRAY,va='top')
text(.59,.526,'What shrinking does',13,True)
text(.59,.508,'Keep the largest number in each 2 × 2 patch.\nThat halves the width and height of every map.',12,color=GRAY,va='top')
text(.06,.469,'One of the eight maps is shown at each stage above; all eight are updated together.',10.5,color=GRAY)
line(.045,.451,.955,.451)
# Phase 3: one of six spatial averages, eight channel summaries, digit scores.
phase(.425,3,'Turn the maps into 48 numbers, then ten digit scores','Six regional averages per map preserve a rough sense of where the responses are.')
last=np.array(d['all_stages'][6]['values']);summary=np.array(d['all_stages'][7]['values'])
ax=tile([.06,.315,.10,.075],last[2],cm,d['all_stages'][6]['maximum'])
ax.add_patch(Rectangle((-.5,-.5),4,3,fill=False,edgecolor=GOLD,lw=2.2))
text(.11,.298,'One 7 × 7 map',11,True,ha='center')
arrow(.18,.35,.245,.35)
ax=tile([.265,.315,.06,.075],summary[2],cm,d['all_stages'][7]['maximum'])
ax.add_patch(Rectangle((-.5,-.5),1,1,fill=False,edgecolor=GOLD,lw=2.2))
for rr in range(3):
 for cc in range(2):
  val=summary[2,rr,cc];ax.text(cc,rr,f'{val:.0f}',ha='center',va='center',fontsize=11,color='white' if val>.5*d['all_stages'][7]['maximum'] else INK)
text(.295,.298,'6 regional averages',11,True,ha='center')
text(.295,.281,'3 rows × 2 columns',10,color=GRAY,ha='center')
arrow(.345,.35,.405,.35)
ax=tile([.425,.315,.16,.075],summary.reshape(8,6).T,cm,d['all_stages'][7]['maximum'])
for rr in range(6):
 for cc in range(8):
  val=summary.reshape(8,6).T[rr,cc];ax.text(cc,rr,f'{val:.0f}',ha='center',va='center',fontsize=8.5,color='white' if val>.5*d['all_stages'][7]['maximum'] else INK)
text(.505,.298,'6 values × 8 maps = 48',11,True,ha='center')
arrow(.605,.35,.695,.35)
text(.65,.38,'Learned weights',10.5,True,ha='center')
s=np.array(d['single_scores']);ax=f.add_axes([.715,.315,.225,.075]);ax.bar(range(10),s,color=[TEAL if i==s.argmax() else '#B7C5C4' for i in range(10)],width=.65)
ax.axhline(0,color=GRID,lw=.8);ax.set_xticks(range(10));ax.set_yticks([]);ax.tick_params(axis='x',length=0,labelsize=10,colors=GRAY);ax.spines[:].set_visible(False)
ax.text(5,s[5]+130,f'{s[5]:,.0f}',ha='center',fontsize=10,color=TEAL);ax.set_ylim(float(s.min())*1.12,float(s.max())*1.22)
text(.8275,.289,'One score per digit',11,True,ha='center')
text(.06,.258,'The outlined region contains 12 values.\nTheir average becomes the outlined summary cell.',11.5,color=GRAY,va='top')
text(.505,.258,'For each digit: multiply the 48 values by that digit’s\n48 learned weights, add the results, then add its bias.',11.5,color=GRAY,va='top')
line(.045,.218,.955,.218)
# Phase 4: per-view scores are averaged by digit (columns), not across digits.
phase(.192,4,'Try 25 shifted views, average by digit, and choose','Run phases 1–3 on 25 shifted views. For each digit, add its 25 scores and divide by 25.')
cols=np.linspace(.31,.81,10);head=.145
text(.06,head,'Three of the 25 views',11,True)
for c,x in enumerate(cols):text(x,head,str(c),11,True,TEAL if c==5 else INK,ha='center')
rows=[(.121,0),(.097,12),(.073,24)]
for y,idx in rows:
 v=d['shifted_views'][idx];tile([.06,y-.005,.025,.01875],v['pixels'])
 text(.1,y,f"Shift ({v['dx']:+d}, {v['dy']:+d})",10.5,color=GRAY)
 for c,x in enumerate(cols):text(x,y,f"{d['view_scores'][idx][c]:,.0f}",10.5,color=TEAL if c==5 else GRAY,ha='center')
text(.06,.052,'… plus 22 other views',10.5,color=GRAY)
line(.29,.047,.835,.047)
text(.06,.031,'Average of all 25',11,True)
for c,x in enumerate(cols):text(x,.031,f"{d['mean_scores'][c]:,.0f}",11,True,TEAL if c==5 else INK,ha='center')
# Emphasize that the 25 scores for the SAME digit form one column.
f.add_artist(Rectangle((cols[5]-.025,.025),.05,.137,transform=f.transFigure,facecolor=TEAL,alpha=.07,edgecolor='none',zorder=-1))
arrow(.844,.036,.885,.036)
text(.92,.087,'Highest average',11,True,ha='center');text(.92,.035,str(d['prediction']),46,True,TEAL,ha='center')
text(.045,.008,'Numbers are rounded for display. Activation colors are scaled separately at each stage.',9,color=GRAY)
for ext in ['png','svg']:f.savefig(O/f'architecture.{ext}',dpi=220,facecolor=BG)
