#ifndef  __USER_H_
#define  __USER_H_
#include <stdio.h>
#include <string>
namespace parse
{
    //example
    typedef struct MyStruct
    {
        int a;
        int b;
        int c;
    } MyStruct;

    bool parse(const std::string& str, MyStruct* result);
}
#endif // __USER_H_