import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import data_analysis as da


class JobAnalysisApp:
    def __init__(self, root, data):
        self.root = root
        self.data = data  # Use the full dataset but exclude unnecessary columns in display
        self.filtered_data = data.copy()  # To store filtered data
        self.root.title("Job Analysis Dashboard")
        self.root.geometry("1200x800")

        # Create a container for all frames
        self.frames = {}

        # Initialize frames
        self.init_home_frame()
        self.init_dashboard_frame()

        # Show the home screen by default
        self.show_frame("Home")

    def init_home_frame(self):
        """Initialize the welcome screen frame."""
        frame = tk.Frame(self.root)
        self.frames["Home"] = frame

        # Add a welcome message
        welcome_label = tk.Label(
            frame,
            text="Welcome to KickStart!",
            font=("Arial", 24),
            pady=20
        )
        welcome_label.pack()

        # Add a brief description
        description_label = tk.Label(
            frame,
            text="KickStart your career with the perfect entry role.",
            font=("Arial", 14),
            pady=10
        )
        description_label.pack()

        # Add a button to proceed to the dashboard
        start_button = tk.Button(
            frame,
            text="Go to Dashboard",
            font=("Arial", 14),
            command=lambda: self.show_frame("Dashboard")
        )
        start_button.pack(pady=20)

        frame.pack(fill=tk.BOTH, expand=True)

    def init_dashboard_frame(self):
        """Initialize the dashboard frame with tabs."""
        frame = tk.Frame(self.root)
        self.frames["Dashboard"] = frame

        # Add a "Back to Home" button
        back_button = tk.Button(
            frame,
            text="Back to Home",
            font=("Arial", 14),
            command=lambda: self.show_frame("Home")
        )
        back_button.pack(pady=10, anchor="nw")

        # Create a tab control
        tab_control = ttk.Notebook(frame)
        self.location_tab = ttk.Frame(tab_control)
        self.dates_tab = ttk.Frame(tab_control)
        self.roles_tab = ttk.Frame(tab_control)
        self.data_tab = ttk.Frame(tab_control)

        tab_control.add(self.location_tab, text="Locations")
        tab_control.add(self.dates_tab, text="Dates by Industry")
        tab_control.add(self.roles_tab, text="Top Roles")
        tab_control.add(self.data_tab, text="Data Table")

        tab_control.pack(expand=1, fill="both")

        # Add content to each tab
        self.display_location_analysis()
        self.display_date_analysis()
        self.display_role_analysis()
        self.display_data_table()

        frame.pack(fill=tk.BOTH, expand=True)

    def display_location_analysis(self):
        """Display the location pie chart in the Locations tab."""
        figure = da.get_location_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.location_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_date_analysis(self):
        """Display the postings by industry line chart in the Dates tab."""
        figure = da.get_dates_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.dates_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_role_analysis(self):
        """Display the top roles bar chart in the Roles tab."""
        figure = da.get_roles_figure(self.data)
        canvas = FigureCanvasTkAgg(figure, self.roles_tab)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def display_data_table(self):
        """Display the data table in the Data Table tab."""
        visible_columns = [col for col in self.data.columns if col != 'location_category']

        # Filter options
        filter_frame = tk.Frame(self.data_tab)
        filter_frame.pack(fill=tk.X, pady=5)

        # Dropdown for location
        tk.Label(filter_frame, text="Location:", font=("Arial", 12)).grid(row=0, column=0, padx=5)
        location_options = sorted(self.data['location'].dropna().unique())
        location_var = tk.StringVar()
        location_dropdown = ttk.Combobox(filter_frame, textvariable=location_var, values=location_options)
        location_dropdown.grid(row=0, column=1, padx=5)

        # Dropdown for industry
        tk.Label(filter_frame, text="Industry:", font=("Arial", 12)).grid(row=0, column=2, padx=5)
        industry_options = sorted(self.data['industry'].dropna().unique())
        industry_var = tk.StringVar()
        industry_dropdown = ttk.Combobox(filter_frame, textvariable=industry_var, values=industry_options)
        industry_dropdown.grid(row=0, column=3, padx=5)

        # Input box for role
        tk.Label(filter_frame, text="Role:", font=("Arial", 12)).grid(row=0, column=4, padx=5)
        role_var = tk.StringVar()
        role_entry = tk.Entry(filter_frame, textvariable=role_var)
        role_entry.grid(row=0, column=5, padx=5)

        # Filter button
        def apply_filters():
            filtered = self.data
            if location_var.get():
                filtered = filtered[filtered['location'] == location_var.get()]
            if industry_var.get():
                filtered = filtered[filtered['industry'] == industry_var.get()]
            if role_var.get():
                filtered = filtered[filtered['role'].str.contains(role_var.get(), case=False, na=False)]
            self.filtered_data = filtered
            update_table()

        tk.Button(filter_frame, text="Apply Filters", command=apply_filters).grid(row=0, column=6, padx=5)

        # Data table
        tree = ttk.Treeview(self.data_tab, columns=visible_columns, show="headings", height=20)
        for col in visible_columns:
            tree.heading(col, text=col)
            tree.column(col, width=150 if col != 'application/link' else 300, anchor="w")

        def update_table():
            tree.delete(*tree.get_children())
            for _, row in self.filtered_data.iterrows():
                values = [row[col] for col in visible_columns]
                tree.insert("", tk.END, values=values)

        update_table()

        # Make application links clickable
        def on_tree_select(event):
            selected_item = tree.selection()
            if selected_item:
                item = tree.item(selected_item)
                values = item['values']
                application_link_index = visible_columns.index('application/link')
                application_link = values[application_link_index]
                if application_link.startswith("http"):
                    webbrowser.open(application_link)

        tree.bind("<<TreeviewSelect>>", on_tree_select)
        tree.pack(fill=tk.BOTH, expand=True)

    def show_frame(self, name):
        """Show a specific frame."""
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[name].pack(fill=tk.BOTH, expand=True)


def launch_ui(data):
    root = tk.Tk()
    app = JobAnalysisApp(root, data)
    root.mainloop()
