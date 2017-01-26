class Solution {
public:
    char* isPrime;
    int len;
    Solution()
    {
        isPrime = (char *) malloc (sizeof(char)*100000);
        len = 100000;
    }
    int countPrimes(int n) {
        // Memory optimization, reuse the malloc
        if (isPrime != NULL) {
            if (len < n) {
                free(isPrime);
                isPrime = NULL;
                isPrime = (char *) malloc (sizeof(char)*n);
                len = n;
            } else {
                memset(isPrime, 0, len );
            }
        } else {
            isPrime = (char *) malloc (sizeof(char)*n);
            len = n;
        }
        memset(isPrime, 0, len );
        
        for (int i = 2; i * i < n; ++i) {
           if (isPrime[i] == 1) {
               continue;
           }
           for (int j = i * i; j < n; j += i) {
              isPrime[j] = 1;
           }
        }
        int count = 0;
        for (int i = 2; i < n; ++i) {
           if (isPrime[i] == 0) {
               count++;
           }
        }
        return count;
    }
};