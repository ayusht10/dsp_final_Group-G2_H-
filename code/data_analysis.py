import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def get_location_figure(data):
    """
    Generate a pie chart of job locations without labels on the pie chart but with a legend.
    """
    try:
        # Get top 5 locations and group the rest as "Others"
        location_counts = data['location_category'].value_counts(normalize=True) * 100
        top_locations = location_counts.head(5)
        others = location_counts[5:].sum()
        if others > 0:
            top_locations['Others'] = others


        # Plot the pie chart
        figure, ax = plt.subplots(figsize=(8, 8))
        wedges, _ = ax.pie(
            top_locations,
            startangle=140,
            wedgeprops=dict(width=0.4),  # Donut-style for better clarity
        )
        ax.set_title('Job Location Distribution', fontsize=16)

        # Add a legend for the labels
        ax.legend(
            wedges,
            top_locations.index,
            title="Locations",
            loc="upper left",
            bbox_to_anchor=(1, 0.8),
            fontsize=9,
        )
        return figure

    except KeyError as e:
        print("KeyError: Missing 'location_category' column in data. Please check the dataset.")
        raise e
    except Exception as e:
        print("An error occurred while creating the pie chart:", str(e))
        raise e



def get_dates_figure(data):
    """
    Generate a time series plot of job postings over time by industry with a legend.
    """
    if not pd.api.types.is_datetime64_any_dtype(data['date_posted']):
        data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce')

    industry_date_counts = data.groupby(['industry', 'date_posted']).size().unstack(fill_value=0)

    figure, ax = plt.subplots(figsize=(12, 6))
    for industry in industry_date_counts.index:
        ax.plot(
            industry_date_counts.columns,
            industry_date_counts.loc[industry],
            label=industry,
            marker='o',
        )

    ax.set_title('Job Postings Over Time by Industry', fontsize=16)
    ax.set_xlabel('Date Posted', fontsize=12)
    ax.set_ylabel('Number of Job Postings', fontsize=12)
    ax.grid(True)
    ax.legend(title='Industry', fontsize=10, loc='upper left', bbox_to_anchor=(1, 1))
    plt.tight_layout()
    return figure


def get_roles_figure(data):
    """
    Generate a bar chart of the most common job roles.
    """
    role_counts = data['role'].value_counts().head(10)
    figure, ax = plt.subplots(figsize=(10, 5))
    role_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 10 Job Roles', fontsize=16)
    ax.set_xlabel('Role', fontsize=12)
    ax.set_ylabel('Number of Postings', fontsize=12)
    ax.set_xticklabels(role_counts.index, rotation=45, fontsize=8)
    plt.tight_layout()
    return figure


def launch_dashboard(data):
    """
    Launch a Tkinter dashboard with all visualizations.
    """
    root = Tk()
    root.title("Job Analysis Dashboard")
    root.geometry("1200x800")

    tab_control = ttk.Notebook(root)

    # Create tabs
    location_tab = ttk.Frame(tab_control)
    dates_tab = ttk.Frame(tab_control)
    roles_tab = ttk.Frame(tab_control)

    tab_control.add(location_tab, text='Locations')
    tab_control.add(dates_tab, text='Postings by Industry')
    tab_control.add(roles_tab, text='Top Roles')
    tab_control.pack(expand=1, fill='both')

    # Add location pie chart
    location_fig = get_location_figure(data)
    location_canvas = FigureCanvasTkAgg(location_fig, location_tab)
    location_canvas.get_tk_widget().pack(fill='both', expand=True)

    # Add postings by industry line chart
    dates_fig = get_dates_figure(data)
    dates_canvas = FigureCanvasTkAgg(dates_fig, dates_tab)
    dates_canvas.get_tk_widget().pack(fill='both', expand=True)

    # Add top roles bar chart
    roles_fig = get_roles_figure(data)
    roles_canvas = FigureCanvasTkAgg(roles_fig, roles_tab)
    roles_canvas.get_tk_widget().pack(fill='both', expand=True)

    root.mainloop()
