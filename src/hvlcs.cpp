#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>

using namespace std;

int main() {
	ios::sync_with_stdio(false);
	cin.tie(nullptr);

	int K;
	if (!(cin >> K)) {
		return 0;
	}

	unordered_map<char, long long> value;
	value.reserve(static_cast<size_t>(K) * 2U + 1U);

	for (int i = 0; i < K; ++i) {
		char ch;
		long long v;
		cin >> ch >> v;
		value[ch] = v;
	}

	string A, B;
	cin >> A >> B;

	const int n = static_cast<int>(A.size());
	const int m = static_cast<int>(B.size());

	// dp[i][j] = best total value using prefixes A[0..i-1] and B[0..j-1].
	vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));

	for (int i = 1; i <= n; ++i) {
		for (int j = 1; j <= m; j++) {
			// either skip one character, or take a matching pair and add its weight.
			dp[i][j] = max(dp[i - 1][j], dp[i][j - 1]);
			if (A[i - 1] == B[j - 1]) {
				const long long w = value[A[i - 1]];
				dp[i][j] = max(dp[i][j], dp[i - 1][j - 1] + w);
			}
		}
	}

	string subseq;
	int i = n;
	int j = m;

	// backtrack through dp to reconstruct one optimal subsequence.
	while (i > 0 && j > 0) {
		if (A[i - 1] == B[j - 1]) {
			const long long w = value[A[i - 1]];
			if (dp[i][j] == dp[i - 1][j - 1] + w) {
				subseq.push_back(A[i - 1]);
				i--;
				j--;
				continue;
			}
		}

		if (dp[i - 1][j] >= dp[i][j - 1]) {
			i--;
		} else {
			j--;
		}
	}

	reverse(subseq.begin(), subseq.end());

	cout << dp[n][m] << '\n';
	cout << subseq << '\n';

	return 0;
}