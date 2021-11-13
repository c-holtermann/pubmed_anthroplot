#!/usr/bin/python3
# -*- coding: utf-8 -*-
import datetime
import urllib.request, urllib.error, urllib.parse
import os
from bs4 import BeautifulSoup
from pyparsing import *
# Word, alphas, makeHTMLTags

year_start = 1940
year_stop  = datetime.datetime.now().year
datadir = "../data"

rebuild = [ 1, 2, 3]

configs = [{'nr': 1,
            'search_term': (
            '(anthropos* OR weleda OR wala OR (curativ* AND eurythm*) OR '
            '(rhythmic* AND massage) OR (rhythmic AND massage)'
            'OR (pressel AND massage) OR eurythm* OR infludo OR nausyn '
            'OR cardiodoron OR combudoron OR hepatozoon OR choleodoron '
            'OR digestodoron OR dermatodoron OR pneumodoron OR '
            'pneumadoron OR erysidoron OR kephalodoron OR cephalodoron '
            'OR biodoron OR (ferrum AND quar*) OR menodoron '
            'OR pertudoron OR echinadoron OR biodor OR onopordon '
            'OR bidor OR venadoron OR (plantago AND bronchial*) OR '
            '(bolus AND eucalypt* AND comp*) OR chirophoneti* OR '
            '(bothmer* AND gymnasti*) OR (mistletoe OR mistletoe*) OR '
            '(viscum OR viscum*) OR (iscador OR iscador*) OR '
            '(iscar OR iscar*) OR (helixor OR helixor*) OR '
            '(iscucin OR iscucin*) OR '
            '(isorel OR isorel* OR visorel OR visorel*) OR abnoba* OR '
            '(waldorf OR waldorf*) OR (rudolf AND steiner)) AND '
            '((study* OR studie*) OR (trial OR trial*) OR evaluat* OR '
            'random* OR investig* OR (cohort* OR kohort*) OR outcome* OR '
            '(review OR review*) OR (ubersicht OR übersicht OR uebersicht) '
            'OR (überblick OR ueberblick OR uberblick) OR metaanalys* OR '
            'meta-analys* OR (meta AND analys*))'),
            'label': "'Ant. Med., Suchterm:'"
            },
           {'nr': 3,
            'search_term': "Suchterm: meditati* or contempl*",
            'label': "Meditation"},
           {'nr': 2,
            'search_term': '',
            'label': "Gesamtpublikationen Pubmed"}]

import locale
locale.setlocale( locale.LC_ALL, 'en_US.UTF-8' )

for config in configs:

    nr = config['nr']
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
        search_term = config['search_term']
        label = config['label']

        datum = datetime.datetime.now()
        datum_str = datum.strftime("%d. %B %Y")
        outfile.write("Suchterm" + "," + search_term + chr(10))
        outfile.write("Datum" + "," + datum_str + chr(10))
        outfile.write("Label" + "," + label + chr(10))

        print("Nr", config['nr'])
        print("Label", label)
        print("Suchterm", search_term)
        print("Filename", outfilename_full)

        for date_end in range(year_start, year_stop):

            search_term_time_interval='("0000/01/01"[Date - Publication] : "'+str(date_end)+'"[Date - Publication])'
            search_term_url='?term='+search_term+" AND "+search_term_time_interval

            base_url="http://www.ncbi.nlm.nih.gov/pubmed/"
            # search_term="?term=anthroposoph*++AND+%28+medicin*+OR+medizin*+%29"

            url_pubmed = base_url + search_term_url

            # print url_pubmed
            url_pubmed = urllib.parse.quote(url_pubmed, safe="%/:=&?~#+!$,;'@()*[]")
            # print url_pubmed

            response = urllib.request.urlopen(url_pubmed)

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
