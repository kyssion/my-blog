# 异步编程-js实现

## promise异步

```javascript
const promise = new Promise(function(resolve, reject) {
  // ... some code
  if (/* 异步操作成功 */){
    resolve(value);
  } else {
    reject(error);
  }
});
```

promise出入的回调函数有一定的要求

- resolve函数的作用是，将Promise对象的状态从“未完成”变为“成功”（即从 pending 变为 resolved），在异步操作成功时调用，并将异步操作的结果，作为参数传递出去

- reject函数的作用是，将Promise对象的状态从“未完成”变为“失败”（即从 pending 变为 rejected），在异步操作失败时调用，并将异步操作报出的错误，作为参数传递出去。

> Promise实例生成以后，可以用then方法分别指定resolved状态和rejected状态的回调函数。


```javascript
promise.then(function(value) {
  // success
}, function(error) {
  // failure
});
```

> 注意: promise对象在js中非常特殊,比如下面的例子

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

### promise的then 链式写法

promise then方法将会返回一个promise,所以js支持链式异步

```javascript
function getJson(path){
    return new Promise((r,v)=>{
        r("123123");
    })
}
getJson("/post/1.json").then(function(post) {
    return getJson(post.commentURL);
}).then(function funcA(comments) {
    console.log("resolved: ", comments);
}, function funcB(err){
    console.log("rejected: ", err);
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

> 注意: 