### mybatis 整体反射框架设计

![](blogimg/mybatis/1.png)

可以看到，Mybatis对这一块抽象的比较复杂，我们可以看到有几个比较主要的部分：Reflector、Invoker、PropertyTokenizer、MetaClass，MetaObject和ObjectWrapper，下面我们一个一个解析这几个部分，最后合并在一起看看他们是如何协作工作的。

### Reflector

我对Reflector的理解是 Reflector是对类的描述 ，我们从一段UT开始（代码位于ReflectorTest）：

```java
static abstract class AbstractEntity implements Entity<Long> {

    private Long id;

    @Override
    public Long getId() {
        return id;
    }

    @Override
    public void setId(Long id) {
        this.id = id;
    }
}
static class Section extends AbstractEntity implements Entity<Long> {
}
@Test
public void testGetSetterType() throws Exception {
    ReflectorFactory reflectorFactory = new DefaultReflectorFactory();
    Reflector reflector = reflectorFactory.findForClass(Section.class);
    Assert.assertEquals(Long.class, reflector.getSetterType("id"));
}
```

这个测试方法首先创建了个ReflectorFactory对象，然后用这个factory创建了一个Section类的Reflector，然后判断Section类中id的setter方法是Long类型的。

ReflectorFactory是对Reflector做的一个简单的工厂，提供类反射的缓存（所以反射这块的开销基本上可以不计了，既灵活又快捷）

DefaultReflectorFactory 是 Reflector的默认实现类，用一个ConcurrentMap缓存所有的Reflector示例，它的findForClass方法如下，它首先尝试从map中获取Reflector，获取失败调用Reflector的构造方法创建示例，缓存并返回：

```java
static interface Entity<T> {
    T getId();
    void setId(T id);
}
@Override
public Reflector findForClass(Class<?> type) {
    if (classCacheEnabled) {
        // synchronized (type) removed see issue #461
        Reflector cached = reflectorMap.get(type);
        if (cached == null) {
            cached = new Reflector(type);
            reflectorMap.put(type, cached);
        }
        return cached;
    } else {
        return new Reflector(type);
    }
}
```

之后是Reflector的构造方法：

```java
public Reflector(Class<?> clazz) {
    type = clazz;
    addDefaultConstructor(clazz);
    addGetMethods(clazz);
    addSetMethods(clazz);
    addFields(clazz);
    readablePropertyNames = getMethods.keySet().toArray(new String[getMethods.keySet().size()]);
    writeablePropertyNames = setMethods.keySet().toArray(new String[setMethods.keySet().size()]);
    for (String propName : readablePropertyNames) {
        caseInsensitivePropertyMap.put(propName.toUpperCase(Locale.ENGLISH), propName);
    }
    for (String propName : writeablePropertyNames) {
        caseInsensitivePropertyMap.put(propName.toUpperCase(Locale.ENGLISH), propName);
    }
}
```

这一块不再细细展开，方法名见名知义，首先将type成员设置为原始的class对象，之后获取class的构造方法，getter/setter属性，成员字段，之后将属性名转大写存放到caseInsensitivePropertyMap中，为了后面的查找，大小写不敏感。

Reflector的其他方法就是对我们保存的这些类的描述做查找， 其中有两个特别的，也就是我们接下来要讨论的 getSetInvoker和 getGetInvoker

### Invoker

Invoker，顾名思义，就是调用，可以调用的东西，他有一个invoke方法，意思就是调用，参数是target和args，就是调用的对象和调用的参数。

我们来看下它的几个实现类：

- MethodInvoker: 方法调用
- SetFieldInvoker：Setter方法调用
- GetFieldInvoker：Getter方法调用
MethodInvoker中invoke方法的实现：

```java
@Override
public Object invoke(Object target, Object[] args) throws IllegalAccessException, InvocationTargetException {
    return method.invoke(target, args);
}
```

就是简单的method.invoke

### PropertyTokenizer

这个就比较牛逼了，他可以处理属性表达式，PropertyTokenizer还实现了Iterator接口，这意味着他可以处理复杂的嵌套属性

