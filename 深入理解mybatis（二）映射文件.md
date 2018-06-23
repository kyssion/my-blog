## 深入理解mybatis（二）映射文件

MyBatis 的真正强大在于它的映射语句，也是它的魔力所在。由于它的异常强大，映射器的 XML 文件就显得相对简单。如果拿它跟具有相同功能的 JDBC 代码进行对比，你会立即发现省掉了将近 95% 的代码。MyBatis 就是针对 SQL 构建的，并且比普通的方法做的更好。

### 配置文件总览

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd">
<!-- mybatis中使用自动映射的文件的时候需要使用一个接口所以 -->
<!-- mapper标签中的namespace 表示配置文件的接口 -->
<!-- !!!!这里非常重要 注意下面语句标签的时候必须加上命名空间才是最好的这样可以防止调用重复 -->
<mapper namespace="S_Mybatis.c_Mapping接口.Mymapping接口">
    <!--映射器 -->
    <select id="getJavaBean"  parameterType="int" resultType="S_Mybatis.z_javabean.MyjavaBean">
        <!-- 1. select 标签 -->
        <!-- 
                    -标签属性-
            1.id   				表示使用接口中那个方法对应这个标签,命名标准使用方法名称
            2.parameterType		表示传入进这个标签所使用的数据的封转集合,
                                (可以使用int等基本类型,如果有多个类型,需要使用java对象进行封装)
                                取参数使用ognl表示方法 #{xx.xxx}
            3.returntype		表示方法返回值对应的类型可以使用基本类型或者使用自定义的
                                javabean-(必须使在允许自动匹配的条件下)
            4.returnMap			使用映射集引用来作为返回值值的匹配项相当于returntype的复杂形式(不允许在自动配置的条件下)
            5.flushCache		将其设置为 true，任何时候只要语句被调用，都会导致本地缓存和二级缓存都会被清空，默认值：false。
             6.useCache			将其设置为 true，将会导致本条语句的结果被二级缓存，默认值：对 select 元素为 true。
             7.timeout			这个设置是在抛出异常之前，驱动程序等待数据库返回请求结果的秒数。默认值为 unset（依赖驱动）。
             8.resultOrdered		这个设置仅针对嵌套结果 select 语句适用：如果为 true，就是假设包含了嵌套结果集或是分组了，
                                 这样的话当返回一个主结果行的时候，就不会发生有对前面结果集的引用的情况。
                                 这就使得在获取嵌套的结果集的时候,不至于导致内存不够用。默认值：false。
            9.resultSets		这个设置仅对多结果集的情况适用，它将列出语句执行后返回的结果集并每个结果集给一个名称，名称是逗号分隔的。
             10.statementType	告诉mybatis使用JDBC那个statement工作-STATEMENT，PREPARED 或 CALLABLE 的一个
                                 (statement,prepared,CallableStatement)
             11.resultSet		对应resultSet接口FORWARD_ONLY(允许有向前访问)，SCROLL_SENSITIVE
                                 (双向跟踪但是修改不会及时反映出来) 或 SCROLL_INSENSITIVE(双向修改结果及时反映出来)
                                 中的一个，默认值为 unset （依赖驱动）。
             12.databaseID		匹配数据库是指的数据库标识(在xml配置文件中使用的databaseIdPr) 
             13.
        -->
    </select>
    <insert id="insertJavabean" >
        <!-- 
            2.insert update delete标签相关属性
            id					命名空间中的唯一标识符，可被用来代表这条语句。
            parameterType		将要传入语句的参数的完全限定类名或别名。这个属性是可选的，因为 MyBatis 可以通过 TypeHandler
                                推断出具体传入语句的参数，默认值为 unset。
            parameterMap		这是引用外部 parameterMap 的已经被废弃的方法。使用内联参数映射和 parameterType 属性。
            flushCache			将其设置为 true，任何时候只要语句被调用，都会导致本地缓存和二级缓存都会被清空，
                                默认值：true（对应插入、更新和删除语句）。
            timeout				这个设置是在抛出异常之前，驱动程序等待数据库返回请求结果的秒数。默认值为 unset（依赖驱动）。
            statementType		STATEMENT，PREPARED 或 CALLABLE 的一个。这会让 MyBatis 分别使用 Statement，
                                PreparedStatement 或 CallableStatement，默认值：PREPARED。
            useGeneratedKeys	(仅对 insert 和 update 有用）这会令 MyBatis 使用 JDBC 的 getGeneratedKeys
                                方法来取出由数据库内部生成的主键-就是主键自动增加
            keyProperty			(仅对 insert 和 update 有用）这个属性是列名称表示当使用数据库自增的属性的时候
                                这个属性表示传入的参数对象
            keyColumn			(仅对 insert 和 update 有用）这个属性是数字表示第几列这个属性和上面的效果相同 - 
            databaseId			如果配置了 databaseIdProvider，MyBatis 会加载所有的不带 databaseId 或匹配当前 databaseId
                                的语句；如果带或者不带的语句都有，则不带的会被忽略。		
        -->
    </insert>
    <update id="updateJavabean"></update>
    <delete id="deleteJavabean"></delete>
    <insert id="x">
        <selectKey></selectKey><!-- 这个标签可以用来对属性属性进行定制但是不要使用因为很麻烦 -->
    </insert>
    <!-- 3.sql标签-动态的声明了一个可以进行任意嵌入的代码片段 -->
    <sql id="userColumns"> ${alias}.id,${alias}.username,${alias}.password </sql>
    <!-- 4.include-引入一个sql标签 -->
    <insert id="">
        <include refid="userColumns"></include>
    </insert>
    <!-- 5.cache mybatis默认只是开启了一级缓存也就是说针对于同一个sqlsession才会缓存 -->
    <cache></cache><!-- 简单的只使用这一个标签就是开启了二级缓存,默认的配置是 -->
    <!-- 
        默认属性：-!!!默认属性可以被select标签的usecache属性显示的表示是否使用缓存
        映射语句文件中的所有 select 语句将会被缓存。
        映射语句文件中的所有 insert,update 和 delete 语句会刷新缓存。
        缓存会使用 Least Recently Used(LRU,最近最少使用的)算法来收回。
        根据时间表(比如 no Flush Interval,没有刷新间隔), 缓存不会以任何时间顺序 来刷新。
        缓存会存储列表集合或对象(无论查询方法返回什么)的 1024 个引用。
        缓存会被视为是 read/write(可读/可写)的缓存,意味着对象检索不是共享的,
        而且可以安全地被调用者修改,而不干扰其他调用者或线程所做的潜在修改。
        flushInterval(刷新间隔)可以被设置为任意的正整数,而且它们代表一个合理的毫秒形式的时间段。
        默认情况是不设置,也就是没有刷新间隔,
        缓存仅仅调用语句时刷新
     -->
    <!-- 使用默认的缓存的时候可以进行相应的配置 -->
    <cache eviction="FIFO" flushInterval="60000" size="512" readOnly="true"/>
    <!-- 开启缓存
        size(引用数目)	可以被设置为任意正整数,要记住你缓存的对象数目和你运行环境的 可用内存资源数目。默认值是 1024。
        readOnly(只读)	属性可以被设置为 true 或 false。只读的缓存会给所有调用者返回缓 存对象的相同实例。
                        因此这些对象不能被修改。这提供了很重要的性能优势。
                        可读写的缓存 会返回缓存对象的拷贝(通过序列化) 。
                        这会慢一些,但是安全,因此默认是 false。
        eviction 缓存策略：
                        LRU – 最近最少使用的:移除最长时间不被使用的对象。
                        FIFO – 先进先出:按对象进入缓存的顺序来移除它们。
                        SOFT – 软引用:移除基于垃圾回收器状态和软引用规则的对象。
                        WEAK – 弱引用:更积极地移除基于垃圾收集器状态和弱引用规则的对象。
     -->
    <cache type="S_Mybatis.e_自定义mybatis缓存.自定义缓存文件"></cache><!-- 自定义缓存 -->
    <!-- <cache-ref namespace="com.someone.application.data.SomeMapper"/> -->
    <!--参照缓存： 回想一下上一节内容, 这个特殊命名空间的唯一缓存会被使用或者刷新相同命名空间内的语句。
                也许将来的某个时候,你会想在命名空间中共享
                相同的缓存配置和实例。在这样的 情况下你可以使用 cache-ref 元素来引用另外一个缓存。
    -->
    <!-- 配置文件的参数问题
            使用ognl表达式可以讲表达式中的字符串动态的更换成想应的字符串类型
            #{property,javaType=int,jdbcType=NUMERIC}
            使用${xxx}只是动态的插入一个字符串的值
     -->
    <!-- 6.resultMap-mybatis中最重要和最关键的标签 -->
    <resultMap type="S_Mybatis.z_z_MyBatis实例.javabean.BeanOne" id="myid" >
        <!-- 
            1.resultMap标签的属性 
                        type-指定结果集的实现类
                        id-指定这个结果集的唯一id标识
                        automapping-是否启用自动映射
                        extends-表示使用
        -->
        <!-- 
            2.construction 
                    标签-当javabean中含有无参数的构造函数的时候可以使用这个方法进行构造注入
         -->
        <constructor>
            <!--注意当使用这个方法的时候 构造函数不能使用自动装箱的方法,也就是说int类型要写成Integer -->
            <idArg column="name" javaType="String" jdbcType="VARCHAR" />
            <!-- 使用这个方法进行构造的时候要保证参数的顺序是按照自己定义的顺序的 -->
            <arg column="name" javaType="String" jdbcType="VARCHAR"/>
        </constructor>
        <!-- id 属性和result属性 这两个属性是相同的效果的只不过id属性表示的是主键二result表示的是一般的键 -->
        <!-- 
            3.id和result的变量属性
                    column-指定进行映射的列名称(就是使用mysql数据库进行查询操作最后上面出现的一列) 
                    javaType-指定映射出来的java变量类型一般指定是基本的变量类型
                    property-指定需要映射的javabean的变量名称	 jdbcType-指定映射出来的数据变量类型
                    typeHandler-指定使用的转换器!!!必须在mybatis的配置文件中进行配置
        -->
        <!-- 使用参数注入的时候不必像构造注入的时候那样int类型必须转化成integer -->
        <id column="name" javaType="String" property="name" jdbcType="VARCHAR"/>
        <result column="age" javaType="String" jdbcType="VARCHAR" property="age"/>
        <!-- 4.设置一对多和一对一连级查询 -->
        <!--
             这两个属性可以使用嵌套模式 当使用其那套模式的时候需要进行相关的属性设置
            通过外链接的方法时 必须的属性！！	
                    property - 设置对应结果集的javabean中的参数
                   javatype(一对一)-
                   oftyp(一对多)(数据库开启了自动映射)-返回结果集的集合或者使用一个resultMap
           通过sql嵌套方法时 必须！！		
                           property - 设置对应结果集的javabean中的参数
                           colomn - 使用关联的列 
                           select - 调用的sql语句
       -->
        <!-- 一对一连级查询  pro表示类中对应的参数-->
        <association property="list" ></association>
        <!-- 一对多连级查询方法这个方法其实和传统的使用方法其实是没有什么区别的只不过需要将其中的属性编程一个集合
        (resultMap属性)并且保证关联集合中的属性名名称对应的数据库列植是通过数据库的查询出来的列值而不是自己在sql语句中定义的列值
        -->
        <collection property="list" column="x" resultMap="myid"></collection>
        <!-- 
            property 		生成结果集中javabean对应的属性!!
           automapping  	自动映射 让得到的数据库列明和声明的结果集（参数名） 相同
           column  		进行一对多sql分层注入的时 决定使用哪一列进行判断!!
           columnPrefix  	允许我们在重复出现的字段名前加上一个统一的字符前缀- 一般不用
           fetchType 		可选的。 有效值是lazy和eager。 
                           如果存在，它将取代此映射的全局配置参数lazyLoadingEnabled。
           jdbctype  		在这个表格之前的所支持的 JDBC 类型列表中的类型。JDBC 类型是仅仅 
                           需要对插入, 更新和删除操作可能为空的列进行处理。
                           这是 JDBC 的需要, jdbcType 而不是 MyBatis 的。
                           如果你直接使用 JDBC 编程,你需要指定这个类型-但 仅仅对可能为空的值。
           javatype		一个 Java 类的完全限定名,或一个类型别名(参考上面内建类型别名的列 表) 。
                           如果你映射到一个 JavaBean,MyBatis 通常可以断定类型。
                           然而,如 javaType 果你映射到的是 HashMap,那么你应该明确地指定 javaType 来保证所需的 行为。
           notnullcolomn 	默认情况下，仅当映射到子对象的属性的列中的至少一列非空时才创建子对象。 
                           使用此属性，您可以通过指定哪些列必须具有值来更改此行为，
                           因此只有当任何这些列不为null时，MyBatis才会创建子对象。 
                           可以使用逗号作为分隔符指定多个列名称。 默认值：unset。
           resultMap		!!
           resultSet
           typeHandle
           select    		!!表示用那个映射id的语句-查询的功能将会依次的进行查询先使用外层的查询语句然后在使用后面的查询语句
            oftype			返回的集合的每一个元素的属性
        -->
        <!-- 使用resultMap鉴别器 -鉴别器是使用在一个result中的里面的case属性的值将会使用外层定义的colum的属性的值都转化成
              javaTye后进行比较如果成立就会使用.里面定义的resultMap处理注意这就说明了映射的属性必须和原来的参数兼容否则就是不匹配的
         -->
        <discriminator javaType="S_Mybatis.z_z_MyBatis实例.javabean.BeanOne" column="xxx">
            <case value="1" resultMap="lll"></case>
        </discriminator>
        <!-- !!!!解决mybatis加载的性能问题 -->
        <!-- 解决办法使用延迟加载和使用非层级加载 在mybatis 的配置文件中进行相关的配置(这个配置方法是全局性的)
           当不是用全局性的变量的时候可以使用在xml属性中如(select)定义的属性fetchType(eager lazy-指定使用延迟加载)
         -->
    </resultMap>
    <resultMap type="S_Mybatis.z_z_MyBatis实例.javabean.BeanOne" id="lll" extends="yyy"></resultMap>
    <!-- 4.Sql动态语句  ognl的标准查看截图  注意#{xxx}不是ognl表达式 使用方法见上面的parameter -->
    <select id="xxx" parameterType="S_Mybatis.z_z_MyBatis实例.javabean.BeanOne">
        <!-- 
                这里使用的ognl表达式
        表达式的功能异常的强大他可以直接使用在变量作用域(parameterType中的yyy)中定义的变量名称别切可以调用变量的相关方法
        -->
        <!-- if就和java中的if语句插不多但是要注意使用转义字符-具体的自己查 -->
        <if test="name!=null"></if>
        <choose>
            <when test="name=null"></when><!-- if else-if else-->
            <otherwise></otherwise>
        </choose>
        <where><!-- 相当于 select语句中的where  当其中的条件语句完全成立的时候才加入 where语句-->
            <if test="xxx"></if><!-- 只用当之中的语句成立的时候才会动态的添加一个where否则不会添加where语句 -->
        </where><!-- 注意表达式中的ognl表达式中#相当于ActionContext. getContext();直接使用 参数就可以了 -->
        <!-- 通用where语句增强版 prefix-表示这段代码块的前缀,prefixOVerrides-表示填充这段代码的分割属性 -->
        <trim prefix="where" prefixOverrides="" suffix="" suffixOverrides=""></trim>
        <!-- 循环语句 -->
        <foreach collection="" close="" open=""></foreach>
        <!-- 
            collection - 一个数字或者list集合 
            item - 配置循环中的当前的元素
            index - 配置当前元素的下标
            open - close - 用什么元素将其中的 元素包裹起来
            separator - 各个元素的间隔符号
        -->
        <!-- 这个元素表示一个配置文件自己定义的上下文变量 -->
        <bind name="xx" value="xxx"/>
    </select>

    <!-- 参数传递方法 -->
    <select id="hehe" parameterType="o_EhCache缓存.ceshi.Javabean" >
        <!-- 使用这个表达式直接将xxx对象或者map中的属性自动的注入进来 -->
        <!-- parameterType="xxx.xxx"-mybaits的内置对象实现自动注入相关的属性 -->
        select * from xxx where name =#{id}
    </select>
</mapper>
```

SQL 映射文件有很少的几个顶级元素（按照它们应该被定义的顺序）：

- cache – 给定命名空间的缓存配置。
- cache-ref – 其他命名空间缓存配置的引用。
- resultMap – 是最复杂也是最强大的元素，用来描述如何从数据库结果集中来加载对象。
- parameterMap – 已废弃！老式风格的参数映射。内联参数是首选,这个元素可能在将来被移除，这里不会记录。
- sql – 可被其他语句引用的可重用语句块。
- insert – 映射插入语句
- update – 映射更新语句
- delete – 映射删除语句
- select – 映射查询语句

### 标签使用详解

#### select insert update delete

selete标签相关的属性

参数名|参数作用
---|---
id|在命名空间中唯一的标识符，可以被用来引用这条语句。
parameterType|将会传入这条语句的参数类的完全限定名或别名。这个属性是可选的，因为 MyBatis 可以通过 TypeHandler 推断出具体传入语句的参数，默认值为 unset。
parameterMap|这是引用外部 parameterMap 的已经被废弃的方法。使用内联参数映射和 parameterType 属性。
resultType|从这条语句中返回的期望类型的类的完全限定名或别名。注意如果是集合情形，那应该是集合可以包含的类型，而不能是集合本身。使用 resultType 或 resultMap，但不能同时使用。
resultMap|外部 resultMap 的命名引用。结果集的映射是 MyBatis 最强大的特性，对其有一个很好的理解的话，许多复杂映射的情形都能迎刃而解。使用 resultMap 或 resultType，但不能同时使用。
flushCache|将其设置为 true，任何时候只要语句被调用，都会导致本地缓存和二级缓存都会被清空，默认值：false。
useCache|将其设置为 true，将会导致本条语句的结果被二级缓存，默认值：对 select 元素为 true。
timeout|这个设置是在抛出异常之前，驱动程序等待数据库返回请求结果的秒数。默认值为 unset（依赖驱动）。
fetchSize|这是尝试影响驱动程序每次批量返回的结果行数和这个设置值相等。默认值为 unset（依赖驱动）。
statementType|STATEMENT，PREPARED 或 CALLABLE 的一个。这会让 MyBatis 分别使用 Statement，PreparedStatement 或 CallableStatement，默认值：PREPARED。
resultSetType|FORWARD_ONLY，SCROLL_SENSITIVE 或 SCROLL_INSENSITIVE 中的一个，默认值为 unset （依赖驱动）。
databaseId|如果配置了 databaseIdProvider，MyBatis 会加载所有的不带 databaseId 或匹配当前 databaseId的语句；如果带或者不带的语句都有，则不带的会被忽略。
resultOrdered|这个设置仅针对嵌套结果 select 语句适用：如果为 true，就是假设包含了嵌套结果集或是分组了，这样的话当返回一个主结果行的时候，就不会发生有对前面结果集的引用的情况。这就使得在获取嵌套的结果集的时候不至于导致内存不够用。默认值：false。
resultSets|这个设置仅对多结果集的情况适用，它将列出语句执行后返回的结果集并每个结果集给一个名称，名称是逗号分隔的。

#### insert update delete属性相关标签

参数名|参数作用
---|---
id|命名空间中的唯一标识符，可被用来代表这条语句。
parameterType|将要传入语句的参数的完全限定类名或别名。这个属性是可选的，因为 MyBatis 可以通过 TypeHandler|推断出具体传入语句的参数，默认值为 unset。
parameterMap|这是引用外部 parameterMap 的已经被废弃的方法。使用内联参数映射和 parameterType 属性。
flushCache|将其设置为 true，任何时候只要语句被调用，都会导致本地缓存和二级缓存都会被清空，默认值：true（对应插入、更新和删除语句）。
timeout|这个设置是在抛出异常之前，驱动程序等待数据库返回请求结果的秒数。默认值为 unset（依赖驱动）。
statementType|STATEMENT，PREPARED 或 CALLABLE 的一个。这会让 MyBatis 分别使用 Statement，PreparedStatement 或 CallableStatement，默认值：PREPARED。
useGeneratedKeys|（仅对 insert 和 update 有用）这会令 MyBatis 使用 JDBC 的 getGeneratedKeys|方法来取出由数据库内部生成的主键（比如：像 MySQL 和 SQL Server 这样的关系数据库管理系统的自动递增字段），默认值：false。
keyProperty|（仅对 insert 和 update 有用）唯一标记一个属性，MyBatis 会通过 getGeneratedKeys 的返回值或者通过 insert 语句的 selectKey 子元素设置它的键值，默认：unset。如果希望得到多个生成的列，也可以是逗号分隔的属性名称列表。
keyColumn|（仅对 insert 和 update 有用）通过生成的键值设置表中的列名，这个设置仅在某些数据库（像 PostgreSQL）是必须的，当主键列不是表中的第一列的时候需要设置。如果希望得到多个生成的列，也可以是逗号分隔的属性名称列表。
databaseId|如果配置了 databaseIdProvider，MyBatis 会加载所有的不带 databaseId 或匹配当前 databaseId 的语句；如果带或者不带的语句都有，则不带的会被忽略。

**注意**：useGeneratedKeys keyProperty keyColumn parameterType主要用来进行 自增加主键的 回调操作，就是当进行插入操作的之后，自动生成的主键重新注入到传入的 parameterType对应的javabean中，（底层使用jbdc的getGeneratedKeys方法）

#### selectKey 和 keyProperty keyColumn 结合使用进行主键回填操作

在insert 和 update 标签中才会有用的一个标签   会在执行语句之前先进行一次查询，并将得到的数据放入 keyProperty属性指定名称的字段中（调用传入的变量的keyproperty指定名称的地方）作为后面进行操作的数据，一般用在 对于不支持自动生成类型的数据库或可能不支持自动生成主键 JDBC 驱动，来生成主键。

参数名|参数作用
---|---
keyProperty|selectKey 语句结果应该被设置的目标属性。如果希望得到多个生成的列，也可以是逗号分隔的属性名称列表。
keyColumn|匹配属性的返回结果集中的列名称。如果希望得到多个生成的列，也可以是逗号分隔的属性名称列表。   注意 Property和Column一一对应
resultType|结果的类型。MyBatis 通常可以推算出来，但是为了更加确定写上也不会有什么问题。MyBatis 允许任何简单类型用作主键的类型，包括字符串。如果希望作用于多个生成的列，则可以使用一个包含期望属性的 Object 或一个 Map。
order|这可以被设置为 BEFORE 或 AFTER。如果设置为 BEFORE，那么它会首先选择主键，设置 keyProperty 然后执行插入语句。如果设置为 AFTER，那么先执行插入语句，然后是 selectKey 元素 – 这和像 Oracle 的数据库相似，在插入语句内部可能有嵌入索引调用。
statementType|与前面相同，MyBatis 支持 STATEMENT，PREPARED 和 CALLABLE 语句的映射类型，分别代表 PreparedStatement 和 CallableStatement 类型。

```xml
<insert id="insertAuthor">
    <selectKey keyProperty="id" resultType="int" order="BEFORE">
        select CAST(RANDOM()*1000000 as INTEGER) a from SYSIBM.SYSDUMMY1
    </selectKey>
    insert into Author
    (id, username, password, email,bio, favourite_section)
    values
    (#{id}, #{username}, #{password}, #{email}, #{bio}, #{favouriteSection,jdbcType=VARCHAR})
</insert>
```

#### sql标签和include 标签

sql和include 标签一般进行组合使用，形成各种参数化配置

```xml
<sql id="userColumns"> ${alias}.id,${alias}.username,${alias}.password </sql><!--设置相关的各种属性-->
<select id="selectUsers" resultType="map"><!--include标签动态的传入相关的属性-->
  select
    <include refid="userColumns"><property name="alias" value="t1"/></include>,
    <include refid="userColumns"><property name="alias" value="t2"/></include>
  from some_table t1
    cross join some_table t2
</select>
```

#### 结果集映射方法

查询语句

```xml
<!-- Very Complex Statement -->
<select id="selectBlogDetails" resultMap="detailedBlogResultMap">
    select
    B.id as blog_id,
    B.title as blog_title,
    B.author_id as blog_author_id,
    A.id as author_id,
    A.username as author_username,
    A.password as author_password,
    A.email as author_email,
    A.bio as author_bio,
    A.favourite_section as author_favourite_section,
    P.id as post_id,
    P.blog_id as post_blog_id,
    P.author_id as post_author_id,
    P.created_on as post_created_on,
    P.section as post_section,
    P.subject as post_subject,
    P.draft as draft,
    P.body as post_body,
    C.id as comment_id,
    C.post_id as comment_post_id,
    C.name as comment_name,
    C.comment as comment_text,
    T.id as tag_id,
    T.name as tag_name
    from Blog B
    left outer join Author A on B.author_id = A.id
    left outer join Post P on B.id = P.blog_id
    left outer join Comment C on P.id = C.post_id
    left outer join Post_Tag PT on PT.post_id = P.id
    left outer join Tag T on PT.tag_id = T.id
    where B.id = #{id}
</select>
```

结果集

```xml
<!-- Very Complex Result Map -->
<resultMap id="detailedBlogResultMap" type="Blog">
    <constructor>
        <idArg column="blog_id" javaType="int"/>
    </constructor>
    <result property="title" column="blog_title"/>
    <association property="author" javaType="Author">
        <id property="id" column="author_id"/>
        <result property="username" column="author_username"/>
        <result property="password" column="author_password"/>
        <result property="email" column="author_email"/>
        <result property="bio" column="author_bio"/>
        <result property="favouriteSection" column="author_favourite_section"/>
    </association>
    <collection property="posts" ofType="Post">
        <id property="id" column="post_id"/>
        <result property="subject" column="post_subject"/>
        <association property="author" javaType="Author"/>
        <collection property="comments" ofType="Comment">
            <id property="id" column="comment_id"/>
        </collection>
        <collection property="tags" ofType="Tag" >
            <id property="id" column="tag_id"/>
        </collection>
        <discriminator javaType="int" column="draft">
            <case value="1" resultType="DraftPost"/>
        </discriminator>
    </collection>
</resultMap>
```

#### resultmap标签

> 表示一个映射结果集

相关属性：

参数名|参数作用
---|---
id|当前命名空间中的一个唯一标识，用于标识一个result map.
type|类的全限定名, 或者一个类型别名 (内置的别名可以参考上面的表格).
autoMapping|如果设置这个属性，MyBatis将会为这个ResultMap开启或者关闭自动映射。这个属性会覆盖全局的属性autoMappingBehavior。默认值为：unset。

#### resultmap标签子标签

id&result设置对应结果集中类的各种参数，注意要有set方法，区别 id 表示的标识属性（一般就是表的主键）

```xml
<id property="id" column="post_id"/>
<result property="subject" column="post_subject"/>
```

相关属性

参数名|参数作用
---|---
property|映射到列结果的字段或属性。如果匹配的是存在的,和给定名称相同 的 JavaBeans 的属性,那么就会使用。否则 MyBatis 将会寻找给定名称 property 的字段。这两种情形你可以使用通常点式的复杂属性导航。比如,你 可以这样映射一些东西: “username” ,或者映射到一些复杂的东西: “address.street.number” 。
column|从数据库中得到的列名,或者是列名的重命名标签。这也是通常和会 传递给 resultSet.getString(columnName)方法参数中相同的字符串。
javaType|一个 Java 类的完全限定名,或一个类型别名(参考上面内建类型别名 的列表) 。如果你映射到一个 JavaBean,MyBatis 通常可以断定类型。 然而,如果你映射到的是 HashMap,那么你应该明确地指定 javaType 来保证所需的行为。
jdbcType|在这个表格之后的所支持的 JDBC 类型列表中的类型。JDBC 类型是仅 仅需要对插入,更新和删除操作可能为空的列进行处理。这是 JDBC jdbcType 的需要,而不是 MyBatis 的。如果你直接使用 JDBC 编程,你需要指定 这个类型-但仅仅对可能为空的值。
typeHandler|我们在前面讨论过默认的类型处理器。使用这个属性,你可以覆盖默 认的类型处理器。这个属性值是类的完全限定名或者是一个类型处理 器的实现,或者是类型别名。

#### constructor标签

constructor标签 使用构造方法进行注入，注意必须提供相对应的构造方法，参数的书写顺序和构造函数的顺序相同（3.4.3起可以不同但是要对构造函数添加@Param注解，和启用useActualParamname）

```xml
<constructor>
    <idArg column="id" javaType="int" name="id" />
    <arg column="age" javaType="_int" name="age" />
    <arg column="username" javaType="String" name="username" />
</constructor>
```

相关属性

参数名|参数作用
---|---
column|来自数据库的类名,或重命名的列标签。这和通常传递给 resultSet.getString(columnName)方法的字符串是相同的。
javaType|一个Java 类的完全限定名,或一个类型别名(参考上面内建类型别名的列表)。如果你映射到一个 JavaBean,MyBatis 通常可以断定类型。然而,如 果你映射到的是 HashMap,那么你应该明确地指定 javaType 来保证所需的 行为。
jdbcType|在这个表格之前的所支持的 JDBC 类型列表中的类型。JDBC 类型是仅仅 需要对插入, 更新和删除操作可能为空的列进行处理。这是 JDBC 的需要, jdbcType 而不是 MyBatis 的。如果你直接使用 JDBC 编程,你需要指定这个类型-但 仅仅对可能为空的值。
typeHandler|我们在前面讨论过默认的类型处理器。使用这个属性,你可以覆盖默认的 类型处理器。这个属性值是类的完全限定名或者是一个类型处理器的实现, 或者是类型别名。
select|用于加载复杂类型属性的映射语句的ID,从column中检索出来的数据，将作为此select语句的参数。具体请参考Association标签。
resultMap|ResultMap的ID，可以将嵌套的结果集映射到一个合适的对象树中，功能和select属性相似，它可以实现将多表连接操作的结果映射成一个单一的ResultSet。这样的ResultSet将会将包含重复或部分数据重复的结果集正确的映射到嵌套的对象树中。为了实现它, MyBatis允许你 “串联” ResultMap,以便解决嵌套结果集的问题。想了解更多内容，请参考下面的Association元素。
name|构造方法形参的名字。通过指定具体的名字你可以以任意顺序写入arg元素。参看上面的解释。从3.4.3版本起。

#### cache-二级缓存

默认情况下只是默认开启了一级缓存，也就是对同一个sqlsession缓存相关的各种数据，开起二级缓存将会在sqlsessionFactory级别进行缓存，缓存的数据所有的sqlsession共享

```xml
<cache eviction="FIFO" flushInterval="60000" size="512"  readOnly="true"/> 
```

参数名|参数作用
---|---
eviction|回收策略，LRU – 最近最少使用的:移除最长时间不被使用的对象。 FIFO – 先进先出:按对象进入缓存的顺序来移除它们。 SOFT – 软引用:移除基于垃圾回收器状态和软引用规则的对象。WEAK – 弱引用:更积极地移除基于垃圾收集器状态和弱引用规则的对象。
flushInterval(刷新间隔)|可以被设置为任意的正整数,而且它们代表一个合理的毫秒 形式的时间段。默认情况是不设置,也就是没有刷新间隔,缓存仅仅调用语句时刷新。
size(引用数目)|可以被设置为任意正整数,要记住你缓存的对象数目和你运行环境的 可用内存资源数目。默认值是 1024
readOnly(只读)|属性可以被设置为 true 或 false。只读的缓存会给所有调用者返回缓 存对象的相同实例。因此这些对象不能被修改。这提供了很重要的性能优势。可读写的缓存 会返回缓存对象的拷贝(通过序列化) 。这会慢一些,但是安全,因此默认是 false。

#### 引申mybatis使用自定义缓存

除了这些自定义缓存的方式, 你也可以通过实现你自己的缓存或为其他第三方缓存方案 创建适配器来完全覆盖缓存行为。

```xml
<cache type="com.domain.something.MyCustomCache"/>
```

这个示 例展 示了 如何 使用 一个 自定义 的缓 存实 现。type 属 性指 定的 类必 须实现 org.mybatis.cache.Cache 接口。这个接口是 MyBatis 框架中很多复杂的接口之一,但是简单 给定它做什么就行。

```java
public interface Cache {
    String getId();

    int getSize();

    void putObject(Object key, Object value);

    Object getObject(Object key);

    boolean hasKey(Object key);

    Object removeObject(Object key);

    void clear();
} 
```

要配置你的缓存, 简单和公有的 JavaBeans 属性来配置你的缓存实现, 而且是通过 cache 元素来传递属性, 比如, 下面代码会在你的缓存实现中调用一个称为 “setCacheFile(String file)” 的方法:

```xml
<cache type="com.domain.something.MyCustomCache">
    <property name="cacheFile" value="/tmp/my-custom-cache.tmp"/>
</cache>
```

你可以使用所有简单类型作为 JavaBeans 的属性,MyBatis 会进行转换。 And you can specify a placeholder(e.g. ${cache.file}) to replace value defined at configuration properties.

从3.4.2版本开始，MyBatis已经支持在所有属性设置完毕以后可以调用一个初始化方法。如果你想要使用这个特性，请在你的自定义缓存类里实现 org.apache.ibatis.builder.InitializingObject 接口。

```java
public interface InitializingObject {
    void initialize() throws Exception;
} 
```



