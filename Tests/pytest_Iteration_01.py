import pytest
import pandas as pd
import os
from travel_func import load_travel_data, save, add_trip, remove_trip

TEST_CSV_FILE = "test_travel_data.csv"

SAMPLE_DATA = pd.DataFrame([
    {"Trip ID": 1, "Destination": "Paris", "Start date": "2025-06-01", "End date": "2025-06-10", "Duration (days)": 10,
     "Traveler name": "Alice", "Traveler age": 30, "Traveler gender": "Female", "Traveler nationality": "French",
     "Accommodation type": "Hotel", "Accommodation cost": 500, "Transportation type": "Flight", "Transportation cost": 300},
    {"Trip ID": 2, "Destination": "New York", "Start date": "2025-07-15", "End date": "2025-07-20", "Duration (days)": 5,
     "Traveler name": "Bob", "Traveler age": 25, "Traveler gender": "Male", "Traveler nationality": "American",
     "Accommodation type": "Hostel", "Accommodation cost": 200, "Transportation type": "Train", "Transportation cost": 100}
])

@pytest.fixture
def setup_test_file():
    SAMPLE_DATA.to_csv(TEST_CSV_FILE, index=False)
    yield TEST_CSV_FILE
    os.remove(TEST_CSV_FILE)

def test_load_travel_data(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    data = load_travel_data(TEST_CSV_FILE)
    
    assert not data.empty
    assert len(data) == 2
    assert data.iloc[0]['Destination'] == "Paris"

def test_add_trip(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(TEST_CSV_FILE, index=False))

    add_trip("London", "2025-09-05", "2025-09-12", 7, "David", 35, "Male", "British", "Airbnb", 300, "Bus", 50)
    data = pd.read_csv(TEST_CSV_FILE)

    assert len(data) == 3
    assert data.iloc[-1]['Destination'] == "London"

def test_remove_trip(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(TEST_CSV_FILE, index=False))

    remove_trip(1)
    data = pd.read_csv(TEST_CSV_FILE)

    assert len(data) == 1
    assert 1 not in data['Trip ID'].values

def test_trip_id_is_number(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    
    data = load_travel_data(TEST_CSV_FILE)
    assert pd.api.types.is_integer_dtype(data['Trip ID'].astype("Int64"))

def test_dates_are_valid(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    
    data = load_travel_data(TEST_CSV_FILE)

    try:
        pd.to_datetime(data['Start date'], format="%Y-%m-%d")
        pd.to_datetime(data['End date'], format="%Y-%m-%d")
    except ValueError:
        pytest.fail("Start date or End date is not in the correct date format (YYYY-MM-DD)")

def test_costs_are_numeric(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda filename=TEST_CSV_FILE: pd.read_csv(TEST_CSV_FILE))
    
    data = load_travel_data(TEST_CSV_FILE)
    
    assert pd.api.types.is_numeric_dtype(data['Accommodation cost'])
    assert pd.api.types.is_numeric_dtype(data['Transportation cost'])

def test_invalid_date_format(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(setup_test_file))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(setup_test_file, index=False))

    invalid_dates = ["10-06-2025", "2025/06/10", "June 10, 2025", "invalid_date"]

    for date in invalid_dates:
        with pytest.raises(ValueError):
            add_trip("Paris", date, "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
                     "Hotel", 500, "Flight", 800)

def test_invalid_trip_id_format(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(setup_test_file))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(setup_test_file, index=False))

    add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
             "Hotel", 500, "Flight", 800)
    
    data = load_travel_data(setup_test_file)
    data.at[0, "Trip ID"] = "NotANumber"
    save(data)

    with pytest.raises(ValueError):
        remove_trip("NotANumber")

def test_invalid_cost_format(setup_test_file, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(setup_test_file))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(setup_test_file, index=False))

    invalid_costs = ["Free", None, "One Hundred", "100$"]

    for cost in invalid_costs:
        with pytest.raises(ValueError):
            add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
                     "Hotel", cost, "Flight", 800)
