import pandas as pd
import requests
import re
from bs4 import BeautifulSoup

'''
Function to scrap data from a given URL
'''
def scrap(url):
    """
    :param url: String containing the website's URL to scrap
    :return: BeautifulSoup4 object containing the raw data scrapped from website
    """
    # Ensuring the response was successful
    try:
        website = requests.get(url)
        website.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e
    # Creating BeautifulSoup object
    soup = BeautifulSoup(website.text, 'html.parser')
    return soup

'''
Function to format the dataframe from New York website's data
'''
def format_ny(data):
    """
    :param data: Pandas DataFrame containing raw csv data downloaded from website
    :return:
    """
    # Making new dataframe with only relevant data
    df = data[['Agency', 'Business Title', 'To Apply', 'Work Location 1', 'Posting Date']]
    # Renaming new dataframe columns
    df = df.rename(columns={'Agency': 'Company', 'Business Title': 'Role', 'To Apply': 'Application/Link',
                       'Work Location 1': 'Work Model', 'Posting Date': 'Date Posted'})
    # Making jobs list with relevant data
    jobs = []
    # Iterating over dataframe and adjusting each column accordingly
    for idx, row in df.iterrows():
        # Formating company name
        company = row['Company'].strip().capitalize()
        # Formating role name
        role = row['Role'].strip()
        # Adding location
        location = "New York, NY"
        # Extracting and adjust application links
        link_pattern = r'(https?://[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+|www\.[a-zA-Z0-9.-]+(?:\.[a-zA-Z]{2,})+)'
        match = re.search(link_pattern, str(row['Application/Link']))
        application_link = match.group(0) if match else None
        application_link = 'https://' + application_link if (application_link
                                    and not application_link.startswith('https://')) else application_link
        # Adjusting work model values
        if "remote" in str(row['Work Model']).lower():
            work_model = "Remote"
        elif type(row['Work Model']) == float:
            work_model = None
        else:
            work_model = "On Site"
        # Formatting date posted
        month, day, year = row['Date Posted'].split('/')
        month_map = {'01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr', '05': 'May', '06': 'Jun', '07': 'Jul',
                     '08': 'Aug', '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'}
        date_posted = f"{month_map[month]} {int(day)}, {year}"
        jobs.append({'Company': company, 'Role': role, 'Location': location, 'Application/Link': application_link,
                     'Work Model': work_model, 'Date Posted': date_posted})
    df = pd.DataFrame(jobs)
    return df

'''
Function to format the tables with data extracted from GitHub repositories
'''
def format_git(table):
    """
    :param table: BeautifulSoup4 object containing the job table's <tr> elements
    :return: List of dictionaries containing the job information
    """
    # Making jobs list
    jobs = []
    # Extracting job information from each row
    for row in table[1:]:
        columns = row.find_all('td')
        if len(columns) == 5:
            # Extracting company name
            company = columns[0].text.strip()
            # Extracting role name
            role = columns[1].text.capitalize().strip()
            # Extracting location
            location = columns[2].text.strip()
            # Extracting application link and work model according to availability
            application_link = None
            work_model = None
            if columns[3].find('a'):
                application_link = columns[3].find('a')['href'].strip()
            elif columns[1].find('a'):
                application_link = columns[1].find('a')['href'].strip()
                work_model = columns[3].text.strip()
            # Extracting date posted
            date_posted = columns[4].text.strip() + ", 2024"
            # Skipping mismatched rows
            date_pattern = r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}\b'
            if not re.search(date_pattern, date_posted) or company == "↳":
                continue
            # Appending job data into list as a dictionary
            jobs.append({'Company': company, 'Role': role, 'Location': location, 'Application/Link': application_link,
                         'Work Model': work_model, 'Date Posted': date_posted})
    return jobs


