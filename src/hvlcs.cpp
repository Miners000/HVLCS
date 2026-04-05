#include <algorithm>
#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <stdio.h>
#include <fstream>
using namespace std;

int main(int argc, char* argv[])
{
    istream* in = &cin;
    ifstream file_in;

    if (argc >= 2)
	{
        file_in.open(argv[1]);
        if (!file_in)
		{
            cerr << "Error: cannot open file '" << argv[1] << "'\n";
            return 1;
        }

        in = &file_in;
    }
 
    int K;
    *in >> K;
 
    unordered_map<char, long long> value;
    for (int i = 0; i < K; ++i)
	{
        char ch;
        long long v;
        *in >> ch >> v;
        value[ch] = v;
    }
 
    string A, B;
    *in >> A >> B;
    int n = (int)A.size();
    int m = (int)B.size();
    vector<vector<long long>> dp(n + 1, vector<long long>(m + 1, 0));
 
    for (int i = 1; i <= n; i++)
	{
        for (int j = 1; j <= m; j++)
		{
            dp[i][j] = max(dp[i-1][j], dp[i][j-1]);
 
            if (A[i-1] == B[j-1])
			{
                long long include = dp[i-1][j-1] + value[A[i-1]];
                dp[i][j] = max(dp[i][j], include);
            }
        }
    }
 
    string subseq;
    int i = n;
	int j = m;

    while (i > 0 && j > 0)
	{
        if (A[i-1] == B[j-1])
		{
            long long include = dp[i-1][j-1] + value[A[i-1]];
            if (dp[i][j] == include)
			{
                subseq += A[i-1];
                i--;
				j--;
                continue;
            }
        }

        if (dp[i-1][j] >= dp[i][j-1])
		{
            i--;
        }
		else
		{
            j--;
        }
    }

    reverse(subseq.begin(), subseq.end());
    cout << dp[n][m] << "\n" << subseq << "\n";
 
    return 0;
}