1. 脚本化运行nodejs

- 安装nodejs ， 然后编写对应的nodejs 脚本
```bash
#!/usr/bin/env node
```

2. 退出

```javascript
process.exit(1)
```
这个方法会抛出一个错误码

- 0 正常
- 1 

3. nodejs 环境初始化

```
export NODE_ENV=production
NODE_ENV=production node app.js
```

- 检测环境信息

```js
if (process.env.NODE_ENV === 'development') {
  // ...
}
if (process.env.NODE_ENV === 'production') {
  // ...
}
if (['production', 'staging'].includes(process.env.NODE_ENV)) {
  // ...
}

// 用法 ， 根据环境配置不同的信息

if (process.env.NODE_ENV === 'development') {
  app.use(express.errorHandler({ dumpExceptions: true, showStack: true }));
}

if (process.env.NODE_ENV === 'production') {
  app.use(express.errorHandler());
}

```
4. webAssembly

```js
// Assume add.wasm file exists that contains a single function adding 2 provided arguments
const fs = require('fs');

const wasmBuffer = fs.readFileSync('/path/to/add.wasm');
WebAssembly.instantiate(wasmBuffer).then(wasmModule => {
  // Exported function live under instance.exports
  const { add } = wasmModule.instance.exports;
  const sum = add(5, 6);
  console.log(sum); // Outputs: 11
});

```

5. npm 包管理

- package.json 是核心
- 初始化自定义package.json (.npm-init.js)

```js
module.exports = {
  customField: 'Example custom field',
  otherCustomField: 'This example field is really cool'
}
```

- "dependencies"：您的应用程序在生产中所需的包。
- "devDependencies"：只需要本地开发和测试的包。


npm 包安装

本地安装（默认）：将内容放入./node_modules当前包根目录。
全局安装（带-g）：将东西放在 /usr/local 或安装节点的任何位置。
如果你要去的话，在本地安装require()它。
如果要在命令行上运行它，请全局安装它。
如果两者都需要，则将其安装在两个位置，或使用npm link.

npm 包格式 
支持 ， 本地加载 ， 版本控制 ， github 控制


- 常用命令

```
npm install 
npm search
npm list -g
npm link - 全局安装引用
```


