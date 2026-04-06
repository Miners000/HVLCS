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

# Question 2: Recurrence Equation

Let dp[i][j] be the maximum total value of a common subsequence between A[0..i-1] and B[0..j-1].

Base cases:
```
dp[0][j] = 0,   dp[i][0] = 0
```
because an empty prefix has no non-empty common subsequence.

For i = 1..n and j = 1..m:
```
dp[i][j] = max(dp[i-1][j], dp[i][j-1])
if A[i-1] == B[j-1]:
    dp[i][j] = max(dp[i][j], dp[i-1][j-1] + v(A[i-1]))
```

Why this is correct (short):
- Any optimal solution for prefixes (i, j) must do one of these: skip A[i-1], skip B[j-1], or (if equal) take both characters.
- The three terms above are exactly those three possibilities.
- Taking the maximum therefore gives the optimal value for (i, j), and filling bottom-up gives the optimal value for the full strings.

# Question 3: Big-Oh Analysis

## Algorithm Pseudocode

```
Algorithm HVLCS_Length(A, B, value)
Input: Strings A and B, character value map
Output: Maximum value of a common subsequence

  n ← length of A
  m ← length of B
  
  // Initialize DP table with base cases
  dp[0..n][0..m] ← all zeros
  
  // Fill DP table bottom-up
  for i ← 1 to n do
    for j ← 1 to m do
      dp[i][j] ← max(dp[i-1][j], dp[i][j-1])
      
      if A[i-1] == B[j-1] then
        dp[i][j] ← max(dp[i][j], dp[i-1][j-1] + value[A[i-1]])
      end if
    end for
  end for
  
  return dp[n][m]
```

## Time Complexity

**O(n·m)** where n = |A| and m = |B|.

**Justification:**
- The algorithm fills an (n+1) × (m+1) DP table.
- Each cell dp[i][j] is computed exactly once.
- Each cell computation requires O(1) time: one character comparison, at most two max operations, and one table lookup.
- Total: (n+1) × (m+1) cells × O(1) per cell = **O(n·m)**.

## Space Complexity

**O(n·m)** for the DP table.

**Optimization:** Space can be reduced to **O(min(n, m))** using a rolling array technique, since each row only depends on the previous row. However, this would complicate reconstruction of the actual subsequence.

