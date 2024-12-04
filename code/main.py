import threading
import queue
import io
import pandas as pd
import dependencies as d
import data_cleaning as dc
import clean_csv as cc
import ui

pd.set_option('display.max_columns', None)

def prepare_data(data_queue):
    try:
        # NYC Jobs
        url = 'https://catalog.data.gov/dataset/nyc-jobs/resource/ab4444d9-85a6-4946-a0ef-3d3638485de8?inner_span=True'
        soup = d.scrap(url)
        download_links = [link['href'] for link in soup.find_all('a', href=True) if link['href'].endswith('DOWNLOAD')]
        soup = d.scrap(download_links[0])
        df_ny = d.format_ny(pd.read_csv(io.StringIO(soup.text)))

        # Cvrve Jobs
        url = 'https://github.com/cvrve/New-Grad-2025'
        soup = d.scrap(url)
        table = soup.find('markdown-accessiblity-table').find_all('tr')
        jobs_cvrve = d.format_git(table[1:])
        df_cvrve = pd.DataFrame(jobs_cvrve)

        # Jobright.ai Jobs
        url = 'https://github.com/jobright-ai/2025-Data-Analysis-New-Grad'
        soup = d.scrap(url)
        table = soup.find('markdown-accessiblity-table').find_all('tr')
        jobs_jobright = d.format_git(table[1:])
        df_jobright = pd.DataFrame(jobs_jobright)

        # Heinz Jobs
        df_heinz_raw = pd.read_csv("heinz_newsletter_postings.csv")
        df_heinz = cc.clean_heinz_csv(df_heinz_raw)

        # Standardize Columns
        df_ny.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']
        df_cvrve.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']
        df_jobright.columns = ['company', 'role', 'location', 'application/link', 'work_model', 'date_posted']

        # Combine DataFrames
        data = pd.concat([df_jobright, df_cvrve, df_ny, df_heinz], ignore_index=True)

        # Clean Data
        cleaned_data = dc.clean_data(data)

        # Pass data to the queue
        data_queue.put(cleaned_data)

    except Exception as e:
        data_queue.put(e)

if __name__ == "__main__":
    data_queue = queue.Queue()
    threading.Thread(target=prepare_data, args=(data_queue,), daemon=True).start()
    ui.launch_ui(data_queue)
