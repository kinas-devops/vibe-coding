# quick_test.py
"""
Quick test to verify all methods work correctly.
"""

from fibonacci_lib import Fibonacci, fibonacci

def quick_verification():
    """Quick verification that all methods produce correct results"""
    fib = Fibonacci()
    
    # Test values and expected results
    test_cases = [
        (0, 0),
        (1, 1),
        (5, 5),
        (10, 55),
        (20, 6765),
    ]
    
    methods = [
        ('naive_recursion', lambda n: fib.naive_recursion(n), 10),  # Only test up to n=10
        ('cached_recursion', lambda n: fib.cached_recursion(n), 100),
        ('imperative_loop', lambda n: fib.imperative_loop(n), 1000),
        ('fast_doubling_iterative', lambda n: fib.fast_doubling_iterative(n), 1000),
        ('matrix_exponentiation', lambda n: fib.matrix_exponentiation(n), 1000),
        ('binet_formula', lambda n: fib.binet_formula(n), 70),  # Precision limit
    ]
    
    print("Quick Verification of Fibonacci Methods")
    print("=" * 50)
    
    all_correct = True
    
    for method_name, method_func, max_n in methods:
        print(f"\nTesting {method_name}:")
        method_correct = True
        
        for n, expected in test_cases:
            if n > max_n:
                continue
                
            try:
                result = method_func(n)
                status = "✓" if result == expected else "✗"
                print(f"  F({n}) = {result} (expected {expected}) {status}")
                
                if result != expected:
                    method_correct = False
                    all_correct = False
                    
            except Exception as e:
                print(f"  F({n}) = ERROR: {e} ✗")
                method_correct = False
                all_correct = False
        
        if method_correct:
            print(f"  {method_name}: ALL TESTS PASSED ✓")
        else:
            print(f"  {method_name}: SOME TESTS FAILED ✗")
    
    print(f"\n{'='*50}")
    if all_correct:
        print("OVERALL: ALL METHODS WORK CORRECTLY ✓")
    else:
        print("OVERALL: SOME METHODS HAVE ISSUES ✗")

if __name__ == "__main__":
    quick_verification()