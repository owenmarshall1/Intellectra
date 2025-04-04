import csv
import tkinter as tk
from tkinter import ttk, messagebox
from TravelDataManager import TravelDataManager #Importing travel functions
from AdminAuth import AdminAuth #Importing admin functions

class TravelApp:
    def __init__(self, root):
        self.auth = AdminAuth() #admin handler
        self.root = root
        self.root.title("🌍 Travel Agent Portal")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.data_manager = TravelDataManager() #data manager
        self.style = ttk.Style()
        self.setup_styles()
        try:
            #try loading data from csv file
            self.travel_data = self.data_manager.load_travel_data().to_dict("records")
        except FileNotFoundError as e:
            messagebox.showerror("File Error", str(e))
            root.destroy()
            return

        self.filtered_data = self.travel_data #filtered data
        self.search_debounce_id = None #debounce to reduce lag when searching

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

        #sort dropdown options
        self.sort_options = [
            "ID", "Price: Low to High", "Price: High to Low",
            "Country", "City", "Duration: Short to Long", "Duration: Long to Short", "Favorites"
        ]
        self.sort_var = tk.StringVar()
        self.sort_dropdown = ttk.Combobox(
            search_frame, textvariable=self.sort_var, values=self.sort_options, state="readonly", width=20)
        self.sort_dropdown.pack(side=tk.LEFT, padx=5)
        self.sort_dropdown.set("Sort by...")
        self.sort_dropdown.bind("<<ComboboxSelected>>", self.sort_data)

        #login button
        self.login_btn = ttk.Button(search_frame, text="Login", style="Login.TButton", command=self.show_login_popup)
        self.login_btn.pack(side=tk.RIGHT, padx=10)

        #scrollable canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        #bottom button frame
        button_frame = ttk.Frame(self.root)
        button_frame.pack(side="bottom", pady=8)

        self.add_trip_button = ttk.Button(button_frame, text="➕ Add New Trip", style="Accent.TButton", command=self.open_add_trip_window)
        self.add_trip_button.pack(side="right", padx=12)
        if not self.auth.get_login_status():
            self.add_trip_button.pack_forget()

        self.display_travel_options(self.filtered_data)

    def show_login_popup(self):
        #show login popup or log out if already logged in
        if self.auth.get_login_status():
            self.auth.logout()
            self.update_ui_for_admin_status()
            messagebox.showinfo("Logged Out!", "Admin mode has been deactivated")
            return

        #create the pop up        
        self.login_popup = tk.Toplevel(self.root)
        self.login_popup.title("Admin Login")
        self.login_popup.geometry("300x200")
        self.login_popup.resizable(False, False)

        #center the pop up
        window_width = 300 
        window_height = 200 
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.login_popup.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        #password label and entry
        ttk.Label(self.login_popup, text="Enter Admin Password:").pack(pady=(10, 0))
        
        self.password_frame = ttk.Frame(self.login_popup)
        self.password_frame.pack(pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.password_frame, show="*", textvariable=self.password_var, width=20) # Hidden password with *
        self.password_entry.pack(side=tk.LEFT)
        
        self.show_pass_btn = ttk.Button(self.password_frame, text="🔓", width=3,command=self.toggle_password_visibility) # Show password button
        self.show_pass_btn.pack(side=tk.LEFT, padx=5)
        login_btn = ttk.Button(self.login_popup, text="Login", command=self.attempt_login) # Login button
        login_btn.pack(pady=10)
        
        self.login_popup.bind('<Return>', lambda e: self.attempt_login())
        self.password_entry.focus() # Focus on password entry

    
    def toggle_password_visibility(self): # Show/Hide password
        if self.password_entry['show'] == "":
            self.password_entry.config(show="*")
            self.show_pass_btn.config(text="🔓")
        else:
            self.password_entry.config(show="")
            self.show_pass_btn.config(text="🔒")

    def attempt_login(self):
        password = self.password_var.get()
        if self.auth.login(password):
            self.login_popup.destroy()
            self.update_ui_for_admin_status()
            messagebox.showinfo("Success!", "Admin mode logged in!")
        else:
            messagebox.showerror("Error!", "Password is incorrect!")
            self.password_var.set("")
            self.password_entry.focus()

    def update_ui_for_admin_status(self):
        is_admin = self.auth.get_login_status()

        self.login_btn.config(text="Logout" if is_admin else "Login")
        
        # Show/hide "Add New Trip" button (might remove this in the future)
        if hasattr(self, 'add_trip_button'):
            if is_admin:
               self.add_trip_button.pack(side="right", padx=12)
            else:
               self.add_trip_button.pack_forget()

        self.display_travel_options(self.filtered_data)

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
        #clear exisiting widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        #create a card for each trip in data
        for idx, item in enumerate(data):
            self.display_travel_option(idx, item)

    def display_travel_option(self, idx, item):
        #outer frame
        outer = tk.Frame(self.scrollable_frame, bg="white")
        outer.pack(fill=tk.X, padx=8, pady=6)

        #card frame
        card = tk.Frame(outer, bg="white", bd=1, relief="solid")
        card.pack(fill=tk.X, ipadx=6, ipady=6)

        #left side of card
        left = ttk.Frame(card)
        left.pack(side="left", padx=10)

        #format trip details
        details = f"{item['City']}, {item['Country']}\n"
        details += f"Duration: {item['Duration (days)']} days\n"
        total_cost = float(item['Accommodation cost']) + float(item['Transportation cost'])
        details += f"Total Cost: ${total_cost:.2f}"

        ttk.Label(left, text=f"#{item['Trip ID']}", font=("Segoe UI", 9, "bold"), foreground="#0078D4").pack(anchor="w")
        ttk.Label(left, text=details, justify="left").pack(anchor="w")

        right = ttk.Frame(card, style="TFrame")
        right.pack(side="right", padx=6)

        # Favorite button (always visible)
        fav_btn = tk.Button(right, text="★" if item['Favorite'] == 1 else "☆",
                            fg="gold" if item['Favorite'] == 1 else "gray",
                            font=("Segoe UI", 11), bd=0, bg="white", activebackground="white",
                            command=lambda tid=item['Trip ID'], b=right: self.toggle_favorite(tid, b))
        fav_btn.pack(side="left", padx=3)

        # View button (always visible)
        ttk.Button(right, text="🔍 View", command=lambda tid=item['Trip ID']: self.view_details(tid)).pack(side="left", padx=2)

        # Admin-only buttons (visible when logged in)
        if self.auth.get_login_status():
            ttk.Button(right, text="✏️ Edit", command=lambda tid=item['Trip ID']: self.open_edit_trip_window(tid)).pack(side="left", padx=2)
            ttk.Button(right, text="❌", style="Delete.TButton", width=3, command=lambda tid=item['Trip ID']: self.confirm_delete_trip(tid)).pack(side="left", padx=2)

    def confirm_delete_trip(self, trip_id):

        if not self.auth.get_login_status():
            messagebox.showerror("Access Denied", "Not admin user!")
            return
        
        confirm = messagebox.askyesno("Delete Trip", f"Are you sure you want to delete this trip? (ID: {trip_id})")
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
        
        #calculate total cost of trip
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

    def open_add_trip_window(self): # Opens a new window to add a trip
        if not self.auth.get_login_status():
            messagebox.showerror("Access Denied", "Not admin user!")
            return
        self.add_trip_window = tk.Toplevel(self.root)
        self.add_trip_window.title("Add New Trip")
        self.add_trip_window.geometry("320x320")

        #creates fields for add new trip form
        fields = [
            ("City:", 1), ("Country:", 2), ("Start Date (YYYY-MM-DD):", 3),
            ("End Date (YYYY-MM-DD):", 4), ("Duration (days):", 5),
            ("Accommodation Type:", 6), ("Accommodation Cost:", 7),
            ("Transportation Type:", 8), ("Transportation Cost:", 9)
        ]

        self.entries = {}
        for label_text, row in fields:
            ttk.Label(self.add_trip_window, text=label_text).grid(row=row, column=0, padx=10, pady=5)
            entry = ttk.Entry(self.add_trip_window)
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[label_text] = entry

        #submit button
        submit_button = ttk.Button(self.add_trip_window, text="Submit", command=self.submit_new_trip)
        submit_button.grid(row=10, column=0, columnspan=2, pady=10)

    def open_edit_trip_window(self, trip_id):
        if not self.auth.get_login_status():
            messagebox.showerror("Access Denied", "Not admin user!")
            return
        
        # Find the trip to edit
        item = next((trip for trip in self.travel_data if trip['Trip ID'] == trip_id), None)
        if item is None:
            messagebox.showerror("Error", "Trip not found!")
            return

        self.edit_trip_window = tk.Toplevel(self.root)
        self.edit_trip_window.title(f"Edit Trip {trip_id}")
        self.edit_trip_window.geometry("320x320")

        # Create form fields with current values
        fields = [
            ("City:", 1, item['City']), ("Country:", 2, item['Country']),
            ("Start Date (YYYY-MM-DD):", 3, item['Start date']),
            ("End Date (YYYY-MM-DD):", 4, item['End date']),
            ("Duration (days):", 5, item['Duration (days)']),
            ("Accommodation Type:", 6, item['Accommodation type']),
            ("Accommodation Cost:", 7, item['Accommodation cost']),
            ("Transportation Type:", 8, item['Transportation type']),
            ("Transportation Cost:", 9, item['Transportation cost'])
        ]

        self.entries = {}
        for label_text, row, value in fields:
            ttk.Label(self.edit_trip_window, text=label_text).grid(row=row, column=0, padx=10, pady=5)
            entry = ttk.Entry(self.edit_trip_window)
            entry.grid(row=row, column=1, padx=10, pady=5)
            entry.insert(0, value)
            self.entries[label_text] = entry

        # Submit button
        submit_button = ttk.Button(self.edit_trip_window, text="Submit",
                                 command=lambda: self.submit_edited_trip(trip_id))
        submit_button.grid(row=13, column=0, columnspan=2, pady=10)

    def submit_edited_trip(self, trip_id):
        #get all field values na
        city = self.entries["City:"].get()
        country = self.entries["Country:"].get()
        start_date = self.entries["Start Date (YYYY-MM-DD):"].get()
        end_date = self.entries["End Date (YYYY-MM-DD):"].get()
        duration = self.entries["Duration (days):"].get()
        accommodation_type = self.entries["Accommodation Type:"].get()
        accommodation_cost = self.entries["Accommodation Cost:"].get()
        transportation_type = self.entries["Transportation Type:"].get()
        transportation_cost = self.entries["Transportation Cost:"].get()

        #check all fields are filled out
        if not all([city, country, start_date, end_date, duration,
                    accommodation_type, accommodation_cost, transportation_type, transportation_cost]):
            messagebox.showerror("Error", "All fields are required!")
            return

        #save changes
        try:  
            self.data_manager.edit_trip(
                trip_id=trip_id,
                city=city,
                country=country,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                accommodation_type=accommodation_type,
                accommodation_cost=accommodation_cost,
                transportation_type=transportation_type,
                transportation_cost=transportation_cost
            )
            messagebox.showinfo("Success", "Trip edited successfully!")
            # close window and refresh data
            self.edit_trip_window.destroy()

            self.travel_data = self.data_manager.load_travel_data().to_dict("records")
            self.filtered_data = self.travel_data

            self.display_travel_options(self.filtered_data)
        #handling errors 
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
             messagebox.showerror("Error", f"Something went wrong:\n{e}")

    def submit_new_trip(self):
        #get all field values
        city = self.entries["City:"].get()
        country = self.entries["Country:"].get()
        start_date = self.entries["Start Date (YYYY-MM-DD):"].get()
        end_date = self.entries["End Date (YYYY-MM-DD):"].get()
        duration = self.entries["Duration (days):"].get()
        accommodation_type = self.entries["Accommodation Type:"].get()
        accommodation_cost = self.entries["Accommodation Cost:"].get()
        transportation_type = self.entries["Transportation Type:"].get()
        transportation_cost = self.entries["Transportation Cost:"].get()

        #make sure all fields are filled out
        if not all([city, country, start_date, end_date, duration,
                    accommodation_type, accommodation_cost, transportation_type, transportation_cost]):
            messagebox.showerror("Error", "All fields are required!")
            return
        
        #add new trip
    
    
        try:
            self.data_manager.add_trip(
                city=city,
                country=country,
                start_date=start_date,
                end_date=end_date,
                duration=duration,
                accommodation_type=accommodation_type,
                accommodation_cost=accommodation_cost,
                transportation_type=transportation_type,
                transportation_cost=transportation_cost
            )
            messagebox.showinfo("Success", "Trip added successfully!")
            self.add_trip_window.destroy()

            self.travel_data = self.data_manager.load_travel_data().to_dict("records")
            self.filtered_data = self.travel_data
            self.display_travel_options(self.filtered_data)
        
        #handle error messages
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong:\n{e}")
        
        

    def sort_data(self):
        # Sort the data based on the total cost (Accommodation + Transportation)
        self.travel_data.sort(key=lambda item: float(item.get("Accommodation cost", 0)) + float(item.get("Transportation cost", 0)))
        # Update the display with sorted data
        self.display_travel_options(self.travel_data)

    def sort_data(self, event=None):

        selected_option = self.sort_var.get()
        #if favorites not selected dont show favorites
        if selected_option != "Favorites":
            self.filtered_data = self.travel_data.copy()

        #apply sorting based on selected option
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

    def toggle_favorite(self, trip_id, container):
        current_btn = container.winfo_children()[0]
        is_fav = current_btn.cget("text") == "★"
        new_status = not is_fav

        #update favorite status in data manager
        if self.data_manager.toggle_favorite(trip_id, new_status):
            current_btn.config(text="★" if new_status else "☆", fg="gold" if new_status else "gray")

        #update local data
        for trip in self.travel_data:
            if trip['Trip ID'] == trip_id:
                trip['Favorite'] = 1 if new_status else 0
        for trip in self.filtered_data:
            if trip['Trip ID'] == trip_id:
                trip['Favorite'] = 1 if new_status else 0
        


if __name__ == "__main__":
    root = tk.Tk()
    app = TravelApp(root)
    root.mainloop()
