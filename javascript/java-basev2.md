# js 对象

1. 声明一个对象

```javascript
let person= {
    name :"name",
    age:29,
    sayName: function (){
        console.log(this.name)
    }
}
```

2. 针对属性类型修改

js 修改这些属性可以使用js的 Object。defineProperty方法进行修改

```javascript
let persion = {}
// 三个属性 -> 定义一个属性
Object.defineProperties(persion,"name", {
    writable:false, // 是否可以被修改
    enumerable: false, // 是否可以被迭代
    configurable: false, // 是否可以delete删除并且重新定义
    value : 12,
    get(){
        return this.name
    },
    set(newValue){
        this.name = newValue
    }
    }
)
// 支持两个属性 - 可以同时创建多个变量
Object.defineProperties(persion, {
        name: {
            writable: false, // 是否可以被修改
            enumerable: false, // 是否可以被迭代
            configurable: false, // 是否可以delete删除并且重新定义
            value: 12,
            get() {
                return this.name
            },
            set(newValue) {
                this.name = newValue
            }
        }
    }
)
```
3. 针对属性类型的读取

```javascript
Object.getOwnPropertyDescriptor(对象, "变量名称")// 返回属性信息枚举
Object.getOwnPropertyDescriptors()// 返回每一个数据行的配置信息
```

4. object 对象属性合并

```javascript
Object.assign({},{}) //  后一个合并到前一个中
```
5. es6 对象声明简写方法

- 属性名称复写

```javascript
let name = "name"
let p = {
    name:name
}

// 等价于

let p={
    name
}

// 函数嵌套保留

function setName(name){
    return {
        name
    }
}
let p = setName("name")
console.log(p.name)// 输出name ， 这个name 是保留的
```

- 字符串（动态）属性直接赋值

```javascript
let name = 'name'
let p ={}
p[name] = name

// 可以写成
let p={
    [name]:"name"
}

// 还支持函数写入

function createName(name){
    return "this_"+name
}

let p = {
    [createName("tttt")]:"name"
}
```

- 快速函数命名
```javascript
let name = "thisName"
let p = {
    name_ :"ffff",
    sayName(name){
        return this.name_
    },
    get name(){ // 获取属性
        return this.name_ 
    },
    set name(name){ // 设置属性
        this.name_ = name
    },
    [name](){ // 自定义方法名称
        
    }
}
```

- 对象解构

```javascript
let p ={
    name:"fsdfs",
    age :16,
    fuc :{
        ppp:"123",
        zzz:{
            qqq:"ffff"
        }
    }
}

let {name:ppp,age:zzz,fuc:{ppp:qqq},fuc:{zzz:{qqq:yyy}}}=p
let {name,age} = p // 简写方法

function item(p,{name,age},z){ //还支持函数
    console.log(name, age)
}
function item2(p,{name:ffff,age:tttt},z){ // 还支持函数
    console.log(ffff, tttt)
}
let i = {
    name:"fff",
    age : 123
}
item2(123,i,123)
```

- 原型链 继承 - 忽略

- class 类

1. 类声明

```javascript
// 两种方法
class Person{}
const Item = class{}
```

> 类一般都是初始化时候定义的 ， 不想函数可以在任意的位置定义，所以类需要在一开始就定义好

2. 类构成

```javascript
class Foo{
    name_ // 原型链中增加变量
    age
    constructor(){
        this.age = 12
        this.arr = [1,2,3,4]
    }
    get name(){
        return this.name_
    }
    set name(name){
        this.name_ = name
    }
    zzz(){ // 相当于定义在原型链中
        
    }
    
    *[Symbol.iterator](){ // 对象直接支持迭代
        yield *this.arr.entries
    }
    [Symbol.iterator](){ // 对象直接支持返回迭代器
        return this.arr.entries()
    }
    
}
    
    static myQux(){ // 静态类可以直接使用类名调用
}
```

特殊地方， 获取表达式名称

