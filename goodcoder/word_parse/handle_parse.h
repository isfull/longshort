#ifndef  __HANDLE_PARSE_H_
#define  __HANDLE_PARSE_H_

#include <vector>
#include <string>

namespace parse {
    // int
    bool parse(const std::string& str, int* result);
    // char*
    bool parse(const std::string& str, char* result);
    // float
    bool parse(const std::string& str, float* result);
    // array num:item1,item2,item3
    template<typename T>
    bool parse(const std::string& str, std::vector<T>* result, int num);
}
#endif // __HANDLE_PARSE_H_