import datetime
import urllib.request
from bs4 import BeautifulSoup
import csv

def GetArrayVersion(dict):
    count = 0
    newArr = [0 for i in range(23)]
    for value in dict.values():
        count+=1
        newArr[count] = value
    return newArr 

def WriteToCSV(company, arr):
    with open('materuity.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([company] + arr)

def GetYear(str):
    dateReformated = datetime.datetime.strptime(str, '%B%d,%Y').strftime('%d/%m/%Y')
    return dateReformated[6:10]

def SearchCompany(act_name, company_name, page_count):
    numberOfPatents = 0
    totalYears = 0
    year_count = {'1998': 0, '1999': 0, '2000': 0, '2002': 0, '2003': 0, '2004': 0, '2005': 0, '2006': 0, '2007': 0,'2008': 0, '2009': 0, '2010': 0, '2011': 0, '2012': 0, '2013': 0, '2014': 0, '2015': 0, '2016': 0, '2017': 0, '2018': 0, '2019': 0, '2020': 0}
    for x in range(page_count):
        urlComp = "https://patents.justia.com/assignee/" + company_name + "?page=" + str(x+1);
        # print(urlComp)
        with urllib.request.urlopen(urlComp) as url:
            s = url.read()
            strV = s.decode("utf-8")
            soup = BeautifulSoup(strV, 'html.parser')
            for link in soup.findAll("div", {"class": "date-issued"}):
                date = link.get_text().replace(" ", "").replace("Publicationdate:", "").replace("DateofPatent:", "").replace("\n", "")
                year = GetYear(date);
                year_count[year]+=1
                totalYears+=int(year)
                numberOfPatents+=1
    print(year_count)
    WriteToCSV(act_name, [numberOfPatents, totalYears/numberOfPatents] + GetArrayVersion(year_count))
    return (str(numberOfPatents) + " patents with average year of " + str(totalYears/numberOfPatents) + " (" + str(totalYears) + ")")

csv_columns = ['Total Contracts','Average Year','1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']
WriteToCSV('Company', csv_columns)
# temp = {'1998': 1, '1999': 0, '2000': 0, '2002': 1, '2003': 1, '2004': 0, '2005': 0, '2006': 0, '2007': 1, '2008': 1, '2009': 4, '2010': 13, '2011': 4, '2012': 10, '2013': 8, '2014': 14, '2015': 8, '2016': 2, '2017': 8, '2018': 4, '2019': 4, '2020': 5}
# WriteToCSV('Fortinet', [1193, 2015.4459346186086] + GetArrayVersion(temp))
print("Fortinet: " + SearchCompany("Fortinet", "fortinet-inc", 60))
print("Palo Alto Networks: " + SearchCompany("Palo Alto Networks", "palo-alto-networks-inc", 14))
print("CrowdStrike Inc: " + SearchCompany("CrowdStrike Inc.", "crowdstrike-inc", 3))
print("FireEye: " + SearchCompany("FireEye", "fireeye-inc", 15))
print("CheckPoint Software: " + SearchCompany("CheckPoint Software", "check-point-software-technologies-ltd", 5))


