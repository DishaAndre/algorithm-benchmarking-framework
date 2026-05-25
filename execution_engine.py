import time
import tracemalloc
from typing import Callable, Tuple

class ExecutionEngine:
    @staticmethod
    def profile_algorithm(algo: Callable, *args) -> Tuple[float, float]:
        tracemalloc.start()
        start_time = time.perf_counter()
        
        algo(*args)
        
        end_time = time.perf_counter()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        execution_time = end_time - start_time
        peak_memory_kb = peak / 1024
        
        return execution_time, peak_memory_kb