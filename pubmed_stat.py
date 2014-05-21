#!/bin/python
# -*- coding: utf-8 -*-
import datetime
import urllib2
from bs4 import BeautifulSoup
from pyparsing import *
# Word, alphas, makeHTMLTags

year_start = 1940
year_stop  = 2014

with open('statistics_1.csv', 'w') as outfile:
  search_term = ( '(anthropos* OR weleda OR wala OR (curativ* AND eurythm*) OR '
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
                  'meta-analys* OR (meta AND analys*))' )
  datum = datetime.datetime.now()
  datum_str = datum.strftime("%d. %B %Y")
  outfile.write ("Suchterm"+","+search_term+chr(10))
  outfile.write ("Datum"+","+datum_str+chr(10))
  outfile.write ("Label"+","+"'Ant. Med., Suchterm:'"+chr(10))

  for date_end in range(year_start, year_stop):

    search_term_time_interval='("-2000"[Date - Publication] : "'+str(date_end)+'"[Date - Publication])'
    search_term_url='?term='+search_term+" AND "+search_term_time_interval

    base_url="http://www.ncbi.nlm.nih.gov/pubmed/"
    # search_term="?term=anthroposoph*++AND+%28+medicin*+OR+medizin*+%29"

    url_pubmed = base_url + search_term_url

    # print url_pubmed
    url_pubmed = urllib2.quote(url_pubmed, safe="%/:=&?~#+!$,;'@()*[]")
    # print url_pubmed

    response = urllib2.urlopen(url_pubmed)

    html_doc = response.read()

    soup = BeautifulSoup(html_doc)
    #print(soup.prettify())

    #print soup.find(id="term")

    res_count = soup.find_all(attrs={"name": "ncbi_resultcount"})[0]["content"]

    print date_end,":",res_count

    outfile.write ("Wert"+","+str(date_end)+","+str(res_count)+chr(10))
