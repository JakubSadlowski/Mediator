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
        self.root.title("Broker Problem Solver")
        self._is_loading = False
        self.style_ui()
        self.setup_ui()

    def style_ui(self):
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TLabelframe.Label", font=("Segoe UI", 11, "bold"))

    def setup_ui(self):
        self.num_suppliers = tk.IntVar(value=2)
        self.num_customers = tk.IntVar(value=2)

        self.main_frame = ttk.Frame(self.root, padding=10)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)

        self.create_config_section()
        self.create_data_input_section()
        self.create_buttons()
        self.create_results_section()

        self.update_data_inputs()

    def create_config_section(self):
        config_frame = ttk.LabelFrame(self.main_frame, text="Configuration", padding=10)
        config_frame.grid(row=0, column=0, sticky="ew", pady=5, padx=5)

        ttk.Label(config_frame, text="Number of suppliers:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_suppliers, command=self.update_data_inputs,
                    width=5).grid(row=0, column=1, padx=5)

        ttk.Label(config_frame, text="Number of customers:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Spinbox(config_frame, from_=1, to=10, textvariable=self.num_customers, command=self.update_data_inputs,
                    width=5).grid(row=1, column=1, padx=5)

    def create_data_input_section(self):
        self.data_frame = ttk.LabelFrame(self.main_frame, text="Input Data", padding=10)
        self.data_frame.grid(row=1, column=0, sticky="ew", pady=5, padx=5)

    def update_data_inputs(self, data=None):
        if self._is_loading:
            return

        for widget in self.data_frame.winfo_children():
            widget.destroy()

        num_s = self.num_suppliers.get()
        num_c = self.num_customers.get()

        self.supply_entries = [ttk.Entry(self.data_frame, width=10) for _ in range(num_s)]
        self.purchase_cost_entries = [ttk.Entry(self.data_frame, width=10) for _ in range(num_s)]
        self.demand_entries = [ttk.Entry(self.data_frame, width=10) for _ in range(num_c)]
        self.selling_price_entries = [ttk.Entry(self.data_frame, width=10) for _ in range(num_c)]
        self.transport_cost_entries = [
            [ttk.Entry(self.data_frame, width=10) for _ in range(num_c)]
            for _ in range(num_s)
        ]

        for j in range(num_c):
            ttk.Label(self.data_frame, text=f"Customer {j + 1}", anchor="center").grid(
                row=0, column=2 + j, padx=5, pady=5, sticky="ew")
        ttk.Label(self.data_frame, text="Demand").grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="e")
        for j in range(num_c):
            self.demand_entries[j].grid(row=1, column=2 + j, padx=5, pady=5)
        ttk.Label(self.data_frame, text="Supply").grid(row=2, column=1, padx=5, pady=(15, 0), sticky="s")
        ttk.Label(self.data_frame, text="Purchase cost").grid(row=2, column=2 + num_c, padx=5, pady=(15, 0),
                                                              sticky="s")
        for i in range(num_s):
            row = 3 + i
            ttk.Label(self.data_frame, text=f"Supplier {i + 1}").grid(row=row, column=0, padx=5, pady=5, sticky="e")
            self.supply_entries[i].grid(row=row, column=1, padx=5, pady=5)
            for j in range(num_c):
                self.transport_cost_entries[i][j].grid(row=row, column=2 + j, padx=5, pady=5)
            self.purchase_cost_entries[i].grid(row=row, column=2 + num_c, padx=5, pady=5)
        row = 3 + num_s
        ttk.Label(self.data_frame, text="Selling price").grid(row=row, column=0, columnspan=2, padx=5, pady=(15, 0),
                                                              sticky="e")
        for j in range(num_c):
            self.selling_price_entries[j].grid(row=row, column=2 + j, padx=5, pady=5)

        if data:
            self.populate_fields(data)

        self.clear_results()

    def populate_fields(self, data):
        def insert_value(entry_widget, value):
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, str(value))

        for i in range(len(self.supply_entries)):
            if i < len(data['supply']): insert_value(self.supply_entries[i], data['supply'][i])
            if i < len(data['purchase_costs']): insert_value(self.purchase_cost_entries[i], data['purchase_costs'][i])
            if i < len(data['transport_costs']):
                for j in range(len(self.transport_cost_entries[i])):
                    if j < len(data['transport_costs'][i]): insert_value(self.transport_cost_entries[i][j],
                                                                         data['transport_costs'][i][j])

        for j in range(len(self.demand_entries)):
            if j < len(data['demand']): insert_value(self.demand_entries[j], data['demand'][j])
            if j < len(data['selling_prices']): insert_value(self.selling_price_entries[j], data['selling_prices'][j])

    def create_buttons(self):
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        ttk.Button(button_frame, text="Solve", command=self.solve_problem).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Load CSV", command=self.load_from_file).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Save CSV", command=self.save_to_file).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_all).grid(row=0, column=3, padx=5)

    def create_results_section(self):
        self.results_frame = ttk.LabelFrame(self.main_frame, text="Results", padding=10)
        self.results_frame.grid(row=3, column=0, sticky="nsew", padx=5)
        self.results_frame.columnconfigure(1, weight=1)

        self.allocation_text = tk.Text(self.results_frame, height=8, width=50, state=tk.DISABLED,
                                       font=("Courier New", 10))
        self.allocation_text.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")

        self.profit_matrix_text = tk.Text(self.results_frame, height=8, width=50, state=tk.DISABLED,
                                          font=("Courier New", 10))
        self.profit_matrix_text.grid(row=1, column=0, columnspan=2, pady=5, sticky="ew")

        results_labels = ["Purchase Cost:", "Transport Cost:", "Income:", "Profit:", "Iterations:"]
        self.results_vars = [tk.StringVar() for _ in results_labels]
        for i, label in enumerate(results_labels):
            ttk.Label(self.results_frame, text=label).grid(row=i + 2, column=0, sticky="w", pady=2)
            ttk.Label(self.results_frame, textvariable=self.results_vars[i]).grid(row=i + 2, column=1, sticky="w",
                                                                                  padx=5)

    def solve_problem(self):
        try:
            supply = [int(e.get()) for e in self.supply_entries]
            purchase = [int(e.get()) for e in self.purchase_cost_entries]
            demand = [int(e.get()) for e in self.demand_entries]
            selling = [int(e.get()) for e in self.selling_price_entries]
            transport = [[int(e.get()) for e in row] for row in self.transport_cost_entries]

            profit_matrix = compute_profit_matrix(purchase, selling, transport)

            bs, bd, bpm, _ = balance_problem(supply, demand, profit_matrix, transport)
            allocation, iterations = max_profit_method_with_iterations(bs, bd, bpm)
            total_purchase, total_transport, revenue, profit = compute_summary(allocation, supply, demand, purchase,
                                                                               selling, transport)
            self.display_results(allocation, profit_matrix, total_purchase, total_transport, revenue, profit,
                                 iterations)
        except (ValueError, IndexError):
            messagebox.showerror("Data Error", "Please enter valid data in all fields.")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))

    def display_results(self, allocation, profit_matrix, purchase, transport, revenue, profit, iterations):
        self.allocation_text.config(state=tk.NORMAL)
        self.profit_matrix_text.config(state=tk.NORMAL)
        self.allocation_text.delete(1.0, tk.END)
        self.profit_matrix_text.delete(1.0, tk.END)

        num_original_suppliers = len(self.supply_entries)
        num_original_customers = len(self.demand_entries)

        header = " " * 4 + "".join([f"C{j + 1:<7}" for j in range(num_original_customers)])

        self.allocation_text.insert(tk.END, "Allocation Matrix:\n")
        self.allocation_text.insert(tk.END, header + "\n")
        self.allocation_text.insert(tk.END, "-" * len(header) + "\n")
        for i in range(num_original_suppliers):
            row_str = f"S{i + 1:<2} |"
            for j in range(num_original_customers):
                row_str += f"{allocation[i][j]:<7}"
            self.allocation_text.insert(tk.END, row_str + "\n")

        self.profit_matrix_text.insert(tk.END, "Unit Profit Matrix:\n")
        self.profit_matrix_text.insert(tk.END, header + "\n")
        self.profit_matrix_text.insert(tk.END, "-" * len(header) + "\n")
        for i in range(num_original_suppliers):
            row_str = f"S{i + 1:<2} |"
            for j in range(num_original_customers):
                row_str += f"{profit_matrix[i][j]:<7}"
            self.profit_matrix_text.insert(tk.END, row_str + "\n")

        self.allocation_text.config(state=tk.DISABLED)
        self.profit_matrix_text.config(state=tk.DISABLED)

        for var, val in zip(self.results_vars, [purchase, transport, revenue, profit, iterations]):
            var.set(str(val))

    def load_from_file(self):
        path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        try:
            data = load_from_csv(path)

            self._is_loading = True
            self.num_suppliers.set(len(data['supply']))
            self.num_customers.set(len(data['demand']))
            self._is_loading = False

            self.update_data_inputs(data)

            messagebox.showinfo("Success", "Data loaded successfully.")
        except Exception as e:
            messagebox.showerror("File Error", f"Failed to load data from file.\n\nError: {e}")
        finally:
            self._is_loading = False

    def save_to_file(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            data = {
                'supply': [int(e.get()) for e in self.supply_entries],
                'purchase_costs': [int(e.get()) for e in self.purchase_cost_entries],
                'demand': [int(e.get()) for e in self.demand_entries],
                'selling_prices': [int(e.get()) for e in self.selling_price_entries],
                'transport_costs': [[int(e.get()) for e in row] for row in self.transport_cost_entries]
            }
            save_to_csv(path, data)
            messagebox.showinfo("Success", "Data saved successfully.")
        except ValueError:
            messagebox.showerror("Data Error", "Please enter valid data in all fields before saving.")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def clear_all(self):
        self.update_data_inputs()

    def clear_results(self):
        self.allocation_text.config(state=tk.NORMAL)
        self.allocation_text.delete(1.0, tk.END)
        self.allocation_text.config(state=tk.DISABLED)

        self.profit_matrix_text.config(state=tk.NORMAL)
        self.profit_matrix_text.delete(1.0, tk.END)
        self.profit_matrix_text.config(state=tk.DISABLED)

        for var in self.results_vars:
            var.set("")