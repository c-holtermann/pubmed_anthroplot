#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import urllib.request, urllib.error, urllib.parse
import os
import json
import argparse
import locale
import backoff
import pathlib
import tqdm
from bs4 import BeautifulSoup
from pyparsing import *
# Word, alphas, makeHTMLTags

year_start = 1940 # can be a number
year_stop  = datetime.datetime.now().year # can be a number or string "today"
datadir = "../data"
configFileName = "./pubmed_anthroplot.json"
verbose = False

rebuild = [ 1, 2, 3]

locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

def readCommandLine():
    # Create the parser
    parser = argparse.ArgumentParser()

    # Add argument datadir
    parser.add_argument('--datadir', type=pathlib.Path, default=datadir)

    # Add argument startdate
    parser.add_argument('--startdate', type=int, default=None, help="year to start counting, default is 1940")

    # Add argument enddate
    parser.add_argument('--enddate', type=int, default=None, help="year to stop counting or string 'today', default is today")

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

def backoff_hdlr(details):
    print ("Backing off {wait:0.1f} seconds after {tries} tries ".format(**details))

@backoff.on_exception(backoff.expo,
                      TimeoutError,
                      max_tries=5)
@backoff.on_exception(backoff.expo,
                      urllib.error.URLError,
                      max_tries=5,
                      on_backoff=backoff_hdlr)
def url_open(url):
    return urllib.request.urlopen(url)

def main():
    global args, config, configData

    args = readCommandLine()
    configData = readConfigFile(args)

    with tqdm.tqdm(configData["figures"]) as t_outer:
      for fig in t_outer:
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

        today = timenow_date_str

        if configData["filename"]:
            outfilename = configData["filename"].format(today=today) + "_"
        else:
            outfilename = timenow_date_str+"_statistics_"
        outfilename += str(nr) + ".csv"
        outfilename_full = os.path.join(datadir, outfilename);

        with open(outfilename_full, 'w') as outfile:
            search_term = ''.join(fig['search_term'])
            label = fig['label']

            datum = datetime.datetime.now()
            datum_str = datum.strftime("%d. %B %Y")
            outfile.write("Suchterm" + "," + search_term + chr(10))
            outfile.write("Datum" + "," + datum_str + chr(10))
            outfile.write("Label" + "," + label + chr(10))

            tqdm.tqdm.write(f"Nr {nr}")
            tqdm.tqdm.write(f"Label {label}")
            tqdm.tqdm.write(f"Suchterm {search_term}")
            tqdm.tqdm.write(f"Filename {outfilename_full}")

            text = ""
            with tqdm.tqdm(range(args.startdate, args.enddate)) as t:

              for date_end in t:

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

                text = f"{date_end}:{res_count}"
                t.set_description(f'{text}')
                # print(text)

                outfile.write ("Wert"+","+str(date_end)+","+str(res_count)+chr(10))

if __name__ == "__main__":
    main()
