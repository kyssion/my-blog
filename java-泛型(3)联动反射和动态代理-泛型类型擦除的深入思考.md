java的泛型实现因为考虑到兼容型的问题,所以一开始采用了类型擦除的机制实现相关的功能.

但是这种类型擦除的机制又带来了一个新的问题,比如这样的场景

```java
public class ReflectorTest2 {
    public static void main(String[] args) throws NoSuchFieldException {
        ReflectorItem<String> reflectorItem =new ReflectorItem<>();
        Class<ReflectorItem<String>> reflectorItemClass = (Class<ReflectorItem<String>>) reflectorItem.getClass();
        Field f = reflectorItemClass.getDeclaredField("item");
        System.out.println(f.getType().getName());
    }
}
class ReflectorItem<T> {
    T item;
    public T getItem() {
        return item;
    }
    public void setItem(T item) {
        this.item = item;
    }
}
```

因为T会在java运行的时候进行擦除,所以这里输出的内容是Object

```shell
java.lang.Object
```

如果想要获取这个参数的类型,我们只能在泛型类的内部获取到

```java
public class ReflectorTest2 {
    public static void main(String[] args) throws NoSuchFieldException {
        ReflectorItem<String> reflectorItem =new ReflectorItem<>("sdf"){};
        reflectorItem.setItem("restset");
    }
}
class  ReflectorItem<T> {
    Type _type;
    ReflectorItem(T s){
        Type superClass = getClass().getGenericSuperclass();
        if (superClass instanceof Class<?>) { // sanity check, should never happen
            throw new IllegalArgumentException("Internal error: TypeReference constructed without actual type information");
        }
        _type = ((ParameterizedType) superClass).getActualTypeArguments()[0];
        TypeVariable<? extends Class<?>>[] typeParameters =s.getClass().getTypeParameters();
    }
    T item;
    public T getItem() {
        return item;
    }
    public void setItem(T item) {
        this.item = item;
    }
}
```