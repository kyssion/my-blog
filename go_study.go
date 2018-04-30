package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	t := time.Now().UnixNano()
	for i := 10000; i < 22222; i++ {
		ddd(2, i)
	}
	i := float64(time.Now().UnixNano()-t) / (1000000 * 1000)
	fmt.Println(i)
}

func RandInt(min, max int) int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min) + min
}
func ddd(k int, n int) int {
	// write your code here
	sum := 0
	for i := 0; i <= n; i++ {
		num := i
		for num/10 != 0 {
			if num%10 == k {
				sum++
			}
			num = num / 10
		}
		if num == k {
			sum = sum + 1
		}

	}
	return sum
}
