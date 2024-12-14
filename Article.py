import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.cafedelabourse.com/bourse/indice-sp-500")
soup = BeautifulSoup(page.text, 'html.parser')
article = soup.find_all("div", class_="block_content mb-2")
document = []
for t in article:
    print(t.text)
    document.append(t.text)
with open("corpus.txt", "w") as fichier:
    fichier.write(str(document[0]))