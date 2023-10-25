import requests, psycopg2
from bs4 import BeautifulSoup

site = requests.get("https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population")
soup = BeautifulSoup(site.text, "html.parser")

conn = psycopg2.connect(f"""
    dbname=Test
    user=postgres
    password={"password"}
    host=localhost
""", options='-c search_path=world')
c = conn.cursor()
#----------------------------------------------------------------------------------------------------------------------
scrapedtable = []
table = soup.find('table', {"class": "wikitable sortable"})
tr = table.find_all("tr")
for row in tr[3:]:
    scrapedtable.append([row.contents[3].text[1:], int(row.contents[5].text.replace(',', ''))])
#----------------------------------------------------------------------------------------------------------------------
try:
    c.execute("ROLLBACK")
    c.execute("DROP TABLE world.country")
    c.execute("COMMIT")
except:
    pass

c.execute("ROLLBACK")
c.execute("CREATE TABLE world.country("
	"ID integer PRIMARY KEY,"
	"Name varchar(255),"
	"Capital varchar(255),"
	"Population integer,"
	"Created_on timestamptz,"
	"HDI real);")
for i in range(len(scrapedtable)):
    c.execute(f"INSERT INTO world.country(ID, Name, Capital, Population, Created_on, HDI)"
              f"VALUES({i+1}, '{scrapedtable[i][0]}', NULL, {scrapedtable[i][1]}, clock_timestamp(), NULL)")
c.execute("COMMIT")
