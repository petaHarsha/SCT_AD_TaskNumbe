import tkinter as tk
from tkinter import messagebox

def calculate():
    try:
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        operation = operation_var.get()

        if operation == "+":
            result = num1 + num2
        elif operation == "-":
            result = num1 - num2
        elif operation == "*":
            result = num1 * num2
        elif operation == "/":
            if num2 == 0:
                result = "Cannot divide by zero"
            else:
                result = num1 / num2
        else:
            result = "Invalid operation"

        result_label.config(text=f"Result: {result}")
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers.")

# Create main window
root = tk.Tk()
root.title("Desktop Calculator")
root.geometry("400x350")
root.configure(bg="#2d2d2d")

# Styles
entry_style = {"font": ("Arial", 16), "width": 20}
label_style = {"bg": "#2d2d2d", "fg": "white", "font": ("Arial", 14)}

# First number
tk.Label(root, text="First Number:", **label_style).pack(pady=(20, 0))
entry1 = tk.Entry(root, **entry_style)
entry1.pack()

# Operation selector
tk.Label(root, text="Operation:", **label_style).pack(pady=(10, 0))
operation_var = tk.StringVar(value="+")
operation_menu = tk.OptionMenu(root, operation_var, "+", "-", "*", "/")
operation_menu.config(font=("Arial", 14))
operation_menu.pack()

# Second number
tk.Label(root, text="Second Number:", **label_style).pack(pady=(10, 0))
entry2 = tk.Entry(root, **entry_style)
entry2.pack()

# Calculate button
tk.Button(root, text="Calculate", font=("Arial", 14), bg="#4caf50", fg="white", command=calculate).pack(pady=15)

# Result display
result_label = tk.Label(root, text="", **label_style)
result_label.pack()

# Run app
root.mainloop()
