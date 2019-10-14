# GoF设计模式-iteratoer

### 迭代器模式


这个设计模式个人在感觉上是非常常用的一种设计模式，通过将数据的遍历过程和业务逻辑结构，可以在遍历过程中分解出一些共用的遍历方法，提高效率。

> 反思：目前的感觉迭代器模式的核心思想就是将数据的遍历和处理和调用过程接偶，其原因是遍历过程具有一定的通用性，通过解耦可以更加方便的降低代码的重复率。重要的思想还有数据的桥接方法，使用继承方式还是使用数据引用传递的方式，通过这种思想将业务独立的itertor和真实的业务数据book组合起来

### 迭代器模式类图

![](blogimg/GAF/1.png)

- aggregate：这个接口的作用是生成迭代器，也就是说数据的集成类需要集成和实现这个接口，从而可以产生自己的迭代器

- iterator：这个接口就是迭代器的接口类，定义了一组迭代器通用的方法

- concreteAggregate：这个为aggregate接口的实现类（实际使用中一般把数据的集合类作为这个类的实现）

- concreteIterator：这个类就是迭代器的实现类，这个类需要针对元素类（就是迭代出来的元素）有针对性的思考要怎么设计


###  迭代器例子

> book 迭代的元素

```java
package org.kys.Gaf.iterator;
public class Book {
    private String bookname;
    public Book(String name) {
        this.bookname = name;
    }
    public String getBookname() {
        return bookname;
    }
    public void setBookname(String bookname) {
        this.bookname = bookname;
    }
}
```

> Aggergate接口

```java
package org.kys.Gaf.iterator;

public interface Aggergate<T> {
    Iterator<T> iterator();
}
```

> concretaAggregate-Aggergate接口的实现类 这里使用bookself作为创建迭代器的实现类

```java
package org.kys.Gaf.iterator;
public class BookSelf implements Aggergate<Book>{
    private Book[] books;
    private int bookPosition=0;
    public BookSelf(int bookLength){
        this.books = new Book[bookLength];
    }
    public boolean addBook(Book book){
        if (bookPosition>=books.length){
            return false;
        }
        this.books[bookPosition++]=book;
        return true;
    }

    public Book getBook(int position){
        return books[position];
    }

    public int getBookNumber(){
        return bookPosition;
    }
    @Override
    public Iterator<Book> iterator() {
        return new BookIterator(this);
    }
}
```


> iterator接口 

```java
package org.kys.Gaf.iterator;

public interface Iterator<T> {
    boolean hasNext();
    T next();
}
```

> iterator实现类

```java
package org.kys.Gaf.iterator;
public class BookIterator implements Iterator<Book> {
    private BookSelf bookSelf = null;
    private int bookSelfPosiont = 0;
    public BookIterator(BookSelf bookSelf) {
        this.bookSelf = bookSelf;
    }
    @Override
    public boolean hasNext() {
        if (bookSelfPosiont >= bookSelf.getBookNumber()) {
            return false;
        }else{
            return true;
        }
    }
    @Override
    public Book next() {
        return bookSelf.getBook(bookSelfPosiont++);
    }
}
```

> 主函数 Main

```java
package org.kys.Gaf.iterator;

public class Main {
    public static void main(String[] args) {
        BookSelf bookSelf = new BookSelf(3);
        bookSelf.addBook(new Book("海底两万里"));
        bookSelf.addBook(new Book("堂吉诃德"));
        bookSelf.addBook(new Book("飘"));
        Iterator<Book> iterator = bookSelf.iterator();
        while(iterator.hasNext()){
            System.out.println(iterator.next().getBookname());
        }
    }
}
```

> 思路： 其实大体上和迭代器原本的思想相同，但是在这个地方使用将bookshef（book元素的实现类）作为aggergate的实现类，在调用的时候将通过本身生成迭代器，然后进行迭代功能的实现，我觉得这里才是迭代器真正的难点和实现痛点-集合和迭代器的通信。


> 反思：目前的感觉迭代器模式的核心思想就是将数据的遍历和处理和调用过程接偶，其原因是遍历过程具有一定的通用性，通过解耦可以更加方便的降低代码的重复率。重要的思想还有数据的桥接方法，使用继承方式还是使用数据引用传递的方式，通过这种思想将业务独立的itertor和真实的业务数据book组合起来

