Compute-math — Week-1 Unified GUI

Run the tkinter GUI to access methods across assignments.

Requirements:
- Python 3.8+
- numpy

From the repository root (where `.venv` may be located), run:

```powershell
# if using the project's venv on Windows
.\.venv\Scripts\Activate.ps1
python week-1\gui_app.py
```

What it provides:
- Assignment 1 tab: Newton-Raphson (enter f(x) and f'(x), initial guess)
- Assignment 2 tab: Inverse matrix (paste rows)
- Assignment 4 tab: Forward/Backward differences (enter x and y lists)

Notes:
- The GUI loads specific functions from the assignment files without modifying them.
- If you want more methods added to the GUI, tell me which ones and I'll add tabs/wrappers.