from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup


def parse_first_placard(soup):
    placard = soup.select_one('.placard.tier2.landscape')

    address_link = placard.select_one('.header-col a.left-h4')
    address = address_link.get_text(strip=True) if address_link else 'Address not found'

    # Extract additional property name or identifier
    subtitle_alpha_link = placard.select_one('.header-col a.left-h6')
    subtitle_alpha = subtitle_alpha_link.get_text(strip=True) if subtitle_alpha_link else ''

    # Extract location information including city, state, and zip code
    location_link = placard.select_one('.header-col a.right-h6')
    location = location_link.get_text(strip=True) if location_link else 'Location not found'

    # Extract the year built
    built_in_year = placard.select_one('.data-points-a li:nth-child(1)')
    built_in = built_in_year.get_text(strip=True) if built_in_year else ''

    # Extract the space size
    space_size = placard.select_one('.data-points-a li:nth-child(2)')
    space = space_size.get_text(strip=True) if space_size else ''

    # Extract price information
    price_info = placard.select_one('.data-points-b li:nth-child(1)')
    price = price_info.get_text(strip=True).replace('Price', '').strip() if price_info else ''

    # Print the extracted data
    print(f'{address}  {subtitle_alpha}\n{location}\n{built_in}\n{space}\n{price}')


def parse_page_content(soup):
    # Select all article elements (placards)
    placards = soup.select('.placard-content')
    print(type(placards))

    for index, placard in enumerate(placards):
        # Extract the main address information
        address_link = placard.select_one('.header-col h4 a')
        if address_link:
            address = address_link.get_text(strip=True)
        else:
            if index == 0:
                parse_first_placard(soup)
                continue
            'Address not found'

        # Extract additional property name or identifier
        subtitle_alpha_link = placard.select_one('.header-col h6 a')
        subtitle_alpha = subtitle_alpha_link.get_text(strip=True) if subtitle_alpha_link else ''

        # Extract location information including city, state, and zip code
        location_link = placard.select_one('.header-col .subtitle-beta')
        location = location_link.get_text(strip=True) if location_link else 'Location not found'

        print(f'\n{address}  {subtitle_alpha}\n{location}')

        lis = placard.find_all('li')
        for index, li in enumerate(lis):
            li_text = li.get_text(strip=True)
            print(f'{li_text}')

        # # Extract the year built
        # built_in_year = placard.select_one('.data-points-2c li:nth-child(1)')
        # built_in = built_in_year.get_text(strip=True) if built_in_year else ''

        # # Extract the space size
        # space_size = placard.select_one('.data-points-2c li:nth-child(2)')
        # space = space_size.get_text(strip=True) if space_size else ''

        # # Extract price information
        # price_info = placard.select_one('.data-points-2c li:nth-child(3)')
        # price = price_info.get_text(strip=True).replace('Price', '').strip() if price_info else ''

        # Print the extracted data
        # print(f'{address}  {subtitle_alpha}\n{location}')


def get_placard_url(soup):
    # Find all <a> tags within elements with class 'placard'
    placards = soup.select('.placard-pseudo a')

    placard_urls = []

    # Iterate over all found <a> tags and print their href attribute
    for placard in placards:
        href = placard.get('href')
        if href:
            placard_urls.append(href)

    return placard_urls


def get_contact(soup):
    # Find all <a> tags within the <ul> element with id "contact-form-contacts"
    contacts = soup.select('ul#contact-form-contacts a.avatar-container')
    contact_urls = []
    # Append all found broker profile links to the contact_urls list
    for link in contacts:
        href = link.get('href')
        if href:
            contact_urls.append(href)

    # # Find all <a> tags within elements with class 'contact'
    # contacts = soup.select('#contact-form-contacts.avatar-container')

    # contact_urls = []

    # # Iterate over all found <a> tags and print their href attribute
    # for contact in contacts:
    #     href = contact.get('href')
    #     if href:
    #         contact_urls.append(href)

    return contact_urls


# def get_info(soup):
#     # Select the element containing the name using its CSS path
#     full_name = soup.select_one("h1.bd-content-highlight span").text.strip()
#     full_name = full_name.split(" ")
#     first_name, last_name = full_name[0], full_name[-1]
#
#     content_title = soup.select_one("h2.bd-content-title span").text.strip()
#     content_title = content_title.split(",")
#
#     role, company_name = content_title[0], content_title[1]
#
#     soup.select_one()
#
#     # Select the element containing the phone number using its CSS path
#     phone = soup.select_one("p.bd-header-modules-desktop-all-phones span").text.strip()
#
#     return first_name, last_name, phone, company_name, role

