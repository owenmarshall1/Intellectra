import pandas as pd

class TravelDataManager:
    def __init__(self, filename="travel_data_demo.csv"):
        self.filename = filename

    def load_travel_data(self):
        return pd.read_csv(self.filename)

    def save(self, data):
        data.to_csv(self.filename, index=False)

    def add_trip(self, city, country, start_date, end_date, duration, accommodation_type, accommodation_cost, transportation_type, transportation_cost):
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
            "Transportation cost": transportation_cost
        }])
        data = pd.concat([data, new_trip], ignore_index=True)
        self.save(data)

    def remove_trip(self, trip_id):
        data = self.load_travel_data()
        data = data[data['Trip ID'] != trip_id]
        self.save(data)

    def edit_trip(self, trip_id, city, country, start_date, end_date, duration, accommodation_type, accommodation_cost, transportation_type, transportation_cost):
        data = self.load_travel_data()
        index = data[data['Trip ID'] == trip_id].index
        if len(index) == 0:
            return False
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
        return True