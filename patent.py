import urllib.request
# import pyperclip
import re
import csv

def GetMentions(input_string, word):
    return (sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), input_string)))

def WriteToCSV(company, arr):
    with open('mentions.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([company] + arr)
        
def GetArrayVersion(dict):
    count = 0
    newArr = [0 for i in range(numberOfWords)]
    for value in dict.values():
        newArr[count] = value
        count+=1
    return newArr 
    
def SearchCompany(act_name, company_name, page_count):
    words_count = {'Firewall': 0, 'IoT': 0, 'Internet of Things': 0, 'SD-WAN': 0,'Fabric': 0, 'WAN': 0, 'Broadband': 0, 'Network': 0, 'Cloud': 0, 'Endpoint': 0, 'VPN': 0, 'Virtual Private Cloud': 0, 'VPC': 0, 'CAN': 0, 'SASE': 0, 'Secure Access Service Edge': 0, 'SaaS': 0, 'Software as a Service': 0, 'APIs': 0, 'MPLS': 0, 'Multiprotocol Label Switching': 0, 'Datacenter': 0}
    for x in range(page_count):
        urlComp = "https://patents.justia.com/assignee/" + company_name + "?page=" + str(x+1);
        with urllib.request.urlopen(urlComp) as url:
            # print(urlComp)
            s = url.read()
            strV = s.decode("utf-8")
            for k, v in words_count.items():
                words_count[k]+=GetMentions(strV.upper(), k.upper())
    WriteToCSV(act_name, GetArrayVersion(words_count))
    return words_count;


csv_columns = ['Firewall', 'IoT', 'Internet of Things', 'SD-WAN','Fabric', 'WAN', 'Broadband', 'Network', 'Cloud', 'Endpoint', 'VPN', 'Virtual Private Cloud', 'VPC', 'CAN', 'SASE', 'Secure Access Service Edge', 'SaaS', 'Software as a Service', 'APIs', 'MPLS', 'Multiprotocol Label Switching', 'Datacenter']
WriteToCSV('Company', csv_columns)
numberOfWords = len(csv_columns)

print("Fortinet: " + str(SearchCompany("Fortinet", "fortinet-inc", 60)))
print("Palo Alto Networks: " + str(SearchCompany("Palo Alto Networks", "palo-alto-networks-inc", 14)))
print("CrowdStrike Inc: " + str(SearchCompany("CrowdStrike Inc.", "crowdstrike-inc", 3)))
print("FireEye: " + str(SearchCompany("FireEye", "fireeye-inc", 15)))
print("CheckPoint Software: " + str(SearchCompany("CheckPoint Software", "check-point-software-technologies-ltd", 5)))