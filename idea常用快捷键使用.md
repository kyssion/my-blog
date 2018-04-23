1. 查看这个类存在什么问题
```
F2
```


<select id="getActiveShopCount"  resultType="java.math.BigDecimal">
    SELECT count(DISTINCT(user_id)) FROM `order`
    <where>
        <if test="regionData != null">
            <choose>
                <when test="regionData.country >= 0 and regionData.province == 0">
                    country_id = #{regionData.country}
                </when>
                <when test="regionData.province > 0 and regionData.city == 0">
                    province_id = #{regionData.province}
                </when>
                <when test="regionData.city > 0 and regionData.district == 0">
                    city_id = #{regionData.city}
                </when>
                <when test="regionData.district > 0 and regionData.region == 0">
                    district_id = #{regionData.district}
                </when>
                <when test="regionData.region > 0 ">
                    region_id = #{regionData.region}
                </when>
            </choose>
        </if>
        <if test="startTime > 0">
            and `added_time` >= #{startTime}
        </if>
        <if test="endTime > 0">
            and #{endTime} >= `added_time`
        </if>
        <if test="channel > 0">
            and `channel_scope` = #{channel}
        </if>
    </where>
</select>

{
    "body":{
        "page":2,
        "list":[
            {
                "id":"1523958428899",
                "body":"ST001020203003",
                "sn":"123",
                "scope":"0/5/50/610",
                "remark":"dddd",
                "address":"河北 保定市 北市区 和平里街道 东风中路邢台银行",
                "name_py":"zhaochengxia",
                "tel":"15631276604",
                "real_name":"赵承霞测试",
                "scope_name":"中国 山西 大同市 城区",
                "add_time":1523958428899
            },
            {
                "id":"1523958428899",
                "body":"ST001020203003",
                "sn":"222",
                "scope":"0/5/50/610",
                "remark":"dddd",
                "address":"河北 保定市 北市区 和平里街道 东风中路邢台银行",
                "name_py":"zhaochengxia",
                "tel":"15631276604",
                "real_name":"赵承霞测试",
                "scope_name":"中国 山西 大同市 城区",
                "add_time":1523958428899
            }
        ],
        "all_page":12
    },
    "header":{
        "desc":"OK",
        "code":200
    }
}
