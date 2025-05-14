import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter import font as tkfont
from tkinter import colorchooser
import pandas as pd
import random
from datetime import datetime, timedelta

class SalesDataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Sales Data")
        
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
        welcome_label = tk.Label(self.root, text="Welcome to Sales Data Manager!", font=self.title_font, bg=self.bg_color, fg=self.accent_color)
        welcome_label.pack(pady=20)

        # Start button
        start_button = tk.Button(self.root, text="Get Started", font=self.button_font, bg=self.accent_color, fg="white", command=self.create_main_screen)
        start_button.pack(pady=20)

        # Change background color button
        color_button = tk.Button(self.root, text="Change Background Color", font=self.button_font, bg=self.accent_color, fg="white", command=self.change_bg_color)
        color_button.pack(pady=10)

    def create_main_screen(self):
        # Clear window for main screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main screen layout
        tk.Label(self.root, text="Employee Name:", bg=self.bg_color).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Sales Amount:", bg=self.bg_color).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self.root, text="Date (YYYY-MM-DD):", bg=self.bg_color).grid(row=2, column=0, padx=10, pady=10)

        self.employee_entry = tk.Entry(self.root)
        self.employee_entry.grid(row=0, column=1, padx=10, pady=10)
        self.sales_entry = tk.Entry(self.root)
        self.sales_entry.grid(row=1, column=1, padx=10, pady=10)
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Add Data", font=self.button_font, bg=self.accent_color, fg="white", command=self.add_data).grid(row=3, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="View Data", font=self.button_font, bg=self.accent_color, fg="white", command=self.view_data).grid(row=4, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Add Random Data", font=self.button_font, bg=self.accent_color, fg="white", command=self.add_random_data).grid(row=5, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Generate Summary", font=self.button_font, bg=self.accent_color, fg="white", command=self.generate_summary).grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Save Data", font=self.button_font, bg=self.accent_color, fg="white", command=self.save_data).grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Employee", "Sales", "Date"), show="headings")
        self.tree.heading("Employee", text="Employee")
        self.tree.heading("Sales", text="Sales")
        self.tree.heading("Date", text="Date")
        self.tree.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

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
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Please check sales amount and date format.")
        else:
            messagebox.showwarning("Warning", "Please fill out all fields.")

    def view_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for index, row in self.data.iterrows():
            self.tree.insert("", tk.END, values=(row["Employee"], row["Sales"], row["Date"].strftime("%Y-%m-%d")))

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.root.configure(bg=self.bg_color)
            self.create_main_screen()

    def add_random_data(self):
        employees = ["John", "Alice", "Bob", "Emma", "David"]
        for _ in range(10):  # Add 10 random entries
            employee = random.choice(employees)
            sales = round(random.uniform(100, 10000), 2)
            date = datetime.now() - timedelta(days=random.randint(0, 365))
            new_data = pd.DataFrame([[employee, sales, date]], columns=["Employee", "Sales", "Date"])
            self.data = pd.concat([self.data, new_data], ignore_index=True)
        messagebox.showinfo("Success", "Random data added successfully!")

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

        tk.Label(summary_window, text="Yearly Summary", font=self.title_font).pack(pady=10)
        yearly_tree = ttk.Treeview(summary_window, columns=("Year", "Total", "Average"), show="headings")
        yearly_tree.heading("Year", text="Year")
        yearly_tree.heading("Total", text="Total Sales")
        yearly_tree.heading("Average", text="Average Sales")
        yearly_tree.pack(pady=10)

        for index, row in yearly_summary.iterrows():
            yearly_tree.insert("", tk.END, values=(index, f"{row[('Sales', 'sum')]:.2f}", f"{row[('Sales', 'mean')]:.2f}"))

        tk.Label(summary_window, text="Monthly Summary", font=self.title_font).pack(pady=10)
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

if __name__ == "__main__":
    root = tk.Tk()
    app = SalesDataApp(root)
    root.mainloop()