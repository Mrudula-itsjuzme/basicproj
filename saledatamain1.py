import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from tkinter import font as tkfont
from tkinter import colorchooser
import pandas as pd
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkbootstrap import Style

class SalesDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Sales Data")
        self.root.geometry("800x600")
        
        # Use ttkbootstrap for a modern look
        self.style = Style(theme="flatly")
        
        # Define fonts and colors
        self.title_font = tkfont.Font(family="Helvetica", size=20, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=12)
        self.bg_color = "#f0f8ff"
        self.accent_color = "#4682b4"

        # Create and pack widgets
        self.create_welcome_screen()

        # Initialize data storage
        self.data = pd.DataFrame(columns=["Employee", "Sales", "Date"])

    def create_welcome_screen(self):
        # Clear window for welcome screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Welcome label
        welcome_label = ttk.Label(self.root, text="Welcome to Sales Data Manager!", font=self.title_font, style="primary.TLabel")
        welcome_label.pack(pady=20)

        # Start button
        start_button = ttk.Button(self.root, text="Get Started", style="primary.TButton", command=self.create_main_screen)
        start_button.pack(pady=20)

        # Change theme button
        theme_button = ttk.Button(self.root, text="Change Theme", style="secondary.TButton", command=self.change_theme)
        theme_button.pack(pady=10)

        # Help button
        help_button = ttk.Button(self.root, text="Help", style="info.TButton", command=self.show_help)
        help_button.pack(pady=10)

    def create_main_screen(self):
        # Clear window for main screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Data Entry Tab
        self.data_entry_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_entry_frame, text="Data Entry")

        # Data View Tab
        self.data_view_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.data_view_frame, text="Data View")

        # Graphs Tab
        self.graphs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graphs_frame, text="Graphs")

        self.create_data_entry_tab()
        self.create_data_view_tab()
        self.create_graphs_tab()

    def create_data_entry_tab(self):
        # Data Entry Tab layout
        ttk.Label(self.data_entry_frame, text="Employee Name:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ttk.Label(self.data_entry_frame, text="Sales Amount:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ttk.Label(self.data_entry_frame, text="Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10, sticky="e")

        self.employee_entry = ttk.Entry(self.data_entry_frame)
        self.employee_entry.grid(row=0, column=1, padx=10, pady=10)
        self.sales_entry = ttk.Entry(self.data_entry_frame)
        self.sales_entry.grid(row=1, column=1, padx=10, pady=10)
        self.date_entry = ttk.Entry(self.data_entry_frame)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self.data_entry_frame, text="Add Data", style="primary.TButton", command=self.add_data).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(self.data_entry_frame, text="Add Random Data", style="secondary.TButton", command=self.add_random_data).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(self.data_entry_frame, text="Generate Summary", style="info.TButton", command=self.generate_summary).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        ttk.Button(self.data_entry_frame, text="Save Data", style="success.TButton", command=self.save_data).grid(row=6, column=0, columnspan=2, padx=10, pady=10)

    def create_data_view_tab(self):
        # Search frame
        search_frame = ttk.Frame(self.data_view_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)
        ttk.Button(search_frame, text="Search", command=self.search_data).pack(side=tk.LEFT, padx=5)

        # Treeview
        self.tree = ttk.Treeview(self.data_view_frame, columns=("Employee", "Sales", "Date"), show="headings")
        self.tree.heading("Employee", text="Employee")
        self.tree.heading("Sales", text="Sales")
        self.tree.heading("Date", text="Date")
        self.tree.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Buttons frame
        buttons_frame = ttk.Frame(self.data_view_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Button(buttons_frame, text="Edit", command=self.edit_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Delete", command=self.delete_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Refresh", command=self.view_data).pack(side=tk.LEFT, padx=5)

    def create_graphs_tab(self):
        # Graphs options
        options_frame = ttk.Frame(self.graphs_frame)
        options_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(options_frame, text="Graph Type:").pack(side=tk.LEFT, padx=5)
        self.graph_type = tk.StringVar(value="Bar")
        graph_type_combo = ttk.Combobox(options_frame, textvariable=self.graph_type, values=["Bar", "Line", "Pie"])
        graph_type_combo.pack(side=tk.LEFT, padx=5)

        ttk.Button(options_frame, text="Generate Graph", command=self.generate_graph).pack(side=tk.LEFT, padx=5)

        # Graph area
        self.graph_area = ttk.Frame(self.graphs_frame)
        self.graph_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def add_data(self):
        employee = self.employee_entry.get()
        sales = self.sales_entry.get()
        date = self.date_entry.get()

        if employee and sales and date:
            try:
                sales = float(sales)
                date = datetime.strptime(date, "%Y-%m-%d")
                new_data = pd.DataFrame([[employee, sales, date]], columns=["Employee", "Sales", "Date"])
                self.data = pd.concat([self.data, new_data], ignore_index=True)
                self.employee_entry.delete(0, tk.END)
                self.sales_entry.delete(0, tk.END)
                self.date_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Data added successfully!")
                self.view_data()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check sales amount and date format.")
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def view_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=(row["Employee"], row["Sales"], row["Date"].strftime("%Y-%m-%d")))

    def change_theme(self):
        themes = self.style.theme_names()
        new_theme = simpledialog.askstring("Change Theme", f"Choose a theme: {', '.join(themes)}")
        if new_theme in themes:
            self.style.theme_use(new_theme)

    def add_random_data(self):
        num_employees = simpledialog.askinteger("Random Data", "How many employees do you want to generate?", minvalue=1, maxvalue=100)
        if num_employees is None:
            return

        employees = [f"Employee_{i}" for i in range(1, num_employees + 1)]
        for _ in range(10 * num_employees):  # Add 10 entries per employee
            employee = random.choice(employees)
            sales = round(random.uniform(100, 10000), 2)
            date = datetime.now() - timedelta(days=random.randint(0, 365))
            new_data = pd.DataFrame([[employee, sales, date]], columns=["Employee", "Sales", "Date"])
            self.data = pd.concat([self.data, new_data], ignore_index=True)
        messagebox.showinfo("Success", f"Random data for {num_employees} employees added successfully!")
        self.view_data()

    def generate_summary(self):
        if self.data.empty:
            messagebox.showwarning("Warning", "No data available for summary.")
            return

        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data['Year'] = self.data['Date'].dt.year
        self.data['Month'] = self.data['Date'].dt.to_period('M')

        yearly_summary = self.data.groupby('Year').agg({'Sales': ['sum', 'mean']})
        monthly_summary = self.data.groupby('Month').agg({'Sales': ['sum', 'mean']})

        summary_window = tk.Toplevel(self.root)
        summary_window.title("Sales Summary")

        ttk.Label(summary_window, text="Yearly Summary", font=self.title_font).pack(pady=10)
        yearly_tree = ttk.Treeview(summary_window, columns=("Year", "Total", "Average"), show="headings")
        yearly_tree.heading("Year", text="Year")
        yearly_tree.heading("Total", text="Total Sales")
        yearly_tree.heading("Average", text="Average Sales")
        yearly_tree.pack(pady=10)

        for index, row in yearly_summary.iterrows():
            yearly_tree.insert("", tk.END, values=(index, f"{row[('Sales', 'sum')]:.2f}", f"{row[('Sales', 'mean')]:.2f}"))

        ttk.Label(summary_window, text="Monthly Summary", font=self.title_font).pack(pady=10)
        monthly_tree = ttk.Treeview(summary_window, columns=("Month", "Total", "Average"), show="headings")
        monthly_tree.heading("Month", text="Month")
        monthly_tree.heading("Total", text="Total Sales")
        monthly_tree.heading("Average", text="Average Sales")
        monthly_tree.pack(pady=10)

        for index, row in monthly_summary.iterrows():
            monthly_tree.insert("", tk.END, values=(index, f"{row[('Sales', 'sum')]:.2f}", f"{row[('Sales', 'mean')]:.2f}"))

    def save_data(self):
        if self.data.empty:
            messagebox.showwarning("Warning", "No data available to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as f:
                f.write(self.data.to_string(index=False))
            messagebox.showinfo("Success", f"Data saved to {file_path}")

    def search_data(self):
        search_term = self.search_entry.get().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in self.data.iterrows():
            if (search_term in str(row["Employee"]).lower() or
                search_term in str(row["Sales"]).lower() or
                search_term in str(row["Date"]).lower()):
                self.tree.insert("", tk.END, values=(row["Employee"], row["Sales"], row["Date"].strftime("%Y-%m-%d")))

    def edit_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to edit.")
            return

        item = self.tree.item(selected_item)
        values = item['values']
        
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Data")

        ttk.Label(edit_window, text="Employee:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Label(edit_window, text="Sales:").grid(row=1, column=0, padx=5, pady=5)
        ttk.Label(edit_window, text="Date:").grid(row=2, column=0, padx=5, pady=5)

        employee_var = tk.StringVar(value=values[0])
        sales_var = tk.StringVar(value=values[1])
        date_var = tk.StringVar(value=values[2])

        employee_entry = ttk.Entry(edit_window, textvariable=employee_var)
        employee_entry.grid(row=0, column=1, padx=5, pady=5)
        sales_entry = ttk.Entry(edit_window, textvariable=sales_var)
        sales_entry.grid(row=1, column=1, padx=5, pady=5)
        date_entry = ttk.Entry(edit_window, textvariable=date_var)
        date_entry.grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            try:
                new_employee = employee_var.get()
                new_sales = float(sales_var.get())
                new_date = datetime.strptime(date_var.get(), "%Y-%m-%d")

                index = self.data.index[(self.data['Employee'] == values[0]) & 
                                        (self.data['Sales'] == float(values[1])) & 
                                        (self.data['Date'] == datetime.strptime(values[2], "%Y-%m-%d"))].tolist()[0]

                self.data.at[index, 'Employee'] = new_employee
                self.data.at[index, 'Sales'] = new_sales
                self.data.at[index, 'Date'] = new_date

                messagebox.showinfo("Success", "Data updated successfully!")
                edit_window.destroy()
                self.view_data()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check your entries.")

        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def delete_data(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select an item to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this item?"):
            item = self.tree.item(selected_item)
            values = item['values']
            
            index = self.data.index[(self.data['Employee'] == values[0]) & 
                                    (self.data['Sales'] == float(values[1])) & 
                                    (self.data['Date'] == datetime.strptime(values[2], "%Y-%m-%d"))].tolist()[0]
            
            self.data = self.data.drop(index)
            self.view_data()
            messagebox.showinfo("Success", "Data deleted successfully!")

    def generate_graph(self):
        if self.data.empty:
            messagebox.showwarning("Warning", "No data available for graphing.")
            return

        graph_type = self.graph_type.get()

        # Clear previous graph
        for widget in self.graph_area.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(10, 6))

        if graph_type == "Bar":
            employee_sales = self.data.groupby('Employee')['Sales'].sum()
            employee_sales.plot(kind='bar', ax=ax)
            ax.set_ylabel('Total Sales')
            ax.set_title('Total Sales by Employee')
        elif graph_type == "Line":
            self.data['Date'] = pd.to_datetime(self.data['Date'])
            daily_sales = self.data.groupby('Date')['Sales'].sum()
            daily_sales.plot(kind='line', ax=ax)
            ax.set_ylabel('Total Sales')
            ax.set_title('Daily Sales Trend')
        elif graph_type == "Pie":
            employee_sales = self.data.groupby('Employee')['Sales'].sum()
            employee_sales.plot(kind='pie', ax=ax, autopct='%1.1f%%')
            ax.set_ylabel('')
            ax.set_title('Sales Distribution by Employee')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_area)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        canvas.draw()

    def show_help(self):
        help_text = """
        Welcome to the Sales Data Manager!

        This application allows you to manage and analyze employee sales data.

        Key Features:
        1. Add individual sales data entries
        2. Generate random sales data for multiple employees
        3. View and search through your data
        4. Edit or delete existing entries
        5. Generate summaries of your sales data
        6. Create visual graphs of your data
        7. Save your data to a text file

        To get started, click on the 'Get Started' button on the welcome screen.
        You can switch between different tabs to access various features.

        If you need further assistance, please contact support.
        """
        messagebox.showinfo("Help", help_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesDataApp(root)
    root.mainloop()