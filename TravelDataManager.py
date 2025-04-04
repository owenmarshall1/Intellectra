import pandas as pd
from datetime import datetime

class TravelDataManager:
    def __init__(self, filename="travel_data.csv"):
        self.filename = filename

    def load_travel_data(self):
        #returning empty if file doesnt exist 
        try:
            return pd.read_csv(self.filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=[
                "Trip ID", "City", "Country", "Start date", "End date",
                "Duration (days)", "Accommodation type", "Accommodation cost",
                "Transportation type", "Transportation cost", "Favorite"
            ])

    def save(self, data):
        data.to_csv(self.filename, index=False)

    def add_trip(self, city, country, start_date, end_date, duration,
                 accommodation_type, accommodation_cost,
                 transportation_type, transportation_cost, favorite=0):
        
        # Validate duration
        try:
            duration = int(duration)
        except ValueError:
            raise ValueError("Duration must be an integer.")

        # Validate costs
        try:
            accommodation_cost = float(accommodation_cost)
        except ValueError:
            raise ValueError("Accommodation cost must be a number.")

        try:
            transportation_cost = float(transportation_cost)
        except ValueError:
            raise ValueError("Transportation cost must be a number.")

        # Validate favorite
        try:
            favorite = int(favorite)
            if favorite not in (0, 1):
                raise ValueError
        except ValueError:
            raise ValueError("Favorite must be 0 or 1.")

        # Validate date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format.")

        # Load and add trip
        data = self.load_travel_data()
        next_trip_id = data['Trip ID'].max() + 1 if not data.empty else 1
        new_trip = pd.DataFrame([{
            "Trip ID": next_trip_id,
            "City": city,
            "Country": country,
            "Start date": start_date,
            "End date": end_date,
            "Duration (days)": duration,
            "Accommodation type": accommodation_type,
            "Accommodation cost": accommodation_cost,
            "Transportation type": transportation_type,
            "Transportation cost": transportation_cost,
            "Favorite": favorite
        }])
        data = pd.concat([data, new_trip], ignore_index=True)
        self.save(data)

    def remove_trip(self, trip_id):
        data = self.load_travel_data()
        if trip_id not in data['Trip ID'].values:
            raise ValueError(f"Trip ID {trip_id} not found.")
        data = data[data['Trip ID'] != trip_id]
        self.save(data)

    def edit_trip(self, trip_id, city, country, start_date, end_date, duration,
                  accommodation_type, accommodation_cost,
                  transportation_type, transportation_cost):
        
        data = self.load_travel_data()
        index = data[data['Trip ID'] == trip_id].index
        #Validate id 
        if len(index) == 0:
            raise ValueError(f"Trip ID {trip_id} not found.")
        #reuse validations 
        ##TODO Make it a function 
        # Validate duration
        try:
            duration = int(duration)
        except ValueError:
            raise ValueError("Duration must be an integer.")

        # Validate costs
        try:
            accommodation_cost = float(accommodation_cost)
        except ValueError:
            raise ValueError("Accommodation cost must be a number.")

        try:
            transportation_cost = float(transportation_cost)
        except ValueError:
            raise ValueError("Transportation cost must be a number.")

        # Validate favorite
        try:
            favorite = int(favorite)
            if favorite not in (0, 1):
                raise ValueError
        except ValueError:
            raise ValueError("Favorite must be 0 or 1.")

        # Validate date format
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Dates must be in YYYY-MM-DD format.")

        data.loc[index, 'City'] = city
        data.loc[index, 'Country'] = country
        data.loc[index, 'Start date'] = start_date
        data.loc[index, 'End date'] = end_date
        data.loc[index, 'Duration (days)'] = duration
        data.loc[index, 'Accommodation type'] = accommodation_type
        data.loc[index, 'Accommodation cost'] = accommodation_cost
        data.loc[index, 'Transportation type'] = transportation_type
        data.loc[index, 'Transportation cost'] = transportation_cost
        self.save(data)

    def toggle_favorite(self, trip_id, new_status):
        data = self.load_travel_data()
        index = data[data['Trip ID'] == trip_id].index
        if len(index) == 0:
            raise ValueError(f"Trip ID {trip_id} not found.")

        if new_status not in (0, 1):
            raise ValueError("Favorite status must be 0 or 1.")

        data.loc[index, "Favorite"] = new_status
        self.save(data)
