import csv

def load_from_csv(file_path):
    with open(file_path, newline='') as csvfile:
        data = [row for row in csv.reader(csvfile) if row]
    
    if len(data) < 6:
        raise ValueError("Incomplete input data in file")
    
    num_suppliers = len(data[0]) - 1
    num_customers = len(data[2]) - 1
    
    result = {
        'supply': list(map(int, data[0][1:1+num_suppliers])),
        'purchase_costs': list(map(int, data[1][1:1+num_suppliers])),
        'demand': list(map(int, data[2][1:1+num_customers])),
        'selling_prices': list(map(int, data[3][1:1+num_customers])),
        'transport_costs': []
    }
    
    for i in range(num_suppliers):
        if 5 + i >= len(data):
            raise ValueError(f"No line with transportation costs for the supplier {i+1}")
        row = data[5 + i]
        result['transport_costs'].append(list(map(int, row[1:1+num_customers])))
    
    return result

def save_to_csv(file_path, data):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write supply row
        writer.writerow([''] + [f'D{i+1}' for i in range(len(data['supply']))])
        writer.writerow([''] + data['supply'])
        
        # Write purchase costs
        writer.writerow([''] + data['purchase_costs'])
        
        # Write demand
        writer.writerow([''] + [f'O{j+1}' for j in range(len(data['demand']))])
        writer.writerow([''] + data['demand'])
        
        # Write selling prices
        writer.writerow([''] + data['selling_prices'])
        
        # Write transport costs header
        writer.writerow([''] + [f'O{j+1}' for j in range(len(data['demand']))])
        
        # Write transport costs
        for i in range(len(data['supply'])):
            writer.writerow([f'D{i+1}'] + data['transport_costs'][i])