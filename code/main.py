import io
import pandas as pd
import dependencies as d
import data_cleaning as dc
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
local_path = '/Users/ayushtripathi/dsp_final_Group-G2_H-/testing_data/Jobs_NYC_Postings.csv'
df_ny = d.format_ny(pd.read_csv(local_path))

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
Data Cleaning
'''

# Combine dataframes into one
data = pd.concat([df_jobright, df_cvrve, df_ny], ignore_index=True)

# Output raw data to a CSV for inspection
data.to_csv('raw_jobs_data.csv', index=False)
print("Raw data saved to 'raw_jobs_data.csv'.")

# Clean the data
cleaned_data = dc.clean_data(data)

# Output cleaned data to a CSV for inspection
cleaned_data.to_csv('cleaned_jobs_data.csv', index=False)
print("Cleaned data saved to 'cleaned_jobs_data.csv'.")

'''
Launch Dashboard
'''

# Launch the Tkinter dashboard
print("Launching the job analysis dashboard...")
ui.launch_ui(cleaned_data)
