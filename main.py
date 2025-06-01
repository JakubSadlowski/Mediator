from file_operations import parse_csv
from broker_problem import (
    compute_profit_matrix,
    balance_problem,
    max_profit_method,
    compute_summary
)

def main():
    try:
        file_path = 'data.csv'
        print("Wczytywanie danych...")
        supply, purchase_costs, demand, selling_prices, transport_costs = parse_csv(file_path)
        
        print("\nObliczanie macierzy zysków...")
        profit_matrix = compute_profit_matrix(purchase_costs, selling_prices, transport_costs)
        
        print("\nBilansowanie problemu...")
        balanced_supply, balanced_demand, balanced_profit_matrix, balanced_transport_costs = balance_problem(
            supply, demand, profit_matrix, transport_costs)
        
        print("\nOptymalizacja alokacji...")
        allocation = max_profit_method(
            balanced_supply, 
            balanced_demand, 
            balanced_profit_matrix,
            balanced_transport_costs
        )
        
        print("\nObliczanie wyników...")
        total_purchase, total_transport, total_revenue, total_profit = compute_summary(
            allocation, supply, demand, purchase_costs, selling_prices, transport_costs)
        
        print("\nWyniki końcowe:")
        print("Macierz alokacji:")
        for i in range(len(supply)):
            print(f"Dostawca {i+1}:", "\t".join(map(str, allocation[i][:len(demand)])))
        
        print(f"\nKoszt zakupu: {total_purchase}")
        print(f"Koszt transportu: {total_transport}")
        print(f"Przychód: {total_revenue}")
        print(f"Zysk: {total_profit}")
    
    except Exception as e:
        print(f"\nKrytyczny błąd: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()