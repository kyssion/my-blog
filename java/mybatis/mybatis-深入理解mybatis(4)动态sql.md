## 深入理解mybatis（四）动态sql

通常使用动态 SQL 不可能是独立的一部分,MyBatis 当然使用一种强大的动态 SQL 语言来改进这种情形,这种语言可以被用在任意的 SQL 映射语句中。

MyBatis 3 大大提升了它们,现在用不到原先一半的元素就可以了。MyBatis 采用功能强大的基于 OGNL 的表达式来消除其他元素。

- if
- choose (when, otherwise)
- trim (where, set)
- foreach
-----
> 引申:ognl表达式介绍

MyBatis常用OGNL表达式

- e1 or e2
- e1 and e2
- e1 == e2,e1 eq e2
- e1 != e2,e1 neq e2
- e1 lt e2：小于
- e1 lte e2：小于等于，其他gt（大于）,gte（大于等于）
- e1 in e2
- e1 not in e2
- e1 + e2,e1 * e2,e1/e2,e1 – e2,e1%e2
- !e,not e：非，求反
- e.method(args)调用对象方法
- e.property对象属性值
- e1[ e2 ]按索引取值，List,数组和Map
- @class@method(args)调用类的静态方法
- @class@field调用类的静态字段值

> mybatis中的# 和 $

'#'会将字符串进行转译

```java
#{property,javaType=int,jdbcType=NUMERIC}
#{age,javaType=int,jdbcType=NUMERIC,typeHandler=MyTypeHandler} //指定类型处理器
#{height,javaType=double,jdbcType=NUMERIC,numericScale=2} //指定保留位数
```

'$'直接进行字符串替换

```java
ORDER BY ${columnName
```

-----

### if 关键字

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG WHERE state = ‘ACTIVE’ 
  <if test="title != null">
    AND title like #{title}
  </if>
  <if test="author != null and author.name != null">  <!--使用ognl表达式-->
    AND author_name like #{author.name}
  </if>
</select>
```

### choose, when, otherwise  关键字

相当于java中的switch语句

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG WHERE state = ‘ACTIVE’
  <choose>
    <when test="title != null">
      AND title like #{title}
    </when>
    <when test="author != null and author.name != null">
      AND author_name like #{author.name}
    </when>
    <otherwise>
      AND featured = 1
    </otherwise>
  </choose>
</select>
```

### trim, where, set 关键字

解决拼接字符串的时候，where and 等字段多余的问题

比如这样的语句

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG 
  WHERE 
  <if test="state != null">
    state = #{state}
  </if> 
  <if test="title != null">
    AND title like #{title}
  </if>
  <if test="author != null and author.name != null">
    AND author_name like #{author.name}
  </if>
</select>
```

如果这些条件没有一个能匹配上，最终的结果竟会变成这样

```xml
SELECT * FROM BLOG WHERE 
```

使用where标签包裹将会解决这个问题

```xml
<select id="findActiveBlogLike"
     resultType="Blog">
  SELECT * FROM BLOG 
  <where> 
    <if test="state != null">
         state = #{state}
    </if> 
    <if test="title != null">
        AND title like #{title}
    </if>
    <if test="author != null and author.name != null">
        AND author_name like #{author.name}
    </if>
  </where>
</select>
```

类似的 trim 相比 where 只是多了定制属性

```xml
<trim prefix="where" prefixOverrides="" suffix="" suffixOverrides=""></trim>
```

|参数|作用|
---|---
prefix|指定包裹块生成sql之后要添加的前缀
prefixOverrides|忽略第一个指定的标识符，可以使用| 表示多个语句
suffix|指定包裹块生成sql之后要添加的后缀
suffixOverrides|忽略最后一个指定的标识符，可以使用| 表示多个语句

set语句一般用在进行动态添加列属性

```xml
<update id="updateAuthorIfNecessary">
  update Author
    <set>
      <if test="username != null">username=#{username},</if>
      <if test="password != null">password=#{password},</if>
      <if test="email != null">email=#{email},</if>
      <if test="bio != null">bio=#{bio}</if>
    </set>
  where id=#{id}
</update>
```

### foreach

动态 SQL 的另外一个常用的必要操作是需要对一个集合进行遍历，通常是在构建 IN 条件语句的时候。比如：

```xml
<select id="selectPostIn" resultType="domain.blog.Post">
  SELECT *
  FROM POST P
  WHERE ID in
  <foreach item="item" index="index" collection="list"
      open="(" separator="," close=")">
        #{item}
  </foreach>
</select>
```

foreach 元素的功能是非常强大的，它允许你指定一个集合，声明可以用在元素体内的集合项和索引变量。它也允许你指定开闭匹配的字符串以及在迭代中间放置分隔符。这个元素是很智能的，因此它不会偶然地附加多余的分隔符。

**注意**：你可以将任何可迭代对象（如列表、集合等）和任何的字典或者数组对象传递给foreach作为集合参数。当使用可迭代对象或者数组时，index是当前迭代的次数，item的值是本次迭代获取的元素。当使用字典（或者Map.Entry对象的集合）时，index是键，item是值。