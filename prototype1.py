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
        elif choice == "4":
            delete_item()
        elif choice == "5":
            print("Exiting program")
            break
        else:
            print("Invalid choice. Please try again.")


# View catalog option - Display from array 
    def view_catalog():
        with open('catalog.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
    
