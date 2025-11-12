import tkinter as tk
from tkinter import messagebox

def type_check(func):
    def wrapper(a, b):
        if not (isinstance(a, int) and isinstance(b, int)):
            # Show popup instead of raising an error
            root = tk.Tk()
            root.withdraw()  # hide main window
            messagebox.showerror("Type Error", "Both arguments must be integers!")
            root.destroy()
            return  # stop execution of the function
        return func(a, b)
    return wrapper


@type_check
def add(a, b):
    result = a + b
    print(f"The sum is: {result}")
    return result


# ✅ Works fine
add(10, 5)

# ❌ Will show popup
add(10, "5")
