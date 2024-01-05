import csv

def add_column_to_csv(csv_file, new_column_data, new_column_header):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = [row for row in reader]

    if rows:
        rows[0].append(new_column_header)

    for i, data in enumerate(new_column_data, start=1):
        if i < len(rows):
            rows[i].append(data)

    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)