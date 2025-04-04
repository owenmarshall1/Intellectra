
#  Testing Plan for Travel Agent App

## 🔹 Unit Tests

Unit tests verify the correctness of individual methods or functionalities in isolation.
Every Test should have two checks before it is dismissed

### ✅ Extended List of Unit Tests:
1. `add_trip()` – Adds a new trip and ensures it's saved correctly.✅
2. `remove_trip()` – Removes a trip by ID.✅
3. `edit_trip()` – Edits a trip and verifies updated values.✅
4. `load_travel_data()` – Loads data correctly from CSV.✅
5. `save()` – Saves DataFrame to CSV without altering or losing data.✅
6. `update_search1()` – Filters data based on user input in the search bar.✅
7. `add_trip()` adds trip witch correct id.✅
8. `remove_trip()` handles a wrong id and doesnt change CSV.✅
9. `edit_trip()` only updates matching Trip ID.✅
10. `load_travel_data()` returns an empty DataFrame if CSV is empty.✅
11. `save()` creates the file if it doesn’t exist.✅
12. `update_search1()` handles numeric and text input searches correctly.✅
13. `edit_trip()` handles wrong data forms ✅

---

## 🔹 Integration Tests

Integration tests verify how components work together.

### ✅ List of Planned Integration Tests:
1. Add a trip via GUI and verify it updates the CSV.✅  Syed
2. Remove a trip with GUI ensuring it removes it from CSV and assign correct ids✅    Arshia
3. Delete a trip via GUI and verify that the list updates and the CSV is changed.✅   Syed 
4. Search functionality interacts with backend data correctly.✅    Syed 
5. Displaying filtered data after search correctly reflects matching results in the UI.✅   Arshia 
6. Edit a trip via GUI and ensure data changes. ✅ Chris 

---

## 🔹 System Tests

System tests are end-to-end tests simulating user actions and verifying the full application behavior.

### ✅ List of Planned System Tests:
1. Adding trips via the interface and verifying they are there with interface ✅  Owen
2. Edit a trip via UI and verify updates persist after restarting the app. ✅  Tara
3. Delete a trip and verify it's no longer found by search. ✅   Arshia
4. Simulate user searching with different filters (city, country, etc.).✅   Owen 
5. Simulate invalid data entries (e.g., blank fields or negative cost) and ensure error handling.✅   Owen 

---

## Box Testing Plan

### 🟦 Clear Box Testing (White Box)

Tests based on internal logic and code structure.

#### ✅ Planned Clear Box Test Cases:
1. Test next Trip ID generation in `add_trip()`. ✅Syed
2. Test `edit_trip()` with invalid ID.  Arshia
3. Test `remove_trip()` ensures ID is completely removed from the dataset. ✅ Syed
4. Verify auto increment logic when adding new trips ✅ Syed
5. Veryfing lambda function works correctly for sorting ✅ Arshia


### Errors: 
1. changing the input to int or float before try and except block so it wasnt handled properly 
---

### 🟨 Translucent Box Testing (Gray Box)

Tests combining knowledge of internal logic and external output, often technical.

#### ✅ Planned Translucent Box Test Cases:
1. Check CSV after adding/removing.  ✅ Tara
2. Memory/resource handling on repeated `load_travel_data()` calls. ✅Tara
3. Check file is not corrupted after multiple edits and saves. ✅ Tara
---

### ⬛ Opaque Box Testing (Black Box)

Functional testing based purely on inputs/outputs, from the user’s perspective.

#### ✅ Planned Opaque Box Test Cases:
1. Search by city “Paris” returns correct result. ✅ Owen
2. Search by trip ID returns accurate trip data.✅ Chris
3. Invalid input in search (“asdfgh”) returns zero results. 
4. Invalid edit values ✅ Chris 
5. Verify all buttons, labels, and layouts are consistent Check for visual defects and usability issues ✅ Chris
---
#### Errors: 
1. Sort not working after adding favourites 
2. the date validation wasnt enough as it could bypassed by enter not real dates 

## 👥 Roles for Box Testing

- **Clear Box Testing**: Owen Arshia 
- **Translucent Box Testing**: Tara, Chris  
- **Opaque Box Testing**: Syed 
