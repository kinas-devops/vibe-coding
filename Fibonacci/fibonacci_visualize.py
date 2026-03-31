# benchmark_visualize.py
"""
Visualization for Fibonacci benchmark results.
"""

import matplotlib.pyplot as plt
import numpy as np
from fibonacci_benchmark import FibonacciBenchmark

def visualize_benchmark_results():
    """Create visualizations of benchmark results"""
    benchmark = FibonacciBenchmark()
    
    # Test cases for visualization
    test_sizes = [10, 20, 50, 100, 200, 500, 1000]
    methods_to_plot = [
        'imperative_loop',
        'fast_doubling_iterative', 
        'matrix_exponentiation',
        'cached_recursion',
        'dp_optimized'
    ]
    
    # Collect data
    times_data = {method: [] for method in methods_to_plot}
    n_values = []
    
    for n in test_sizes:
        print(f"Collecting data for n={n}...")
        n_values.append(n)
        
        # Get benchmark results
        results = benchmark._benchmark_single_n(n)
        
        for result in results:
            method = result['method']
            if method in methods_to_plot and result['success'] and result['time']:
                times_data[method].append(result['time'])
            elif method in methods_to_plot:
                times_data[method].append(None)
    
    # Create plots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot 1: Execution time vs n
    for method, times in times_data.items():
        valid_times = [t for t in times if t is not None]
        valid_n = [n for i, n in enumerate(n_values) if times[i] is not None]
        
        if valid_times:
            ax1.plot(valid_n, valid_times, 'o-', label=method, linewidth=2)
    
    ax1.set_xlabel('n (Fibonacci number to compute)')
    ax1.set_ylabel('Execution Time (seconds)')
    ax1.set_title('Fibonacci Methods Performance Comparison')
    ax1.set_yscale('log')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Speedup relative to imperative loop
    if 'imperative_loop' in times_data:
        imperative_times = times_data['imperative_loop']
        
        for method, times in times_data.items():
            if method != 'imperative_loop':
                speedups = []
                for i, time in enumerate(times):
                    if time is not None and imperative_times[i] is not None and imperative_times[i] > 0:
                        speedups.append(imperative_times[i] / time)
                    else:
                        speedups.append(None)
                
                valid_speedups = [s for s in speedups if s is not None]
                valid_n = [n for i, n in enumerate(n_values) if speedups[i] is not None]
                
                if valid_speedups:
                    ax2.plot(valid_n, valid_speedups, 'o-', label=method, linewidth=2)
    
    ax2.set_xlabel('n (Fibonacci number to compute)')
    ax2.set_ylabel('Speedup Relative to Imperative Loop')
    ax2.set_title('Performance Speedup Compared to Baseline')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('fibonacci_benchmark.png', dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    visualize_benchmark_results()