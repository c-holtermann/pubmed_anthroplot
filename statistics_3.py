import datetime
import urllib2
from bs4 import BeautifulSoup
from pyparsing import * 
# Word, alphas, makeHTMLTags

with open('statistics_3.csv', 'w') as outfile:

  datum = datetime.datetime.now()

  datum_str = datum.strftime("%d. %B %Y")
  
  #search_term='((anthroposoph* AND ( medicin* OR medizin* )))'
  search_term="meditati*"
  outfile.write ("Suchterm"+","+search_term+chr(10))
  outfile.write ("Datum"+","+datum_str+chr(10))
  outfile.write ("Label"+","+"'Suchterm: '"+chr(10)) 
  
  for date_end in range(1900, 2012):
    
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

    html_results = soup.find_all("h2", class_="result_count")
    #print html_results[0]
    #print alphas
    if len(html_results) != 0:  
      digits = "0123456789"
      integer = Word( digits )

      h2Start,h2End = makeHTMLTags("h2")
      # results_parsing = h2Start + SkipTo(h2End).setResultsName("body") + h2End

      results_parsing = h2Start + "Results:" + Optional(Word ( digits )("n1") + "to" + Word ( digits )("n2") + "of" )+ Word ( digits )("res_count") + h2End
    
      #results_parsing = h2Start + "Results:" + Word ( digits )("n1") + "to" + Word ( digits )("n2") + "of" + Word ( digits )("res_count") + h2End

      result_parsed = results_parsing.parseString(str(html_results[0]))
    
      res_count = result_parsed.res_count
    else:
      res_count= 0
    print date_end,":",res_count

    outfile.write ("Wert"+","+str(date_end)+","+str(res_count)+chr(10))

