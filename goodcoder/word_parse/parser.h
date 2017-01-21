// Copyright 2017 Baidu Inc. All Rights Reserved.
// Author: yue song (songyue02@baidu.com)
//
// <注意：上面空一行。此处开始描述文件功能>

#ifndef  __PARSER_H_
#define  __PARSER_H_

#include <stdio.h>
#include <iostream>
#include <vector>
#include <string>

#include "toft/base/string/number.h"
#include "toft/base/string/algorithm.h"

#include "handle_parse.h"
#include "user.h"

// http://www.jianshu.com/p/594985b23a01

#define DISALLOW_COPY_AND_ASSIGN(TypeName) \
    TypeName(const TypeName&); \
    TypeName& operator=(const TypeName&)

namespace parse
{
    class Parser
    {
    
    public:
        int ParseLine(const char* line, int column_num) 
        {
            v_fileds_.clear();

            std::string trim_str = toft::StringTrimRight(line);
            toft::SplitString(trim_str, "\t", &v_fileds_);
            int fildes_size = static_cast<int>(v_fileds_.size());
            if (fildes_size != column_num) {
                return false;
            } else {
                return true;
            }
        };

        template<typename T>
        bool GetColumn(int index, T* result) {
            bool ret = false;
            int column_num = static_cast<int>(v_fileds_.size());
            if (index < column_num) {
                ret = parse(v_fileds_[index], result);
            } else {
                ret = true;
            }
            return ret;
        }
        template<typename T>
        bool GetArrayColumn(int index, T* result, int size) {
            bool ret = false;
            int column_num = static_cast<int>(v_fileds_.size());
            if (index < column_num) {
                ret = parse(v_fileds_[index], result, size);
            } else {
                ret = true;
            }
            return ret;
        }
    private:
        std::vector<std::string> v_fileds_;
        DISALLOW_COPY_AND_ASSIGN(Parser);
    };

} // namespace parse
#endif // __PARSER_H_