import tkinter as tk
from tkinter import ttk

class ExampleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Example GUI Program")

        # Text Label
        self.label = ttk.Label(root, text="This is a basic example of a GUI using tkinter")
        self.label.pack(pady=10)

        # Drawing a line (canvas widget)
        self.canvas = tk.Canvas(root, width=300, height=50)
        self.canvas.pack()
        self.canvas.create_line(10, 25, 290, 25, fill="blue", width=2)

        # Check box
        self.check_var = tk.IntVar()
        self.checkbox = ttk.Checkbutton(root, text="Check me", variable=self.check_var)
        self.checkbox.pack(pady=10)

        # Radio buttons
        self.radio_var = tk.StringVar(value="Option1")

        self.radio1 = ttk.Radiobutton(root, text="Option 1", variable=self.radio_var, value="Option1")
        self.radio1.pack(pady=5)

        self.radio2 = ttk.Radiobutton(root, text="Option 2", variable=self.radio_var, value="Option2")
        self.radio2.pack(pady=5)

        # Button to print the current status
        self.button = ttk.Button(root, text="Show Status", command=self.show_status)
        self.button.pack(pady=10)

    def show_status(self):
        print(f"Checkbox is {'checked' if self.check_var.get() == 1 else 'unchecked'}")
        print(f"Selected Radio Button: {self.radio_var.get()}")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ExampleGUI(root)
    root.mainloop()
