#!/usr/bin/env python3
"""
Benchmark the DP solution on generated test inputs and plot results.
"""
import os
import subprocess
import time
import json

def run_benchmark():
    """Run the compiled binary on all test files and measure execution time."""
    
    binary_path = "build/hvlcs.exe" if os.name == "nt" else "build/hvlcs"
    test_dir = "tests"
    
    # Ensure binary exists
    if not os.path.exists(binary_path):
        print(f"Error: {binary_path} not found. Please compile first.")
        return None
    
    results = []
    
    # Find all test inputs
    test_files = sorted([f for f in os.listdir(test_dir) if f.endswith(".in")])
    
    if not test_files:
        print("No test files found in tests directory.")
        return None
    
    print(f"Running {len(test_files)} benchmarks...\n")
    
    for test_file in test_files:
        filepath = os.path.join(test_dir, test_file)
        
        # Read input to extract test parameters
        with open(filepath, "r") as f:
            lines = f.readlines()
            K = int(lines[0].strip())
            # Lines 1..K are alphabet values
            str_a = lines[K+1].strip()
            str_b = lines[K+2].strip()
        
        # Run binary and measure time
        start_time = time.perf_counter()
        try:
            result = subprocess.run(
                [binary_path, filepath],
                capture_output=True,
                text=True,
                timeout=30
            )
            elapsed = (time.perf_counter() - start_time) * 1000  # Convert to ms
            
            if result.returncode != 0:
                print(f"  {test_file}: FAILED (return code {result.returncode})")
                continue
            
            # Parse output
            output_lines = result.stdout.strip().split('\n')
            if len(output_lines) < 2:
                print(f"  {test_file}: FAILED (invalid output)")
                continue
            
            value = int(output_lines[0])
            subseq = output_lines[1]
            
            results.append({
                "test_file": test_file,
                "K": K,
                "len_A": len(str_a),
                "len_B": len(str_b),
                "time_ms": elapsed,
                "max_value": value,
                "subseq_len": len(subseq)
            })
            
            print(f"  {test_file}: K={K:2d}, |A|={len(str_a):3d}, |B|={len(str_b):3d} => {elapsed:8.3f} ms")
        
        except subprocess.TimeoutExpired:
            print(f"  {test_file}: TIMEOUT (>30s)")
        except Exception as e:
            print(f"  {test_file}: ERROR ({e})")
    
    return results


def plot_results(results):
    """Plot runtime vs. input size."""
    import matplotlib.pyplot as plt
    import numpy as np
    
    if not results:
        print("No results to plot.")
        return
    
    # Extract data
    test_names = [r["test_file"] for r in results]
    times = [r["time_ms"] for r in results]
    sizes = [r["len_A"] * r["len_B"] for r in results]  # Total problem size
    
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Plot 1: Runtime vs Test Index
    ax1 = axes[0]
    ax1.bar(range(len(test_names)), times, color='steelblue')
    ax1.set_xlabel('Test Number')
    ax1.set_ylabel('Runtime (ms)')
    ax1.set_title('Runtime of DP Solution on Test Cases')
    ax1.set_xticks(range(len(test_names)))
    ax1.set_xticklabels([f"T{i+1}" for i in range(len(test_names))], rotation=45)
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Runtime vs Problem Size
    ax2 = axes[1]
    ax2.scatter(sizes, times, s=100, color='darkred', alpha=0.6)
    ax2.set_xlabel('Problem Size (|A| × |B|)')
    ax2.set_ylabel('Runtime (ms)')
    ax2.set_title('Runtime vs Problem Size')
    ax2.grid(True, alpha=0.3)
    
    # Add a fitted line (O(n*m) expected)
    z = np.polyfit(sizes, times, 2)
    p = np.poly1d(z)
    ax2.plot(sorted(sizes), p(sorted(sizes)), "r--", alpha=0.8, label='Fitted curve')
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('benchmark_results.png', dpi=100)
    print("\nPlot saved to benchmark_results.png")
    plt.show()


def save_results(results):
    """Save results to JSON for later analysis."""
    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Results saved to benchmark_results.json")


def main():
    print("=" * 60)
    print("Empirical Comparison: DP Solution Runtime Analysis")
    print("=" * 60)
    
    results = run_benchmark()
    
    if results:
        print("\n" + "=" * 60)
        print(f"Successfully ran {len(results)} tests")
        print("=" * 60)
        
        # Summary statistics
        times = [r["time_ms"] for r in results]
        print(f"\nRuntime Statistics (ms):")
        print(f"  Min:    {min(times):.3f}")
        print(f"  Max:    {max(times):.3f}")
        print(f"  Avg:    {sum(times)/len(times):.3f}")
        
        save_results(results)
        plot_results(results)
    else:
        print("\nBenchmarking failed.")


if __name__ == "__main__":
    main()
