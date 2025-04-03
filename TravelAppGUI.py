import csv
import tkinter as tk
from tkinter import ttk, messagebox
from TravelDataManager import TravelDataManager #Importing travel functions
from AdminAuth import AdminAuth #Importing admin functions

class TravelApp:
    def __init__(self, root):
        self.auth = AdminAuth()
        self.root = root
        self.root.title("🌍 Travel Agent Portal")
        self.root.geometry("800x600")

        self.data_manager = TravelDataManager()

         ## Custom style for button
        self.style = ttk.Style()
        self.setup_styles()

        try:
            self.travel_data = self.data_manager.load_travel_data().to_dict("records")
        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
            root.destroy()
            return

        self.filtered_data = self.travel_data
        self.search_debounce_id = None

        self.create_widgets()

    def setup_styles(self):
        self.style.theme_use("clam")
        self.style.configure("TFrame", background="white")
        self.style.configure("TopBar.TFrame", background="#0078D4")
        self.style.configure("TLabel", background="white", font=("Segoe UI", 9))
        self.style.configure("TButton", font=("Segoe UI", 9), padding=4)
        self.style.configure("Accent.TButton", foreground="white", background="#0078D4")
        self.style.map("Accent.TButton", background=[("active", "#005A9E")])
        self.style.configure("Delete.TButton", foreground="white", background="#D32F2F", padding=1, width=2)
        self.style.map("Delete.TButton", background=[("active", "#B71C1C")])
        self.style.configure("Login.TButton", foreground="#0078D4", background="white", padding=4, font=("Segoe UI", 9, "bold"))
        self.style.map("Login.TButton", background=[("active", "#f0f0f0")])

    def create_widgets(self):
        # Company name banner
        company_frame = tk.Frame(self.root, bg="white")
        company_frame.pack(fill=tk.X, pady=(8, 0))

        company_label = tk.Label(company_frame, text="Intellectra", font=("Copperplate Gothic Bold", 18), fg="#003366", bg="white")
        company_label.pack(side=tk.LEFT, padx=12, anchor="w")

        # Search bar frame
        search_frame = ttk.Frame(self.root, style="TopBar.TFrame")
        search_frame.pack(fill=tk.X, padx=0, pady=0)

        search_label = tk.Label(search_frame, text="🔍 Search Destinations:", bg="#0078D4", fg="white", font=("Segoe UI", 10))
        search_label.pack(side=tk.LEFT, padx=5, pady=10)

        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.search_entry.bind("<KeyRelease>", self.update_search)

        self.sort_options = [
            "ID", "Price: Low to High", "Price: High to Low",
            "Country", "City", "Duration: Short to Long", "Duration: Long to Short", "Favorites"
        ]
        self.sort_var = tk.StringVar()
        self.sort_dropdown = ttk.Combobox(search_frame, textvariable=self.sort_var, values=self.sort_options, state="readonly")
        self.sort_dropdown.pack(side=tk.RIGHT, padx=5)
        self.sort_dropdown.set("Sort by...")  # Default text
        self.sort_dropdown.bind("<<ComboboxSelected>>", self.sort_data)  # Trigger sorting

        # added scrollbar !!!
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        button_frame = ttk.Frame(self.root)
        button_frame.pack(side="bottom", pady=10)

        #add button
        add_trip_button = ttk.Button(button_frame, text="Add New Trip", command=self.open_add_trip_window)
        add_trip_button.pack(side="left", padx=10)
        #remove button

        self.display_travel_options(self.filtered_data)

    #update search method when key is pressed
    def debounce_search(self, event=None):
        if self.search_debounce_id:
            self.root.after_cancel(self.search_debounce_id)
        self.search_debounce_id = self.root.after(500, self.update_search)

    def update_search(self, event=None):
        search_term = self.search_entry.get().lower()
        self.filtered_data = [item for item in self.travel_data if
            search_term in str(item['Trip ID']).lower() or
            search_term in item['City'].lower() or
            search_term in item['Country'].lower() or
            search_term in item['Accommodation type'].lower() or
            search_term in item['Transportation type'].lower()
        ]
        self.display_travel_options(self.filtered_data)

    def display_travel_options(self, data):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        for idx, item in enumerate(data):
            self.display_travel_option(idx, item)

    def display_travel_option(self, idx, item):
        option_frame = ttk.Frame(self.scrollable_frame)
        option_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(option_frame, text=f"{item['Trip ID']}", font=("Arial", 12), width=3).pack(side=tk.LEFT, padx=10)

        total_cost = float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0))

        details_frame = ttk.Frame(option_frame)
        details_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(details_frame, text=f"{str(item['City']) + ', '+ str(item['Country'])}", font=("Arial", 12)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Duration: {item['Duration (days)']} days", font=("Arial", 10)).pack(anchor=tk.W)
        ttk.Label(details_frame, text=f"Total Cost: ${total_cost}", font=("Arial", 10)).pack(anchor=tk.W)
        delete_button = tk.Button(option_frame, text="❌", fg="white", bg="red", font=("Arial", 12, "bold"), command=lambda tid=item['Trip ID']: self.confirm_delete_trip(tid))
        delete_button.pack(side=tk.RIGHT, padx=15)
        ttk.Button(option_frame, text="View Details", command=lambda tid=item['Trip ID']: self.view_details(tid)).pack(side="right", padx=10)
        ttk.Button(option_frame, text="Edit Trip", command=lambda tid=item['Trip ID']: self.open_edit_trip_window(tid)).pack(side="right", padx=10)

        #determining whether the package is favourited then using the correct button
        is_favorited = str(item["Favorite"]).strip() == "1"
        star_symbol = "★" if is_favorited else "☆"
        star_color = "gold" if is_favorited else "black"
    
        fav_button = tk.Button(option_frame,text=star_symbol,font=("Arial", 14),fg=star_color,command=lambda tid=item['Trip ID']: self.toggle_favorite(tid, fav_button))
        fav_button.pack(side=tk.RIGHT, padx=5)


        # # Deletion Button
        # delete_button = tk.Button(option_frame, text="❌", fg="white", bg="red", font=("Arial", 12, "bold"), command=lambda tid=item['Trip ID']: self.confirm_delete_trip(tid))
        # delete_button.pack(side=tk.RIGHT, padx=10)

    def confirm_delete_trip(self, trip_id):
        confirm = messagebox.askyesno("Delete Trip", "Are you sure you want to delete this trip? (ID: " + str(trip_id) + ")")
        if confirm:
            self.delete_trip(trip_id)

    def delete_trip(self, trip_id):
        self.travel_data = [trip for trip in self.travel_data if trip['Trip ID'] != trip_id]
        self.filtered_data = self.travel_data
        self.display_travel_options(self.filtered_data)
        messagebox.showinfo("Success", "Trip deleted successfully!")

    def view_details(self, trip_id):
        item = next((trip for trip in self.travel_data if trip['Trip ID'] == trip_id), None)
        if item is None:
            messagebox.showerror("Error", "Trip not found!")
            return

        total_cost = float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0))

        details = (
            f"Destination: {item['City']}, {item['Country']}\n"
            f"Start Date: {item['Start date']}\n"
            f"End Date: {item['End date']}\n"
            f"Duration: {item['Duration (days)']} days\n"
            f"Accommodation Type: {item['Accommodation type']}\n"
            f"Accommodation Cost: ${item['Accommodation cost']}\n"
            f"Transportation Type: {item['Transportation type']}\n"
            f"Transportation Cost: ${item['Transportation cost']}\n"
            f"Total Cost: ${total_cost:.2f}"
        )
        messagebox.showinfo("Travel Details", details)
    # opens a new window to add a trip
    def open_add_trip_window(self):
        self.add_trip_window = tk.Toplevel(self.root)
        self.add_trip_window.title("Add New Trip")
        self.add_trip_window.geometry("320x320")

        ttk.Label(self.add_trip_window, text="City:").grid(row=1, column=0, padx=10, pady=5)
        self.city_entry = ttk.Entry(self.add_trip_window)
        self.city_entry.grid(row=1, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Country:").grid(row=2, column=0, padx=10, pady=5)
        self.country_entry = ttk.Entry(self.add_trip_window)
        self.country_entry.grid(row=2, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.start_date_entry = ttk.Entry(self.add_trip_window)
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.end_date_entry = ttk.Entry(self.add_trip_window)
        self.end_date_entry.grid(row=4, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Duration (days):").grid(row=5, column=0, padx=10, pady=5)
        self.duration_entry = ttk.Entry(self.add_trip_window)
        self.duration_entry.grid(row=5, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Accommodation Type:").grid(row=6, column=0, padx=10, pady=5)
        self.accommodation_type_entry = ttk.Entry(self.add_trip_window)
        self.accommodation_type_entry.grid(row=6, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Accommodation Cost:").grid(row=7, column=0, padx=10, pady=5)
        self.accommodation_cost_entry = ttk.Entry(self.add_trip_window)
        self.accommodation_cost_entry.grid(row=7, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Transportation Type:").grid(row=8, column=0, padx=10, pady=5)
        self.transportation_type_entry = ttk.Entry(self.add_trip_window)
        self.transportation_type_entry.grid(row=8, column=1, padx=10, pady=5)

        ttk.Label(self.add_trip_window, text="Transportation Cost:").grid(row=9, column=0, padx=10, pady=5)
        self.transportation_cost_entry = ttk.Entry(self.add_trip_window)
        self.transportation_cost_entry.grid(row=9, column=1, padx=10, pady=5)

        submit_button = ttk.Button(self.add_trip_window, text="Submit", command=self.submit_new_trip)
        submit_button.grid(row=10, column=0, columnspan=2, pady=10)

    def open_edit_trip_window(self, trip_id):
        if not self.auth.get_login_status():
            messagebox.showerror("Access Denied", "Not admin user!")
            return
        
        item = next((trip for trip in self.travel_data if trip['Trip ID'] == trip_id), None)
        if item is None:
            messagebox.showerror("Error", "Trip not found!")
            return

        self.edit_trip_window = tk.Toplevel(self.root)
        self.edit_trip_window.title("Edit Trip " + str(trip_id))
        self.edit_trip_window.geometry("320x320")

        ttk.Label(self.edit_trip_window, text="City:").grid(row=1, column=0, padx=10, pady=5)
        self.city_entry = ttk.Entry(self.edit_trip_window)
        self.city_entry.grid(row=1, column=1, padx=10, pady=5)
        self.city_entry.insert(0, item['City'])

        ttk.Label(self.edit_trip_window, text="Country:").grid(row=2, column=0, padx=10, pady=5)
        self.country_entry = ttk.Entry(self.edit_trip_window)
        self.country_entry.grid(row=2, column=1, padx=10, pady=5)
        self.country_entry.insert(0, item['Country'])

        ttk.Label(self.edit_trip_window, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, padx=10, pady=5)
        self.start_date_entry = ttk.Entry(self.edit_trip_window)
        self.start_date_entry.grid(row=3, column=1, padx=10, pady=5)
        self.start_date_entry.insert(0, item['Start date'])

        ttk.Label(self.edit_trip_window, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, pady=5)
        self.end_date_entry = ttk.Entry(self.edit_trip_window)
        self.end_date_entry.grid(row=4, column=1, padx=10, pady=5)
        self.end_date_entry.insert(0, item['End date'])

        ttk.Label(self.edit_trip_window, text="Duration (days):").grid(row=5, column=0, padx=10, pady=5)
        self.duration_entry = ttk.Entry(self.edit_trip_window)
        self.duration_entry.grid(row=5, column=1, padx=10, pady=5)
        self.duration_entry.insert(0, item['Duration (days)'])

        ttk.Label(self.edit_trip_window, text="Accommodation Type:").grid(row=6, column=0, padx=10, pady=5)
        self.accommodation_type_entry = ttk.Entry(self.edit_trip_window)
        self.accommodation_type_entry.grid(row=6, column=1, padx=10, pady=5)
        self.accommodation_type_entry.insert(0, item['Accommodation type'])

        ttk.Label(self.edit_trip_window, text="Accommodation Cost:").grid(row=7, column=0, padx=10, pady=5)
        self.accommodation_cost_entry = ttk.Entry(self.edit_trip_window)
        self.accommodation_cost_entry.grid(row=7, column=1, padx=10, pady=5)
        self.accommodation_cost_entry.insert(0, item['Accommodation cost'])

        ttk.Label(self.edit_trip_window, text="Transportation Type:").grid(row=8, column=0, padx=10, pady=5)
        self.transportation_type_entry = ttk.Entry(self.edit_trip_window)
        self.transportation_type_entry.grid(row=8, column=1, padx=10, pady=5)
        self.transportation_type_entry.insert(0, item['Transportation type'])

        ttk.Label(self.edit_trip_window, text="Transportation Cost:").grid(row=9, column=0, padx=10, pady=5)
        self.transportation_cost_entry = ttk.Entry(self.edit_trip_window)
        self.transportation_cost_entry.grid(row=9, column=1, padx=10, pady=5)
        self.transportation_cost_entry.insert(0, item['Transportation cost'])

        submit_button = ttk.Button(self.edit_trip_window, text="Submit", command=lambda: self.submit_edited_trip(trip_id))
        submit_button.grid(row=13, column=0, columnspan=2, pady=10)

    def submit_edited_trip(self, trip_id):
        city = self.city_entry.get()
        country = self.country_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        duration = self.duration_entry.get()
        accommodation_type = self.accommodation_type_entry.get()
        accommodation_cost = self.accommodation_cost_entry.get()
        transportation_type = self.transportation_type_entry.get()
        transportation_cost = self.transportation_cost_entry.get()

        if not all([city, country, start_date, end_date, duration,
                    accommodation_type, accommodation_cost, transportation_type, transportation_cost]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.data_manager.edit_trip(
            trip_id=trip_id,
            city=city,
            country=country,
            start_date=start_date,
            end_date=end_date,
            duration=int(duration),
            accommodation_type=accommodation_type,
            accommodation_cost=float(accommodation_cost),
            transportation_type=transportation_type,
            transportation_cost=float(transportation_cost)
        )
        messagebox.showinfo("Success", "Trip edited successfully!")

        self.edit_trip_window.destroy()

        self.travel_data = self.data_manager.load_travel_data().to_dict("records")
        self.filtered_data = self.travel_data

        self.display_travel_options(self.filtered_data)


    def submit_new_trip(self):
        city = self.city_entry.get()
        country = self.country_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        duration = self.duration_entry.get()
        accommodation_type = self.accommodation_type_entry.get()
        accommodation_cost = self.accommodation_cost_entry.get()
        transportation_type = self.transportation_type_entry.get()
        transportation_cost = self.transportation_cost_entry.get()

        if not all([city, country, start_date, end_date, duration,
                    accommodation_type, accommodation_cost, transportation_type, transportation_cost]):
            messagebox.showerror("Error", "All fields are required!")
            return

        self.data_manager.add_trip(
            city=city,
            country=country,
            start_date=start_date,
            end_date=end_date,
            duration=int(duration),
            accommodation_type=accommodation_type,
            accommodation_cost=float(accommodation_cost),
            transportation_type=transportation_type,
            transportation_cost=float(transportation_cost)
        )
        messagebox.showinfo("Success", "Trip added successfully!")

        self.add_trip_window.destroy()

        self.travel_data = self.data_manager.load_travel_data().to_dict("records")
        self.filtered_data = self.travel_data

        self.display_travel_options(self.filtered_data)

    def confirm_remove_trip(self):
        trip_id_to_remove = self.trip_id_to_remove_entry.get()

        if not trip_id_to_remove:
            messagebox.showerror("Error", "Please enter a Trip ID!")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this trip? (ID: " + str(trip_id_to_remove) + ")")
        if confirm: 
            self.data_manager.remove_trip(int(trip_id_to_remove))
            
            messagebox.showinfo("Success", "Trip removed successfully!")
            
            self.remove_trip_window.destroy()

            self.travel_data = self.data_manager.load_travel_data().to_dict("records")
            self.filtered_data = self.travel_data

            self.display_travel_options(self.filtered_data)

    def sort_data(self):
        # Sort the data based on the total cost (Accommodation + Transportation)
        self.travel_data.sort(key=lambda item: float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0)))
        # Update the display with sorted data
        self.display_travel_options(self.travel_data)

    def sort_data(self, event=None):

        selected_option = self.sort_var.get()
        if selected_option == "ID":
            self.filtered_data.sort(key=lambda x: x["Trip ID"])
        elif selected_option == "Price: Low to High":
            self.filtered_data.sort(key=lambda x: float(x["Accommodation cost"]) + float(x["Transportation cost"]))
        elif selected_option == "Price: High to Low":
            self.filtered_data.sort(key=lambda x: float(x["Accommodation cost"]) + float(x["Transportation cost"]), reverse=True)
        elif selected_option == "Country":
            self.filtered_data.sort(key=lambda x: x["Country"])
        elif selected_option == "City":
            self.filtered_data.sort(key=lambda x: x["City"])
        elif selected_option == "Duration: Short to Long":
            self.filtered_data.sort(key=lambda x: x["Duration (days)"])
        elif selected_option == "Duration: Long to Short":
            self.filtered_data.sort(key=lambda x: x["Duration (days)"], reverse=True)
        elif selected_option == "Favorites":
            self.filtered_data = [x for x in self.filtered_data if str(x["Favorite"]) == "1"]
        self.display_travel_options(self.filtered_data)

    def toggle_favorite(self, trip_id, button):
        # Get current favorite status from button appearance
        current_status = button.cget("text") == "★"
    
        # Toggle in data manager (pass the opposite of current status)
        new_status = not current_status
        success = self.data_manager.toggle_favorite(trip_id, new_status)
    
        if success:
            # Update button appearance
            button.config(
                text="★" if new_status else "☆",
                fg="gold" if new_status else "black"
            )
        


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()
