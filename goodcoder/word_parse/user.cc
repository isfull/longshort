#include "user.h"
namespace parse
{
    //对于用户类型，请自定义解析实现
    bool parse(const std::string& str, MyStruct* result)
    {
        sscanf(str.c_str(), "%d %d %d", &result->a, &result->b, &result->c);
        return true;
    } 
}