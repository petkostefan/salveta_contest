import requests
from bs4 import BeautifulSoup
import time

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

# Uzimamo pocetak
with open('pocetak.txt', 'r') as f:
    pocetak = int(f.read())
f.close()

# Primamo kraj
print("Zdravo, stigao si do %s tako da kreces odatle, dokle hoces da radis?" %pocetak)
kraj = int(input())

while(kraj<=pocetak):
    print("Greska, kraj treba da bude veci od pocetka, unesi opet")
    kraj = int(input())

print("To ce trajati oko %.2f minuta" %((kraj-pocetak)/180.0))

glasovi = []
glasovi_dict = []
top50 = []

start_timer = time.time()
# Pocinje scrapovanje i skupljanje dok se ne dodje do kraja
while(pocetak<kraj):
    URL = 'https://salveta.rs/salveta.php?id='+str(pocetak)

    page = requests.get(URL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    votes = soup.find(class_ = 'salveta-votes')
    if(votes == None):
        pass
    else:
        # Lista za sve glasove
        glasovi_pom = (int(votes.get_text()))
        glasovi.append(int(votes.get_text()))

        # Beleze se u dict za listu glasova i linkova
        glas = {
            "link": URL,
            "broj" : glasovi_pom
        }

        glasovi_dict.append(glas)

    pocetak=pocetak+1

    # Status
    if(pocetak%10 == 0):
        print('Status: '+str(pocetak)+"/"+str(kraj))

# Sortiranje i ispisivanje top 3 preko dict.
glasovi_dict_sorted = sorted(glasovi_dict, key = lambda i: i['broj'], reverse = True)
print("Top 3:")
print(str(glasovi_dict_sorted[0]["broj"]) +" "+ glasovi_dict_sorted[0]["link"])
print(str(glasovi_dict_sorted[1]["broj"]) +" "+ glasovi_dict_sorted[1]["link"])
print(str(glasovi_dict_sorted[2]["broj"]) +" "+ glasovi_dict_sorted[2]["link"])

# Sortiranje i ispisivanje preko liste
glasovi.sort(reverse=True)
print("Top 3: "+str(glasovi[0])+" "+str(glasovi[1])+" "+str(glasovi[2])+" ")

end_timer = time.time()

print("\nBravo, skupio si jos %i glasova" %len(glasovi))
print("Sledeci put pocinjes od %i" %kraj)
print("Sve to je trajalo %i minuta i %.1f sekundi" %(int(((end_timer - start_timer)/60)), ((end_timer - start_timer)%60)))

# Pocetak dobija novu vrednost i zapisuje se
pocetak = kraj
with open('pocetak.txt', 'w') as f:
    f.write("%i" %pocetak)
f.close()

# Zapisuju se svi glasovi iz liste
with open('glasovi.txt', 'a') as f:
    for item in glasovi:
        f.write("%s\n" %item)
f.close()

# Uzimaju se stari glasovi iz top 50
with open('top50.txt', 'r') as f:
   pom = f.read().split("\n")
f.close()
pom.pop()

for item in pom:
    pom_deli = item.split(" ")
    glas = {
    "link": pom_deli[1],
    "broj" : int(pom_deli[0])
    }
    top50.append(glas)

# I spajaju sa novim glasovima
for item in glasovi_dict_sorted:
    top50.append(item)

# Glasovi se sortiraju i kreira se novi top 50 i zapisuje
top50_sorted = sorted(top50, key = lambda i: i['broj'], reverse = True)
top50 = top50_sorted[:50]   

with open('top50.txt', 'w') as f:
    for item in top50:
        f.write(str(item["broj"])+" "+item["link"] +"\n")
f.close()