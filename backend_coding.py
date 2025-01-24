import csv

# Read CSV file
def readFile():
    with open('data.csv', mode ='r') as file:    
       csvFile = csv.DictReader(file)
       for lines in csvFile:
            print(lines)


def editName(name, id):
    """
    Edit the name field for a specific record based on the given ID.
    :param name: New name to be set
    :param id: The ID of the record to edit
    """
    updated_rows = []
    with open('data.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        fieldnames = csvFile.fieldnames
        for row in csvFile:
            if row['id'] == id:  # Assuming 'id' is a column in the CSV
                row['name'] = name  # Update the name
            updated_rows.append(row)
    
    # Save the updated rows back to the CSV
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

# Edit the description for a specific record
def editDescription(description, id):
    """
    Edit the description field for a specific record based on the given ID.
    :param description: New description to be set
    :param id: The ID of the record to edit
    """
    updated_rows = []
    with open('data.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        fieldnames = csvFile.fieldnames
        for row in csvFile:
            if row['id'] == id:  # Assuming 'id' is a column in the CSV
                row['description'] = description  # Update the description
            updated_rows.append(row)
    
    # Save the updated rows back to the CSV
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

# Validate the data
def validate():
    """
    Validate the data in the CSV file (e.g., check for missing or invalid fields).
    """
    with open('data.csv', mode='r') as file:
        csvFile = csv.DictReader(file)
        for line in csvFile:
            for key, value in line.items():
                if value == "" or value is None:
                    print(f"Missing value in column '{key}' for row with ID: {line['id']}")  # Adjust based on CSV structure

# Save data (can also act as a generic function to save any modifications)
def saveData(updated_rows, fieldnames):
    """
    Save the updated rows to the CSV file.
    :param updated_rows: List of rows to be written back to the CSV
    :param fieldnames: Column headers for the CSV
    """
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)