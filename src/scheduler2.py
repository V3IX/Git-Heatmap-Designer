import tkinter as tk
from tkinter import ttk
from datetime import date, timedelta
import json

def create_year_calendar_grid(master, year, command=None):
    """Creates a year calendar grid (7 columns x 53 weeks) with day labels 1-365/366, starting with Sunday."""
    start_date = date(year, 1, 1)
    end_date = date(year, 12, 31)
    delta = timedelta(days=1)
    
    # Calculate initial padding to align start day with Sunday
    first_weekday = start_date.weekday()
    all_days = [None] * ((first_weekday + 1) % 7)  # Shift to start from Sunday
    
    day_count = 1
    current_date = start_date
    
    while current_date <= end_date:
        all_days.append((current_date.month, current_date.day, day_count))
        current_date += delta
        day_count += 1
    
    # Ensure 7x53 grid (371 cells max)
    while len(all_days) < 371:
        all_days.append(None)
    
    row_frames = [ttk.Frame(master) for _ in range(7)]
    for frame in row_frames:
        frame.pack(fill=tk.X)
    
    buttons = {}
    for row_idx in range(7):
        for col_idx in range(53):
            day_index = row_idx + col_idx * 7
            if day_index >= len(all_days):
                break
            day_data = all_days[day_index]
            
            if day_data is None:
                button = ttk.Button(row_frames[row_idx], text="", state=tk.DISABLED)
            else:
                month, day, day_of_year = day_data
                button = ttk.Button(row_frames[row_idx], text=str(day_of_year), style="Default.TButton")
                if command:
                    button.config(command=lambda m=month, d=day, btn=button: command(year, m, d, btn))
                buttons[(row_idx, col_idx)] = button
            
            button.grid(row=0, column=col_idx, sticky="nsew", padx=1, pady=1)
            row_frames[row_idx].columnconfigure(col_idx, weight=1)
    
    return buttons

def on_day_click(year, month, day, button):
    print(f"Clicked: {year}-{month}-{day}")
    button.config(style="Clicked.TButton" if button.cget("style") == "Default.TButton" else "Default.TButton")

def get_year_input():
    def show_calendar():
        try:
            year = int(year_entry.get())
            if 1900 <= year <= 2100:
                input_window.destroy()
                buttons = create_year_calendar_grid(root, year, command=on_day_click)
                ttk.Button(root, text="Save Dates", command=lambda: save_clicked_dates(year, buttons)).pack(pady=10)
            else:
                error_label.config(text="Enter a year between 1900 and 2100")
        except ValueError:
            error_label.config(text="Invalid year input")
    
    input_window = tk.Tk()
    input_window.title("Enter Year")
    ttk.Label(input_window, text="Enter Year:").pack(pady=5)
    year_entry = ttk.Entry(input_window)
    year_entry.pack(pady=5)
    ttk.Button(input_window, text="Show Calendar", command=show_calendar).pack(pady=10)
    error_label = ttk.Label(input_window, text="", foreground="red")
    error_label.pack()
    input_window.mainloop()

def save_clicked_dates(year, buttons):
    clicked_dates = [
        (date(year, 1, 1) + timedelta(days=int(button.cget("text")) - 1)).strftime("%Y-%m-%d")
        for (row, col), button in buttons.items() if button.cget("style") == "Clicked.TButton"
    ]
    with open("dates.json", "w") as f:
        json.dump(clicked_dates, f)
    print("Clicked dates saved to dates.json")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Year Calendar (7x53)")
    
    style = ttk.Style()
    style.configure("Default.TButton", background="lightgray")
    style.configure("Clicked.TButton", background="green", foreground="white")
    
    get_year_input()
    root.mainloop()
