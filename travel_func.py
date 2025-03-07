import pandas as pd

# Loading the data as and returning pandas datafram 
def load_travel_data(filename="travel_data_demo.csv"):
        return pd.read_csv(filename)
        return pd.DataFrame(columns=columns)


## All are working with data demo for now 
# Saving the data to csv file (make sure index=False to avoid saving row numbers)
def save(data):
    data.to_csv("travel_data_demo.csv", index=False)

# Adding a new trip

##Gets every detail of a trip and makes a new trip in our csv file 
def add_trip(destination, start_date, end_date, duration, name, age, gender, nationality,
             accommodation_type, accommodation_cost, transportation_type, transportation_cost):
    
    data = load_travel_data()

    if not data.empty:
         next_trip_id = data['Trip ID'].max() + 1
    else:
         next_trip_id = 1
    
    new_trip = pd.DataFrame([{
        "Trip ID": next_trip_id,
        "Destination": destination,
        "Start date": start_date,
        "End date": end_date,
        "Duration (days)": duration,
        "Traveler name": name,
        "Traveler age": age,
        "Traveler gender": gender,
        "Traveler nationality": nationality,
        "Accommodation type": accommodation_type,
        "Accommodation cost": accommodation_cost,
        "Transportation type": transportation_type,
        "Transportation cost": transportation_cost
    }])
    data = load_travel_data()
    data = pd.concat([data, new_trip], ignore_index=True)
    save(data)

# Removing a trip by ID

##Gets the id of a trip and removes that trip from our csv file 
def remove_trip(trip_id):
    data = load_travel_data()
    data = data[data['Trip ID'] != trip_id]  
    save(data)
    