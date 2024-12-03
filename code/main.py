import io
import pandas as pd
import dependencies as d

pd.set_option('display.max_columns', None)

'''
New York City Jobs
'''

# Setting url of NYC website
url = 'https://catalog.data.gov/dataset/nyc-jobs/resource/ab4444d9-85a6-4946-a0ef-3d3638485de8?inner_span=True'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Finding link to download csv file
download_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('DOWNLOAD')]

'''
DEFINITE VERSION CODE

# Making dataframe with csv file downloaded
soup = d.scrap(download_links[0])
df_ny = d.format_ny(pd.read_csv(io.StringIO(soup.text)))
'''

'''
TEMPORARY CODE FOR FASTER RUNNING
'''

# Making dataframe from local csv file
local_path = '/Users/lucas.oliveira/Library/CloudStorage/OneDrive-ChathamUniversity/Classes/Fall 2024/Data Focused Python/Final Project/Jobs_NYC_Postings.csv'
df_ny = d.format_ny(pd.read_csv(local_path))

'''
Cvrve Jobs
'''

# Setting url of GitHub repository
url = 'https://github.com/cvrve/New-Grad-2025'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Getting jobs table from HTML code
table = soup.find('markdown-accessiblity-table').find_all('tr')

# Formatting job information scrapped
jobs_cvrve = d.format_git(table[1:])

# Making dataframe with jobs_cqs list
df_cvrve = pd.DataFrame(jobs_cvrve)

'''
Jobright.ai Jobs
'''

# Setting url of GitHub repository
url = 'https://github.com/jobright-ai/2025-Data-Analysis-New-Grad'

# Getting BeautifulSoup object
soup = d.scrap(url)

# Getting jobs table from HTML code
table = soup.find('markdown-accessiblity-table').find_all('tr')

# Formatting job information scrapped
jobs_jobright = d.format_git(table[1:])

# Making dataframe with jobs_cqs list
df_jobright = pd.DataFrame(jobs_jobright)

'''
Data Analysis
'''

# Combining dataframes into one
data = pd.concat([df_jobright, df_cvrve, df_ny], ignore_index=True)
print(data.shape)
print(data.head())



