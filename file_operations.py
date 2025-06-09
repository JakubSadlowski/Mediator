import csv

def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(['supply'] + data['supply'])
        writer.writerow(['purchase_costs'] + data['purchase_costs'])
        writer.writerow(['demand'] + data['demand'])
        writer.writerow(['selling_prices'] + data['selling_prices'])

        for row in data['transport_costs']:
            writer.writerow(['transport_costs'] + row)


def load_from_csv(file_path):
    result = {
        'supply': [],
        'purchase_costs': [],
        'demand': [],
        'selling_prices': [],
        'transport_costs': []
    }

    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row:
                continue

            key = row[0]
            values = row[1:]

            try:
                if key in ['supply', 'purchase_costs', 'demand', 'selling_prices']:
                    result[key] = list(map(int, values))
                elif key == 'transport_costs':
                    result['transport_costs'].append(list(map(int, values)))
            except ValueError:
                raise ValueError(f"Invalid non-numeric data found in row with key '{key}'. Please check the CSV file.")

    # Final validation to ensure all data was loaded
    if not all(result.values()):
        raise ValueError("The CSV file is incomplete or in an incorrect format. Not all required data was found.")

    return result