```javascript
let Person = class Item{
    identify(){
        console.log(Person.name,Item.name) // 可以打印出类的内部名称
    }
}
let p = new Person()
p.identify()
console.log(Person.name) // 外部只能获取表层类的信息

```

js 类其实是一个特殊函数对象是绑定构造函数

```javascript
class Person{
    name
    construction(use){
        if(use===true){
            return {
                name:"p2"
            }
        }
        this.name = "p1"
    }
}

let p1 = new Person()
let p2 = new Person(true)
console.log(p1)
console.log(p2)
console.log(p1 instanceof Person)
console.log(p2 instanceof Person)
// 输出：Person { name: 'p1' }
// { name: 'p2' }
// true
// false
// -- 这种方法也可以创建
let p3 = p1.construction()
console.log(p3)
console.log(p3 instanceof Person)

console.log(typeof Person)// 类是一种特殊的函数

// class 底层也是函数 ， 所以原型链这套class 也可以用
console.log(Person == Person.prototype.constructor) // true

// -- 立即调用

let p = new class Foo{
    constructor(x){
        console.log(x)
    }
}('ccc')

```

-- 继承？ 使用组合 忽略

# js 函数

js 的函数现在和一些基本语言的函数没啥区别 ， 主要要注意的地方那个

0. 箭头函数

箭头函数需要和this 关键字一起说 
```javascript

let o = {
    color : "red"
}

let p = {
    color : "red"
}

global.color = "blue"

function item(){
    console.log(this.color)
}

let pp = ()=>{
    console.log(this.color)
}


item() // blue
o.item = item;
o.item() // red

pp() // underfind
p.pp = pp
p.pp() // underfind

```

> 没有箭头函数的时候 this是运行时确定的， 如果有箭头函数， this是声明时候定义的

1. 函数内部的特殊对象

```javascript

// 1. arguments - 一个数组 ， 传入函数的所有属性
function factorial(num){ // 递归相加
    if (arguments[0]<=1){ // 取值
        
        return 1
        
    }else{
        
        return arguments[0]+arguments.callee(arguments[0]-1)  // 取函数
    
    }
}
```

> js支持这个的原因是js支持函数重命名 ， 重命名的函数递归会有问题 ， 所以一般内部使用这个方法

2. new target => 这个用来检测当前函数是不是使用new 方法创建对象了
```javascript
function Test(){
    if (!new.target){
        console.log("start new")
    }
    console.log("start end")
}

let a = new Test()
Test()
```

3. js 函数 apply call bind 区别

call 、bind 、 apply 这三个函数的第一个参数都是 this 的指向对象，第二个参数差别就来了：
call 的参数是直接放进去的，第二第三第 n 个参数全都用逗号分隔，直接放到后面 obj.myFun.call(db,'成都', ... ,'string' )。
apply 的所有参数都必须放在一个数组里面传进去 obj.myFun.apply(db,['成都', ..., 'string' ])。
bind 除了返回是函数以外，它 的参数和 call 一样。

4. 函数使用的时候需要特殊注意的地方

```javascript
// js 不建议使用这种方法创建动态函数，而是推荐使用函数表达式来创建
let sayHello;
let boolItem = 12>13;
if (boolItem){
    function sayHell0(){
        console.log("ffff")
    }
}else{
    function sayHell0(){
        console.log("xxxx")
    }
}
if (boolItem){
   sayHell0 = function (){
        console.log("ffff")
    }
}else{
    sayHell0 = function (){
        console.log("xxxx")
    }
}
```
6. js尾调用优化例子-菲薄纳妾数列

```javascript
function sum(a){
    if(a<2){
        return a;
    }
    return sum(a-1)+sum(a-2)
}
```

7. 匿名函数的作用域范围

1. 匿名函数会继承父函数所有可以访问的变量（作用域）
2. 匿名函数是永远没有办法访问到外部函数的this， this 一定是声明时候确认的



```javascript
function create(){
    return ()=>{
        console.log(this.name)
    }
}

let a = {
    name:"ffff"
}
// a.say = function (){
//     console.log(this.name)
// }

a.say = create()

a.say()
```

红包书 10.16 再支持

