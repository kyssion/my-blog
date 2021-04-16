# 问题描述

解决go请求流量控制的问题，实现对于将并发控制在一定的范围内。
我们遇到的场景：拉取数据时，数据源可能会有一定的QPS限制，防止访问失败，在请求时需要保证请求不超过接口限制。

方案调研

方案|优缺点
---|---
Waiting Group + Channel | 控制并发数，但不控制QPS
Go Ticker | 简单，不能支持不均匀
Go 官方 RateLimiter | 功能强大，使用较为复杂
Uber RateLimiter | 使用方便，功能相对少一些

# 1. Waiting Group + Channel

```golang
package main

import (
   "fmt"
   "math/rand"
   "sync"
   "time"
)

func main() {
   var wg sync.WaitGroup
   ch := make(chan struct{}, 2)
   //
   // ch <- struct{}{}
   for i := 0; i < 10; i++{
      wg.Add(1)
      go func(index int) {
         defer wg.Done()
         //放在里面可能会有内存泄露
         ch <- struct{}{}

         // do something ...
         fmt.Println("current", index, time.Now())
         time.Sleep(time.Millisecond * time.Duration(rand.Intn(5000)))

         <- ch
      }(i)
   }
   
   wg.Wait()
}

```

保证任意时刻最大的并发数不会超过channel的容量，但不能保证QPS