```java
@Override
public boolean hasNext() {
    return children != null;
}

@Override
public PropertyTokenizer next() {
    return new PropertyTokenizer(children);
}
```

字段的含义，name表示当前对象的名字，indexedName是当前对象的名字加上后面的索引（[]）如果有的话，index是索引下标，children是延伸属性（子对象）
比如：用PropertyTokenizer去解析 "richType.richList[0].value"，那么 name=richType, indexedName=richType，index=null，children=richList[0].value
之后执行tokenizer.next()得到新的tokenizer，此时 name=richList, indexdName=richList[0],index=0, children=value 
之后我们会结合MetaClass和MetaObject看看他有多牛逼

### MetaClass

MetaClass实际上是对Reflector和ProeprtyTokenizer的一种结合，是我们可以用复杂的属性表达式来获取类型的描述。

同样的，我们结合UT来看看它是怎样工作的，首先是一个示例的复杂类型 RichType

```java
public class RichType {

    private RichType richType;

    private String richField;

    private String richProperty;

    private Map richMap = new HashMap();

    private List richList = new ArrayList() {
        {
            add("bar");
        }
    };

    public RichType getRichType() {
        return richType;
    }

    public void setRichType(RichType richType) {
        this.richType = richType;
    }

    public String getRichProperty() {
        return richProperty;
    }

    public void setRichProperty(String richProperty) {
        this.richProperty = richProperty;
    }

    public List getRichList() {
        return richList;
    }

    public void setRichList(List richList) {
        this.richList = richList;
    }

    public Map getRichMap() {
        return richMap;
    }

    public void setRichMap(Map richMap) {
        this.richMap = richMap;
    }
}
```

```java
@Test
public void shouldCheckGetterExistance() {
    ReflectorFactory reflectorFactory = new DefaultReflectorFactory();
    MetaClass meta = MetaClass.forClass(RichType.class, reflectorFactory);
    assertTrue(meta.hasGetter("richField"));
    assertTrue(meta.hasGetter("richProperty"));
    assertTrue(meta.hasGetter("richList"));
    assertTrue(meta.hasGetter("richMap"));
    assertTrue(meta.hasGetter("richList[0]"));

    assertTrue(meta.hasGetter("richType"));
    assertTrue(meta.hasGetter("richType.richField"));
    assertTrue(meta.hasGetter("richType.richProperty"));
    assertTrue(meta.hasGetter("richType.richList"));
    assertTrue(meta.hasGetter("richType.richMap"));
    assertTrue(meta.hasGetter("richType.richList[0]"));

    assertFalse(meta.hasGetter("[0]"));
}
```

这段代码说明了metaClass.hasGetter方法可以接受一个复杂的属性表达式来找到对应的类型描述（利用PropertyTokenizer），这个神奇的功能是这么实现的：

```java
public boolean hasGetter(String name) {
    PropertyTokenizer prop = new PropertyTokenizer(name);
    if (prop.hasNext()) {
        if (reflector.hasGetter(prop.getName())) {
            MetaClass metaProp = metaClassForProperty(prop);
            return metaProp.hasGetter(prop.getChildren());
        } else {
            return false;
        }
    } else {
        return reflector.hasGetter(prop.getName());
    }
}
```

首先检查tokenizer的name字段对应的属性是不是有getter方法，之后迭代子属性，直到最后，children为空。

MetaClass中的还有几个方法的实现和这个类似，hasSetter, getGetterType, getSetterType

以上都是类级别的反射抽象，下面看看对象级别的

### ObjectWrapper

ObjectWrapper是对对象的描述的抽象，它抽象出一系列对对象描述的查询和更新的接口

```java
public interface ObjectWrapper {
    Object get(PropertyTokenizer prop);
    void set(PropertyTokenizer prop, Object value);
    String findProperty(String name, boolean useCamelCaseMapping);
    String[] getGetterNames();
    String[] getSetterNames();
    Class<?> getSetterType(String name);
    Class<?> getGetterType(String name);
    boolean hasSetter(String name);
    boolean hasGetter(String name);
    MetaObject instantiatePropertyValue(String name, PropertyTokenizer prop, ObjectFactory objectFactory);
    boolean isCollection();
    void add(Object element);
    <E> void addAll(List<E> element);
}
```

