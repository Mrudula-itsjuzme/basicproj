import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import math
import random

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("800x900")
        self.history = []
        self.theme = 'light'
        self.mode = 'scientific'
        self.create_welcome_screen()

    def create_welcome_screen(self):
        self.welcome_window = tk.Toplevel(self.root)
        self.welcome_window.title("Welcome")
        self.welcome_window.geometry("500x600")

        tk.Label(self.welcome_window, text="Welcome to the Advanced Calculator!", font=('Arial', 24, 'bold')).pack(pady=20)

        tk.Label(self.welcome_window, text="Choose a Theme:", font=('Arial', 18)).pack(pady=10)

        self.theme_var = tk.StringVar(value='light')
        theme_options = ['Light', 'Dark', 'Blue', 'Green', 'Minty', 'Solar', 'Retro', 'Ocean']

        theme_frame = tk.Frame(self.welcome_window)
        theme_frame.pack(pady=20)

        for theme in theme_options:
            tk.Radiobutton(theme_frame, text=theme, variable=self.theme_var, value=theme.lower(), font=('Arial', 14), command=self.theme_selected).pack(anchor='w', padx=20, pady=5)

        tk.Button(self.welcome_window, text="Start Calculator", font=('Arial', 16), command=self.theme_selected).pack(pady=20)

    def theme_selected(self):
        self.theme = self.theme_var.get()
        self.welcome_window.destroy()
        self.create_calculator_interface()

    def create_calculator_interface(self):
        self.root.deiconify()  # Show the main window
        self.display = tk.Entry(self.root, font=('Arial', 24), bd=10, relief='ridge', justify='right')
        self.display.pack(expand=True, fill='both')

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(expand=True, fill='both')

        self.create_buttons()

        self.switch_button = tk.Button(self.root, text='Switch to Advanced', font=('Arial', 14), command=self.switch_mode)
        self.switch_button.pack(side='bottom', fill='both', pady=5)

        tk.Button(self.root, text='C', font=('Arial', 14), command=self.clear).pack(side='bottom', fill='both', pady=10)

        tk.Button(self.root, text='View History', font=('Arial', 14), command=self.view_history).pack(side='bottom', fill='both', pady=5)

        tk.Button(self.root, text='Interactive Help', font=('Arial', 14), command=self.show_help).pack(side='bottom', fill='both', pady=5)

        self.apply_theme()

    def create_buttons(self):
        self.clear_buttons()

        buttons = [
            '7', '8', '9', '/', 'sqrt', 'pow',
            '4', '5', '6', '*', 'log', 'exp',
            '1', '2', '3', '-', '(', ')',
            '0', '.', '=', '+', 'sin', 'cos',
            'tan', 'asin', 'acos', 'atan', '!', 'nCr',
            'nPr', 'Equation', 'History', 'Themes', 'Unit Converter', 'Font Selection'
        ]

        row = 0
        col = 0
        for button in buttons:
            btn = tk.Button(self.button_frame, text=button, font=('Arial', 14), width=5, height=2)
            btn.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
            btn.bind("<Enter>", self.on_hover)
            btn.bind("<Leave>", self.on_leave)
            if button == '=':
                btn.config(command=self.evaluate)
            elif button == 'History':
                btn.config(command=self.view_history)
            elif button == 'Themes':
                btn.config(command=self.change_theme)
            elif button == 'Equation':
                btn.config(command=self.equation_solver)
            elif button == 'Unit Converter':
                btn.config(command=self.unit_converter)
            elif button == 'Font Selection':
                btn.config(command=self.font_selection)
            elif button in {'sqrt', 'pow', 'log', 'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan'}:
                btn.config(command=lambda b=button: self.append_function(b))
            else:
                btn.config(command=lambda b=button: self.append_value(b))

            col += 1
            if col > 5:
                col = 0
                row += 1

        for i in range(6):
            self.button_frame.grid_columnconfigure(i, weight=1)
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)

    def on_hover(self, event):
        event.widget.config(bg='lightblue')

    def on_leave(self, event):
        self.apply_theme()

    def clear_buttons(self):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def apply_theme(self):
        themes = {
            'light': {'bg': 'white', 'fg': 'black', 'btn_bg': '#f0f0f0', 'btn_fg': 'black'},
            'dark': {'bg': '#333333', 'fg': 'white', 'btn_bg': '#555555', 'btn_fg': 'white'},
            'blue': {'bg': '#d0e0f0', 'fg': 'black', 'btn_bg': '#b0c0f0', 'btn_fg': 'black'},
            'green': {'bg': '#d0f0d0', 'fg': 'black', 'btn_bg': '#b0f0b0', 'btn_fg': 'black'},
            'minty': {'bg': '#e0f2f1', 'fg': 'black', 'btn_bg': '#b9fbc0', 'btn_fg': 'black'},
            'solar': {'bg': '#fff9c4', 'fg': 'black', 'btn_bg': '#ffcc80', 'btn_fg': 'black'},
            'retro': {'bg': '#ffab91', 'fg': 'black', 'btn_bg': '#ff8a80', 'btn_fg': 'black'},
            'ocean': {'bg': '#e0f7fa', 'fg': 'black', 'btn_bg': '#80deea', 'btn_fg': 'black'}
        }
        current_theme = themes[self.theme]
        
        self.root.config(bg=current_theme['bg'])
        self.display.config(bg=current_theme['bg'], fg=current_theme['fg'])
        self.button_frame.config(bg=current_theme['bg'])

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=current_theme['btn_bg'], fg=current_theme['btn_fg'])

        for widget in self.button_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.config(bg=current_theme['btn_bg'], fg=current_theme['btn_fg'])

    def append_value(self, value):
        self.display.insert(tk.END, value)

    def append_function(self, func):
        text = self.display.get()
        if func == 'sqrt':
            text += 'math.sqrt('
        elif func == 'pow':
            text += '**'
        elif func == 'log':
            text += 'math.log('
        elif func == 'exp':
            text += 'math.exp('
        elif func in {'sin', 'cos', 'tan', 'asin', 'acos', 'atan'}:
            text += f'math.{func}('
        elif func == '!':
            text += 'math.factorial('
        elif func == 'nCr':
            text += 'math.comb('
        elif func == 'nPr':
            text += 'math.perm('
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, text)

    def evaluate(self):
        try:
            text = self.display.get()
            result = eval(text, {'__builtins__': None}, {'math': math})
            self.display.delete(0, tk.END)
            self.display.insert(tk.END, str(result))
            self.history.append(text + ' = ' + str(result))
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Input: {str(e)}")

    def clear(self):
        self.display.delete(0, tk.END)

    def view_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("History")
        history_window.geometry("500x600")

        history_frame = tk.Frame(history_window)
        history_frame.pack(expand=True, fill='both', padx=10, pady=10)

        scrollbar = tk.Scrollbar(history_frame)
        scrollbar.pack(side='right', fill='y')

        history_listbox = tk.Listbox(history_frame, font=('Arial', 14), yscrollcommand=scrollbar.set)
        history_listbox.pack(expand=True, fill='both')

        scrollbar.config(command=history_listbox.yview)

        for entry in self.history:
            history_listbox.insert(tk.END, entry)

        search_frame = tk.Frame(history_window)
        search_frame.pack(fill='x', padx=10, pady=5)

        tk.Label(search_frame, text="Search:").pack(side='left')
        search_entry = tk.Entry(search_frame)
        search_entry.pack(side='left', expand=True, fill='x', padx=5)
        tk.Button(search_frame, text="Find", command=lambda: self.search_history(search_entry.get(), history_listbox)).pack(side='left')

        tk.Button(history_window, text='Export', command=self.export_history).pack(side='bottom', fill='x', padx=10, pady=10)

    def search_history(self, query, listbox):
        listbox.delete(0, tk.END)
        for entry in self.history:
            if query.lower() in entry.lower():
                listbox.insert(tk.END, entry)

    def export_history(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                for entry in self.history:
                    file.write(entry + '\n')

    def show_help(self):
        help_window = tk.Toplevel(self.root)
        help_window.title("Interactive Help")
        help_window.geometry("600x400")

        help_text = tk.Text(help_window, wrap=tk.WORD, font=('Arial', 12))
        help_text.pack(expand=True, fill='both', padx=10, pady=10)

        help_content = """
        Welcome to the Advanced Calculator!

        1. Basic Operations:
           Use the number buttons and operators (+, -, *, /) for basic calculations.

        2. Scientific Functions:
           - sqrt: Square root
           - pow: Power (use ** for exponentiation)
           - log: Natural logarithm
           - exp: Exponential function
           - sin, cos, tan: Trigonometric functions
           - asin, acos, atan: Inverse trigonometric functions

        3. Advanced Features:
           - Equation: Solve simple equations
           - Unit Converter: Convert between different units
           - Themes: Change the calculator's appearance
           - Font Selection: Customize the display font

        4. History:
           - View History: See past calculations
           - Search: Find specific calculations in history
           - Export: Save your calculation history

        5. Modes:
           Switch between Scientific and Advanced modes for different features.

        Enjoy using the calculator!
        """

        help_text.insert(tk.END, help_content)
        help_text.config(state='disabled')

    def equation_solver(self):
        equation = simpledialog.askstring("Input", "Enter the equation to solve (e.g., x**2 - 5*x + 6 = 0):")
        if equation:
            try:
                # This is a very basic equation solver for quadratic equations
                # You might want to implement a more robust solver for various types of equations
                a, b, c = map(float, equation.replace("x**2", "").replace("x", "").replace("=0", "").split())
                discriminant = b**2 - 4*a*c
                if discriminant > 0:
                    x1 = (-b + math.sqrt(discriminant)) / (2*a)
                    x2 = (-b - math.sqrt(discriminant)) / (2*a)
                    messagebox.showinfo("Solution", f"x1 = {x1:.2f}, x2 = {x2:.2f}")
                elif discriminant == 0:
                    x = -b / (2*a)
                    messagebox.showinfo("Solution", f"x = {x:.2f}")
                else:
                    messagebox.showinfo("Solution", "No real solutions")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid equation: {str(e)}")

    def unit_converter(self):
        converter_window = tk.Toplevel(self.root)
        converter_window.title("Unit Converter")
        converter_window.geometry("400x300")

        tk.Label(converter_window, text="Select Conversion Type:").pack(pady=10)
        conversion_types = ['Length', 'Weight', 'Temperature']
        conversion_var = tk.StringVar(value=conversion_types[0])
        tk.OptionMenu(converter_window, conversion_var, *conversion_types).pack(pady=5)

        tk.Label(converter_window, text="Enter Value:").pack(pady=5)
        value_entry = tk.Entry(converter_window)
        value_entry.pack(pady=5)

        tk.Label(converter_window, text="From Unit:").pack(pady=5)
        from_unit = tk.Entry(converter_window)
        from_unit.pack(pady=5)

        tk.Label(converter_window, text="To Unit:").pack(pady=5)
        to_unit = tk.Entry(converter_window)
        to_unit.pack(pady=5)

        result_var = tk.StringVar()
        tk.Label(converter_window, textvariable=result_var).pack(pady=10)

        def convert():
            try:
                value = float(value_entry.get())
                conv_type = conversion_var.get().lower()
                from_u = from_unit.get().lower()
                to_u = to_unit.get().lower()

                # Simplified conversion logic (replace with more comprehensive conversions)
                conversions = {
                    'length': {'m': 1, 'cm': 0.01, 'km': 1000, 'in': 0.0254, 'ft': 0.3048},
                    'weight': {'kg': 1, 'g': 0.001, 'lb': 0.453592},
                    'temperature': {'c': lambda x: x, 'f': lambda x: (x - 32) * 5/9, 'k': lambda x: x - 273.15}
                }

                if conv_type in conversions and from_u in conversions[conv_type] and to_u in conversions[conv_type]:
                    if conv_type == 'temperature':
                        # Convert to Celsius first
                        celsius = conversions[conv_type][from_u](value)
                        # Then convert from Celsius to target unit
                        result = {
                            'c': lambda x: x,
                            'f': lambda x: x * 9/5 + 32,
                            'k': lambda x: x + 273.15
                        }[to_u](celsius)
                    else:
                        result = value * conversions[conv_type][from_u] / conversions[conv_type][to_u]
                    result_var.set(f"{value} {from_u} = {result:.4f} {to_u}")
                else:
                    result_var.set("Invalid conversion units")
            except ValueError:
                result_var.set("Invalid input")

        tk.Button(converter_window, text="Convert", command=convert).pack(pady=10)

    def font_selection(self):
        font_window = tk.Toplevel(self.root)
        font_window.title("Font Selection")
        font_window.geometry("300x200")

        tk.Label(font_window, text="Select Font:").pack(pady=10)
        fonts = ['Arial', 'Helvetica', 'Times', 'Courier', 'Verdana']
        font_var = tk.StringVar(value=fonts[0])
        tk.OptionMenu(font_window, font_var, *fonts).pack(pady=5)

        tk.Label(font_window, text="Font Size:").pack(pady=5)
        size_var = tk.IntVar(value=24)
        tk.Spinbox(font_window, from_=8, to=72, textvariable=size_var).pack(pady=5)

        def apply_font():
            selected_font = font_var.get()
            selected_size = size_var.get()
            self.display.config(font=(selected_font, selected_size))
            font_window.destroy()

        tk.Button(font_window, text="Apply", command=apply_font).pack(pady=10)

    def change_theme(self):
        theme_window = tk.Toplevel(self.root)
        theme_window.title("Theme Selection")
        theme_window.geometry("300x300")

        tk.Label(theme_window, text="Select Theme:").pack(pady=10)
        themes = ['Light', 'Dark', 'Blue', 'Green', 'Minty', 'Solar', 'Retro', 'Ocean']
        theme_var = tk.StringVar(value=self.theme.capitalize())
        
        for theme in themes:
            tk.Radiobutton(theme_window, text=theme, variable=theme_var, value=theme.lower()).pack(anchor='w', padx=20, pady=5)

        def apply_theme():
            self.theme = theme_var.get().lower()
            self.apply_theme()
            theme_window.destroy()

        tk.Button(theme_window, text="Apply", command=apply_theme).pack(pady=10)

    def switch_mode(self):
        if self.mode == 'scientific':
            self.mode = 'advanced'
            self.switch_button.config(text='Switch to Scientific')
            # Add more advanced buttons or functionality here
        else:
            self.mode = 'scientific'
            self.switch_button.config(text='Switch to Advanced')
        self.create_buttons()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the main window initially
    app = CalculatorApp(root)
    root.mainloop()