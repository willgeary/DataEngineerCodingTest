# Will Geary
# 
# willcgeary@gmail.com

# # Part 2 - Web Scrape

# *To Do: Write a script to scrape a sample site and output its data in JSON.*
# 
# *[edgar](http://data-interview.enigmalabs.org/companies/) is a company listings site containing ten pages of company links. Each link endpoint holds company-specific data such as name, description and address. The sole requirement of this part of the test is to produce JSON of all of the company listings data for the site.*
# 
# *Please attach a "solution.json" file of the parsed company listings data along with your solution code in your reply!*

from BeautifulSoup import BeautifulSoup
import json
import urllib2
import re
import pandas as pd


# First, let's get a list of all the companies listed on the site.
base = "http://data-interview.enigmalabs.org/companies/"
page = "?page={}"

# store companies in a list
companies = []

for page_number in range(1,11):
    
    # Construct url query
    url_query = base + page.format(page_number)
    
    # Read url and scrape it with BeautifulSoup
    url = urllib2.urlopen(url_query)
    content = url.read()
    soup = BeautifulSoup(content)

    # find all elements starting with 'a' and id = some number 
    for item in soup.findAll('a', id=re.compile(r"\d+$")):
        href = item.get('href')
        company = re.sub("/companies/", "", href)
        companies.append(company)

print len(companies), "companies have been scraped."


# Next, let's go to each company's individual profile to get the data.

# store results as a list of dictionaries
results = []

# parse data for each company
for company in companies:
    
    company_replace_spaces = re.sub(" ", "%20", company)
    company_url = base + company_replace_spaces
    
    url = urllib2.urlopen(company_url)
    content = url.read()
    soup = BeautifulSoup(content)
    
    company_name = str(soup.findAll('td', id='name')[0].contents[0])
    street_address = str(soup.findAll('td', id='street_address')[0].contents[0])
    street_address_2 = str(soup.findAll('td', id='street_address_2')[0].contents[0])
    city = str(soup.findAll('td', id='city')[0].contents[0])
    state = str(soup.findAll('td', id='state')[0].contents[0])
    zipcode = str(soup.findAll('td', id='zipcode')[0].contents[0])
    phone_number = str(soup.findAll('td', id='phone_number')[0].contents[0])
    website = str(soup.findAll('td', id='website')[0].contents[0])
    description = str(soup.findAll('td', id='description')[0].contents[0])
    
    result = {
        'company_name': company_name,
        'street_address': street_address,
        'street_address_2': street_address_2,
        'city': city,
        'state': state,
        'zipcode': zipcode,
        'phone_number': phone_number,
        'website': website,
        'description': description
    }
    
    results.append(result)

# Save results to json:
with open("solution.json", 'w') as f:
    json.dump(results, f)
