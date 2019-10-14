## spring5-SpEL表达式

SpEL是一种强大的、简洁的装配Bean的方式，它通过运行期执行的表达式将值装配到Bean的属性或构造器参数中。比如说 xml文件中动态的加入上下文信息，使用类的静态方法等相关方法载入参数

### 载入基本类型

```xml
<property name="count" value="#{5}" />
<property name="frequency" value="#{89.7}" />
<property name="capacity" value="#{1e4}" />
<property name="name" value="#{'moonlit'}" />
<property name="name" value='#{"moonlit"}' />
<property name="enabled" value="#{true}" />
```

### 使用xml配置文件中的其他配置选项

```xml
<bean id="poem" class="com.moonlit.myspring.Poem" />
    <bean id="poet" class="com.moonlit.myspring.Poet">
    <property name="poem" value="#{poem}">
</bean>
```

获取poet中传入的poem对象的两种方法

```spEL
#{poet.poem}
```

### 调用方法

调用其他 名字为poet bean的方法

```xml
#{poet.getPoem()}
#{songSelector.selectSong()?.toUpperCase()}
```

上面使用 ?. 运算符代替点（.）来访问toUpperCase()方法。在访问邮编方法之前，该运算符会确保左边项的值不为null。所以，如果selectorSong返回null，SpEL就不再尝试调用toUpperCase()方法。

在SpEL中，使用T()运算符会调用类作用域的方法和常量

```xml
#{T(java.lang.Math).PI}
#{T(java.lang.Math).random()}
```

### 使用逻辑算数运行

算数表达式

```spEL
#{circle.radius + 100.0}
```

操作一个表达式的值：eq(==),lt(<),le(<=),gt(>),ge(>=)。逻辑表达式：and,or,not或!。条件运算符：使用三元运算符 ？：

```spEL
#{sonSelector.selecSOng()=='Jingle Bells'?piano:saxophone}
#{kenny.song != null ? kenny.song : 'Greensleeves'}
#{kenny.song ?: 'Greensleeves'}
```

正则表达式匹配

```spEL
#{admin.email matches '[a-zA-Z0-9._%+_]+@[a-zA-Z0-9.-]+\\.com'}
```


