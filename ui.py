import sys
import math
import matplotlib.pyplot as plt
from typing import List, Callable, Dict, Tuple

# Import our custom modules
from dataset_generator import DatasetGenerator
from execution_engine import ExecutionEngine
import algorithm_library as al

# ANSI Color Codes for terminal UI
class Colors:
    HEADER = '\033[95m'    
    BLUE = '\033[94m'      
    CYAN = '\033[96m'      
    GREEN = '\033[92m'     
    YELLOW = '\033[93m'    
    RED = '\033[91m'       
    RESET = '\033[0m'      
    BOLD = '\033[1m'       

class UI:
    def __init__(self):
        self.input_sizes = [] 
        
        self.sort_algos = {
            "1": ("Bubble Sort", al.bubble_sort),
            "2": ("Selection Sort", al.selection_sort),
            "3": ("Insertion Sort", al.insertion_sort),
            "4": ("Merge Sort", al.merge_sort),
            "5": ("Quick Sort", al.quick_sort),
            "6": ("Counting Sort", al.counting_sort),
            "7": ("Radix Sort", al.radix_sort)
        }
        self.search_algos = {
            "1": ("Linear Search", al.linear_search),
            "2": ("Binary Search", al.binary_search),
            "3": ("Jump Search", al.jump_search),
            "4": ("Fibonacci Search", al.fibonacci_search)
        }
        self.dist_map = {
            "1": "Random", 
            "2": "Sorted (Ascending)", 
            "3": "Left Skewed", 
            "4": "Right Skewed"
        }

    def run(self):
        try:
            while True:
                print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*50}")
                print(" ALGORITHM BENCHMARKING FRAMEWORK ")
                print(f"{'='*50}{Colors.RESET}")
                print(f"{Colors.GREEN}1. Benchmark Sorting Algorithms")
                print(f"2. Benchmark Searching Algorithms")
                print(f"{Colors.RED}3. Exit{Colors.RESET}")
                
                choice = input(f"\n{Colors.YELLOW}Select an option (1/2/3): {Colors.RESET}").strip()
                
                if choice == "1":
                    self._run_benchmark(self.sort_algos, is_sorting=True)
                elif choice == "2":
                    self._run_benchmark(self.search_algos, is_sorting=False)
                elif choice == "3":
                    print(f"\n{Colors.CYAN}Exiting framework. Goodbye!{Colors.RESET}")
                    sys.exit(0)
                else:
                    print(f"{Colors.RED}Invalid choice. Please try again.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n\n{Colors.RED}Execution interrupted by user. Exiting framework. Goodbye!{Colors.RESET}")
            sys.exit(0)

    def _print_complexity_table(self, algo_dict, is_sorting: bool):
        title = "SORTING ALGORITHM COMPLEXITIES" if is_sorting else "SEARCHING ALGORITHM COMPLEXITIES"
        print(f"\n{Colors.HEADER}{'-'*88}")
        print(f"{title:^88}")
        print(f"{'-'*88}{Colors.RESET}")
        print(f"{Colors.BOLD}{'Algorithm':<18} | {'Best Time':<15} | {'Average Time':<15} | {'Worst Time':<15} | {'Space'}{Colors.RESET}")
        print("-" * 88)
        
        for _, (name, _) in algo_dict.items():
            comps = al.COMPLEXITIES.get(name, {})
            best = comps.get('best', 'N/A')
            avg = comps.get('avg', 'N/A')
            worst = comps.get('worst', 'N/A')
            space = comps.get('space', 'N/A')
            print(f"{Colors.GREEN}{name:<18}{Colors.RESET} | {best:<15} | {avg:<15} | {worst:<15} | {space}")
        print("-" * 88)

    def _get_selections(self, algo_dict) -> List[Tuple[str, Callable]]:
        for key, (name, _) in algo_dict.items():
            print(f"{Colors.CYAN}{key}.{Colors.RESET} {name}")
        selections = input(f"\n{Colors.YELLOW}Enter comma-separated numbers (e.g., 1,4,5) or 'all': {Colors.RESET}").strip().lower()
        
        selected_algos = []
        if selections == 'all':
            return list(algo_dict.values())
            
        for s in selections.split(","):
            if s.strip() in algo_dict:
                selected_algos.append(algo_dict[s.strip()])
        return selected_algos

    def _generate_plot_points(self, max_size: int):
        if max_size <= 500:
            sizes = [10, 50, 100, max_size]
        else:
            step = max_size // 5
            sizes = [100] + [step * i for i in range(1, 5)] + [max_size]
        self.input_sizes = sorted(list(set(sizes)))

    def _run_benchmark(self, algo_dict, is_sorting: bool):
        self._print_complexity_table(algo_dict, is_sorting)

        algo_type = 'Sorting' if is_sorting else 'Searching'
        print(f"\n{Colors.HEADER}--- Select {algo_type} Algorithms to Benchmark ---{Colors.RESET}")
        selected = self._get_selections(algo_dict)
        if not selected: return

        dist_choices = []
        is_all_searches = not is_sorting and len(selected) == len(self.search_algos)
        is_linear_only = not is_sorting and len(selected) == 1 and selected[0][0] == "Linear Search"

        if is_sorting or is_linear_only:
            print(f"\n{Colors.HEADER}--- Select Dataset Distribution(s) ---{Colors.RESET}")
            print(f"{Colors.GREEN}1. Random")
            print("2. Sorted (Ascending)")
            print("3. Left Skewed")
            print("4. Right Skewed")
            print(f"5. ALL Distributions{Colors.RESET}")
            print(f"{Colors.CYAN}(You can select multiple by separating with commas, e.g., 1,3,4){Colors.RESET}")
            
            choice_str = input(f"{Colors.YELLOW}Choices: {Colors.RESET}").strip().lower()
            
            if "5" in choice_str or "all" in choice_str:
                dist_choices = ["1", "2", "3", "4"]
            else:
                dist_choices = [c.strip() for c in choice_str.split(",") if c.strip() in self.dist_map]
            
            if not dist_choices: 
                print(f"{Colors.RED}No valid distribution selected. Defaulting to Random.{Colors.RESET}")
                dist_choices = ["1"]
        else:
            if is_all_searches:
                print(f"\n{Colors.BLUE}* Note: Selecting 'All' automatically uses 'Sorted (Ascending)' datasets for fairness.{Colors.RESET}")
            else:
                print(f"\n{Colors.BLUE}* Note: You selected an algorithm that requires it, so 'Sorted (Ascending)' datasets will be used.{Colors.RESET}")
            dist_choices = ["2"]

        print(f"\n{Colors.HEADER}--- Select Maximum Input Size ---{Colors.RESET}")
        print(f"{Colors.CYAN}The system will benchmark smaller datasets up to this maximum to generate the graph.{Colors.RESET}")
        max_size_input = input(f"{Colors.YELLOW}Enter maximum size (e.g., 5000): {Colors.RESET}").strip()
        
        try:
            max_size = int(max_size_input)
            if max_size <= 0: raise ValueError
        except ValueError:
            print(f"{Colors.RED}Invalid size. Defaulting to 4000.{Colors.RESET}")
            max_size = 4000
            
        self._generate_plot_points(max_size)

        print(f"\n{Colors.CYAN}Executing points {self.input_sizes}... Please wait.{Colors.RESET}\n")

        all_dist_results = {}

        for dist_id in dist_choices:
            dist_name = self.dist_map[dist_id]
            
            time_results = {name: [] for name, _ in selected}
            mem_results = {name: [] for name, _ in selected}
            
            print(f"\n{Colors.HEADER}{Colors.BOLD}{'*'*20} BENCHMARKING: {dist_name.upper()} DATASET {'*'*20}{Colors.RESET}")

            for size in self.input_sizes:
                if dist_id == "1": base_data = DatasetGenerator.generate_random(size)
                elif dist_id == "3": base_data = DatasetGenerator.generate_left_skewed(size)
                elif dist_id == "4": base_data = DatasetGenerator.generate_right_skewed(size)
                else: base_data = DatasetGenerator.generate_sorted(size)

                target = base_data[-1] if not is_sorting else None
                
                print(f"\n{Colors.CYAN}{'='*20} INPUT SIZE: {size} {'='*20}{Colors.RESET}")
                print(f"{Colors.BOLD}{'Algorithm':<18} | {'Time (s)':<10} | {'Peak Mem (KB)'}{Colors.RESET}")
                print("-" * 50)

                for name, func in selected:
                    test_data = base_data.copy() 
                    
                    if is_sorting:
                        t_time, p_mem = ExecutionEngine.profile_algorithm(func, test_data)
                    else:
                        t_time, p_mem = ExecutionEngine.profile_algorithm(func, test_data, target)
                        
                    time_results[name].append(t_time)
                    mem_results[name].append(p_mem)
                    
                    print(f"{Colors.GREEN}{name:<18}{Colors.RESET} | {t_time:<10.5f} | {p_mem:<14.2f}")
            
            all_dist_results[dist_name] = {"time": time_results, "memory": mem_results}

        main_title = f"{algo_type} Benchmark Analysis"
        self._plot_subplots(all_dist_results, main_title)

    def _plot_subplots(self, all_dist_results: Dict[str, Dict[str, Dict[str, List[float]]]], main_title: str):
        num_datasets = len(all_dist_results)
        
        # Calculate grid layout for datasets within each figure
        cols = 2 if num_datasets > 1 else 1
        rows = math.ceil(num_datasets / cols)
        
        # --- Figure 1: Execution Time (Line Graphs) ---
        fig_time = plt.figure(figsize=(12 if cols==2 else 8, 5 * rows))
        fig_time.canvas.manager.set_window_title(f"{main_title} - Execution Time")
        fig_time.suptitle(f"{main_title}\nExecution Time vs Input Size", fontsize=16, fontweight='bold')
        
        for i, (dist_name, metrics) in enumerate(all_dist_results.items()):
            ax_time = fig_time.add_subplot(rows, cols, i + 1)
            for name, times in metrics["time"].items():
                ax_time.plot(self.input_sizes, times, marker='o', label=name, linewidth=2)
                
            ax_time.set_title(f"Dataset: {dist_name}", fontsize=12, fontweight='bold')
            ax_time.set_xlabel('Input Size (n)', fontsize=10)
            ax_time.set_ylabel('Execution Time (s)', fontsize=10)
            ax_time.grid(True, linestyle='--', alpha=0.5)
            ax_time.legend(fontsize=8, loc='upper left')

        plt.tight_layout()
        
        # --- Figure 2: Peak Memory (Bar Graphs) ---
        fig_mem = plt.figure(figsize=(12 if cols==2 else 8, 6 * rows))
        fig_mem.canvas.manager.set_window_title(f"{main_title} - Memory Usage")
        fig_mem.suptitle(f"{main_title}\nMaximum Peak Memory Usage", fontsize=16, fontweight='bold')
        
        for i, (dist_name, metrics) in enumerate(all_dist_results.items()):
            ax_mem = fig_mem.add_subplot(rows, cols, i + 1)
            
            algo_names = list(metrics["memory"].keys())
            max_memory_usage = [max(mems) for mems in metrics["memory"].values()]
            colors = plt.cm.tab10(range(len(algo_names)))
            
            bars = ax_mem.bar(algo_names, max_memory_usage, color=colors, edgecolor='black', alpha=0.8)
            
            ax_mem.set_title(f"Dataset: {dist_name}", fontsize=12, fontweight='bold')
            ax_mem.set_ylabel('Peak Memory (KB)', fontsize=10)
            ax_mem.tick_params(axis='x', rotation=45)
            ax_mem.grid(axis='y', linestyle='--', alpha=0.5)
            
            for bar in bars:
                yval = bar.get_height()
                ax_mem.text(bar.get_x() + bar.get_width()/2.0, yval + (yval * 0.02), f'{yval:.2f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        plt.tight_layout()
        plt.show(block=False) 
        plt.pause(0.1)