import random
from typing import List

class DatasetGenerator:
    
    @staticmethod
    def generate_random(size: int, min_val: int = 1, max_val: int = 10000) -> List[int]:
        """Generates a dataset of uniformly distributed random integers."""
        return [random.randint(min_val, max_val) for _ in range(size)]

    @staticmethod
    def generate_sorted(size: int, min_val: int = 1, max_val: int = 10000) -> List[int]:
        """Generates a sorted dataset of random integers."""
        dataset = [random.randint(min_val, max_val) for _ in range(size)]
        dataset.sort()
        return dataset

    @staticmethod
    def generate_left_skewed(size: int, min_val: int = 1, max_val: int = 10000) -> List[int]:
        """
        Generates a naturally left-skewed dataset (tail points towards smaller numbers).
        Uses a Beta distribution where alpha > beta.
        """
        return [
            int(min_val + (max_val - min_val) * random.betavariate(5, 2))
            for _ in range(size)
        ]

    @staticmethod
    def generate_right_skewed(size: int, min_val: int = 1, max_val: int = 10000) -> List[int]:
        """
        Generates a naturally right-skewed dataset (tail points towards larger numbers).
        Uses a Beta distribution where alpha < beta.
        """
        return [
            int(min_val + (max_val - min_val) * random.betavariate(2, 5))
            for _ in range(size)
        ]