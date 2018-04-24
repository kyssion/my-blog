package main

import (
	"fmt"
	"math/rand"
	"time"
)

func main() {
	r := RandInt(10, 13) //产生范围内随机数，防止编译器优化
	fmt.Println(r, time.Now().UnixNano())
	t := time.Now().UnixNano()
	sum := 0
	for i := 0; i <= 40000+r; i++ {
		for j := 0; j <= 40000; j++ {
			sum = sum + i*j
		}
	}
	i := float64(time.Now().UnixNano()-t) / (1000000 * 1000)
	fmt.Println(sum)
	fmt.Println(i)
}

func RandInt(min, max int) int {
	rand.Seed(time.Now().UnixNano())
	return rand.Intn(max-min) + min
}
