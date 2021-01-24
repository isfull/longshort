package main

import (
	"fmt"
	"strconv"
)


func main() {
	fmt.Println("Hello, World!")
	a := Fib(7)
	fmt.Println(strconv.Itoa(a))
}
