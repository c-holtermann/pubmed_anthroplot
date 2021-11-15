#!/usr/bin/python3
# -*- coding: utf-8 -*-
import csv
from pylab import *
import glob
import datetime
import os
import json
import argparse
import pathlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Plot_data:

  def __init__(self):
    self.x = []
    self.y = []
    self.title = ""
    self.keys = {}

datadir = "../data"
imgdir = "../img"
configFileName = "./pubmed_anthroplot.json"
ax_ylabels = ["Publikationen Ant. Med.", "Publikationen Pubmed gesamt", "Publikationen Meditation"]

timenow = datetime.datetime.now()
today = timenow_date_str = str(timenow.year) + "-" + \
                str(timenow.month) + "-" + \
                str(timenow.day)

def get_infiles():

    _glob = timenow_date_str + "_statistics_*.csv"
    glob_full = os.path.join(datadir, _glob)

    files = glob.glob(glob_full)

    # sort files (by number)
    # where number n is "YYYY-(M)M-DD_statistics_n.csv"

    files = sorted(files, key=lambda name: os.path.basename(name))

    return files

def read_infiles(files):

    plot_datas = []
    
    for file_ in files:
        print(file_)

        with open(file_, 'r') as csvfile:
          statistics_reader = csv.reader(csvfile, delimiter=',', quotechar="'")

          plot_data = Plot_data()
          plot_data.filename = file_

          for row in statistics_reader:
            if row[0] == "Wert":
              plot_data.x.append(int(row[1]))
              plot_data.y.append(int(row[2]))
            else:
              plot_data.keys[row[0]] = row[1]
            print(', '.join(row))

        plot_datas.append(plot_data)

    return plot_datas

def main():
    files = get_infiles()

    print("plotting files", files)

    outfile_img_name = timenow_date_str + "_fig"
    outfile_img_name_full = os.path.join(imgdir, outfile_img_name)

    # files=["statistics_1.csv","statistics_2.csv"]

    plot_datas = read_infiles(files)

    fig = plt.figure()

    n_plot = 0
    min_x = 10000
    max_x = 0
    

    styles = [ "", "g--", "r." ]
    legpl = []
    label_list = []

    for plot_data in plot_datas:
      if n_plot == 0:
        ax_base = fig.add_subplot(111)
        ax = ax_base
      else:
        ax = ax_base.twinx()

      print(n_plot,":",plot_data.x,plot_data.y)

      label = ""
      #if "Label" in plot_data.keys:
      #  label += plot_data.keys["Label"].decode("utf8")
      #if "Suchterm" in plot_data.keys:
      #  label += plot_data.keys["Suchterm"].decode("utf8")

      label = ax_ylabels[n_plot]
      pltmp, = ax.plot(plot_data.x, plot_data.y, styles[n_plot], label=label)

      label_list.append(label)

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
      # legend = ax.legend(loc="upper center")
      n_plot += 1

    #fig_legend = ax.legend(legpl,label_list,loc=2, bbox_to_anchor=(.05,-0.1), borderaxespad=0.)

    ax_base.set_title("Summe auf Pubmed gelisteter Publikationen")
    ax_base.set_xlabel("Jahr")
    #ax_base.set_ylabel("Summe Publikationen Ant. Med.")
    #ax.set_ylabel("Summe Publikationen Pubmed")

    ax.yaxis.set_major_locator(MaxNLocator(prune='lower'))
    ax_base.yaxis.set_major_locator(MaxNLocator(prune='lower'))

    ax.legend(legpl, label_list, loc="upper center")

    plt.tight_layout()
    plt.xlim([min_x,max_x])
    fig.savefig(outfile_img_name_full, #bbox_extra_artists=(fig_legend,),
                bbox_inches='tight', pad_inches=0.2)

    plt.draw()
    plt.show()

if __name__ == "__main__":
    main()
