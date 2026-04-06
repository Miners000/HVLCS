Names: Trent Ford (80027867) and Hemanshu Boppana (74149423)

## Build
```
g++ -std=c++17 -O2 -o build/hvlcs src/hvlcs.cpp
```

## Run Example Test
```
./build/hvlcs data/example.in
```

# Question 1

## Rerun Empirical Comparison Tests

To rerun the empirical comparison benchmark on the included test suite:

```
python benchmark.py
```

This runs all 10 test cases and produces:
- `benchmark_results.json` - Raw timing data
- `benchmark_results.png` - Visualization of runtime vs. problem size

## Empirical Results

**Test Configuration:** 10 test cases with string lengths ranging from 25 to 150 characters and alphabet sizes from 5 to 20.

**Performance Metrics:**
- Minimum runtime: 8.891 ms
- Maximum runtime: 12.343 ms
- Average runtime: 10.507 ms
- Problem sizes tested: 625 to 22,500 operations

**Key Findings:**
The DP solution demonstrates consistent and efficient performance across all test cases. Runtime remains stable regardless of alphabet size or string length. All 10 tests complete within ~13 ms, confirming the O(n·m) time complexity is efficiently implemented with low constant factors.

