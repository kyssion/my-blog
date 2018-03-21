### Bean操作和BeanWrapper

BeanWrapper 实现了对bean更加细致的操作这种方法将会让bean的各种操作更加容易和方便,并且提供了高级使用方法

#### 设置和获取基本和嵌套的属性

设置和获取属性是通过使用setPropertyValue(s)和 getPropertyValue(s)两个重载变量都有的方法完成的。

s字符串支持的属性见下

|表达|说明|
| ------------ | ------------ |
|name|指示与name方法getName()或isName() 和相对应的属性setName(..)|
|account.name|指示对应于例如方法或属性name的属性的嵌套属性accountgetAccount().setName()getAccount().getName()|
|account[2]|指示索引属性的第三个元素account。索引属性可以是类型的array，也可以是list其他自然顺序的集合|
|account[COMPANYNAME]|指示由Map属性的键COMPANYNAME索引的地图条目的值account|

```java
public class Company {
    private String name;
    private Employee managingDirector;
    public String getName() {
        return this.name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public Employee getManagingDirector() {
        return this.managingDirector;
    }
    public void setManagingDirector(Employee managingDirector) {
        this.managingDirector = managingDirector;
    }
}
public class Employee {
    private String name;
    private float salary;
    public String getName() {
        return this.name;
    }
    public void setName(String name) {
        this.name = name;
    }
    public float getSalary() {
        return salary;
    }
    public void setSalary(float salary) {
        this.salary = salary;
    }
}
```

下面的代码片断展示了如何检索和操作的一些实例化属性的一些例子Companies和Employees：
```java
BeanWrapper company = new BeanWrapperImpl(new Company());
// setting the company name..
company.setPropertyValue("name", "Some Company Inc.");
// ... can also be done like this:
PropertyValue value = new PropertyValue("name", "Some Company Inc.");
company.setPropertyValue(value);
// ok, let's create the director and tie it to the company:
BeanWrapper jim = new BeanWrapperImpl(new Employee());
jim.setPropertyValue("name", "Jim Stravinsky");
company.setPropertyValue("managingDirector", jim.getWrappedInstance());
// retrieving the salary of the managingDirector through the company
Float salary = (Float) company.getPropertyValue("managingDirector.salary");
```
