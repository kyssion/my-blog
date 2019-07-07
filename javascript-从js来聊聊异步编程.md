 # 从js来聊聊异步编程

## 文章的目的

揭开go的 gorouter,c#的 async/await等 使用同步的写法写异步代码的神秘面纱 , 证明其本质就是一个语法糖

## 为什么使用js来讲异步编程

因为js可以通过编程语言自己的语法特性,实现原生语言不提供的同步化异步编程

## js异步最底层写法promise

```javascript
const promise = new Promise(function(resolve, reject) {
  xxxxx.异步IO操作((res)=>{
      if(res成功){
          resolve(res)
      }else{
          reject(res)
      }
  })
});
```



promise出入的回调函数有一定的要求

- resolve函数的作用是，将Promise对象的状态从“未完成”变为“成功”（即从 pending 变为 resolved），在异步操作成功时调用，并将异步操作的结果，作为参数传递出去

- reject函数的作用是，将Promise对象的状态从“未完成”变为“失败”（即从 pending 变为 rejected），在异步操作失败时调用，并将异步操作报出的错误，作为参数传递出去。

> Promise实例生成以后，可以用then方法分别指定resolved状态和rejected状态的回调函数(处理返回的结果)。


```javascript
promise.then(function(value) {
  // success
}, function(error) {
  // failure
});
```

> 引申-注意: promise对象在js中非常特殊,比如下面的例子

```JavaScript
const p1 = new Promise(function (resolve, reject) {
  setTimeout(() => reject(new Error('fail')), 3000)
})

const p2 = new Promise(function (resolve, reject) {
  setTimeout(() => resolve(p1), 1000)
})
p2
  .then(result => console.log(result))
  .catch(error => console.log(error))
```

> 这个的结果是failt 因为 p2中resolve返回一个promise对象,这个操作将会导致p2的状态升级成p1的状态(标准)

### promise的then链式写法

promise then方法将会返回一个promise,所以js支持链式异步

```javascript
var getJSON = function (url, callback) {
    var promise = new Promise(function (resolve, reject) {
        var client = new XMLHttpRequest();
        client.open("GET", url);
        client.onreadystatechange = handler;//readyState属性的值由一个值变为另一个值时，都会触发readystatechange事件
        client.responseType = "json";
        client.setRequestHeader("Accept", "application/json");
        client.send();

        function handler() {
            if (this.readyState !== 4) {
                return;
            }
            if (this.status === 200) {
                callback(this.response);
                resolve(this.response);
            } else {
                reject(new Error(this.statusText))
            }
        };
    });
    return promise;
};
getJSON("./e2e-tests/get.json", function (resp) {
    console.log("get:" + resp.name);
}).then(function (json) {
    getJSON("./e2e-tests/get2.json", function (resp) {
        console.log("get2:" + resp.name);
    })
}).catch(function (error) {
    console.log("error1：" + error);
});
```

### promise 异常捕获

```javascript
p.then((val) => console.log('fulfilled:', val))
  .catch((err) => console.log('rejected', err));

// 等同于
p.then((val) => console.log('fulfilled:', val))
  .then(null, (err) => console.log("rejected:", err));
```

这个异常捕获和java相同,捕获在eventLoop中产生的异常

> 注意一点这个异常和java的try catch是不同的,如果产生了异常将不会在主线程中显示出来

### promise的finally

这个和java的异常体系相同,finally 无关状态,最后都会执行

```javascript
Promise.resolve(2).finally(() => {})
```

### 更加方便的编写异步使用Promise.resolve(xxx)

```JavaScript
Promise.resolve('foo')
// 等价于
new Promise(resolve => resolve('foo'))
```

> 注意: promise异步化结果只能在回调函数中获得,如果异步的操作太多,将会调至调用链路过长

## 如何解决js的promise异步编程的问题?

promise 写法有什么问题? ---- 调用链路过长

比如: 使用promise 实现 异步ajax请求
```javascript
var getJSON = function (url, callback) {
    var promise = new Promise(function (resolve, reject) {
        var client = new XMLHttpRequest();
        client.open("GET", url);
        client.onreadystatechange = handler;//readyState属性的值由一个值变为另一个值时，都会触发readystatechange事件
        client.responseType = "json";
        client.setRequestHeader("Accept", "application/json");
        client.send();
        function handler() {
            if (this.readyState !== 4) {
                return;
            }
            if (this.status === 200) {
                callback(this.response);
                resolve(this.response);
            } else {
                reject(new Error(this.statusText))
            }
        };
    });
    return promise;
};
getJSON("./e2e-tests/get.json", function (resp) {
    console.log("get:" + resp.name);
}).then(function (json) {
    getJSON("./e2e-tests/get2.json", function (resp) {
        console.log("get2:" + resp.name);
    })
}).catch(function (error) {
    console.log("error1：" + error);
});
```