ObjectWrapper有个几个实现类

- BeanWrapper，包装Javabean的描述，
- MapWrapper，包装Map（键值对）的描述
- CollectionWrapper，包装Collection（集合）的描述
- ObjectWrapperFactory 了操作实例化ObjectWrapper的工厂方法的抽象，可自定义实现

```java
private Object getBeanProperty(PropertyTokenizer prop, Object object) {
    try {
        Invoker method = metaClass.getGetInvoker(prop.getName());
        try {
            return method.invoke(object, NO_ARGUMENTS);
        } catch (Throwable t) {
            throw ExceptionUtil.unwrapThrowable(t);
        }
    } catch (RuntimeException e) {
        throw e;
    } catch (Throwable t) {
        throw new ReflectionException("Could not get property '" + prop.getName() + "' from " + object.getClass() + ".  Cause: " + t.toString(), t);
    }
}
private void setBeanProperty(PropertyTokenizer prop, Object object, Object value) {
    try {
        Invoker method = metaClass.getSetInvoker(prop.getName());
        Object[] params = {value};
        try {
            method.invoke(object, params);
        } catch (Throwable t) {
            throw ExceptionUtil.unwrapThrowable(t);
        }
    } catch (Throwable t) {
        throw new ReflectionException("Could not set property '" + prop.getName() + "' of '" + object.getClass() + "' with value '" + value + "' Cause: " + t.toString(), t);
    }
}
```

### MetaObject

MetaObject也是对对象的描述，它代理了objectWrapper的大部分方法，和MetaClass一样，它利用PropertyTokenizer做了对复杂属性表达式的处理

```java
@Test
public void shouldGetAndSetNestedField() {
    RichType rich = new RichType();
    MetaObject meta = SystemMetaObject.forObject(rich);
    meta.setValue("richType.richField", "foo");
    assertEquals("foo", meta.getValue("richType.richField"));
}
```

MetaObject有5个成员字段，

- originalObject：原始对象，
- objectWrapper，被包装的objectWrapper，
- objectFactory，对象创建工厂，用于在setValue方法中创建不存在的对象属性实例，
- objectWrapperFactory，创建特定的objectWrapper，
- reflectorFactory，用来自定一反射类生成的，如果需要可以自行的扩展

### 协作

反射层的类互相协作，最终根据入参制作出来一个完美的MetaObject和MetaClass给其他组件使用，这其中，比较重要的方法有：

Configuration.newMetaObject，根据传入的object和配置的factory创建对象描述

实际上，ObjectFactory，ObjectWrapperFactory，ReflectorFactory是可以在XML中配置成自定义的，工厂对象全局单例（Configuration对象中）

```java
private void parseConfiguration(XNode root) {
    try {
        //issue #117 read properties first
        propertiesElement(root.evalNode("properties"));
        Properties settings = settingsAsProperties(root.evalNode("settings"));
        loadCustomVfs(settings);
        typeAliasesElement(root.evalNode("typeAliases"));
        pluginElement(root.evalNode("plugins"));
        objectFactoryElement(root.evalNode("objectFactory"));
        objectWrapperFactoryElement(root.evalNode("objectWrapperFactory"));
        reflectorFactoryElement(root.evalNode("reflectorFactory"));
        settingsElement(settings);
        // read it after objectFactory and objectWrapperFactory issue #631
        environmentsElement(root.evalNode("environments"));
        databaseIdProviderElement(root.evalNode("databaseIdProvider"));
        typeHandlerElement(root.evalNode("typeHandlers"));
        mapperElement(root.evalNode("mappers"));
    } catch (Exception e) {
        throw new BuilderException("Error parsing SQL Mapper Configuration. Cause: " + e, e);
    }
}
```

XMlConfigBuilder.settingsAsProperties方法使用MetaClass检查Properties参数有没有非法的key

MetaObject和MetaClass在Session的执行周期（executor, mapping, builder...）中还具有广泛的应用