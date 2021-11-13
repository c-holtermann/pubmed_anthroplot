#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import urllib.request, urllib.error, urllib.parse
import os
import json
import argparse
import locale
import backoff
from bs4 import BeautifulSoup
from pyparsing import *
# Word, alphas, makeHTMLTags

year_start = 1940
year_stop  = datetime.datetime.now().year
datadir = "../data"
configFileName = "./pubmed_anthroplot.json"
verbose = False

rebuild = [ 1, 2, 3]

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

def readCommandLine():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add argument startdate
    parser.add_argument('--startdate', type=int, default=None)

    # Add argument enddate
    parser.add_argument('--enddate', type=int, default=None)

    # Add argument configfile
    parser.add_argument('--configfile', type=argparse.FileType('r'), default=configFileName)

    # Add argument verbose
    parser.add_argument('--verbose', type=bool)

    # Parse the argument
    args = parser.parse_args()

    return args

def readConfigFile(args):
    configFile = args.configfile
    data = json.load(configFile)

    if not args.startdate:
        if data["year_start"]:
            args.startdate = data["year_start"]
        else:
            args.startdate = year_start

    if not args.enddate:
        if data["year_end"]:
            if data["year_end"] == "today":
                args.enddate = datetime.datetime.now().year
            else:
                args.enddate = data["year_end"]
        else:
            args.enddate = year_stop

    return data

@backoff.on_exception(backoff.expo,
                      urllib.error.URLError,
                      max_value=120)
def url_open(url):
    return urllib.request.urlopen(url)

def main():
    global args, config, configData

    args = readCommandLine()
    configData = readConfigFile(args)

    for fig in configData["figures"]:
        #for config in configs:

        #nr = config['nr']
        nr = int(fig)
        fig = configData["figures"][fig]

        # only rebuild the configs in array rebuild
        if not nr in rebuild:
            continue

        timenow = datetime.datetime.now()
        timenow_date_str = str(timenow.year) + "-" + \
                        str(timenow.month) + "-" + \
                        str(timenow.day)

        outfilename = timenow_date_str+"_statistics_" + str(nr)  + ".csv"
        outfilename_full = os.path.join(datadir, outfilename);

        with open(outfilename_full, 'w') as outfile:
            search_term = ''.join(fig['search_term'])
            label = fig['label']

            datum = datetime.datetime.now()
            datum_str = datum.strftime("%d. %B %Y")
            outfile.write("Suchterm" + "," + search_term + chr(10))
            outfile.write("Datum" + "," + datum_str + chr(10))
            outfile.write("Label" + "," + label + chr(10))

            print("Nr", nr)
            print("Label", label)
            print("Suchterm", search_term)
            print("Filename", outfilename_full)

            for date_end in range(args.startdate, args.enddate):

                search_term_time_interval='("0000/01/01"[Date - Publication] : "'+str(date_end)+'"[Date - Publication])'
                search_term_url='?term='+search_term+" AND "+search_term_time_interval

                base_url="http://www.ncbi.nlm.nih.gov/pubmed/"
                # search_term="?term=anthroposoph*++AND+%28+medicin*+OR+medizin*+%29"

                url_pubmed = base_url + search_term_url

                # print url_pubmed
                url_pubmed = urllib.parse.quote(url_pubmed, safe="%/:=&?~#+!$,;'@()*[]")
                # print url_pubmed

                response = url_open(url_pubmed)

                html_doc = response.read()

                soup = BeautifulSoup(html_doc, "lxml")
                #print(soup.prettify())

                #print soup.find(id="term")

                # works if there is more than 1 result
                res_container = soup.find_all(attrs={"class": "results-amount-container"})
                if res_container:
                    res_inner_container = res_container[0].findAll('span', attrs={"class": "value"})
                    if res_inner_container:
                        res_count = locale.atoi(res_inner_container[0].get_text())
                else:
                    res_container = soup.find_all(attrs={"class": "article-page"})
                    if res_container:
                        res_count = 1
                    else:
                        res_count = 0

                print(date_end,":",res_count)

                outfile.write ("Wert"+","+str(date_end)+","+str(res_count)+chr(10))

if __name__ == "__main__":
    main()
