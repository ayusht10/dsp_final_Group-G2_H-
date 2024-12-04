import io
import pandas as pd
import dependencies as d
import data_cleaning as dc
import clean_csv as cc
import ui

pd.set_option('display.max_columns', None)

'''
New York City Jobs
'''

# Setting URL of NYC website
url = 'https://catalog.data.gov/dataset/nyc-jobs/resource/ab4444d9-85a6-4946-a0ef-3d3638485de8?inner_span=True'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Finding link to download csv file
download_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('DOWNLOAD')]

'''
TEMPORARY CODE FOR FASTER RUNNING
'''

# Making dataframe from local csv file
local_path = 'Jobs_NYC_Postings.csv'
df_ny_temp = d.format_ny(pd.read_csv(local_path))

'''
DEFINITE VERSION CODE

# Making dataframe with csv file downloaded
soup = d.scrap(download_links[0])
df_ny = d.format_ny(pd.read_csv(io.StringIO(soup.text)))
'''

# Use temporary version for now
df_ny = df_ny_temp

'''
Cvrve Jobs
'''

# Setting URL of GitHub repository
url = 'https://github.com/cvrve/New-Grad-2025'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Getting jobs table from HTML code
table = soup.find('markdown-accessiblity-table').find_all('tr')

# Formatting job information scraped
jobs_cvrve = d.format_git(table[1:])

# Making dataframe with jobs list
df_cvrve = pd.DataFrame(jobs_cvrve)

'''
Jobright.ai Jobs
'''

# Setting URL of GitHub repository
url = 'https://github.com/jobright-ai/2025-Data-Analysis-New-Grad'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Getting jobs table from HTML code
table = soup.find('markdown-accessiblity-table').find_all('tr')

# Formatting job information scraped
jobs_jobright = d.format_git(table[1:])

# Making dataframe with jobs list
df_jobright = pd.DataFrame(jobs_jobright)

'''
Heinz Jobs
'''

# Reading and cleaning Heinz CSV
df_heinz_raw = pd.read_csv("heinz_newsletter_postings.csv")
df_heinz = cc.clean_heinz_csv(df_heinz_raw)

print("Cleaned Heinz Data:")
print(df_heinz.head())

'''
Data Cleaning and Combining
'''

# Standardize column names for all datasets
df_ny.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']
df_cvrve.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']
df_jobright.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']

# Combine all dataframes
data = pd.concat([df_jobright, df_cvrve, df_ny, df_heinz], ignore_index=True)

print("Combined Data Before Cleaning:")
print(data.head())

# Save raw combined data for inspection
data.to_csv('raw_jobs_data.csv', index=False)
print("Raw data saved to 'raw_jobs_data.csv'.")

# Clean combined data
cleaned_data = dc.clean_data(data)

# Save cleaned data for inspection
cleaned_data.to_csv('cleaned_jobs_data.csv', index=False)
print("Cleaned data saved to 'cleaned_jobs_data.csv'.")

'''
Launch Dashboard
'''
# Launch the Tkinter dashboard
print("Launching the job analysis dashboard...")
ui.launch_ui(cleaned_data)
