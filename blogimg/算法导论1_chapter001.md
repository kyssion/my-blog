## 算法

1. 插入排序

```java
public void sort1(int[] arr) {
    for (int a = 1; a < arr.length; a++) {
        int k = arr[a];
        int index = a - 1;
        //这一步很关键,思想变成算法的时候需要深刻的理解变量所表达的意思
        while (index >= 0 && k < arr[index]) {
            arr[index + 1] = arr[index];
            index--;
        }
        arr[index + 1] = k;
    }
}
```

> 其实这个算法我们要理解一个关键的地方就是,将思想变成算法时候的方法,一定要非常的理解变量所表达的意思,函数变量在运行过程中所代表意义的变化情况