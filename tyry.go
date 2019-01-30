package main

func fib(n int64) int64 {
	if n <= 2 {
		return 1
	}
	return fib(n-1) + fib(n-2)
}

func main() {
	println(fib(45))
}
