import csv
from pylab import *
import glob
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Plot_data:

  def __init__(self):
    self.x = []
    self.y = []
    self.title = ""
    self.keys = {}

plot_datas = []

files=glob.glob("statistics_*.csv")

#files=["statistics_1.csv","statistics_2.csv"]

for files in files:
    print files

    with open(files, 'rb') as csvfile:
      statistics_reader = csv.reader(csvfile, delimiter=',', quotechar="'")

      plot_data = Plot_data()
      plot_data.filename = files

      for row in statistics_reader:
        if row[0] == "Wert":
          plot_data.x.append(int(row[1]))
          plot_data.y.append(int(row[2]))
        else:
          plot_data.keys[row[0]] = row[1]
        print ', '.join(row)

    plot_datas.append(plot_data)


fig = plt.figure()

#title("Suchterm: "+plot_datas[0].keys["Suchterm"])
#xlabel("Jahr")
#ylabel("Anzahl Publikationen")

n_plot = 0
min_x = 10000
max_x = 0
ax_ylabels = ["Publikationen Ant. Med.", "Publikationen Pubmed gesamt", "Publikationen Meditation"]

styles = [ "","g--","r." ]
legpl = []
label_list = []
for plot_data in plot_datas:
  if n_plot == 0:
    ax_base = fig.add_subplot(111)
    ax = ax_base
  else:
    ax = ax_base.twinx()

  print n_plot,":",plot_data.x,plot_data.y
  pltmp, = ax.plot(plot_data.x,plot_data.y, styles[n_plot])

  label = ""
  if "Label" in plot_data.keys:
    label += plot_data.keys["Label"]
  if "Suchterm" in plot_data.keys:
    label += plot_data.keys["Suchterm"]

  label_list.append(label.decode("utf8"))
  legpl.append(pltmp)

  min_x_this = min(plot_data.x)
  max_x_this = max(plot_data.x)

  if min_x_this < min_x:
    min_x = min_x_this
  if max_x_this > max_x:
    max_x = max_x_this

  if n_plot > 1:
    ax.spines['right'].set_position(('axes', 1.1))
    ax.set_frame_on(True)
    ax.patch.set_visible(False)

  ax.set_ylabel(ax_ylabels[n_plot])

  n_plot += 1

#fig_legend = ax.legend(legpl,label_list,loc=2, bbox_to_anchor=(.05,-0.1), borderaxespad=0.)

ax_base.set_title("Summe auf Pubmed gelisterer Publikationen")
ax_base.set_xlabel("Jahr")
#ax_base.set_ylabel("Summe Publikationen Ant. Med.")
#ax.set_ylabel("Summe Publikationen Pubmed")

ax.yaxis.set_major_locator(MaxNLocator(prune='lower'))
ax_base.yaxis.set_major_locator(MaxNLocator(prune='lower'))

plt.tight_layout()
plt.xlim([min_x,max_x])
fig.savefig('samplefigure', #bbox_extra_artists=(fig_legend,),
            bbox_inches='tight', pad_inches=0.2)

# plt.draw()
# plt.show()
