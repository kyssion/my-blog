# jackson 使用代码进行配置的一个例子

```java
public class JsonUtils {
    /**
     * Logger for this class
     */
    private static final Logger logger = LoggerFactory.getLogger(JsonUtils.class);
 
    private final static ObjectMapper objectMapper = new ObjectMapper();
 
    static {
        objectMapper.configure(JsonParser.Feature.ALLOW_COMMENTS, true);
        objectMapper.configure(JsonParser.Feature.ALLOW_UNQUOTED_FIELD_NAMES, true);
        objectMapper.configure(JsonParser.Feature.ALLOW_SINGLE_QUOTES, true);
        objectMapper.configure(JsonParser.Feature.ALLOW_UNQUOTED_CONTROL_CHARS, true);
        objectMapper.configure(JsonParser.Feature.INTERN_FIELD_NAMES, true);
        objectMapper.configure(JsonParser.Feature.CANONICALIZE_FIELD_NAMES, true);
        objectMapper.configure(DeserializationConfig.Feature.FAIL_ON_UNKNOWN_PROPERTIES, false);
    }
 
    private JsonUtils() {
    }
 
    public static String encode(Object obj) {
        try {
            return objectMapper.writeValueAsString(obj);
        } catch (JsonGenerationException e) {
            logger.error("encode(Object)", e); //$NON-NLS-1$
        } catch (JsonMappingException e) {
            logger.error("encode(Object)", e); //$NON-NLS-1$
        } catch (IOException e) {
            logger.error("encode(Object)", e); //$NON-NLS-1$
        }
        return null;
    }
 
    /**
     * 将json string反序列化成对象
     *
     * @param json
     * @param valueType
     * @return
     */
    public static <T> T decode(String json, Class<T> valueType) {
        try {
            return objectMapper.readValue(json, valueType);
        } catch (JsonParseException e) {
            logger.error("decode(String, Class<T>)", e);
        } catch (JsonMappingException e) {
            logger.error("decode(String, Class<T>)", e);
        } catch (IOException e) {
            logger.error("decode(String, Class<T>)", e);
        }
        return null;
    }
 
    /**
     * 将json array反序列化为对象
     *
     * @param json
     * @param jsonTypeReference
     * @return
     */
    @SuppressWarnings("unchecked")
    public static <T> T decode(String json, TypeReference<T> typeReference) {
        try {
            return (T) objectMapper.readValue(json, typeReference);
        } catch (JsonParseException e) {
            logger.error("decode(String, JsonTypeReference<T>)", e);
        } catch (JsonMappingException e) {
            logger.error("decode(String, JsonTypeReference<T>)", e);
        } catch (IOException e) {
            logger.error("decode(String, JsonTypeReference<T>)", e);
        }
        return null;
```

# Jackson配置属性
如果上面的工具类实例，在Jackson中存在一些属性配置，这些配置决定了最后在解析或者编码后数据视图。因此，在分析Jackson之前，先了解下，Jackson具有的一些配置含义。

## JsonParser解析相关配置属性

