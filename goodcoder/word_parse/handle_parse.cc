#include "handle_parse.h"

#include <stdio.h>
#include <stdint.h>

#include "toft/base/string/number.h"
#include "toft/base/string/algorithm.h"

namespace parse {
    // int
    bool parse(const std::string& str, int* result) {
        bool ret = false;
        ret = toft::StringToNumber(str.c_str(), result);
        return ret;
    }
    // char*
    bool parse(const std::string& str, char* result) {
        strcpy(result, str.c_str());
        return true;
    }
    // float
    bool parse(const std::string& str, float* result) {
        bool ret = false;
        ret = toft::StringToNumber(str, result);
        return ret;
    }
    // array
    template<typename T>
    bool parse(const std::string& str, std::vector<T>* result, int num) {
        // split-> num:item1,item2,item3
        std::vector<std::string> v_num_val;
        toft::SplitString(str, ":", &v_num_val);
        if (v_num_val.size() != 2) {
            return false;
        } else {
            int size = 0;
            if (!parse(v_num_val[0], &size)) {
                return false;
            } else {
                // split-> item1,item2,item3
                std::vector<std::string> v_val;
                toft::SplitString(v_num_val[1], ",", &v_val);
                int real_size = static_cast<int>(v_val.size());
                if (real_size != size || size != num) {
                    return false;
                } else {
                    for (int i = 0; i < size; ++i) {
                        T val;
                        if (!parse(v_val, &val)) {
                            return false;
                        } else {
                            result->push_back(val);
                        }
                    }
                    return true;
                }
            }
        }
    }
}