import csv

def parse_csv(file_path):
    with open(file_path, newline='') as csvfile:
        data = [row for row in csv.reader(csvfile) if row]
    
    if len(data) < 6:
        raise ValueError("Niekompletne dane wejściowe")
    
    num_suppliers = len(data[0]) - 1
    num_customers = len(data[2]) - 1
    
    supply = list(map(int, data[0][1:1+num_suppliers]))
    purchase_costs = list(map(int, data[1][1:1+num_suppliers]))
    demand = list(map(int, data[2][1:1+num_customers]))
    selling_prices = list(map(int, data[3][1:1+num_customers]))
    
    transport_costs = []
    for i in range(num_suppliers):
        if 5 + i >= len(data):
            raise ValueError(f"Brak wiersza z kosztami transportu dla dostawcy {i+1}")
        row = data[5 + i]
        transport_costs.append(list(map(int, row[1:1+num_customers])))
    
    return supply, purchase_costs, demand, selling_prices, transport_costs