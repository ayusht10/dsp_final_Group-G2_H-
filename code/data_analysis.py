import pandas as pd
import matplotlib.pyplot as plt

def get_location_figure(data):
    # Get top 5 locations and group the rest as "Others"
    location_counts = data['Location'].value_counts(normalize=True) * 100
    top_locations = location_counts.head(5)
    others = location_counts[5:].sum()
    top_locations['Others'] = others

    # Plot the pie chart
    figure, ax = plt.subplots(figsize=(8, 8))
    top_locations.plot.pie(autopct='%1.1f%%', ax=ax, startangle=140)
    ax.set_title('Job Location Distribution')
    ax.set_ylabel('')  # Hide y-axis label
    ax.legend(top_locations.index, loc="best", fontsize=8, bbox_to_anchor=(1, 0.5))
    return figure


def get_dates_figure(data):
    data['Date Posted'] = pd.to_datetime(data['Date Posted'], format='%b %d, %Y')
    date_counts = data['Date Posted'].value_counts().sort_index()
    figure, ax = plt.subplots(figsize=(10, 5))
    date_counts.plot(kind='line', ax=ax)
    ax.set_title('Job Postings Over Time')
    ax.set_xlabel('Date Posted')
    ax.set_ylabel('Number of Job Postings')
    ax.grid(True)
    return figure


def get_roles_figure(data):
    role_counts = data['Role'].value_counts().head(10)
    figure, ax = plt.subplots(figsize=(10, 5))
    role_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 10 Job Roles')
    ax.set_xlabel('Role')
    ax.set_ylabel('Number of Postings')
    ax.set_xticklabels(role_counts.index, rotation=45, fontsize=8)
    plt.tight_layout()
    return figure
