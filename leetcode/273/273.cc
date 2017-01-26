class Solution {
public:
    string numberToWords(int num) {
        if(num == 0) {
            return "Zero";
        } else {
            int section = 0;
            string result_str = "";
            int sec_int = 0;
            while (num > 0) {
                sec_int = num % 1000;
                if (sec_int != 0)
                {
                    if (section == 0) {
                        result_str = GenSection(sec_int) + " " + result_str;
                    } else {
                        result_str = GenSection(sec_int) + " " + k_Thousands[section] + " " + result_str;
                    }
                    
                }
                num /= 1000;
                ++section;
            }
            return result_str.substr(0,result_str.size() - 1); 
        }
    }
    string GenSection(int n) {
        int sec_hundred = 0;
        int sec_20 = 0;
        int sec_10 = 0;
        int sec_0 = 0;
        sec_hundred = n / 100;
        sec_20 = n % 100;

        string rt = "";
        // hundred
        if (sec_hundred != 0) {
            rt = rt + k20[sec_hundred - 1] + " Hundred ";
        }
        // under hundred
        if (sec_20 == 0) {
            return rt.substr(0,rt.size() - 1);
        } else if (sec_20 < 20) {
            rt = rt + k20[sec_20 - 1];
            return rt;
        } else {
            sec_10 = sec_20 / 10;
            sec_0 = sec_20 % 10;
            if (sec_0 == 0) {
                rt = rt + k100[sec_10 - 2];
            } else {
                rt = rt + k100[sec_10 - 2] + " " + k20[sec_0 - 1];
            }
            return rt;
            
        }
    }
public:
    const static char* k20[];
    const static char* k100[];
    const static char* k_Thousands[];
};

const char* Solution::k_Thousands[] = {"", "Thousand", "Million", "Billion"};
const char* Solution::k100[] = {"Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"};
const char* Solution::k20[] =  {"One", "Two", "Three", "Four","Five","Six","Seven","Eight","Nine","Ten", "Eleven","Twelve","Thirteen","Fourteen","Fifteen","Sixteen","Seventeen","Eighteen","Nineteen"};