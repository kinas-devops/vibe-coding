"""
Fibonacci Library - 17 Different Implementations
A comprehensive collection of Fibonacci algorithms for various use cases.
"""

import math
from functools import lru_cache
from typing import Tuple, List, Dict, Any
import concurrent.futures

class Fibonacci:
    """
    Main Fibonacci class containing all 17 implementation methods.
    """
    
    # ===== METHOD 1: Naive Binary Recursion =====
    @staticmethod
    def naive_recursion(n: int) -> int:
        """
        Compute Fibonacci using naive binary recursion.
        Time: O(2^n), Space: O(n)
        WARNING: Extremely inefficient for n > 35
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        return Fibonacci.naive_recursion(n - 1) + Fibonacci.naive_recursion(n - 2)
    
    # ===== METHOD 2: Cached Binary Recursion / Memoization =====
    @staticmethod
    @lru_cache(maxsize=None)
    def cached_recursion(n: int) -> int:
        """
        Compute Fibonacci using cached recursion with LRU cache.
        Time: O(n), Space: O(n)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        return Fibonacci.cached_recursion(n - 1) + Fibonacci.cached_recursion(n - 2)
    
    # ===== METHOD 3: Cached Linear Recursion / Infinite Lazy List =====
    class LazyFibonacci:
        """Infinite lazy-evaluated Fibonacci sequence with caching"""
        def __init__(self):
            self.cache = [0, 1]
        
        def __getitem__(self, n: int) -> int:
            if n < 0:
                raise IndexError("Fibonacci sequence index must be non-negative")
            while len(self.cache) <= n:
                next_fib = self.cache[-1] + self.cache[-2]
                self.cache.append(next_fib)
            return self.cache[n]
        
        def get_sequence(self, n: int) -> List[int]:
            """Get first n Fibonacci numbers"""
            return [self[i] for i in range(n)]
    
    # ===== METHOD 4: Linear Recursion with Accumulator =====
    @staticmethod
    def accumulator_recursion(n: int, a: int = 0, b: int = 1) -> int:
        """
        Compute Fibonacci using tail recursion with accumulators.
        Time: O(n), Space: O(n) due to recursion stack
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return a
        elif n == 1:
            return b
        return Fibonacci.accumulator_recursion(n - 1, b, a + b)
    
    # ===== METHOD 5: Imperative Loop with Mutable Variables =====
    @staticmethod
    def imperative_loop(n: int) -> int:
        """
        Compute Fibonacci using imperative programming with mutable variables.
        Time: O(n), Space: O(1)
        Recommended for most practical applications.
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b
    
    # ===== METHOD 6: Matrix Multiplication =====
    @staticmethod
    def matrix_exponentiation(n: int) -> int:
        """
        Compute Fibonacci using matrix exponentiation.
        Time: O(log n), Space: O(1)
        Best for very large n.
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            """Multiply two 2x2 matrices"""
            return [
                [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
            ]
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            """Raise a 2x2 matrix to a power using exponentiation by squaring"""
            result = [[1, 0], [0, 1]]  # Identity matrix
            base = matrix
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, base)
                base = matrix_mult(base, base)
                power //= 2
            
            return result
        
        base_matrix = [[1, 1], [1, 0]]
        powered_matrix = matrix_power(base_matrix, n - 1)
        return powered_matrix[0][0]
    
    # ===== METHOD 7: Fast Recursion (Fast Doubling) =====
    @staticmethod
    def fast_doubling(n: int) -> int:
        """
        Compute Fibonacci using fast doubling method.
        Time: O(log n), Space: O(log n)
        Best overall for very large n.
        """
        def fast_doubling_pair(k: int) -> Tuple[int, int]:
            if k == 0:
                return (0, 1)
            a, b = fast_doubling_pair(k // 2)
            c = a * (2 * b - a)
            d = a * a + b * b
            if k % 2 == 0:
                return (c, d)
            else:
                return (d, c + d)
        
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        return fast_doubling_pair(n)[0]
    
    @staticmethod
    def fast_doubling_iterative(n: int) -> int:
        """
        Iterative version of fast doubling to avoid recursion limits.
        Time: O(log n), Space: O(1)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        
        a, b = 0, 1
        bit_mask = 1 << (n.bit_length() - 1)
        
        while bit_mask > 0:
            a2 = a * (2 * b - a)
            b2 = a * a + b * b
            
            if n & bit_mask:
                a, b = b2, a2 + b2
            else:
                a, b = a2, b2
            
            bit_mask >>= 1
        
        return a
    
    # ===== METHOD 8: Binet's Formula with Rounding =====
    @staticmethod
    def binet_formula(n: int) -> int:
        """
        Compute Fibonacci using Binet's closed-form formula.
        Time: O(1), Space: O(1)
        Mathematical elegance but limited by floating-point precision.
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        
        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2
        psi = (1 - sqrt5) / 2
        
        fib_n = (phi**n - psi**n) / sqrt5
        return round(fib_n)
    
    # ===== METHOD 9: Generalized Fibonacci with Matrix Exponentiation =====
    @staticmethod
    def generalized_fibonacci(a: int, b: int, n: int) -> int:
        """
        Compute generalized Fibonacci: F(n) = a*F(n-1) + b*F(n-2)
        Time: O(log n), Space: O(1)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            """Multiply two 2x2 matrices"""
            return [
                [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
            ]
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            """Raise a 2x2 matrix to a power"""
            result = [[1, 0], [0, 1]]  # Identity matrix
            base = matrix
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, base)
                base = matrix_mult(base, base)
                power //= 2
            
            return result
        
        base_matrix = [[a, b], [1, 0]]
        powered_matrix = matrix_power(base_matrix, n - 1)
        return powered_matrix[0][0]
    
    # ===== METHOD 10: Modular Fibonacci =====
    @staticmethod
    def modular_fibonacci(n: int, mod: int) -> int:
        """
        Compute F(n) mod m using fast doubling.
        Time: O(log n), Space: O(log n)
        Essential for competitive programming.
        """
        def fib_pair(k: int, modulus: int) -> Tuple[int, int]:
            if k == 0:
                return (0, 1)
            a, b = fib_pair(k // 2, modulus)
            c = (a * ((2 * b - a) % modulus)) % modulus
            d = (a * a + b * b) % modulus
            if k % 2 == 0:
                return (c, d)
            else:
                return (d, (c + d) % modulus)
        
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if mod <= 0:
            raise ValueError("Modulus must be positive")
        
        return fib_pair(n, mod)[0]
    
    # ===== METHOD 11: Generating Functions Approach =====
    _generating_function_cache = {}
    
    @classmethod
    def generating_function(cls, n: int) -> int:
        """
        Using generating function approach with memoization.
        Time: O(n), Space: O(n)
        """
        if n in cls._generating_function_cache:
            return cls._generating_function_cache[n]
        
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        result = cls.generating_function(n-1) + cls.generating_function(n-2)
        cls._generating_function_cache[n] = result
        return result
    
    # ===== METHOD 12: Cassini's Identity Approach =====
    @staticmethod
    def cassini_identity(n: int) -> int:
        """
        Using Cassini's identity for computation.
        Time: O(n), Space: O(n)
        Mainly for educational purposes.
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        fibs = [0, 1]
        for i in range(2, n + 1):
            fibs.append(fibs[i-1] + fibs[i-2])
        
        return fibs[n]
    
    # ===== METHOD 13: Linear Recurrence Solver (Fibonacci-specific) =====
    @staticmethod
    def linear_recurrence_fibonacci(n: int) -> int:
        """
        Linear recurrence solver specifically for Fibonacci sequence.
        Uses the recurrence: F(n) = F(n-1) + F(n-2)
        Time: O(log n), Space: O(1)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            return [
                [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
                [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
            ]
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            result = [[1, 0], [0, 1]]
            base = matrix
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, base)
                base = matrix_mult(base, base)
                power //= 2
            return result
        
        # Companion matrix for Fibonacci: [[1, 1], [1, 0]]
        companion = [[1, 1], [1, 0]]
        powered = matrix_power(companion, n - 1)
        
        # F(n) is the top-left element for this formulation
        return powered[0][0]
        
    # ===== METHOD 13: Linear Recurrence Solver =====
    @staticmethod
    def linear_recurrence_err(n: int, coefficients: List[int] = None, initial: List[int] = None) -> int:
        """
        General linear recurrence solver for Fibonacci-like sequences.
        Time: O(k³ log n), Space: O(k²)
        """
        if coefficients is None:
            coefficients = [1, 1]
        if initial is None:
            initial = [0, 1]
        
        k = len(initial)
        if n < k:
            return initial[n]
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            n_size = len(A)
            p_size = len(B)
            m_size = len(B[0])
            C = [[0] * m_size for _ in range(n_size)]
            for i in range(n_size):
                for j in range(m_size):
                    for l in range(p_size):
                        C[i][j] += A[i][l] * B[l][j]
            return C
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            n_size = len(matrix)
            result = [[1 if i == j else 0 for j in range(n_size)] for i in range(n_size)]
            base = matrix
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, base)
                base = matrix_mult(base, base)
                power //= 2
            return result
        
        # Build companion matrix
        companion = [[0] * k for _ in range(k)]
        for i in range(k-1):
            companion[i][i+1] = 1
        for i in range(k):
            companion[k-1][i] = coefficients[k-1-i]
        
        powered = matrix_power(companion, n - k + 1)
        
        # Extract result
        result = 0
        for i in range(k):
            result += powered[0][i] * initial[k-1-i]
        
        return result


    # ===== METHOD 13: Linear Recurrence Solver =====
    @staticmethod
    def linear_recurrence(n: int, coefficients: List[int] = None, initial: List[int] = None) -> int:
        """
        General linear recurrence solver for Fibonacci-like sequences.
        F(n) = c0*F(n-1) + c1*F(n-2) + ... + ck*F(n-k-1)
        Time: O(k³ log n), Space: O(k²)
        """
        if coefficients is None:
            coefficients = [1, 1]  # Fibonacci coefficients: F(n) = 1*F(n-1) + 1*F(n-2)
        if initial is None:
            initial = [0, 1]  # Fibonacci initial: F(0)=0, F(1)=1
        
        k = len(initial)
        
        # Base cases
        if n < k:
            return initial[n]
        
        def matrix_mult(A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
            """Multiply two matrices"""
            n_size = len(A)
            p_size = len(B)
            m_size = len(B[0])
            C = [[0] * m_size for _ in range(n_size)]
            for i in range(n_size):
                for j in range(m_size):
                    for l in range(p_size):
                        C[i][j] += A[i][l] * B[l][j]
            return C
        
        def matrix_power(matrix: List[List[int]], power: int) -> List[List[int]]:
            """Raise a matrix to a power using exponentiation by squaring"""
            n_size = len(matrix)
            result = [[1 if i == j else 0 for j in range(n_size)] for i in range(n_size)]
            base = matrix
            
            while power > 0:
                if power % 2 == 1:
                    result = matrix_mult(result, base)
                base = matrix_mult(base, base)
                power //= 2
            
            return result
        
        # Build the companion matrix correctly
        # For recurrence: F(n) = c0*F(n-1) + c1*F(n-2) + ... + c_{k-1}*F(n-k)
        companion = [[0] * k for _ in range(k)]
        
        # First row contains the coefficients
        for i in range(k):
            companion[0][i] = coefficients[i]  # Note: coefficients should be in order [c0, c1, ..., c_{k-1}]
        
        # Fill the sub-diagonal with 1s
        for i in range(1, k):
            companion[i][i-1] = 1
        
        # Compute M^(n-k+1)
        powered = matrix_power(companion, n - k + 1)
        
        # Extract result: F(n) = first row of powered matrix dot initial vector
        result = 0
        for i in range(k):
            result += powered[0][i] * initial[i]
        
        return result
    
    # ===== METHOD 14: Fast Doubling with Precomputation =====
    class PrecomputedFibonacci:
        """
        Precompute Fibonacci numbers for O(1) queries.
        """
        def __init__(self, limit: int = 10**6):
            self.limit = limit
            self.fib = [0, 1]
            self._precompute()
        
        def _precompute(self):
            for i in range(2, self.limit + 1):
                self.fib.append(self.fib[i-1] + self.fib[i-2])
        
        def get(self, n: int) -> int:
            if n < 0:
                raise ValueError("Index must be non-negative")
            if n > self.limit:
                raise ValueError(f"Index {n} exceeds precomputation limit {self.limit}")
            return self.fib[n]
        
        def get_range(self, start: int, end: int) -> List[int]:
            return self.fib[start:end+1]
    
    # ===== METHOD 15: Mathematical Properties =====
    @staticmethod
    def mathematical_properties(n: int) -> int:
        """
        Use mathematical properties for computation.
        Time: O(1), Space: O(1)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        
        # Use properties like F(2n) = F(n) * (2*F(n+1) - F(n))
        # For simplicity, using Binet's formula here
        sqrt5 = math.sqrt(5)
        phi = (1 + sqrt5) / 2
        return round(phi**n / sqrt5)
    
    # ===== METHOD 16: Parallel Computation =====
    @staticmethod
    def parallel_fibonacci_range(start: int, end: int, chunk_size: int = 1000) -> List[int]:
        """
        Parallel computation of Fibonacci numbers for ranges.
        Time: O(n) with parallel speedup, Space: O(n)
        """
        def compute_chunk(chunk_start: int, chunk_end: int) -> List[int]:
            a, b = 0, 1
            if chunk_start > 0:
                for _ in range(chunk_start):
                    a, b = b, a + b
            result = []
            for i in range(chunk_start, chunk_end + 1):
                result.append(a)
                a, b = b, a + b
            return result
        
        if start > end:
            raise ValueError("Start must be <= end")
        
        total_numbers = end - start + 1
        if total_numbers <= chunk_size:
            return compute_chunk(start, end)
        
        chunks = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = []
            for chunk_start in range(start, end + 1, chunk_size):
                chunk_end = min(chunk_start + chunk_size - 1, end)
                futures.append(executor.submit(compute_chunk, chunk_start, chunk_end))
            
            for future in concurrent.futures.as_completed(futures):
                chunks.extend(future.result())
        
        return chunks
    
    # ===== METHOD 17: Dynamic Programming with Space Optimization =====
    @staticmethod
    def dp_optimized(n: int) -> int:
        """
        Dynamic programming with rolling array for space optimization.
        Time: O(n), Space: O(1)
        """
        if n < 0:
            raise ValueError("Fibonacci sequence index must be non-negative")
        if n == 0:
            return 0
        elif n == 1:
            return 1
        
        # Only store last two values
        prev_prev, prev = 0, 1
        for i in range(2, n + 1):
            current = prev_prev + prev
            prev_prev, prev = prev, current
        
        return prev

    # ===== UTILITY METHODS =====
    @staticmethod
    def get_method_recommendations() -> Dict[str, Any]:
        """
        Get recommendations for which method to use in different scenarios.
        """
        return {
            "learning": ["naive_recursion", "cached_recursion", "accumulator_recursion"],
            "production": ["imperative_loop", "dp_optimized"],
            "competitive_programming": ["fast_doubling_iterative", "modular_fibonacci"],
            "mathematical_research": ["matrix_exponentiation", "binet_formula"],
            "very_large_n": ["fast_doubling_iterative", "matrix_exponentiation"],
            "multiple_queries": ["PrecomputedFibonacci"],
            "memory_constrained": ["dp_optimized", "imperative_loop"],
            "educational": ["all_methods"]
        }
    
    @staticmethod
    def compare_methods(n: int, methods: List[str] = None) -> Dict[str, Any]:
        """
        Compare performance of different methods for a given n.
        """
        import time
        
        if methods is None:
            methods = [
                "imperative_loop", 
                "fast_doubling_iterative", 
                "matrix_exponentiation",
                "binet_formula"
            ]
        
        results = {}
        fib = Fibonacci()
        
        for method_name in methods:
            try:
                start_time = time.time()
                if hasattr(fib, method_name):
                    method = getattr(fib, method_name)
                    result = method(n)
                else:
                    continue
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                results[method_name] = {
                    "result": result,
                    "time": execution_time,
                    "success": True
                }
            except Exception as e:
                results[method_name] = {
                    "result": None,
                    "time": None,
                    "success": False,
                    "error": str(e)
                }
        
        return results


# ===== CONVENIENCE FUNCTIONS =====
def fibonacci(n: int, method: str = "imperative_loop", **kwargs) -> int:
    """
    Convenience function to compute Fibonacci numbers using specified method.
    
    Args:
        n: Fibonacci number to compute
        method: Method to use ('imperative_loop', 'fast_doubling', etc.)
        **kwargs: Additional arguments for specific methods
    
    Returns:
        The nth Fibonacci number
    """
    fib = Fibonacci()
    
    if method == "naive_recursion":
        return fib.naive_recursion(n)
    elif method == "cached_recursion":
        return fib.cached_recursion(n)
    elif method == "accumulator_recursion":
        return fib.accumulator_recursion(n)
    elif method == "imperative_loop":
        return fib.imperative_loop(n)
    elif method == "matrix_exponentiation":
        return fib.matrix_exponentiation(n)
    elif method == "fast_doubling":
        return fib.fast_doubling(n)
    elif method == "fast_doubling_iterative":
        return fib.fast_doubling_iterative(n)
    elif method == "binet_formula":
        return fib.binet_formula(n)
    elif method == "modular_fibonacci":
        mod = kwargs.get('mod', 10**9 + 7)
        return fib.modular_fibonacci(n, mod)
    elif method == "generating_function":
        return fib.generating_function(n)
    elif method == "cassini_identity":
        return fib.cassini_identity(n)
    elif method == "linear_recurrence":
        coeffs = kwargs.get('coefficients', [1, 1])
        initial = kwargs.get('initial', [0, 1])
        return fib.linear_recurrence(n, coeffs, initial)
    elif method == "mathematical_properties":
        return fib.mathematical_properties(n)
    elif method == "dp_optimized":
        return fib.dp_optimized(n)
    else:
        raise ValueError(f"Unknown method: {method}")


# ===== EXAMPLE USAGE =====
if __name__ == "__main__":
    # Example usage and demonstration
    fib = Fibonacci()
    
    print("Fibonacci Library Demo")
    print("=" * 50)
    
    # Test different methods
    n = 20
    print(f"Computing F({n}) using different methods:")
    print(f"Imperative Loop: {fib.imperative_loop(n)}")
    print(f"Fast Doubling: {fib.fast_doubling_iterative(n)}")
    print(f"Matrix Exponentiation: {fib.matrix_exponentiation(n)}")
    print(f"Binet's Formula: {fib.binet_formula(n)}")
    
    # Compare performance
    print(f"\nPerformance comparison for F(1000):")
    results = fib.compare_methods(1000)
    for method, data in results.items():
        if data["success"]:
            print(f"  {method:25}: {data['time']:.6f}s")
    
    # Show recommendations
    print(f"\nMethod Recommendations:")
    recommendations = fib.get_method_recommendations()
    for scenario, methods in recommendations.items():
        print(f"  {scenario:20}: {', '.join(methods[:3])}")
    
    # Convenience function example
    print(f"\nConvenience function examples:")
    print(f"fibonacci(10): {fibonacci(10)}")
    print(f"fibonacci(10, 'fast_doubling'): {fibonacci(10, 'fast_doubling')}")
    print(f"fibonacci(10, 'modular_fibonacci', mod=1000): {fibonacci(10, 'modular_fibonacci', mod=1000)}")