#include "parser.h"
#include <stdio.h>
#include <iostream>

using namespace parse;

std::string test1 = "abcdef\t123\t3.9\t456\tyiyg\n";
std::string test2 = "abcdef\t3:4,5,6\t3.9\t456\tyiyg\t4:1,2,3,4\n";
std::string test3 = "abcdef\t123\t3.9\t456\tyiyg\t22 33 44\n";



int main()
{
    Parser test;
    test.ParseLine(test1.c_str(), 5);
    int x;
    test.GetColumn(3, &x);
    char* y = new char[20];
    test.GetColumn(4, y);
    float z;
    test.GetColumn(2, &z);
    printf("%d, %s, %f\n", x, y, z);


    test.ParseLine(test3.c_str(), 6);

    MyStruct my_struct;
    test.GetColumn(5, &my_struct);
    printf("%d %d %d\n", my_struct.a, my_struct.b, my_struct.c);
    return 0;
}