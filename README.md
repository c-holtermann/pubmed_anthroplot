pubmed_anthroplot
=================

Python scripts to create a plot of publications on pubmed a) in relation to anthroposophic medicine and b) in relation to publications about meditation compared to the overall publications on pubmed

* pubmed_stat.py fetches data from pubmed and writes csv outfiles
* plot_statistics.py creates graphs from previously written csv

First run ```pubmed_stat.py```. It will create data files in the datadir (default: ```../data```).

After that run ```plot_statistics.py```. It will create an image file in the imagedir (default: ```../img```).

Both scripts need a config file. Default ist ```pubmed_anthroplot.json```. This defines the search term and label of plot and axes.

ToDo
====
The term for anthroposophic medicine includes a lot of publications that are not directly related to anthroposophic medicine. It needs to be refined.

3 plots
=======
![example plot](2021-11-14_fig_3_en.png)


2 plots
=======
![example plot](2021-11-15_fig_2_en.png)

Usage
=====
* Mediawiki Commons: https://commons.wikimedia.org/wiki/File:2021-11-15_fig_2_en_pubmed_anthroplot.png
* Imedwiki, article about anthroposophic medicine: 

Issues
======
The search term is to broad to adequately reflect anthroposophic medical research as it overestimates the number of publications. The search term needs to be narrowed.

Credits
=======
Original publication Kienle, Gunver; Glockmann, Anja; Grugek, Renate; Hamre, Harald Johan; Kiene, Helmut (2011), "Klinische Forschung zur Anthroposophischen Medizin – Update eines «Health Technology Assessment»-Berichts und Status Quo" [Clinical research on anthroposophic medicine - Update of a "Health Technology Assessment" report and Status Quo], Forschende Komplementärmedizin / Research in Complementary Medicine, 18, pp. 269–282, [doi:10.1159/000331812](https://www.doi.org/10.1159/000331812), ISSN 1661-4119
