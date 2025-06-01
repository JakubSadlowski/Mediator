import copy

def compute_profit_matrix(purchase_costs, selling_prices, transport_costs):
    return [
        [
            selling_prices[j] - purchase_costs[i] - transport_costs[i][j]
            for j in range(len(selling_prices))
        ]
        for i in range(len(purchase_costs))
    ]

def balance_problem(supply, demand, profit_matrix, transport_costs):
    total_supply = sum(supply)
    total_demand = sum(demand)
    
    balanced_supply = supply.copy()
    balanced_demand = demand.copy()
    balanced_profit_matrix = copy.deepcopy(profit_matrix)
    balanced_transport_costs = copy.deepcopy(transport_costs)
    
    if total_supply < total_demand:
        balanced_supply.append(total_demand - total_supply)
        balanced_profit_matrix.append([0] * len(balanced_demand))
        balanced_transport_costs.append([0] * len(balanced_demand))
    elif total_supply > total_demand:
        balanced_demand.append(total_supply - total_demand)
        for row in balanced_profit_matrix:
            row.append(0)
        for row in balanced_transport_costs:
            row.append(0)
    
    return balanced_supply, balanced_demand, balanced_profit_matrix, balanced_transport_costs

def max_profit_method(supply, demand, profit_matrix, transport_costs):
    supply = copy.deepcopy(supply)
    demand = copy.deepcopy(demand)
    allocation = [[0] * len(demand) for _ in range(len(supply))]
    
    routes = []
    for i in range(len(supply)):
        for j in range(len(demand)):
            routes.append((
                -profit_matrix[i][j],  # Sortowanie po zysku (malejąco)
                transport_costs[i][j],  # Drugie kryterium (niższe koszty lepsze)
                i, j
            ))
    
    routes.sort()
    
    for _, _, i, j in routes:
        if supply[i] == 0 or demand[j] == 0:
            continue
        quantity = min(supply[i], demand[j])
        allocation[i][j] = quantity
        supply[i] -= quantity
        demand[j] -= quantity
    
    return allocation

def compute_summary(allocation, original_supply, original_demand, purchase_costs, selling_prices, transport_costs):
    total_purchase = 0
    total_transport = 0
    total_revenue = 0
    
    for i in range(len(original_supply)):
        for j in range(len(original_demand)):
            if allocation[i][j] > 0:
                if (i < len(purchase_costs) and 
                    j < len(selling_prices) and 
                    i < len(transport_costs) and 
                    j < len(transport_costs[i])):
                    
                    qty = allocation[i][j]
                    total_purchase += qty * purchase_costs[i]
                    total_transport += qty * transport_costs[i][j]
                    total_revenue += qty * selling_prices[j]
    
    total_profit = total_revenue - total_purchase - total_transport
    return total_purchase, total_transport, total_revenue, total_profit