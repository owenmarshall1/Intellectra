import csv 

def add_item(id, name, description, csv_filename):
    with open(csv_filename, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(id, name, description)

def edit_item(id, new_name=None, new_description=None, csv_filename='data.csv'):

    updated_rows = []

    with open(csv_filename, mode='r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if int(row[0]) == id:
                if new_name:
                    row[1] = new_name
                if new_description:
                    row[2] = new_description
            updated_rows.append(row)

    with open(csv_filename, mode='w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(updated_rows)


# Menu option

def main():
    while True:
        print("\nCatalog Management System")
        print("1. View Catalog")
        print("2. Add a new item")
        print("3. Edit item description/name")
        print("4. Delete item")
        print("5. Exit program")
        choice = input("Enter a choice: ")

        if choice == "1":
            view_catalog()
        elif choice == "2":
            add_item()
        elif choice == "3":
            edit_item()
        # elif choice == "4":
        #     delete_item()
        elif choice == "5":
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")


# View catalog option - Display from array 
def view_catalog():
    with open('data.csv', mode ='r') as file:    
        csvFile = csv.DictReader(file)
        for lines in csvFile:
            print(lines)
    

# Read CSV file            



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

if __name__ == "__main__":
    main()