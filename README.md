Names: Trent Ford (80027867) and Hemanshu Boppana (74149423)

## Build
```
g++ -std=c++17 -O2 -o build/hvlcs src/hvlcs.cpp
```

## Run Example Test
```
./build/hvlcs data/example.in
```

## Assumptions and Dependencies

### Assumptions
- Input format is exactly:
  - First line: integer `K`
  - Next `K` lines: `<character> <nonnegative integer value>`
  - Next line: string `A`
  - Next line: string `B`
- Characters in `A` and `B` are from the provided alphabet/value map.
- Character values are nonnegative integers.
- If multiple optimal subsequences exist, any one may be output.

### Dependencies
- C++17-compatible compiler (e.g., `g++`) to build `src/hvlcs.cpp`.
- Python 3 for running `benchmark.py`.
- Python packages for plotting benchmark graphs:
  - `matplotlib`
  - `numpy`

# Question 1

## RTo rerun the empirical comparison benchmark on the included test suite, create a virtual Python environment and run:

```
python benchmark.py
```

This runs all 10 test cases and produces:
- `benchmark_results.json` - Raw timing data
- `benchmark_results.png` - Visualization of runtime vs. problem size.

## Empirical Results

**Test Configuration:** 10 test cases with string lengths ranging from 25 to 150 characters and alphabet sizes from 5 to 20.

**Performance Metrics:**
- Minimum runtime: 8.891 ms
- Maximum runtime: 12.343 ms
- Average runtime: 10.507 ms
- Problem sizes tested: 625 to 22,500 operations

**Key Findings:**
The DP solution demonstrates consistent and efficient performance across all test cases. Runtime remains stable regardless of alphabet size or string length. All 10 tests complete within about 13 ms, confirming the `O(nm)` time complexity is efficiently implemented with low constant factors.

# Question 2: Recurrence Equation

Let `dp[i][j]` be the maximum total value of a common subsequence between `A[0..i-1]` and `B[0..j-1]`.

`OPT(i, j) = 0` if `i = 0` or `j = 0`, otherwise:

`OPT(i, j) = OPT(i-1, j-1) + v_i, max(OPT(i-1, j), OPT(i, j-1))`

Why this is correct:
- Any optimal solution for prefixes `(i, j)` must do one of these: skip `A[i-1]`, skip `B[j-1]`, or (if equal) take both characters.
- The three terms above are exactly those three possibilities.
- Taking the maximum therefore gives the optimal value for `(i, j)`, and filling bottom-up gives the optimal value for the full strings.

# Question 3: Big-Oh Analysis

## Algorithm Pseudocode

```
Algorithm HVLCS_Length(A, B)
Input: Strings A and B
Output: Length of a common subsequence

  n <- length of A
  m <- length of B

  // len[i][j] stores the LCS length for prefixes A[0..i-1] and B[0..j-1]
  len[0..n][0..m] <- all zeros

  // Fill table bottom-up
  for i <- 1 to n do
    for j <- 1 to m do
      if A[i-1] == B[j-1] then
        len[i][j] <- len[i-1][j-1] + 1
      else
        len[i][j] <- max(len[i-1][j], len[i][j-1])
  return len[n][m]
```

## Time Complexity

**O(nm)** where `n = |A|` and `m = |B|`.

**Justification:**
- The algorithm fills an `(n+1) x (m+1)` DP table.
- Each cell `len[i][j]` is computed exactly once.
- Each cell computation requires `O(1)` time: one character comparison and at most one max operation.
- Total: `(n+1) x (m+1)` cells x `O(1)` per cell = **O(nm)**.

## Space Complexity

**O(nm)** for the DP table.


