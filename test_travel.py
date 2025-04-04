import pytest
import pandas as pd
from TravelDataManager import TravelDataManager  
@pytest.fixture
def temp_manager(tmp_path):
    csv_path = tmp_path / "travel_data.csv"
    pd.DataFrame(columns=[
        "Trip ID", "City", "Country", "Start date", "End date",
        "Duration (days)", "Accommodation type", "Accommodation cost",
        "Transportation type", "Transportation cost", "Favorite"
    ]).to_csv(csv_path, index=False)
    return TravelDataManager(filename=str(csv_path))

def test_add_valid_trip(temp_manager):
    temp_manager.add_trip(
        city="Paris", country="France",
        start_date="2025-05-01", end_date="2025-05-10", duration="9",
        accommodation_type="Hotel", accommodation_cost="500",
        transportation_type="Flight", transportation_cost="300"
    )
    data = temp_manager.load_travel_data()
    assert len(data) == 1
    assert data.iloc[0]["City"] == "Paris"
    assert data.iloc[0]["Duration (days)"] == 9

def test_add_invalid_duration(temp_manager):
    with pytest.raises(ValueError, match="Duration must be an integer"):
        temp_manager.add_trip(
            city="Rome", country="Italy",
            start_date="2025-07-01", end_date="2025-07-05", duration="five",
            accommodation_type="Hostel", accommodation_cost="200",
            transportation_type="Bus", transportation_cost="150"
        )

def test_invalid_date_format(temp_manager):
    with pytest.raises(ValueError, match="Dates must be in YYYY-MM-DD format"):
        temp_manager.add_trip(
            city="Berlin", country="Germany",
            start_date="2025/06/01", end_date="2025-06-10", duration="9",
            accommodation_type="Hotel", accommodation_cost="400",
            transportation_type="Flight", transportation_cost="250"
        )

def test_invalid_cost_format(temp_manager):
    with pytest.raises(ValueError, match="Accommodation cost must be a number"):
        temp_manager.add_trip(
            city="Athens", country="Greece",
            start_date="2025-08-01", end_date="2025-08-10", duration="9",
            accommodation_type="Hotel", accommodation_cost="five hundred",
            transportation_type="Boat", transportation_cost="300"
        )

def test_remove_trip(temp_manager):
    temp_manager.add_trip(
        city="Tokyo", country="Japan",
        start_date="2025-09-01", end_date="2025-09-10", duration="9",
        accommodation_type="Capsule", accommodation_cost="300",
        transportation_type="Train", transportation_cost="200"
    )
    data = temp_manager.load_travel_data()
    trip_id = int(data.iloc[0]["Trip ID"])
    temp_manager.remove_trip(trip_id)
    data = temp_manager.load_travel_data()
    assert data.empty

def test_remove_nonexistent_trip(temp_manager):
    with pytest.raises(ValueError, match="Trip ID 999 not found"):
        temp_manager.remove_trip(999)
