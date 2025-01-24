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