调用链太长,不停的promise调用

## js如何解决回调地狱---同步方法写异步

### 解决方法 使用js的协程 --Generator

> generator:js的特殊语法,使用yield 关键字将函数分块了,然后可以使用遍历器手动控制执行

例子:

```javascript
function * gen(){
    let a= 123;
    let b = yield a;
    let c = yield a+b;
    return a+b+c;
}

let start = gen();

console.log(start.next());
console.log(start.next(2));
console.log(start.next(3));
```

> 本质上是函数分片

js在每次yield的时候都会获得当前位置的表达式,然后再手动的嵌入就可以实现分片控制的效果了

### 怎么用generator实现异步化呢 -- yield配合promise实现异步

看一下这个方法

```javascript
function* asyncFn(value) {
    let a = yield promiseOne(value);
    let b = yield promiseTwo(a);
    return a + b;
}
```

想让他能异步执行,只要能让前一个promise的结果是下一个promise的输入就可以了

这里有两种写法

#### 写法一

递归方程: f(最终结果) = f(到目前的结果)+f(接下来执行的结果)

```javascript
function promiseOne(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
function promiseTwo(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
function* asyncFn(value) {
    let a = yield promiseOne(value);
    let b = yield promiseTwo(a);
    return a + b;
}
function runAsync(fn,value) {
    let item = fn.next(value);
    return new Promise((res, rej) => {
        if (!item.done) {
            if (item.value instanceof Promise) {
                item.value.then((re)=>{
                    runAsync(fn,re).then(res);
                })
            } else {
                runAsync(fn,fn.valueOf()).then(res);
            }
        } else {
            res(item.value);//这个res方法其实是所有人的res方法
        }
    })
}
runAsync(asyncFn(12)).then(res=>{
    console.log(res);
});
```

> co 工具包的写法

```javascript
function run (gen) {
  gen = gen()
  return next(gen.next())
  function next ({done, value}) {
    return new Promise(resolve => {
     if (done) { // finish
       resolve(value)
     } else { // not yet
       value.then(data => {
         next(gen.next(data)).then(resolve)
       })
     }
   })
  }
}
function getRandom () {
  return new Promise(resolve => {
    setTimeout(_ => resolve(Math.random() * 10 | 0), 1000)
  })
}
function * main () {
  let num1 = yield getRandom()
  let num2 = yield getRandom()
 
  return num1 + num2
}
run(main).then(data => {
  console.log(`got data: ${data}`);
})
```

#### 写法二

递归方程 f(最终结果) = f(之前所有的结果)+f(最后一步的结果)

```javascript
//同步方式写异步
function asyncRun(resf, fn, value) {
    let a = fn(value);
    go(value);
    function go(value) {
        let next = a.next(value);
        if (!next.done) {
            if (next.value instanceof Promise) {
                next.value.then((res) => {
                    go(res);
                });
            } else {
                return go(next.value);
            }
        } else {
            resf(next.value);
        }
    }
}
function* asyncFn(value) {
    let a = yield promiseOne(value);
    let b = yield promiseTwo(a);
    return a + b;
}
function show(item) {
    console.log(item)
}
asyncRun(show, asyncFn, 12);
function promiseOne(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
function promiseTwo(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
```

## 更简单的方法 async/await

上面复杂的代码如果变成async/await要怎么做呢

很简单

```javascript
// function* asyncFn(value) {
//     let a = yield promiseOne(value);
//     let b = yield promiseTwo(a);
//     return a + b;
// }
function promiseOne(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
function promiseTwo(xxx) {
    return new Promise((res, rej) => {
        res(xxx + 1);
    })
}
async function asyncFn(value) {
    let a = await promiseOne(value);
    let b = await promiseTwo(a);
    return a + b;
}
asyncFn(12).then((res)=>{
    console.log(res)
});
```

通过上面的例子,我们可以发现其实async/await本质上其实是 generator的一个语法糖

await就是yield , async 的作用就是将函数编程语法糖

如果背的话很简答两条规则:

1. await后面必须是promise函数
2. async 标记过得函数执行后返回的promise

通过这种方法就可以简单的实现异步了