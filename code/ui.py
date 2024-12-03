import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import data_analysis as da


class JobAnalysisApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data
        self.root.title("Job Analysis Dashboard")
        self.root.geometry("1000x700")  # Increase window size for better readability

        # Create tabs for different visualizations
        self.tab_control = ttk.Notebook(root)
        self.location_tab = ttk.Frame(self.tab_control)
        self.dates_tab = ttk.Frame(self.tab_control)
        self.roles_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.location_tab, text='Locations')
        self.tab_control.add(self.dates_tab, text='Dates')
        self.tab_control.add(self.roles_tab, text='Roles')

        self.tab_control.pack(expand=1, fill='both')

        # Add content to each tab
        self.display_location_analysis()
        self.display_date_analysis()
        self.display_role_analysis()

    def display_location_analysis(self):
        figure = da.get_location_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.location_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_date_analysis(self):
        figure = da.get_dates_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.dates_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_role_analysis(self):
        figure = da.get_roles_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.roles_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def launch_ui(data):
    root = tk.Tk()
    app = JobAnalysisApp(root, data)
    root.mainloop()
