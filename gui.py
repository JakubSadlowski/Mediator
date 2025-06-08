import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from broker_problem import (
    compute_profit_matrix,
    balance_problem,
    max_profit_method_with_iterations,
    compute_summary
)
from file_operations import save_to_csv, load_from_csv

class BrokerProblemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Problem Pośrednika - Broker Problem Solver")
        self.setup_ui()
        
    def setup_ui(self):
        # Variables
        self.num_suppliers = tk.IntVar(value=2)
        self.num_customers = tk.IntVar(value=3)
        self.supply_entries = []
        self.purchase_cost_entries = []
        self.demand_entries = []
        self.selling_price_entries = []
        self.transport_cost_entries = []
        
        # Main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create UI sections
        self.create_config_section()
        self.create_data_input_section()
        self.create_results_section()
        self.create_buttons()
        
        # Initialize with default values
        self.update_data_inputs()
    
    def create_config_section(self):
        config_frame = ttk.LabelFrame(self.main_frame, text="Konfiguracja", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        ttk.Label(config_frame, text="Liczba dostawców:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_suppliers, 
                   command=self.update_data_inputs).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(config_frame, text="Liczba odbiorców:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_customers, 
                   command=self.update_data_inputs).grid(row=1, column=1, padx=5, pady=5)
    
    def create_data_input_section(self):
        self.data_frame = ttk.LabelFrame(self.main_frame, text="Dane wejściowe", padding="10")
        self.data_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        self.update_data_inputs()
    
    def update_data_inputs(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()
            
        # Supply section
        ttk.Label(self.data_frame, text="Podaż:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.supply_entries = []
        for i in range(self.num_suppliers.get()):
            entry = ttk.Entry(self.data_frame, width=8)
            entry.grid(row=0, column=i+1, padx=5, pady=5)
            self.supply_entries.append(entry)
            ttk.Label(self.data_frame, text=f"D{i+1}").grid(row=1, column=i+1)
        
        # Purchase costs
        ttk.Label(self.data_frame, text="Koszt zakupu:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.purchase_cost_entries = []
        for i in range(self.num_suppliers.get()):
            entry = ttk.Entry(self.data_frame, width=8)
            entry.grid(row=2, column=i+1, padx=5, pady=5)
            self.purchase_cost_entries.append(entry)
        
        # Demand section
        ttk.Label(self.data_frame, text="Popyt:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.demand_entries = []
        for j in range(self.num_customers.get()):
            entry = ttk.Entry(self.data_frame, width=8)
            entry.grid(row=3, column=j+1, padx=5, pady=5)
            self.demand_entries.append(entry)
            ttk.Label(self.data_frame, text=f"O{j+1}").grid(row=4, column=j+1)
        
        # Selling prices
        ttk.Label(self.data_frame, text="Cena sprzedaży:").grid(row=5, column=0, padx=5, pady=5, sticky=tk.W)
        self.selling_price_entries = []
        for j in range(self.num_customers.get()):
            entry = ttk.Entry(self.data_frame, width=8)
            entry.grid(row=5, column=j+1, padx=5, pady=5)
            self.selling_price_entries.append(entry)
        
        # Transport costs
        ttk.Label(self.data_frame, text="Koszty transportu:").grid(row=6, column=0, padx=5, pady=5, sticky=tk.W)
        self.transport_cost_entries = []
        for i in range(self.num_suppliers.get()):
            row_entries = []
            for j in range(self.num_customers.get()):
                entry = ttk.Entry(self.data_frame, width=8)
                entry.grid(row=7+i, column=j+1, padx=5, pady=5)
                row_entries.append(entry)
            self.transport_cost_entries.append(row_entries)
            ttk.Label(self.data_frame, text=f"D{i+1}").grid(row=7+i, column=0, padx=5, pady=5)
    
    def create_results_section(self):
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Wyniki", padding="10")
        self.results_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky=(tk.W, tk.E))
        
        self.allocation_text = tk.Text(self.results_frame, height=10, width=60, state=tk.DISABLED)
        self.allocation_text.grid(row=0, column=0, padx=5, pady=5, columnspan=2)
        
        # Add iterations label
        ttk.Label(self.results_frame, text="Liczba iteracji:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.iterations_var = tk.StringVar()
        ttk.Label(self.results_frame, textvariable=self.iterations_var).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        results_labels = ["Koszt zakupu:", "Koszt transportu:", "Przychód:", "Zysk:"]
        self.results_vars = []
        
        for i, label in enumerate(results_labels):
            ttk.Label(self.results_frame, text=label).grid(row=i+2, column=0, sticky=tk.W, padx=5, pady=2)
            var = tk.StringVar()
            ttk.Label(self.results_frame, textvariable=var).grid(row=i+2, column=1, sticky=tk.W, padx=5, pady=2)
            self.results_vars.append(var)
    
    def create_buttons(self):
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        
        ttk.Button(self.button_frame, text="Oblicz", command=self.solve_problem).grid(row=0, column=0, padx=5)
        ttk.Button(self.button_frame, text="Wczytaj z pliku", command=self.load_from_file).grid(row=0, column=1, padx=5)
        ttk.Button(self.button_frame, text="Zapisz do pliku", command=self.save_to_file).grid(row=0, column=2, padx=5)
        ttk.Button(self.button_frame, text="Wyczyść", command=self.clear_all).grid(row=0, column=3, padx=5)
    
    def solve_problem(self):
        try:
            supply = [int(entry.get()) for entry in self.supply_entries]
            purchase_costs = [int(entry.get()) for entry in self.purchase_cost_entries]
            demand = [int(entry.get()) for entry in self.demand_entries]
            selling_prices = [int(entry.get()) for entry in self.selling_price_entries]
            transport_costs = [
                [int(entry.get()) for entry in row] 
                for row in self.transport_cost_entries
            ]
            
            # Compute using broker_problem module
            profit_matrix = compute_profit_matrix(purchase_costs, selling_prices, transport_costs)
            balanced_supply, balanced_demand, balanced_profit_matrix, _ = balance_problem(
                supply, demand, profit_matrix, transport_costs)
            allocation, iterations = max_profit_method_with_iterations(
                balanced_supply, balanced_demand, balanced_profit_matrix)
            total_purchase, total_transport, total_revenue, total_profit = compute_summary(
                allocation, supply, demand, purchase_costs, selling_prices, transport_costs)
            
            self.display_results(allocation, total_purchase, total_transport, total_revenue, total_profit, iterations)
            
        except ValueError as e:
            messagebox.showerror("Błąd danych", "Wprowadź poprawne wartości liczbowe we wszystkich polach.")
        except Exception as e:
            messagebox.showerror("Błąd obliczeń", str(e))
    
    def display_results(self, allocation, total_purchase, total_transport, total_revenue, total_profit, iterations):
        self.allocation_text.config(state=tk.NORMAL)
        self.allocation_text.delete(1.0, tk.END)
        
        # Display allocation matrix
        self.allocation_text.insert(tk.END, "Macierz alokacji:\n")
        for i in range(len(self.supply_entries)):
            row_str = f"D{i+1}:\t"
            for j in range(len(self.demand_entries)):
                row_str += f"{allocation[i][j]}\t"
            self.allocation_text.insert(tk.END, row_str + "\n")
        
        self.allocation_text.config(state=tk.DISABLED)
        self.iterations_var.set(str(iterations))
        self.results_vars[0].set(f"{total_purchase}")
        self.results_vars[1].set(f"{total_transport}")
        self.results_vars[2].set(f"{total_revenue}")
        self.results_vars[3].set(f"{total_profit}")
    
    def load_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
            
        try:
            data = load_from_csv(file_path)
            self.num_suppliers.set(len(data['supply']))
            self.num_customers.set(len(data['demand']))
            self.update_data_inputs()
            
            for i, value in enumerate(data['supply']):
                self.supply_entries[i].delete(0, tk.END)
                self.supply_entries[i].insert(0, value)
            
            for i, value in enumerate(data['purchase_costs']):
                self.purchase_cost_entries[i].delete(0, tk.END)
                self.purchase_cost_entries[i].insert(0, value)
            
            for j, value in enumerate(data['demand']):
                self.demand_entries[j].delete(0, tk.END)
                self.demand_entries[j].insert(0, value)
            
            for j, value in enumerate(data['selling_prices']):
                self.selling_price_entries[j].delete(0, tk.END)
                self.selling_price_entries[j].insert(0, value)
            
            for i, row in enumerate(data['transport_costs']):
                for j, value in enumerate(row):
                    self.transport_cost_entries[i][j].delete(0, tk.END)
                    self.transport_cost_entries[i][j].insert(0, value)
            
            messagebox.showinfo("Sukces", "Dane wczytane pomyślnie!")
            
        except Exception as e:
            messagebox.showerror("Błąd wczytywania", f"Nie udało się wczytać danych: {str(e)}")
    
    def save_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
            
        try:
            data = {
                'supply': [int(entry.get()) for entry in self.supply_entries],
                'purchase_costs': [int(entry.get()) for entry in self.purchase_cost_entries],
                'demand': [int(entry.get()) for entry in self.demand_entries],
                'selling_prices': [int(entry.get()) for entry in self.selling_price_entries],
                'transport_costs': [
                    [int(entry.get()) for entry in row] 
                    for row in self.transport_cost_entries
                ]
            }
            save_to_csv(file_path, data)
            messagebox.showinfo("Sukces", "Dane zapisane pomyślnie!")
            
        except Exception as e:
            messagebox.showerror("Błąd zapisywania", f"Nie udało się zapisać danych: {str(e)}")
    
    def clear_all(self):
        for entry in self.supply_entries:
            entry.delete(0, tk.END)
        for entry in self.purchase_cost_entries:
            entry.delete(0, tk.END)
        for entry in self.demand_entries:
            entry.delete(0, tk.END)
        for entry in self.selling_price_entries:
            entry.delete(0, tk.END)
        for row in self.transport_cost_entries:
            for entry in row:
                entry.delete(0, tk.END)
        
        self.allocation_text.config(state=tk.NORMAL)
        self.allocation_text.delete(1.0, tk.END)
        self.allocation_text.config(state=tk.DISABLED)
        
        self.iterations_var.set("")
        for var in self.results_vars:
            var.set("")