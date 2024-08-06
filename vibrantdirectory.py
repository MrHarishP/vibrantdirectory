import requests
from bs4 import BeautifulSoup
import pandas as pd
# Fetch the main web page

url = 'https://vibrantdirectory.com/search-by-cat/index.php?cat=TEXTILE&ct=All%20City'
response = requests.get(url)

# Initialize a list to store hrefs
hrefs = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all divs with the class 'job-text'
    job_text_divs = soup.find_all('div', class_='job-text')
    
    for div in job_text_divs:
        # Find all anchor tags within the div
        a_tags = div.find_all('a',href=lambda href: href and 'company-profile' in href)
        
        for a_tag in a_tags:
            if 'href' in a_tag.attrs:
                href = a_tag['href']
                if '..' in href:
                    href = href.replace('..', '')
                if not href.startswith('http'):
                    href = f'https://vibrantdirectory.com{href}'
                hrefs.append(href)
                
# Function to extract company details from a profile URL
def extract_company_details(profile_url):
    response = requests.get(profile_url)
    response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract company name
    company_name = soup.find('h2').text.strip() if soup.find('h2') else 'N/A'
    # find_telephone = soup.find('div', class_='col-md-4')
    # find_a = find_telephone.get_text(strip=True)
    tel_links = soup.find_all('a', href=lambda href: href and 'tel' in href)[0].get_text(strip=True)

    # Extract the phone number by removing 'tel:'
    phone_number = tel_links.replace('+91:', '')

    # Print the phone number
    # print(phone_number) # Output: +91792970791

    # Extract contact person and telephone details
    contact_person_div = soup.find('div', class_='single-defination')
    # print(contact_person_div)
    contact_person_name = 'N/A'
    telephone = phone_number

    if contact_person_div:
        # Split the text in the div by newlines
        contact_person_texts = contact_person_div.text.strip().split('\n')
        contact_person_name = contact_person_texts[1].strip() if len(contact_person_texts) > 1 else 'N/A'

        # Extract telephone number from href or text within the single-defination div
        telephone_tag = contact_person_div.find('a')
        # print(telephone_tag,'---->')
        if telephone_tag:
            telephone = telephone_tag.get('href', '').strip() or telephone_tag.get_text(strip=True)
        # print(telephone)

    return {
        'company_name': company_name,
        'contact_person': contact_person_name,
        'telephone': telephone
    }
all_company_data = []
# # URL of the company profile page
# profile_url = hrefs
i=0
while(True):
    profile_url=hrefs[i]
    i+=1
    company_details = extract_company_details(profile_url)
    print(f"Company Name: {company_details['company_name']}")
    # print(f"Contact Person: {company_details['contact_person']}")
    # print(f"Telephone: {company_details['telephone']}")
    all_company_data.append(company_details)
    if(i>=len(hrefs)):
        break
    # break
# if all_company_data:
print("-->",len(company_details))
df = pd.DataFrame(all_company_data)
df.to_csv('company_data.csv', index=False)
print("Data has been saved to company_data.csv")
# else:
#     print("No data extracted.")

# # Extract and print company details
# print(all_company_data,'--->')
