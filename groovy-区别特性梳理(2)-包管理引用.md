## groovy 和java 在包管理特性上的不同

其实本质上groovy和java 在包管理上其实是类似的,但是groovy提供了更加强大的静态功能

1. 许您定义与导入方法同名的方法，只要您有不同的类型

```groovy
import static java.lang.String.format 

class SomeClass {

    String format(Integer i) { 
        i.toString()
    }

    static void main(String[] args) {
        assert format('String') == 'String' 
        assert new SomeClass().format(Integer.valueOf(1)) == '1'
    }
}
```

2. 导入别名

1. 静态函数名称导入别名

```groovy
//将一个静态函数的名称定义成别名
import static Calendar.getInstance as now
assert now().class == Calendar.getInstance().class
```

2. 对象别名

```groovy
import java.util.Date
import java.sql.Date as SQLDate

Date utilDate = new Date(1000L)
SQLDate sqlDate = new SQLDate(1000L)

assert utilDate instanceof java.util.Date
assert sqlDate instanceof java.sql.Date
```

## groovy 和 java 运行上的不同

groovy继承了java类的定义,如果使用了class来表示groovy对象,本质上和java并没有区别

```groovy
class Main {                                    
    static void main(String... args) {          
        println 'Groovy world!'                 
    }
}
```

但是如果使用groovy脚本模式变成并运行,groovy内部会将脚本进行编译

比如这样一个groovy脚本

```groovy
println 'Hello'                                 
int power(int n) { 2**n }                       
println "2^6==${power(6)}"     
```

groovy将会将这个脚本编译成

```groovy
import org.codehaus.groovy.runtime.InvokerHelper
class Main extends Script {
    int power(int n) { 2** n}                   
    def run() {
        println 'Hello'                         
        println "2^6==${power(6)}"              
    }
    static void main(String[] args) {
        InvokerHelper.runScript(Main, args)
    }
}
```