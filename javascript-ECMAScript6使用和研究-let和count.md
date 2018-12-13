### 一.let关键字  

#### 特性

##### (1)let关键字的闭包特性

> 列子一

```javascript
for(let i = 0;i<10;i++){
    global.setTimeout(function(){
        console.log("使用let"+i);
    },10*i);
}
// console.log(i);//ReferenceError这里报错
for(var a =0;a<10;a++){
    global.setTimeout(function(){
        console.log("使用var"+a);
    },0);
}
console.log("输出的结果是var的i:"+a);
```

- 输出:

```shell
输出的结果是var的i:10
使用let0
使用var10
使用var10
使用var10
使用var10
使用var10
使用var10
使用var10
使用var10
使用var10
使用var10
使用let1
使用let2
使用let3
使用let4
使用let5
使用let6
使用let7
使用let8
使用let9 
```

这个例子可以体现给出let具有的以下几个特性

1. 自闭包性:从使用var和使用let输出的差异性可以看出来,for循环(或者while循环)使用let的时候值就是自己循环时候的值而不是最终值

2. 块级作用于独占性:let只有在自己的作用于才有效,上面的ReferenceError报错可以体现出来,注意:for循环中设置变量的时候也是一个单独的作用域(有坑点见下面的例子)

> 例子二

```javascript
//for循环1
for(let i = 0;i<10;i++){
    global.setTimeout(function(){
        console.log("第一个for循环:"+i);
    },100);
}
//for循环2
for(let i = 0;i<10;i++){
    let i=1;
    global.setTimeout(function(){
        console.log("第二个for循环:"+i);
    },200);
    i++;
}
```

- 输出

```javascript
第一个for循环:0
第一个for循环:1
第一个for循环:2
第一个for循环:3
第一个for循环:4
第一个for循环:5
第一个for循环:6
第一个for循环:7
第一个for循环:8
第一个for循环:9
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
第二个for循环:2
```

- 第二个for循环只输出 2 是因为 let虽然提供了闭包的特性但是没有在本质上改变js的特性,是有循环2在到达时间的时候候读取的是自己块级作用域中的let元素的值

> 例子三

```javascript
//变量提升使用 var 的情况
console.log(foo); // 输出undefined
var foo = 2;
//变量提升使用 let 的情况
console.log(bar); // 报错ReferenceError
let bar = 2;
var ddd=3234;
let ddd=123;//SyntaxError 只能有一个参数let和var 其实在一定程度上是相同的
console.log(ddd);
```

- 这个例子可以体现给出let的以下几个特性:

1. let和var不同:let使用必须先进行声明否则会报错,var会输出underfind

1. let和var不同:let不允许和var或者let变量在相同的作用域下同名

> 例子四**暂时性死区**

```javascript
let i=123;
{
    let i=222;
    console.log(i);
}
```

- 输出

```javascript
222
```

- 这个例子可以体现给出let的以下特性:let属性区域性独立,外部不会影响到内部,大多数变成语言都这个特性

```javascript
if (true) {
    // TDZ开始
    tmp = 'abc'; // ReferenceError
    console.log(tmp); // ReferenceError
    let tmp; // TDZ结束
    console.log(tmp); // undefined
    tmp = 123;
    console.log(tmp); // 123
}
function bar(x = y, y = 2) {
    return [x, y];
}
bar(); // 报错
```
这个例子可以体现给出let的以下特性:TDZ

1. 在变量声明前都会不能使用

1. 只要出现生命前使用了变量都会出现TDZ错误

> 坑点记录

```javascript
var tmp = new Date();
function f() {
    console.log(tmp);
    if (false) {
        var tmp = 'hello world';
    }
}
f(); // undefined 因为变量提升的问题所以var是可以判断块级作用域的
var s = 'hello';
for (var i = 0; i < s.length; i++) {
  console.log(s[i]);
}
console.log(i); // 5 使用var会将for循环中的属性暴露在全剧中
```

### 二.const关键字

这个关键字的左右就是常量,但是他是锁定变量的地址的,其余的和let相同

- 注意:因为是锁定地址的所以需要进行对象的锁定是不安全的(对象中也有指向地址的东东)

如果要实现锁对象那么就使用

```javascript
const foo = Object.freeze({});
// 常规模式时，下面一行不起作用；
// 严格模式时，该行会报错
foo.prop = 123;
```




