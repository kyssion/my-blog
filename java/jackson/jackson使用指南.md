# jaskson注解详解

# 序列化相关注解

## @JsonAnyGetter

这个注解可以将javabean中的mapper在**序列化**的时候展开成变量

比如这个json 就可以由这个javabean序列化而来

```java
public class ExtendableBean {
    public String name;
    private Map<String, String> properties;
 
    @JsonAnyGetter
    public Map<String, String> getProperties() {
        return properties;
    }
}
```

## @JsonGetter

指定变量名称和getter方法的绑定关系,比如下面的例子将name属性和getThemName方法绑定在一起

```java
public class MyBean {
    public int id;
    private String name;
    @JsonGetter("name")
    public String getTheName() {
        return name;
    }
}
```

## @JsonPropertyOrder

指定序列化的顺序

注意：我们还可以使用@JsonPropertyOrder（alphabetic = true）按字母顺序对属性进行排序

## @JsonRawValue

强制jack序列化 被格式化的json字符串

比如有一个javabean 其中string存了一个json，可以使用这个注解将这个json格式化出来

```json
{
    "name":"My bean",
    "json":{
        "attr":false
    }
}
```

```java
public class RawBean {
    public String name;
 
    @JsonRawValue
    public String json;
}
```

## @JsonValue

@JsonValue表示库将用于序列化整个实例的单个方法

简单的说就是指定了一个方法用来在序列化的时候调用

```java
public enum TypeEnumWithValue {
    TYPE1(1, "Type A"), TYPE2(2, "Type 2");
 
    private Integer id;
    private String name;
 
    // standard constructors
 
    @JsonValue
    public String getName() {
        return name;
    }
}
```

## @JsonRootName

将序列化的javabean外层包裹一个包名称

```java
@JsonRootName(value = "user")
public class UserWithRoot {
    public int id;
    public String name;
}
```

```json
{
    "User": {
        "id": 1,
        "name": "John"
    }
}
```

## @JsonSerialize

自定义序列化过程

```java
public class Event {
    public String name;
 
    @JsonSerialize(using = CustomDateSerializer.class)
    public Date eventDate;
}
```

```java
public class CustomDateSerializer extends StdSerializer<Date> {
 
    private static SimpleDateFormat formatter 
      = new SimpleDateFormat("dd-MM-yyyy hh:mm:ss");
 
    public CustomDateSerializer() { 
        this(null); 
    } 
 
    public CustomDateSerializer(Class<Date> t) {
        super(t); 
    }
 
    @Override
    public void serialize(
      Date value, JsonGenerator gen, SerializerProvider arg2) 
      throws IOException, JsonProcessingException {
        gen.writeString(formatter.format(value));
    }
}
```

# Jackson反序列化注释

## @JsonCreator

和@JsonProperty连用可以在创建bean的时候强制绑定json中的属性

比如这个json中的theName绑定到javabean中的name

```json
{
    "id":1,
    "theName":"My bean"
}
```

```java
public class BeanWithCreator {
    public int id;
    public String name;
 
    @JsonCreator
    public BeanWithCreator(
      @JsonProperty("id") int id, 
      @JsonProperty("theName") String name) {
        this.id = id;
        this.name = name;
    }
}
```

# @JacksonInject

属性注入，这个场景貌似有点晕

```java
public class BeanWithInject {
    @JacksonInject
    public int id;
     
    public String name;
}
```

```java
@Test
public void whenDeserializingUsingJsonInject_thenCorrect()
  throws IOException {
    String json = "{\"name\":\"My bean\"}";
    InjectableValues inject = new InjectableValues.Std()
      .addValue(int.class, 1);
    BeanWithInject bean = new ObjectMapper().reader(inject)
      .forType(BeanWithInject.class)
      .readValue(json);
    assertEquals("My bean", bean.name);
    assertEquals(1, bean.id);
}
```

# @JsonAnySetter

这个@JsonAnyGetter相反

@JsonAnySetter使我们可以灵活地使用Map作为标准属性。反序列化时，JSON中尚未绑定的属性，将被简单地添加到map中

```java
public class ExtendableBean {
    public String name;
    private Map<String, String> properties;
 
    @JsonAnySetter
    public void add(String key, String value) {
        properties.put(key, value);
    }
}
```

# @JsonSetter

@JsonSetter是一种替代@JsonProperty -这标志着方法作为setter方法。

当我们需要读取一些JSON数据但目标实体类与该数据不完全匹配时，这非常有用，因此我们需要调整过程以使其适合。

和@JsonGetter逻辑相同

