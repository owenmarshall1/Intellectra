
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
        # added scrollbar !!!
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        #add button
        add_trip_button = ttk.Button(button_frame, text="Add New Trip", command=self.open_add_trip_window)
        add_trip_button.pack(side="left", padx=10)
        #remove button
        remove_trip_button = ttk.Button(button_frame, text="Remove Trip", command=self.open_remove_trip_window)
        remove_trip_button.pack(side="left", padx=10)

        self.display_travel_options(self.travel_data)

    def display_travel_options(self, data):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for idx, item in enumerate(data):
            self.display_travel_option(idx, item)

    def display_travel_option(self, idx, item):
        option_frame = ttk.Frame(self.scrollable_frame)
        option_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(option_frame, text=f"{item['Trip ID']}", font=("Arial", 12)).pack(side=tk.LEFT, padx=10)

        total_cost = float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0))

        details_frame = ttk.Frame(option_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(details_frame, text=f"Destination: {item['Destination']}", font=("Arial", 12)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Duration: {item['Duration (days)']} days", font=("Arial", 10)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Total Cost: ${total_cost}", font=("Arial", 10)).pack(anchor=tk.W)

        ttk.Button(option_frame, text="View Details", command=lambda i=idx: self.view_details(i)).pack(side="right", padx=10)

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
    # opens a new window to add a trip
    def open_add_trip_window(self):
        self.add_trip_window = tk.Toplevel(self.root)
        self.add_trip_window.title("Add New Trip")
        self.add_trip_window.geometry("400x600")

        ttk.Label(self.add_trip_window, text="Destination:").grid(row=1, column=0, padx=10, pady=5)
        self.destination_entry = ttk.Entry(self.add_trip_window)
        self.destination_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.start_date_entry = ttk.Entry(self.add_trip_window)
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="End Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.end_date_entry = ttk.Entry(self.add_trip_window)
        self.end_date_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Duration (days):").grid(row=4, column=0, padx=10, pady=5)
        self.duration_entry = ttk.Entry(self.add_trip_window)
        self.duration_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Traveler Name:").grid(row=5, column=0, padx=10, pady=5)
        self.name_entry = ttk.Entry(self.add_trip_window)
        self.name_entry.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Traveler Age:").grid(row=6, column=0, padx=10, pady=5)
        self.age_entry = ttk.Entry(self.add_trip_window)
        self.age_entry.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Traveler Gender:").grid(row=7, column=0, padx=10, pady=5)
        self.gender_entry = ttk.Entry(self.add_trip_window)
        self.gender_entry.grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Traveler Nationality:").grid(row=8, column=0, padx=10, pady=5)
        self.nationality_entry = ttk.Entry(self.add_trip_window)
        self.nationality_entry.grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Accommodation Type:").grid(row=9, column=0, padx=10, pady=5)
        self.accommodation_type_entry = ttk.Entry(self.add_trip_window)
        self.accommodation_type_entry.grid(row=9, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Accommodation Cost:").grid(row=10, column=0, padx=10, pady=5)
        self.accommodation_cost_entry = ttk.Entry(self.add_trip_window)
        self.accommodation_cost_entry.grid(row=10, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Transportation Type:").grid(row=11, column=0, padx=10, pady=5)
        self.transportation_type_entry = ttk.Entry(self.add_trip_window)
        self.transportation_type_entry.grid(row=11, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Transportation Cost:").grid(row=12, column=0, padx=10, pady=5)
        self.transportation_cost_entry = ttk.Entry(self.add_trip_window)
        self.transportation_cost_entry.grid(row=12, column=1, padx=10, pady=5)

        submit_button = ttk.Button(self.add_trip_window, text="Submit", command=self.submit_new_trip)
        submit_button.grid(row=13, column=0, columnspan=2, pady=10)

    def submit_new_trip(self):
        destination = self.destination_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        duration = self.duration_entry.get()
        name = self.name_entry.get()
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        nationality = self.nationality_entry.get()
        accommodation_type = self.accommodation_type_entry.get()
        accommodation_cost = self.accommodation_cost_entry.get()
        transportation_type = self.transportation_type_entry.get()
        transportation_cost = self.transportation_cost_entry.get()

        if not all([destination, start_date, end_date, duration, name, age, gender, nationality,
                    accommodation_type, accommodation_cost, transportation_type, transportation_cost]):
            messagebox.showerror("Error", "All fields are required!")
            return

        travel_func.add_trip(
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            duration=int(duration),
            name=name,
            age=int(age),
            gender=gender,
            nationality=nationality,
            accommodation_type=accommodation_type,
            accommodation_cost=float(accommodation_cost),
            transportation_type=transportation_type,
            transportation_cost=float(transportation_cost)
        )
        messagebox.showinfo("Success", "Trip added successfully!")

        self.add_trip_window.destroy()

        self.travel_data = travel_func.load_travel_data().to_dict("records")
        self.display_travel_options(self.travel_data)

    def open_remove_trip_window(self):
        self.remove_trip_window = tk.Toplevel(self.root)
        self.remove_trip_window.title("Remove Trip")
        self.remove_trip_window.geometry("300x150")

        ttk.Label(self.remove_trip_window, text="Enter Trip ID to Remove:").pack(pady=10)
        self.trip_id_to_remove_entry = ttk.Entry(self.remove_trip_window)
        self.trip_id_to_remove_entry.pack(pady=5)

        confirm_button = ttk.Button(self.remove_trip_window, text="Remove Trip", command=self.confirm_remove_trip)
        confirm_button.pack(pady=10)

    def confirm_remove_trip(self):
        trip_id_to_remove = self.trip_id_to_remove_entry.get()

        if not trip_id_to_remove:
            messagebox.showerror("Error", "Please enter a Trip ID!")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this trip?")
        if confirm: 
            travel_func.remove_trip(int(trip_id_to_remove))
            
            messagebox.showinfo("Success", "Trip removed successfully!")
            
            self.remove_trip_window.destroy()

            self.travel_data = travel_func.load_travel_data().to_dict("records")
            self.display_travel_options(self.travel_data)


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()