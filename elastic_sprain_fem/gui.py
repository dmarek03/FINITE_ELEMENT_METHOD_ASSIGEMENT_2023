import tkinter as tk
import re
from tkinter import messagebox
from fem_solver import FemSolver
from plot import show


class Application:
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title('Elastic sprain fem solver')
        self.window.minsize(width=600, height=600)

        self.label = tk.Label(master=self.window, text='Elastic sprain solver', font=('Cambria Math', 20))
        self.label.pack(padx=10, pady=10)

        self.label = tk.Label(master=self.window, text='Enter number of elements', font=('Cambria Math', 12))
        self.label.pack(side='top')

        self.entry = tk.Entry(
            self.window,
            justify='center',
            validate='focusin',
        )
        self.entry.pack(side='top')

        self.button = tk.Button(self.window, justify='center', text="confirm", height=1, width=8, command=self.solve)
        self.button.pack(padx=10, pady=47)

        self.window.mainloop()

    @staticmethod
    def validate_input(value: str) -> int | ValueError:

        if not re.match(r'^\d+$', value):
            raise ValueError('Number of elements must be integer')

        if int(value) <= 2:
            raise ValueError('Number of elements must be greater than 2')

        if re.match(r'^\d+$', value) and int(value) > 2:
            return int(value)

    def solve(self) -> None:
        try:
            n = self.entry.get()
            validated_n = self.validate_input(n)
            fem_solver = FemSolver(validated_n)
            x, y, y2 = fem_solver.solve()
            show(x, y, validated_n)
            show(x, y2, validated_n)

        except ValueError as e:
            messagebox.showwarning(title="Error", message=str(e))
