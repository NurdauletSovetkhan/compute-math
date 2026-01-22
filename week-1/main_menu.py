import tkinter as tk
from tkinter import messagebox
import subprocess
import os

ASSIGNMENTS = {
    'Assignment 1 (Nonlinear Equations)': r'week-1/assignment-1/main.py',
    'Assignment 2 (Linear Systems)': r'week-1/assignment-2/main.py',
    'Assignment 3 (Approximation)': r'week-1/assignment-3/main.py',
    'Assignment 4.1 (Finite Differences)': r'week-1/assignment-4/part-1/main.py',
}


def run_assignment(path):
    abs_path = os.path.abspath(path)
    if not os.path.exists(abs_path):
        messagebox.showerror('Error', f'File not found: {abs_path}')
        return
    try:
        subprocess.Popen(['python', abs_path], creationflags=subprocess.CREATE_NEW_CONSOLE)
    except Exception as e:
        messagebox.showerror('Error', str(e))


def main():
    root = tk.Tk()
    root.title('Compute Math App')
    root.geometry('400x350')

    tk.Label(root, text='Choose an assignment:', font=('Book Antiqua', 14)).pack(pady=20)

    for name, path in ASSIGNMENTS.items():
        btn = tk.Button(root, text=name, font=('Book Antiqua', 12), width=35,
                        command=lambda p=path: run_assignment(p))
        btn.pack(pady=5)

    tk.Button(root, text='Exit', font=('Book Antiqua', 12), width=35, command=root.quit).pack(pady=20)

    root.mainloop()


if __name__ == '__main__':
    main()
