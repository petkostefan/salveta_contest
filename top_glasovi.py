#Refreshuje samo top 50 glasova

import time
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

start_timer = time.time()

with open('glasovi.txt', 'r') as f:
    glasovi = f.read().split('\n')
f.close()
glasovi.pop()

for i in range(0,len(glasovi)):
    glasovi[i] = int(glasovi[i])

glasovi.sort(reverse=True)
print("Top 3: "+str(glasovi[0])+" "+str(glasovi[1])+" "+str(glasovi[2])+" ")


with open('top50.txt', 'r') as f:
   pom = f.read().split("\n")
f.close()
pom.pop()

indeksi =[]
glasovi_dict = []
brojac = 0

for item in pom:
    pom_deli = item.split("=")
    indeks = int(pom_deli[1])
    indeksi.append(indeks)

for i in indeksi:
    URL = 'https://salveta.rs/salveta.php?id='+str(i)
    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    votes = soup.find(class_ = 'salveta-votes')
    if(votes == None):
        pass
    else:
        glas = {
            "link": URL,
            "broj" : (int(votes.get_text()))
        }

        glasovi_dict.append(glas)
        brojac = brojac+1

        if(brojac%10 == 0):
            print('Status: '+str(brojac)+"/50")

top50 =  sorted(glasovi_dict, key = lambda i: i['broj'], reverse = True)

with open('top50.txt', 'w') as f:
    for item in top50:
        f.write(str(item["broj"])+" "+item["link"] +"\n")
f.close()

with open('glasovi.txt', 'w') as f:
    for item in glasovi:
        f.write("%s\n" %item)
f.close()

print("Glasovi su sortirani!")

end_timer = time.time()


print("Sve to je trajalo %f sekundi" %(end_timer - start_timer))
