import requests
from bs4 import BeautifulSoup

# Step 1: Fetch the HTML content
url = "https://worldfoodindia.gov.in/2017/exhibitor-list.html"
response = requests.get(url)
html_content = response.text

# Step 2: Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
tables = soup.find_all('table', class_='sectionlist')
# print(tables,'------>')

exhibitors = []

headers = []
# Step 3: Extract data from the table
for table in tables:
    for tr in table.find_all('tr')[1:]:  # Skip the header row
        tds = tr.find_all('td')
        # print(tds,'---->')
        # Extract headers from the first row
        if tr == table.find_all('tr')[0]:  # Header row
            headers = [td.text.strip() for td in tds]
            print(headers,'---')
        else:
            # Extract data from each column
            row_data = [td.text.strip() for td in tds]
            exhibitors.append(dict(zip(headers, row_data)))
            # print(exhibitors,'---->')

