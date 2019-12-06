import requests

key = 'k9908EXzqDE7w8Ntt4vdfIlyKWp7ngYq' #string variable

url= 'https://api.nytimes.com/svc/archive/v1/2019/1.json?api-key='+key
r = requests.get(url)
json_data = r.json()
  
  
!pip install pyjq
import pyjq

# exemple de requête : une requête pour récupérer le copyright

copyright = pyjq.all('.copyright', json_data)
print(copyright)

# requête pour obtenir headline et date 

jq_query = f'.response .docs [] | {{ the_headline: .headline .main, the_date: .pub_date }}'
output = pyjq.all(jq_query, json_data)

# requête pour obtenir tous les articles sur une certaines durée en obtenant l'API archive  (il faut faire une boucle car l'API archive ne donne que mois par mois) 

!pip install datetime
import datetime 
from dateutil.rrule import rrule, MONTHLY

# # create a list of (year,month) pairs for the data from start_dt to end_date inclusive

start_dt = datetime.date(2009,1,1)
end_dt = datetime.date(2009,1,31)
dates = [(dt.year,dt.month) for dt in rrule(MONTHLY,dtstart=start_dt, until=end_dt)]

# # extraire les articles pour chaque (year,month) qui est dans l'intervall
all_output =[]
for year, month in dates:
    print(year,month)
    url = f'https://api.nytimes.com/svc/archive/v1/{year}/{month}.json?&api-key='+'i5GTBJVBEnxg9P9BPvNvz3Wv7lRZbUFu'
    r = requests.get(url)
    json_data = r.json()
    
    length = pyjq.all('.response .docs | length', json_data)[0]
    print(f'For month {month} in {year} there were {length} articles')
    
    jq_query = f'.response .docs [] | {{ the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date }}'
    output = pyjq.all(jq_query, json_data)
    
    all_output.append([f'{year}{month:02}',output])

print(all_output)

# requête pour extraire les articles du domaine "Politics" en utilisant l'API "article search"

url=f'https://api.nytimes.com/svc/search/v2/articlesearch.json?fq=news_desk:("Politics")&api-key='+'aQSnNaOL0wXF4PpTaENAnS7v3W86soCM'
r = requests.get(url)
json_data = r.json()

jq_query = f'.response .docs [] | {{ the_snippet: .snippet, the_headline: .headline .main, the_date: .pub_date }}'
output = pyjq.all(jq_query, json_data)

print(output)

    
