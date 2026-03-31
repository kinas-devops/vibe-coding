"""
Fibonacci Methods Benchmark Test
Comprehensive performance evaluation of all 17 Fibonacci algorithms.
"""

import time
import math
import sys
import tracemalloc
from typing import Dict, List, Tuple, Any
from fibonacci_lib import Fibonacci, fibonacci

class FibonacciBenchmark:
    """
    Benchmark class to test and compare all Fibonacci methods.
    """
    
    def __init__(self):
        self.fib = Fibonacci()
        self.results = {}
        
    def measure_time(self, func, *args, **kwargs) -> Tuple[Any, float]:
        """Measure execution time of a function"""
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        return result, end_time - start_time
    
    def measure_memory(self, func, *args, **kwargs) -> Tuple[Any, int]:
        """Measure memory usage of a function"""
        tracemalloc.start()
        result = func(*args, **kwargs)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, peak
    
    def run_single_benchmark(self, n: int, method_name: str, func) -> Dict[str, Any]:
        """Run benchmark for a single method"""
        benchmark_result = {
            'method': method_name,
            'n': n,
            'success': False,
            'result': None,
            'time': None,
            'memory': None,
            'error': None
        }
        
        try:
            # Measure time
            result, exec_time = self.measure_time(func, n)
            benchmark_result['result'] = result
            benchmark_result['time'] = exec_time
            benchmark_result['success'] = True
            
            # Measure memory for methods that don't cause recursion errors
            if method_name not in ['naive_recursion'] and n <= 1000:
                try:
                    _, memory_peak = self.measure_memory(func, n)
                    benchmark_result['memory'] = memory_peak
                except:
                    benchmark_result['memory'] = None
            
        except Exception as e:
            benchmark_result['error'] = str(e)
        
        return benchmark_result
    
    def run_comprehensive_benchmark(self, test_cases: List[Tuple[str, int]]) -> Dict[str, Any]:
        """
        Run comprehensive benchmarks for all methods across different test cases.
        """
        all_results = {}
        
        for case_name, n in test_cases:
            print(f"\n{'='*60}")
            print(f"Benchmarking n = {n} ({case_name})")
            print(f"{'='*60}")
            
            case_results = self._benchmark_single_n(n)
            all_results[case_name] = case_results
            
            self._print_case_results(case_results, n)
        
        return all_results
    
    def _benchmark_single_n(self, n: int) -> List[Dict[str, Any]]:
        """Benchmark all methods for a single n value"""
        methods = [
            # Method 1: Naive Recursion (only for very small n)
            ("naive_recursion", lambda x: self.fib.naive_recursion(x), n <= 30),
            
            # Method 2: Cached Recursion
            ("cached_recursion", lambda x: self.fib.cached_recursion(x), n <= 1000),
            
            # Method 3: Lazy Fibonacci (first access)
            ("lazy_fibonacci", lambda x: Fibonacci.LazyFibonacci()[x], True),
            
            # Method 4: Accumulator Recursion
            ("accumulator_recursion", lambda x: self.fib.accumulator_recursion(x), n <= 900),
            
            # Method 5: Imperative Loop
            ("imperative_loop", lambda x: self.fib.imperative_loop(x), True),
            
            # Method 6: Matrix Exponentiation
            ("matrix_exponentiation", lambda x: self.fib.matrix_exponentiation(x), True),
            
            # Method 7: Fast Doubling (Recursive)
            ("fast_doubling", lambda x: self.fib.fast_doubling(x), n <= 900),
            
            # Method 8: Fast Doubling (Iterative)
            ("fast_doubling_iterative", lambda x: self.fib.fast_doubling_iterative(x), True),
            
            # Method 9: Binet's Formula
            ("binet_formula", lambda x: self.fib.binet_formula(x), n <= 70),  # Precision limit
            
            # Method 10: Generalized Fibonacci (standard Fibonacci)
            ("generalized_fibonacci", lambda x: self.fib.generalized_fibonacci(1, 1, x), True),
            
            # Method 11: Generating Functions
            ("generating_function", lambda x: self.fib.generating_function(x), n <= 1000),
            
            # Method 12: Cassini's Identity
            ("cassini_identity", lambda x: self.fib.cassini_identity(x), n <= 10000),
            
            # Method 13: Linear Recurrence
            #("linear_recurrence", lambda x: self.fib.linear_recurrence(x), n <= 1000),
            # Method 13: Linear Recurrence (Fibonacci-specific)
            ("linear_recurrence", lambda x: Fibonacci.linear_recurrence_fibonacci(x), n <= 1000),
            # Method 13: Linear Recurrence (with correct Fibonacci parameters)
            #("linear_recurrence", lambda x: Fibonacci.linear_recurrence(x, [1, 1], [0, 1]), n <= 1000),
            
            # Method 14: Precomputed Fibonacci
            ("precomputed_fibonacci", self._get_precomputed_func(n), n <= 1000000),
            
            # Method 15: Mathematical Properties
            ("mathematical_properties", lambda x: self.fib.mathematical_properties(x), n <= 70),
            
            # Method 16: Parallel Computation (single number)
            ("parallel_single", lambda x: self.fib.parallel_fibonacci_range(x, x)[0], n <= 10000),
            
            # Method 17: DP Optimized
            ("dp_optimized", lambda x: self.fib.dp_optimized(x), True),
        ]
        
        results = []
        reference_result = None
        
        for method_name, method_func, should_run in methods:
            if not should_run:
                print(f"  {method_name:25} [SKIPPED - n too large]")
                continue
            
            print(f"  {method_name:25}...", end=" ", flush=True)
            
            result = self.run_single_benchmark(n, method_name, method_func)
            results.append(result)
            
            # Set reference result from first successful method
            if result['success'] and reference_result is None:
                reference_result = result['result']
            
            # Verify result correctness
            if result['success'] and reference_result is not None:
                if result['result'] != reference_result:
                    result['success'] = False
                    result['error'] = f"Result mismatch: expected {reference_result}, got {result['result']}"
            
            if result['success']:
                time_str = f"{result['time']:.6f}s" if result['time'] else "N/A"
                mem_str = f"{result['memory']} bytes" if result['memory'] else "N/A"
                print(f"[✓] Time: {time_str}, Memory: {mem_str}")
            else:
                print(f"[✗] Error: {result['error']}")
        
        return results
    
    def _get_precomputed_func(self, n):
        """Get precomputed Fibonacci function for given n"""
        precomputed = Fibonacci.PrecomputedFibonacci(limit=max(n, 1000))
        return precomputed.get
    
    def _print_case_results(self, results: List[Dict[str, Any]], n: int):
        """Print formatted results for a test case"""
        # Filter successful results
        successful = [r for r in results if r['success']]
        
        if not successful:
            print("No successful methods for this test case!")
            return
        
        # Sort by execution time
        successful.sort(key=lambda x: x['time'] if x['time'] else float('inf'))
        
        print(f"\nResults for n={n} (sorted by speed):")
        print("-" * 80)
        print(f"{'Method':25} {'Time':12} {'Memory':15} {'Result'}")
        print("-" * 80)
        
        for result in successful:
            time_str = f"{result['time']:.6f}s" if result['time'] else "N/A"
            mem_str = f"{result['memory']:>8} B" if result['memory'] else "N/A"
            result_str = str(result['result'])
            if len(result_str) > 20:
                result_str = result_str[:17] + "..."
            print(f"{result['method']:25} {time_str:12} {mem_str:15} {result_str}")
    
    def benchmark_range_performance(self):
        """Benchmark methods that work well for ranges of numbers"""
        print(f"\n{'='*60}")
        print("RANGE PERFORMANCE BENCHMARK")
        print(f"{'='*60}")
        
        range_sizes = [100, 1000, 10000]
        
        for size in range_sizes:
            print(f"\nBenchmarking range 0 to {size}:")
            
            # Test lazy Fibonacci for range access
            start_time = time.perf_counter()
            lazy_fib = Fibonacci.LazyFibonacci()
            for i in range(size + 1):
                _ = lazy_fib[i]
            lazy_time = time.perf_counter() - start_time
            
            # Test precomputed for range access
            start_time = time.perf_counter()
            precomputed = Fibonacci.PrecomputedFibonacci(limit=size)
            for i in range(size + 1):
                _ = precomputed.get(i)
            precomputed_time = time.perf_counter() - start_time
            
            # Test parallel for range
            start_time = time.perf_counter()
            _ = Fibonacci.parallel_fibonacci_range(0, size)
            parallel_time = time.perf_counter() - start_time
            
            print(f"  Lazy Fibonacci:     {lazy_time:.6f}s")
            print(f"  Precomputed:        {precomputed_time:.6f}s")
            print(f"  Parallel:           {parallel_time:.6f}s")
    
    def benchmark_modular_performance(self):
        """Benchmark modular Fibonacci performance"""
        print(f"\n{'='*60}")
        print("MODULAR FIBONACCI BENCHMARK")
        print(f"{'='*60}")
        
        mod = 10**9 + 7
        test_values = [100, 1000, 10000, 100000, 1000000]
        
        for n in test_values:
            print(f"\nn = {n}:")
            
            # Method 10: Modular Fibonacci
            start_time = time.perf_counter()
            try:
                result1 = fibonacci(n, 'modular_fibonacci', mod=mod)
                time1 = time.perf_counter() - start_time
                print(f"  Modular Fibonacci: {time1:.6f}s")
            except Exception as e:
                print(f"  Modular Fibonacci: Failed - {e}")
            
            # Compare with regular method + modulo
            start_time = time.perf_counter()
            try:
                result2 = fibonacci(n, 'fast_doubling_iterative') % mod
                time2 = time.perf_counter() - start_time
                print(f"  Fast Doubling + %:  {time2:.6f}s")
                
                # Verify results match
                if result1 == result2:
                    print(f"  Results match: ✓")
                else:
                    print(f"  Results mismatch: {result1} vs {result2}")
            except Exception as e:
                print(f"  Fast Doubling + %:  Failed - {e}")
    
    def generate_report(self, all_results: Dict[str, Any]):
        """Generate a comprehensive benchmark report"""
        print(f"\n{'='*80}")
        print("COMPREHENSIVE BENCHMARK REPORT")
        print(f"{'='*80}")
        
        # Overall rankings
        method_performance = {}
        
        for case_name, results in all_results.items():
            for result in results:
                if result['success'] and result['time']:
                    method = result['method']
                    if method not in method_performance:
                        method_performance[method] = []
                    method_performance[method].append(result['time'])
        
        # Calculate average performance
        avg_performance = {}
        for method, times in method_performance.items():
            avg_performance[method] = sum(times) / len(times)
        
        # Sort by average performance
        sorted_methods = sorted(avg_performance.items(), key=lambda x: x[1])
        
        print("\nOVERALL PERFORMANCE RANKING (Average Time):")
        print("-" * 50)
        for i, (method, avg_time) in enumerate(sorted_methods, 1):
            print(f"{i:2}. {method:25} {avg_time:.6f}s")
        
        # Recommendations
        print(f"\n{'='*80}")
        print("FINAL RECOMMENDATIONS")
        print(f"{'='*80}")
        
        recommendations = self.fib.get_method_recommendations()
        for scenario, methods in recommendations.items():
            available_methods = [m for m in methods if m in avg_performance]
            if available_methods:
                # Sort available methods by performance
                available_methods.sort(key=lambda m: avg_performance.get(m, float('inf')))
                best_method = available_methods[0]
                print(f"  {scenario:25}: {best_method} (avg: {avg_performance[best_method]:.6f}s)")

def main():
    """Main benchmark execution"""
    benchmark = FibonacciBenchmark()
    
    # Define test cases for different scenarios
    test_cases = [
        ("Very Small", 10),      # Educational purposes
        ("Small", 20),           # Typical usage
        ("Medium", 50),          # Practical applications
        ("Large", 100),          # Performance testing
        ("Very Large", 1000),    # Algorithm efficiency
        ("Extreme", 10000),      # Scalability testing
    ]
    
    print("FIBONACCI METHODS COMPREHENSIVE BENCHMARK")
    print("Testing all 17 implementations across different input sizes")
    
    # Run comprehensive benchmarks
    all_results = benchmark.run_comprehensive_benchmark(test_cases)
    
    # Run specialized benchmarks
    benchmark.benchmark_range_performance()
    benchmark.benchmark_modular_performance()
    
    # Generate final report
    benchmark.generate_report(all_results)
    
    # System information
    print(f"\n{'='*80}")
    print("SYSTEM INFORMATION")
    print(f"{'='*80}")
    print(f"Python: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Recursion Limit: {sys.getrecursionlimit()}")

if __name__ == "__main__":
    main()