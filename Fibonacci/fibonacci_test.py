from fibonacci_lib import Fibonacci, fibonacci

def main():
    # Using the class directly
    fib = Fibonacci()
    
    # Basic usage
    print(f"F(10) = {fib.imperative_loop(10)}")
    print(f"F(20) = {fib.fast_doubling_iterative(20)}")
    print(f"F(30) = {fib.matrix_exponentiation(30)}")
    
    # Using convenience function
    print(f"F(15) = {fibonacci(15)}")
    print(f"F(15) with fast doubling = {fibonacci(15, 'fast_doubling')}")
    
    # Modular Fibonacci (for competitive programming)
    print(f"F(100) mod 10^9+7 = {fibonacci(100, 'modular_fibonacci', mod=10**9+7)}")
    
    # Precomputation for multiple queries
    precomputed = Fibonacci.PrecomputedFibonacci(limit=1000)
    print(f"F(100) from precomputed: {precomputed.get(100)}")
    print(f"F(200) from precomputed: {precomputed.get(200)}")
    
    # Compare methods
    results = fib.compare_methods(100)
    print("\nMethod comparison for F(100):")
    for method, data in results.items():
        if data['success']:
            print(f"  {method}: {data['time']:.6f}s")

if __name__ == "__main__":
    main()