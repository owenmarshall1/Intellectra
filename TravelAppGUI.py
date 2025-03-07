
import tkinter as tk
from tkinter import ttk, messagebox
import travel_func #Importing travel functions
class TravelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Agent App - Demo")
        self.root.geometry("800x600")

        try:
            self.travel_data = travel_func.load_travel_data().to_dict("records")
        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
            root.destroy()
            return

        self.create_widgets()

    def create_widgets(self):
        self.travel_frame = ttk.Frame(self.root)
        self.travel_frame.pack(fill=tk.BOTH, expand=True)

        self.display_travel_options(self.travel_data)

    def display_travel_options(self, data):
        for widget in self.travel_frame.winfo_children():
            widget.destroy()

        for idx, item in enumerate(data):
            self.display_travel_option(idx, item)

    def display_travel_option(self, idx, item):
        option_frame = ttk.Frame(self.travel_frame)
        option_frame.pack(fill=tk.X, padx=10, pady=5)

        total_cost = float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0))

        details_frame = ttk.Frame(option_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(details_frame, text=f"Destination: {item['Destination']}", font=("Arial", 12)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Duration: {item['Duration (days)']} days", font=("Arial", 10)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Total Cost: ${total_cost}", font=("Arial", 10)).pack(anchor=tk.W)

        ttk.Button(option_frame, text="View Details", command=lambda i=idx: self.view_details(i)).pack(side=tk.RIGHT, padx=10)

    def view_details(self, idx):
        item = self.travel_data[idx]
        total_cost = float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0))

        details = (
            f"Destination: {item['Destination']}\n"
            f"Start Date: {item['Start date']}\n"
            f"End Date: {item['End date']}\n"
            f"Duration: {item['Duration (days)']} days\n"
            f"Accommodation Type: {item['Accommodation type']}\n"
            f"Accommodation Cost: ${item['Accommodation cost']}\n"
            f"Transportation Type: {item['Transportation type']}\n"
            f"Transportation Cost: ${item['Transportation cost']}\n"
            f"Total Cost: ${total_cost}"
        )

        messagebox.showinfo("Travel Details", details)

if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()