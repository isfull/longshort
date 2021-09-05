
cc_library(
    name = "codelib",
    #srcs = glob(["*.cc","*.h"]),
    srcs = ["1.two-sum.cpp","1482.cpp"],
    deps = [
    ],
    copts = [
        "-std=c++11",
    ],
    linkopts = [
        "-ldl",
    ],
)

cc_test(
    name = "leetcode_test",
    srcs = ["leetcode_test.cc","two_sum.h","1482.h"],
    
    visibility = ["//visibility:public"],
    deps = [
        #":codelib",
        "@com_google_googletest//:gtest_main",
    ],
)