import requests
from bs4 import BeautifulSoup  
import pandas as pd 

# Step 1: Fetch the HTML content
url = "https://worldfoodindia.gov.in/2017/exhibitor-list.html"
response = requests.get(url)
html_content = response.text

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
# target_div = soup.find('div', class_='sectionlist')

all_company_data=[]
all_div = soup.find_all('div', class_='modal-body')
for target_div in all_div:
    table = target_div.find('table')


    def getdata(col):
        return col.get_text()
    line=[]
    for tbody in table.find_all('tr'):
        print("--->start",tbody)
        row_data =list(map(getdata,tbody.find_all('td')))
        if len(row_data) >= 2 and row_data[0] in ['Company Name','City','Contact Person','Telephone']:
            # print(row_data)
            # line+=row_data[1]+','
            line.append(row_data[1])
            # company_name = row_data[1]
        # line+=line+'\n'

    all_company_data.append(line)
    # print(company_name)
    print("endline--->",line)
        
df = pd.DataFrame(all_company_data)
df.to_csv('Transforming_the_food_economy.csv', index=False)
print("Data has been saved to company_data.csv")
        