```java

/**
     * Enumeration that defines all togglable features for parsers.
     */
    public enum Feature {
 
        // // // Low-level I/O handling features:
 
        /**
         * 这个特性，决定了解析器是否将自动关闭那些不属于parser自己的输入源。 如果禁止，则调用应用不得不分别去关闭那些被用来创建parser的基础输入流InputStream和reader；
         * 如果允许，parser只要自己需要获取closed方法（当遇到输入流结束，或者parser自己调用 JsonParder#close方法），就会处理流关闭。
         *
         * 注意：这个属性默认是true，即允许自动关闭流
         *
         */
        AUTO_CLOSE_SOURCE(true),
 
        // // // Support for non-standard data format constructs
 
        /**
         * 该特性决定parser将是否允许解析使用Java/C++ 样式的注释（包括'/'+'*' 和'//' 变量）。 由于JSON标准说明书上面没有提到注释是否是合法的组成，所以这是一个非标准的特性；
         * 尽管如此，这个特性还是被广泛地使用。
         *
         * 注意：该属性默认是false，因此必须显式允许，即通过JsonParser.Feature.ALLOW_COMMENTS 配置为true。
         *
         */
        ALLOW_COMMENTS(false),
 
        /**
         * 这个特性决定parser是否将允许使用非双引号属性名字， （这种形式在Javascript中被允许，但是JSON标准说明书中没有）。
         *
         * 注意：由于JSON标准上需要为属性名称使用双引号，所以这也是一个非标准特性，默认是false的。
         * 同样，需要设置JsonParser.Feature.ALLOW_UNQUOTED_FIELD_NAMES为true，打开该特性。
         *
         */
        ALLOW_UNQUOTED_FIELD_NAMES(false),
 
        /**
         * 该特性决定parser是否允许单引号来包住属性名称和字符串值。
         *
         * 注意：默认下，该属性也是关闭的。需要设置JsonParser.Feature.ALLOW_SINGLE_QUOTES为true
         *
         */
        ALLOW_SINGLE_QUOTES(false),
 
        /**
         * 该特性决定parser是否允许JSON字符串包含非引号控制字符（值小于32的ASCII字符，包含制表符和换行符）。 如果该属性关闭，则如果遇到这些字符，则会抛出异常。
         * JSON标准说明书要求所有控制符必须使用引号，因此这是一个非标准的特性。
         *
         * 注意：默认时候，该属性关闭的。需要设置：JsonParser.Feature.ALLOW_UNQUOTED_CONTROL_CHARS为true。
         *
         */
        ALLOW_UNQUOTED_CONTROL_CHARS(false),
 
        /**
         * 该特性可以允许接受所有引号引起来的字符，使用‘反斜杠\’机制：如果不允许，只有JSON标准说明书中 列出来的字符可以被避开约束。
         *
         * 由于JSON标准说明中要求为所有控制字符使用引号，这是一个非标准的特性，所以默认是关闭的。
         *
         * 注意：一般在设置ALLOW_SINGLE_QUOTES属性时，也设置了ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER属性，
         * 所以，有时候，你会看到不设置ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER为true，但是依然可以正常运行。
         *
         * @since 1.6
         */
        ALLOW_BACKSLASH_ESCAPING_ANY_CHARACTER(false),
 
        /**
         * 该特性决定parser是否允许JSON整数以多个0开始(比如，如果000001赋值给json某变量，
         * 如果不设置该属性，则解析成int会抛异常报错：org.codehaus.jackson.JsonParseException: Invalid numeric value: Leading zeroes not
         * allowed)
         *
         * 注意：该属性默认是关闭的，如果需要打开，则设置JsonParser.Feature.ALLOW_NUMERIC_LEADING_ZEROS为true。
         *
         * @since 1.8
         */
        ALLOW_NUMERIC_LEADING_ZEROS(false),
 
        /**
         * 该特性允许parser可以识别"Not-a-Number" (NaN)标识集合作为一个合法的浮点数。 例如： allows (tokens are quoted contents, not including
         * quotes):
         * <ul>
         * <li>"INF" (for positive infinity), as well as alias of "Infinity"
         * <li>"-INF" (for negative infinity), alias "-Infinity"
         * <li>"NaN" (for other not-a-numbers, like result of division by zero)
         * </ul>
         */
 
        ALLOW_NON_NUMERIC_NUMBERS(false),
 
        // // // Controlling canonicalization (interning etc)
 
        /**
         * 该特性决定JSON对象属性名称是否可以被String#intern 规范化表示。
         *
         * 如果允许，则JSON所有的属性名将会 intern() ；如果不设置，则不会规范化，
         *
         * 默认下，该属性是开放的。此外，必须设置CANONICALIZE_FIELD_NAMES为true
         *
         * 关于intern方法作用：当调用 intern 方法时，如果池已经包含一个等于此 String 对象的字符串 （该对象由 equals(Object) 方法确定），则返回池中的字符串。否则，将此 String
         * 对象添加到池中， 并且返回此 String 对象的引用。
         *
         * @since 1.3
         */
        INTERN_FIELD_NAMES(true),
 
        /**
         * 该特性决定JSON对象的属性名称是否被规范化。
         *
         * @since 1.5
         */
        CANONICALIZE_FIELD_NAMES(true),
 
        ;
 
        final boolean _defaultState;
 
        /**
         * Method that calculates bit set (flags) of all features that are enabled by default.
         */
        public static int collectDefaults() {
            int flags = 0;
            for (Feature f : values()) {
                if (f.enabledByDefault()) {
                    flags |= f.getMask();
                }
            }
            return flags;
        }
 
        private Feature(boolean defaultState) {
            _defaultState = defaultState;
        }
 
        public boolean enabledByDefault() {
            return _defaultState;
        }
 
        public boolean enabledIn(int flags) {
            return (flags & getMask()) != 0;
        }
 
        public int getMask() {
            return (1 << ordinal());
        }
    }
}
```

> Note: 在枚举最后有一个公共静态方法collectDefaults()，这个方法返回一个整形，整形包含的是所有枚举项对应位bit为初始默认值（true：1；false：0），如果默认属性为true，则通过对1 << ordinal()的值和flags进行亦或来置位。

## DeserializationConfig反序列化相关配置属性

将Java 对象序列化为Json字符串。Jackson在序列化Java对象的时候，对于有些不存在的属性处理，以及一些类型转换等，都可以通过配置来设置。

