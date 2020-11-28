import datetime
import urllib.request
from bs4 import BeautifulSoup

def GetYear(str):
    dateReformated = datetime.datetime.strptime(str, '%B%d,%Y').strftime('%d/%m/%Y')
    return dateReformated[6:10]

# temp = datetime.datetime.strptime('October 3, 2006', '%B %d, %Y').strftime('%d/%m/%Y')
# print(2020 - int(str(temp)[6:10]))
urlComp = "https://patents.justia.com/assignee/fortinet-inc?page=1"
with urllib.request.urlopen(urlComp) as url:
    s = url.read()
    strV = s.decode("utf-8")

soup = BeautifulSoup(strV, 'html.parser')
for link in soup.findAll("div", {"class": "date-issued"}):
    date = link.get_text().replace(" ", "").replace("Publicationdate:", "").replace("DateofPatent:", "").replace("\n", "")
    print(GetYear(date))