```java
public class MyBean {
    public int id;
    private String name;
 
    @JsonSetter("name")
    public void setTheName(String name) {
        this.name = name;
    }
}
```

# @JsonDeserialize

自定义反序列化逻辑

```java
public class Event {
    public String name;
 
    @JsonDeserialize(using = CustomDateDeserializer.class)
    public Date eventDate;
}
```

```java
public class CustomDateDeserializer
  extends StdDeserializer<Date> {
 
    private static SimpleDateFormat formatter
      = new SimpleDateFormat("dd-MM-yyyy hh:mm:ss");
 
    public CustomDateDeserializer() { 
        this(null); 
    } 
 
    public CustomDateDeserializer(Class<?> vc) { 
        super(vc); 
    }
 
    @Override
    public Date deserialize(
      JsonParser jsonparser, DeserializationContext context) 
      throws IOException {
         
        String date = jsonparser.getText();
        try {
            return formatter.parse(date);
        } catch (ParseException e) {
            throw new RuntimeException(e);
        }
    }
}
```

## @JsonAlias

反序列化过程为属性的一个或多个的替代名称

```java
public class AliasBean {
    @JsonAlias({ "fName", "f_name" })
    private String firstName;   
    private String lastName;
}
```

# Jackson属性展示型注解

## @JsonIgnoreProperties

@JsonIgnoreProperties是一个类级别的注释，用于标记Jackson将忽略的一个属性或一系列属性。

```java
@JsonIgnoreProperties({ "id" })
public class BeanWithIgnore {
    public int id;
    public String name;
}
```

## @JsonIgnore

该@JsonIgnore注释用来标记在外地被忽略的属性。

```java
public class BeanWithIgnore {
    @JsonIgnore
    public int id;
 
    public String name;
}
```

## @JsonIgnoreType

@JsonIgnoreType将带注释类型的所有属性标记为忽略。

```java
public class User {
    public int id;
    public Name name;
 
    @JsonIgnoreType
    public static class Name {
        public String firstName;
        public String lastName;
    }
}
```

## @JsonInclude

```java
@JsonInclude(Include.NON_NULL)
public class MyBean {
    public int id;
    public String name;
}
```

## @JsonAutoDetect

@JsonAutoDetect可以覆盖默认语义，即哪些属性可见，哪些属性不可见。

让我们来看一个简单的示例，该批注如何非常有用–让我们序列化私有属性：

```java
@JsonAutoDetect(fieldVisibility = Visibility.ANY)
public class PrivateBean {
    private int id;
    private String name;
}
```

# Jackson多态类型处理注释

> 有点麻烦掠过

# 其他通用注解

## @JsonProperty

在处理非标准的getter和setter时，让我们使用@JsonProperty对属性名称进行序列化/反序列化：

```java
public class MyBean {
    public int id;
    private String name;
 
    @JsonProperty("name")
    public void setTheName(String name) {
        this.name = name;
    }
 
    @JsonProperty("name")
    public String getTheName() {
        return name;
    }
}
```

## @JsonFormat

该@JsonFormat序列化的日期/时间值时，注解指定的格式。

```java
public class Event {
    public String name;
 
    @JsonFormat(
      shape = JsonFormat.Shape.STRING,
      pattern = "dd-MM-yyyy hh:mm:ss")
    public Date eventDate;
}
```

## @JsonUnwrapped

@JsonUnwrapped定义在序列化/反序列化时应该解包/展平的值。

## @JsonView
@JsonView指示将在其中包含属性以进行序列化/反序列化的View。

## @ JsonManagedReference，@ JsonBackReference
该@JsonManagedReference和@JsonBackReference注释可以处理父/子关系和解决循环。

## @JsonIdentityInfo
@JsonIdentityInfo指示在对值进行序列化/反序列化时应使用对象标识，例如，以处理无限递归类型的问题。

## @JsonFilter

该@JsonFilter注释指定一个过滤器序列化过程中使用。

# 自定义杰克逊注释

创建自定义Jackson注释。我们可以使用@JacksonAnnotationsInside注释

```java
@Retention(RetentionPolicy.RUNTIME)
    @JacksonAnnotationsInside
    @JsonInclude(Include.NON_NULL)
    @JsonPropertyOrder({ "name", "id", "dateCreated" })
    public @interface CustomAnnotation {}
```
我们可以看到它如何将现有的注释合并为一个更简单的自定义注释，可以用作速记：


```java
@CustomAnnotation
public class BeanWithCustomAnnotation {
    public int id;
    public String name;
    public Date dateCreated;
}
```