def get_info(soup):
    # Initialize default values
    first_name, last_name, phone, company_name, role = '', '', '', '', ''

    # Select the element containing the name using its CSS path
    full_name_element = soup.select_one("h1.bd-content-highlight span")
    if full_name_element:
        full_name = full_name_element.get_text(strip=True).split(" ")
        if len(full_name) > 1:
            first_name, last_name = full_name[0], full_name[-1]

    content_title_element = soup.select_one("h2.bd-content-title span")
    if content_title_element:
        content_title = content_title_element.get_text(strip=True).split(",")
        if len(content_title) > 1:
            role, company_name = content_title[0], content_title[1]

    phone_element = soup.select_one("p.bd-header-modules-desktop-all-phones span")
    if phone_element:
        phone = phone_element.get_text(strip=True)

    return first_name, last_name, phone, company_name, role


# Set options for Selenium WebDriver
options = Options()
options.headless = True  # You can choose to run in headless mode

# Specify the path to ChromeDriver
# webdriver_path = r"C:\Users\WDAGUtilityAccount\Downloads\chromedriver_win32\chromedriver.exe"
webdriver_path = r"/Users/ivy/Downloads/chromedriver-mac-arm64/chromedriver"

# Create the WebDriver object
service = Service(webdriver_path)
driver = webdriver.Chrome(service=service, options=options)

# Target URL - can change city
url = 'https://www.loopnet.com/search/restaurants/buffalo-ny/for-lease/'

# Use Selenium to open the webpage
driver.get(url)

# Wait for some time to ensure JavaScript is loaded
# time.sleep(5)  # The wait time may need to be adjusted based on the actual situation
try:
    # Wait for the element with ID "placardSec" to become visible within 5 seconds
    element = WebDriverWait(driver, 5).until(
        EC.visibility_of_element_located((By.ID, "placardSec"))
    )
    # print("Element is visible!")
except TimeoutException:
    print("Element not visible within 5 seconds")

# Get the webpage source code
web_content = driver.page_source

# Print the obtained webpage content
# print(web_content)
# exit()


# Assume you have already obtained the webpage content using requests and stored it in the variable web_content
# web_content = requests.get(url).text


placard_urls = []
while True:
    # Use BeautifulSoup to parse the webpage content
    soup = BeautifulSoup(web_content, 'html.parser')

    # parse_page_content(soup)

    placard_urls += get_placard_url(soup)

    next_page_element = soup.find('a', {'data-automation-id': 'NextPage'})
    if next_page_element:
        next_page_url = next_page_element.get('href')
        driver.get(next_page_url)
        # time.sleep(5)
        try:
            # Wait for the element with ID "placardSec" to become visible within 5 seconds
            element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.ID, "placardSec"))
            )
            print("Element is visible!")
        except TimeoutException:
            print("Element not visible within 5 seconds")
        web_content = driver.page_source
    else:
        break

print(len(placard_urls))

contacts_urls = []

for url in placard_urls:
    driver.get(url)
    time.sleep(1)
    web_content = driver.page_source
    soup = BeautifulSoup(web_content, 'html.parser')
    contact_urls = get_contact(soup)
    contacts_urls.append(contact_urls)
    print(contact_urls)

# data = []
#
# for index, contact_urls in enumerate(contacts_urls):
#     contact_url = contact_urls[0]  # only use the first contact url
#     driver.get(contact_url)
#     time.sleep(1)
#     web_content = driver.page_source
#     soup = BeautifulSoup(web_content, 'html.parser')
#     first_name, last_name, phone, company_name, role = get_info(soup)
#     city = 'Albany'
#     link = placard_urls[index]
#     print(first_name, last_name, phone, company_name, role, city, link)
#     data.append([first_name, last_name, phone, company_name, role, city, link])

data = []

for index, contact_urls in enumerate(contacts_urls):
    if contact_urls:  # Check if there are any contact URLs
        contact_url = contact_urls[0]  # only use the first contact URL
        driver.get(contact_url)
        time.sleep(1)
        web_content = driver.page_source
        soup = BeautifulSoup(web_content, 'html.parser')
        first_name, last_name, phone, company_name, role = get_info(soup)
        city = 'Buffalo'
        link = placard_urls[index]
        if first_name and last_name and phone:  # Ensure essential fields are not empty
            print(first_name, last_name, phone, company_name, role, city, link)
            data.append([first_name, last_name, phone, company_name, role, city, link])
        else:
            print(f"Skipping incomplete contact info at index {index}")

# parse_page_content(soup)z

# Close the WebDriver
driver.quit()

# add data to google sheet

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r"/Users/ivy/Downloads/apicred.json", scope)
client = gspread.authorize(creds)

#edit the following line with the sheet # that you are adding responses to
sheet = client.open('LL Contact Tracker').sheet4

# sheet.update(range_name=f'A16:G{len(data)+18}', values=data)

# Add data to Google Sheet
if data:
    sheet.update(range_name=f'A3:G{len(data)+5}', values=data)
else:
    print("No valid data to update in the Google Sheet.")