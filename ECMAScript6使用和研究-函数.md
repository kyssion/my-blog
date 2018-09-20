### ECMAScript6使用和研究-函数


```javascript
function log(x, y) {
  y = y || 'World';
  console.log(x, y);
}
 
log('Hello') // Hello World
log('Hello', 'China') // Hello China
log('Hello', '') // Hello World
```


注意:参数变量是默认声明的，所以不能用let或const再次声明。使用参数默认值时，函数不能有同名参数。

```javascript
function foo(x = 5) {
  let x = 1; // error
  const x = 2; // error
}
```

```javascript 
// 不报错
function foo(x, x, y) {
  // ...
}
 
// 报错
function foo(x, x, y = 1) {
  // ...
}
// SyntaxError: Duplicate parameter name not allowed in this context
```

注意:函数的表达式中可以添加任意的表达式

```javascript
let x = 99;
function foo(p = x + 1) {
  console.log(p);
}
 
foo() // 100
 
x = 100;
foo() // 101
```

```javascript
默认参数支持结构赋值

// 写法一
function m1({x = 0, y = 0} = {}) {
  return [x, y];
}
 
// 写法二
function m2({x, y} = { x: 0, y: 0 }) {
  return [x, y];
}
```


```javascript 
// 函数没有参数的情况
m1() // [0, 0]
m2() // [0, 0]
 
// x 和 y 都有值的情况
m1({x: 3, y: 8}) // [3, 8]
m2({x: 3, y: 8}) // [3, 8]
 
// x 有值，y 无值的情况
m1({x: 3}) // [3, 0]
m2({x: 3}) // [3, undefined]
 
// x 和 y 都无值的情况
m1({}) // [0, 0];
m2({}) // [undefined, undefined]
 
m1({z: 3}) // [0, 0]
m2({z: 3}) // [undefined, undefined]
```

默认参数可以使用underfind补位

```javascript
// 例一
function f(x = 1, y) {
  return [x, y];
}
 
f() // [1, undefined]
f(2) // [2, undefined])
f(, 1) // 报错
f(undefined, 1) // [1, 1]
 
// 例二
function f(x, y = 5, z) {
  return [x, y, z];
}
 
f() // [undefined, 5, undefined]
f(1) // [1, 5, undefined]
f(1, ,2) // 报错
f(1, undefined, 2) // [1, 5, 2]
```

函数参数和作用域的坑点

```javascript
var x = 1;
function foo(x, y = function() { x = 2; }) {
  var x = 3;
  y();
  console.log(x);
}
 
foo() // 3
x // 1
var x = 1;
function foo(x, y = function() { x = 2; }) {
  x = 3;
  y();
  console.log(x);
}
 
foo() // 2
x // 1
```

利用参数默认值，可以指定某一个参数不得省略，如果省略就抛出一个错误。

```javascript
function throwIfMissing() {
  throw new Error('Missing parameter');
}
 
function foo(mustBeProvided = throwIfMissing()) {
  return mustBeProvided;
}
 
foo()
// Error: Missing parameter
```

可以将参数默认值设为undefined，表明这个参数是可以省略的。

```javascript
function foo(x = 5, y = 6) {
  console.log(x, y);
}
 
foo(undefined, null)
// 5 null
```

ES6中函数的作用域同样满足相关的私有化的特性但是一定要记住,ES6在这方面和ES5的区别本质上是,Es6使用的是定义的位置而ES5使用给的运行的位置

```javascript

let foo = 'outer';
 
function bar(func = () => foo) {
  let foo = 'inner';
  console.log(func());
}
 
bar(); // outer
```

ES6使用默认参数还可以抛出异常

```javascript
function throwIfMissing() {
  throw new Error('Missing parameter');
}
 
function foo(mustBeProvided = throwIfMissing()) {
  return mustBeProvided;
}
 
foo()
// Error: Missing parameter
```

### ES6升级版箭头函数

```javascript
var f = v => v;
```

上面的箭头函数等同于

```javascript
var f = function(v) {
  return v;
};
```

如果箭头函数不需要参数或需要多个参数，就使用一个圆括号代表参数部分。

```javascript
var f = () => 5;
// 等同于
var f = function () { return 5 };
 
var sum = (num1, num2) => num1 + num2;
// 等同于
var sum = function(num1, num2) {
  return num1 + num2;
};
```

注意如果像直接返回对象需要在对象外面套上()

```javascript
let getTempItem = id => ({ id: id, name: "Temp" });
```

箭头函数可以与变量解构结合使用。

```javascript
const full = ({ first, last }) => first + ' ' + last;
 
// 等同于
function full(person) {
  return person.first + ' ' + person.last;
}
```

箭头函数有几个使用注意点。

1. 函数体内的this对象，就是定义时所在的对象，而不是使用时所在的对象。
2. 不可以当作构造函数，也就是说，不可以使用new命令，否则会抛出一个错误。
3. 不可以使用arguments对象，该对象在函数体内不存在。如果要用，可以用 rest 参数代替。
4. 不可以使用yield命令，因此箭头函数不能用作 Generator 函数。
5. this指向的固定化，并不是因为箭头函数内部有绑定this的机制，实际原因是箭头函数根本没有自己的this，导致内部的this就是外层代码块的this。正是因为它没有this，所以也就不能用作构造函数。相当一下面这种写法

```javascript
// ES6
function foo() {
  setTimeout(() => {
    console.log('id:', this.id);
  }, 100);
}
 
// ES5
function foo() {
  var _this = this;
 
  setTimeout(function () {
    console.log('id:', _this.id);
  }, 100);
}
```

除了this，以下三个变量在箭头函数之中也是不存在的，指向外层函数的对应变量：arguments、super、new.target。

### 双冒号运算符

箭头函数可以绑定this对象，大大减少了显式绑定this对象的写法（call、apply、bind）。但是，箭头函数并不适用于所有场合，所以现在有一个提案，提出了“函数绑定”（function bind）运算符，用来取代call、apply、bind调用。

函数绑定运算符是并排的两个冒号（::），双冒号左边是一个对象，右边是一个函数。该运算符会自动将左边的对象，作为上下文环境（即this对象），绑定到右边的函数上面。

```javascript
foo::bar;
// 等同于
bar.bind(foo);
 
foo::bar(...arguments);
// 等同于
bar.apply(foo, arguments);
 
const hasOwnProperty = Object.prototype.hasOwnProperty;
function hasOwn(obj, key) {
  return obj::hasOwnProperty(key);
}
```

如果双冒号左边为空，右边是一个对象的方法，则等于将该方法绑定在该对象上面。

```javascript
var method = obj::obj.foo;
// 等同于
var method = ::obj.foo;
 
let log = ::console.log;
// 等同于
var log = console.log.bind(console);


```
