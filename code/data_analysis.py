import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates


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
            loc="center left",
            bbox_to_anchor=(1, 0.5),
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
    Generate a time series plot of job postings over time by industry with better visualization.
    """
    try:
        # Ensure 'date_posted' is in datetime format
        if not pd.api.types.is_datetime64_any_dtype(data['date_posted']):
            data['date_posted'] = pd.to_datetime(data['date_posted'], errors='coerce')

        # Filter out rows where industry is "Other"
        data = data[data['industry'] != 'Other']

        # Filter valid dates and group by industry and date
        valid_data = data.dropna(subset=['date_posted'])
        industry_date_counts = valid_data.groupby(['industry', 'date_posted']).size().unstack(fill_value=0)

        # Apply a rolling average (e.g., 30-day window)
        rolling_window = 30  # Use a 30-day window for a smoother line
        smoothed_data = industry_date_counts.T.rolling(window=rolling_window, min_periods=1).mean().T

        # Create the plot
        figure, ax = plt.subplots(figsize=(12, 6))  # Adjust the figure size
        for industry in smoothed_data.index:
            ax.plot(
                smoothed_data.columns,
                smoothed_data.loc[industry],
                label=industry
            )

        # Format the x-axis to reduce tick density
        ax.xaxis.set_major_locator(mdates.YearLocator())  # Major ticks every year
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))  # Format as Year only
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right', fontsize=10)  # Rotate labels for readability

        # Simplify gridlines
        ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)  # Thinner, less prominent gridlines

        # Add labels and title
        ax.set_title('Job Postings Over Time by Industry', fontsize=14)
        ax.set_xlabel('Date Posted', fontsize=12)
        ax.set_ylabel('Average Number of Postings', fontsize=12)

        # Adjust the legend
        ax.legend(
            title='Industry',
            fontsize=9,
            title_fontsize=10,
            loc='upper center',
            bbox_to_anchor=(0.5, -0.3),  # Move legend below the plot
            ncol=4  # Reduce number of columns if necessary
        )

        # Adjust layout to prevent overlaps
        plt.tight_layout(rect=[0.1, 0.1, 1, 1])  # Add padding below for legend

        return figure

    except KeyError as e:
        print("KeyError: Missing 'date_posted' or 'industry' column in data. Please check the dataset.")
        raise e
    except Exception as e:
        print("An error occurred while creating the line chart:", str(e))
        raise e
    
def get_roles_figure(data):
    """
    Generate a bar chart of the most common job roles.
    """
    role_counts = data['role'].value_counts().head(10)
    figure, ax = plt.subplots(figsize=(10, 4))
    role_counts.plot(kind='bar', ax=ax, color='skyblue')
    ax.set_title('Top 10 Job Roles', fontsize=16)
    ax.set_xlabel('Role', fontsize=12)
    ax.set_ylabel('Number of Postings', fontsize=8)
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
