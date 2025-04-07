import pytest
import pandas as pd
import os
from travel_func import load_travel_data, save, add_trip, remove_trip

@pytest.fixture
def sample_csv(tmp_path):
    file_path = tmp_path / "test_travel_data.csv"
    df = pd.DataFrame(columns=[
        "Trip ID", "Destination", "Start date", "End date", "Duration (days)",
        "Traveler name", "Traveler age", "Traveler gender", "Traveler nationality",
        "Accommodation type", "Accommodation cost", "Transportation type", "Transportation cost"
    ])
    df.to_csv(file_path, index=False)
    return file_path

def test_load_travel_data_empty(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    data = load_travel_data()
    assert data.empty, "Expected empty DataFrame but got data"

def test_add_trip(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    pd.DataFrame(columns=[
        "Trip ID", "Destination", "Start date", "End date", "Duration (days)",
        "Traveler name", "Traveler age", "Traveler gender", "Traveler nationality",
        "Accommodation type", "Accommodation cost", "Transportation type", "Transportation cost"
    ]).to_csv(sample_csv, index=False)  

    add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
             "Hotel", 500, "Flight", 800)

    data = load_travel_data()
    assert len(data) == 1, f"Expected 1 trip, but found {len(data)}"
    assert data.iloc[0]["Destination"] == "Paris"

def test_remove_trip(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
             "Hotel", 500, "Flight", 800)
    data = load_travel_data()
    trip_id = int(data.iloc[0]["Trip ID"])

    remove_trip(trip_id)
    data = load_travel_data()
    assert data.empty, "Trip should have been removed"

def test_add_trip_with_missing_data(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    with pytest.raises(ValueError):
        add_trip(None, None, None, None, None, None, None, None, None, None, None, None)

    data = load_travel_data()
    assert data.empty, "Trip with missing data should not have been added"

def test_add_trip_with_invalid_trip_id(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
             "Hotel", 500, "Flight", 800)
    
    data = load_travel_data()
    data.at[0, "Trip ID"] = "InvalidID"
    save(data)

    data = load_travel_data()
    assert isinstance(data.iloc[0]["Trip ID"], (int, float)), "Trip ID should be a number"

def test_invalid_date_format(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    invalid_dates = ["10-06-2025", "2025/06/10", "June 10, 2025", "invalid_date"]

    for date in invalid_dates:
        with pytest.raises(ValueError):
            add_trip("Paris", date, "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
                     "Hotel", 500, "Flight", 800)

def test_invalid_trip_id_format(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
             "Hotel", 500, "Flight", 800)
    
    data = load_travel_data()
    data.at[0, "Trip ID"] = "NotANumber"
    save(data)

    with pytest.raises(ValueError):
        remove_trip("NotANumber")

def test_invalid_cost_format(sample_csv, monkeypatch):
    monkeypatch.setattr("travel_func.load_travel_data", lambda: pd.read_csv(sample_csv))
    monkeypatch.setattr("travel_func.save", lambda data: data.to_csv(sample_csv, index=False))

    invalid_costs = ["Free", None, "One Hundred", "100$"]

    for cost in invalid_costs:
        with pytest.raises(ValueError):
            add_trip("Paris", "2025-06-10", "2025-06-20", 10, "John Doe", 30, "Male", "Canadian",
                     "Hotel", cost, "Flight", 800)
