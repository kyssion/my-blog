> 变量结构赋值在python中其实是非常常见的技术,这里整理一下ES6的相关变量结构赋值

### 一.针对数组的解构方法

#### (1)使用简单的实例

```javascript
//一般表示
let [foo, [[bar], baz]] = [1, [[2], 3]];
foo // 1
bar // 2
baz // 3
//缺省表示
let [ , , third] = ["foo", "bar", "baz"];
third // "baz"
//空位表示
let [x, , y] = [1, 2, 3];
x // 1
y // 3
//嵌套表示
let [head, ...tail] = [1, 2, 3, 4];
head // 1
tail // [2, 3, 4]
//特殊情况
let [x, y, ...z] = ['a'];
x // "a"
y // undefined
z // []
```

输出结果：

```javascript
let [a, [b], d] = [1, [2, 3], 4];
a // 1
b // 2
d // 4
```

- 引申：还有一中特殊的情况是实现了 Iterator 接口 这个之后再进行讨论

> 使用默认值

```javascript
let [foo = true] = [];
foo // true
 
let [x, y = 'b'] = ['a']; // x='a', y='b'
let [x, y = 'b'] = ['a', undefined]; // x='a', y='b'
```

- 注意：ES6 内部使用严格相等运算符（===），判断一个位置是否有值。所以，只有当一个数组成员严格等于undefined，默认值才会生效。

```javascript
let [x = 1] = [undefined];
x // 1
 
let [x = 1] = [null];
x // null
```

#### (2)针对对象

> 例子

```javascript
let { foo: baz } = { foo: 'aaa', bar: 'bbb' };
baz // "aaa"
 
let obj = { first: 'hello', last: 'world' };
let { first: f, last: l } = obj;
f // 'hello'
l // 'world'
```

> 输出

```javascript
let { foo, bar } = { foo: "aaa", bar: "bbb" };
foo // "aaa"
bar // "bbb"
```

- 总体上就是这两种形式,其实也是将一些变量添加到空间中而已,只是使用对象需要指定映射关系罢了,深入理解见下

```javascript
const node = {
  loc: {
    start: {
      line: 1,
      column: 5
    }
  }
};
 
let { loc, loc: { start }, loc: { start: { line }} } = node;   拆开依次赋值 line // 1
loc  // Object {start: Object}
start // Object {line: 1, column: 5}
```

- 对象的组合赋值可以引用外部参数的

```javascript
let obj = {};
let arr = [];
 
({ foo: obj.prop, bar: arr[0] } = { foo: 123, bar: true });
 
obj // {prop:123}
arr // [true]
```

- 也可以使用默认值,默认值生效的条件是，对象的属性值严格等于undefined。

```javascript
var {x = 3} = {};
x // 3
var {x, y = 5} = {x: 1};
x // 1
y // 5
var {x: y = 3} = {};
y // 3
var {x: y = 3} = {x: 5};
y // 5
var { message: msg = 'Something went wrong' } = {};
msg // "Something went wrong"
```

```javascript
var {x = 3} = {x: undefined};
x // 3
var {x = 3} = {x: null};
x // null
```

#### (3)字符串的解构赋值

```javascript
const [a, b, c, d, e] = 'hello';
a // "h"
b // "e"
c // "l"
d // "l"
e // "o"
```

- 还支持length

```javascript
let {length : len} = 'hello';
len // 5
```

#### (4)函数参数的解构赋值

- 函数的参数也可以使用解构赋值。

```javascript
function add([x, y]){
  return x + y;
}
add([1, 2]); // 3
```

- 函数参数的解构也可以使用默认值。

```javascript
function move({x = 0, y = 0} = {}) {
  return [x, y];
}
move({x: 3, y: 8}); // [3, 8]
move({x: 3}); // [3, 0]
move({}); // [0, 0]
move(); // [0, 0]
```

- 上面代码是为函数move的参数指定默认值，而不是为变量x和y指定默认值，所以会得到与前一种写法不同的结果。

```javascript
function move({x, y} = { x: 0, y: 0 }) {
  return [x, y];
}
move({x: 3, y: 8}); // [3, 8]
move({x: 3}); // [3, undefined]
move({}); // [undefined, undefined]
move(); // [0, 0]
```

### 二.总结-用途

#### （1）交换变量的值

```javascript
let x = 1;
let y = 2;
[x, y] = [y, x];
```

- 上面代码交换变量x和y的值，这样的写法不仅简洁，而且易读，语义非常清晰。

#### （2）从函数返回多个值

- 函数只能返回一个值，如果要返回多个值，只能将它们放在数组或对象里返回。有了解构赋值，取出这些值就非常方便。

```javascript
// 返回一个数组
function example() {
  return [1, 2, 3];
}
let [a, b, c] = example();
// 返回一个对象
function example() {
  return {
    foo: 1,
    bar: 2
  };
}
let { foo, bar } = example();
```

#### （3）函数参数的定义

- 解构赋值可以方便地将一组参数与变量名对应起来。

```javascript
// 参数是一组有次序的值
function f([x, y, z]) { ... }
f([1, 2, 3]);
// 参数是一组无次序的值
function f({x, y, z}) { ... }
f({z: 3, y: 2, x: 1});
```

#### （4）提取 JSON 数据

- 解构赋值对提取 JSON 对象中的数据，尤其有用。

```javascript
let jsonData = {
  id: 42,
  status: "OK",
  data: [867, 5309]
};
let { id, status, data: number } = jsonData;
console.log(id, status, number);
// 42, "OK", [867, 5309]
```

- 上面代码可以快速提取 JSON 数据的值。

#### （5）函数参数的默认值

- 指定参数的默认值，就避免了在函数体内部再写var foo = config.foo || ‘default foo’;这样的语句。

```javascript
jQuery.ajax = function (url, {
  async = true,
  beforeSend = function () {},
  cache = true,
  complete = function () {},
  crossDomain = false,
  global = true,
  // ... more config
}) {
  // ... do stuff
};
```

#### （6）遍历 Map 结构

- 任何部署了 Iterator 接口的对象，都可以用for…of循环遍历。Map 结构原生支持 Iterator 接口，配合变量的解构赋值，获取键名和键值就非常方便。

```javascript
const map = new Map();
map.set('first', 'hello');
map.set('second', 'world');
 
for (let [key, value] of map) {
  console.log(key + " is " + value);
}
// first is hello
// second is world
```

- 如果只想获取键名，或者只想获取键值，可以写成下面这样。

```javascript
// 获取键名
for (let [key] of map) {
  // ...
}
// 获取键值
for (let [,value] of map) {
  // ...
}
```

#### （7）输入模块的指定方法

- 加载模块时，往往需要指定输入哪些方法。解构赋值使得输入语句非常清晰。

```javascript
const { SourceMapConsumer, SourceNode } = require("source-map");
```