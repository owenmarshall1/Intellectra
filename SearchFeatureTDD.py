import unittest
import tkinter as tk
from TravelAppGUI import TravelApp

class TestTravelSearch(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = TravelApp(self.root)

        test_data = [
            {
                "Trip ID": 101,
                "City": "Paris",
                "Country": "France",
                "Accommodation type": "Hotel",
                "Accommodation cost": 500,
                "Transportation type": "Flight",
                "Transportation cost": 300,
                "Duration (days)": 5,
                "Start date": "2025-05-01",
                "End date": "2025-05-06"
            },
            {
                "Trip ID": 202,
                "City": "Tokyo",
                "Country": "Japan",
                "Accommodation type": "Hostel",
                "Accommodation cost": 300,
                "Transportation type": "Train",
                "Transportation cost": 100,
                "Duration (days)": 7,
                "Start date": "2025-06-01",
                "End date": "2025-06-08"
            }
        ]

        self.app.travel_data = test_data
        self.app.filtered_data = test_data
        self.app.display_travel_options = lambda data: None  # Disable GUI rendering
        self.app.search_entry.unbind("<KeyRelease>")

    def test_search_by_city(self):
        self._run_search_test("paris", expected_city="paris")

    def test_search_by_country(self):
        self._run_search_test("japan", expected_country="japan")

    def test_search_by_trip_id(self):
        self._run_search_test("101", expected_city="paris")

    def test_search_by_accommodation_type(self):
        self._run_search_test("hostel", expected_city="tokyo")

    def test_search_by_transportation_type(self):
        self._run_search_test("flight", expected_city="paris")


    def test_search_no_match(self):
        self.app.search_entry.delete(0, tk.END)
        self.app.search_entry.insert(0, "berlin")
        self.app.update_search1()
        filtered = self.app.filtered_data
        self.assertEqual(len(filtered), 0, "Expected no results when searching for 'berlin'")

    def _run_search_test(self, search_term, expected_city=None, expected_country=None):
        self.app.search_entry.delete(0, tk.END)
        self.app.search_entry.insert(0, search_term)
        self.app.update_search1()
        filtered = self.app.filtered_data
        self.assertGreaterEqual(len(filtered), 1, f"Expected at least one result for '{search_term}'")
        if expected_city:
            self.assertIn(expected_city.lower(), filtered[0]["City"].lower())
        if expected_country:
            self.assertIn(expected_country.lower(), filtered[0]["Country"].lower())

    def tearDown(self):
        self.root.destroy()

if __name__ == "__main__":
    unittest.main()