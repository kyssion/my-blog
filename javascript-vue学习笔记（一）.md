考虑到要提高工作的效率，通过调查发现使用vue可以提高前端进行编写时候的效率，所以准备花费两天的时间进行vue的element框架的学习和使用

### 声明式渲染

其实这个很好理解就是指定了变量让框架自动的对相关的参数附上指定的值

```html
<div id="app">
  {{ message }}
</div>
<!--vue 可以对参数进行赋值 使用v-bind 标签-->
<div id="app-2">
  <span v-bind:title="message">
    鼠标悬停几秒钟查看此处动态绑定的提示信息！
  </span>
</div>
```

```javascript
var app = new Vue({
  el: '#app',
  data: {
    message: 'Hello Vue!'
  }
})

//使用v-bind 进行参数的绑定的时候和不使用没有太大的差别
var app2 = new Vue({
  el: '#app-2',
  data: {
    message: '页面加载于 ' + new Date().toLocaleString()
  }
})
```

### 条件与循环

vue 通过使用v-if v-for 标签实现了循环操作

```html
<div id="app-3">
  <p v-if="seen">现在你看到我了</p>
</div>
```

```javascript
var app3 = new Vue({
  el: '#app-3',
  data: {
    seen: true // 针对v-if 的时候应该使用 boolean 类型进行操作
  }
})
```

v-for 好理解类似java 中的for each

```html
<div id="app-4">
  <ol>
    <li v-for="todo in todos">
      {{ todo.text }}
    </li>
  </ol>
</div>
```

```javascript
var app4 = new Vue({
  el: '#app-4',
  data: {
    todos: [
      { text: '学习 JavaScript' },
      { text: '学习 Vue' },
      { text: '整个牛项目' }
    ]
  }
})
```

### 表单数据动态绑定

这个特性针对 input textarea 的使用v-model 进行数据绑定

```html
<div id="app-6">
  <p>{{ message }}</p>
  <input v-model="message">
</div>
```

```javascript
var app6 = new Vue({
  el: '#app-6',
  data: {
    message: 'Hello Vue!'
  }
})
```

v-on 可以绑定在对象中定义的属性

```html
<div id="app-5">
  <p>{{ message }}</p>
  <button v-on:click="reverseMessage">逆转消息</button>
</div>
```

```javascript
var app5 = new Vue({
  el: '#app-5',
  data: {
    message: 'Hello Vue.js!'
  },
  methods: {
    reverseMessage: function () {
      this.message = this.message.split('').reverse().join('')
    }
  }
})
```

### 组件化应用构建


