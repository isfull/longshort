package main

import (
	"testing"
)

func TestFib(t *testing.T) {
	var suits = []struct {
		input  int
		output int
	}{
		{1, 1},
		{2, 1},
		{3, 2},
		{4, 3},
		{5, 5},
		{6, 8},
		{7, 13},
	}
	for key, tt := range suits {
		rt := Fib(tt.input)
		if rt != tt.output {
			t.Errorf("Fib(%d) = %d; expected %d (key:%d)", tt.input, rt, tt.output, key)
		}
	}
}

func BenchmarkFib(b *testing.B) {
	b.ReportAllocs()
	for n := 0; n < b.N; n++ {
		Fib(10)
	}
}