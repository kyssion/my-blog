# 上下文解析到底

上下文解析的本质是：在几十毫秒内，把一个"裸请求"变成一个"富特征向量"，供下游定向、召回、排序使用。

# 原始请求中有什么

在DSP系统中，本质上这个请求是一个RTB协议，不同的公司有不同的标准，这里行业标准OpenRTB协议为例

## OpenRTB协议

真实的 RTB Bid Request 长这样（简化版）里面涵盖了各种用户信息

```json
{
  "id": "req-abc-123",
  "imp": [{
    "id": "1",
    "banner": { "w": 320, "h": 250 },
    "bidfloor": 0.5,
    "tagid": "slot_feed_001"
  }],
  "site": {
    "domain": "news.example.com",
    "page": "https://news.example.com/tech/ai-2024.html",
    "cat": ["IAB19"],           // 页面分类
    "ref": "https://google.com"
  },
  "app": {
    "bundle": "com.example.newsapp",
    "name": "ExampleNews",
    "cat": ["IAB12"]
  },
  "device": {
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)...",
    "ip": "116.232.xxx.xxx",
    "geo": { "lat": 31.23, "lon": 121.47 },
    "make": "Apple",
    "model": "iPhone 15",
    "os": "iOS",
    "osv": "17.0",
    "devicetype": 4,
    "ifa": "8A2E0370-...",      // IDFA
    "connectiontype": 2          // WiFi
  },
  "user": {
    "id": "user_hash_456",
    "buyeruid": "dsp_mapped_789"
  }
}
```

# 原始请求解析

原始请求的解析主要包括以下的流程

原始请求（HTTP/SDK上报）
    │
    ├── ① 设备与环境解析
    ├── ② 地理位置解析
    ├── ③ 用户身份识别与映射
    ├── ④ 页面/内容语义理解
    ├── ⑤ 场景与意图识别
    ├── ⑥ 隐私信号解析
实时特征拼装
    │
    ▼
富化后的请求上下文（Request Context）→ 传给下游 Targeting（定向） / Recall（召回） / Ranking（排序）

## 1. 设备与环境解析

目标： 识别设备的特征化信息，比如手机，浏览器，操作系统等等信息。 

企业的一些做法

| 公司/平台         | 做法                                                                 |
|------------------|----------------------------------------------------------------------|
| Google DV360     | 内部维护海量 UA 映射表 + 设备能力数据库（屏幕尺寸、是否支持 MRAID/VPAID 等） |
| 巨量引擎（字节）   | SDK 直接上报设备型号、分辨率、存储空间等；服务端有机型库映射到价格段（用于消费能力推断） |
| 阿里妈妈          | UMID（统一设备指纹）体系，设备型号 → 映射到「设备档次」特征，直接用于排序模型     |

以web端为例

```
原始: "Mozilla/5.0 (Linux; Android 13; SM-S9180) AppleWebKit/537.36..."
         │
         ▼  UA Parser / DeviceAtlas / WURFL / 51Degrees
解析结果:
  ├── device_brand:  Samsung
  ├── device_model:  Galaxy S23 Ultra
  ├── os:            Android
  ├── os_version:    13
  ├── browser:       Chrome
  ├── browser_ver:   118
  ├── screen_size:   large
  ├── device_type:   smartphone
  └── price_tier:    high-end (>5000元)    ← 设备价格档位推断
```
关键工程点：
- UA 解析库需要持续更新（新设备/新浏览器不断出现）
- 很多团队维护一份 机型 → 价格/档次映射表，每季度更新
- 设备信息直接影响广告格式选择（如是否支持视频、互动广告）

## 2.  地理位置解析

目标：将原始的IP / GPS转化为 国家 / 省 / 市 / 区 / 商圈 / POI 这种信息

```
输入源（优先级从高到低）:
  1. GPS 坐标（用户授权时，精度最高）
  2. Wi-Fi 定位 / 基站定位
  3. IP 地址（兜底，精度最低）

         │
         ▼

┌──────────────────────────────┐
│  IP → 地理位置映射            │
│  - MaxMind GeoIP2            │
│  - IP2Location               │
│  - 国内：IPIP / 埃文科技      │
│  - 自建 IP 库             │
│    (结合用户行为校准)          │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  GPS → 行政区 + 商圈 + POI   │
│  - 逆地理编码（Reverse Geo）  │
│  - 高德/百度/腾讯地图 API     │
│  - 自建网格索引（GeoHash/S2） │
└──────────┬───────────────────┘
           │
           ▼
  解析结果:
  ├── country:     CN
  ├── province:    上海市
  ├── city:        上海市
  ├── district:    浦东新区
  ├── geohash:     wtw3sm
  ├── biz_circle:  陆家嘴      ← 商圈
  ├── nearby_poi:  [上海中心大厦, 正大广场, ...]
  └── scene_hint:  office_area  ← 场景推断（写字楼区 → 白领）
```

业内公司常见做法

| 公司           | 做法                                                                 |
|----------------|----------------------------------------------------------------------|
| 美团           | 自建 POI 体系 + 配送地址数据 → 精确到「小区/写字楼」级别的位置理解；LBS 广告的核心优势 |
| 巨量引擎       | GeoHash 网格化 + 商圈库；支持 "到店" 场景广告主按商圈投放                     |
| Google Ads     | IP-based + GPS；支持 radius targeting（半径定向），实时判断用户是否在目标区域内     |

生产中怎么处理
MaxMind 提供的 GeoIP 服务是行业标准——通过非侵入式的 IP 地理定位和情报数据来为内容和广告提供区域化服务，覆盖 99.9999% 在用的 IP 地址。 MaxMind
生产中的具体实现方式是：
离线下载 MaxMind 的 MMDB 数据库文件（GeoIP2-City.mmdb，大小约 60-80MB），这些可下载的数据库会定期更新，可以本地托管，非常适合高流量应用场景——消除了按次查询的费用和网络延迟。 MaxMind
在广告服务进程启动时，将整个 MMDB 文件加载到内存，使用 mmap 或直接读入堆外内存。MaxMind 提供了 C/Java/Go/Python 等多语言的 Reader 库，底层是一棵优化过的 B-tree 结构。
每次请求到达时，用 IP 做一次内存中的树查找，返回 country code、region/state、city、postal code、latitude/longitude、ISP、connection type、ASN 等信息。单次查询延迟：< 0.1ms。
数据库定期更新（通常每周），通过热加载的方式替换内存中的数据库引用，不需要重启服务。

即使是 Ethical Ad Server 这样的开源广告服务器也使用 MaxMind 创建的 GeoLite2 数据来做地理定位。 Readthedocs这说明从小型开源方案到 Google AdX 级别的系统，MaxMind 都是基础设施级别的组件。
补充：GPS 数据的处理。 当客户端上报了 GPS 经纬度时，系统会做一次反向地理编码（reverse geocoding），将经纬度映射为行政区划（省/市/区）。这通常通过本地的 GeoHash 索引或预构建的多边形匹配表完成，而不是实时调用 Google Maps API（太慢、太贵）。

## 3. 用户身份识别与 ID 映射

目标： 把各种 ID 统一到一个用户身份，连接用户画像

```json
请求中可能携带的 ID:
  ├── IDFA / GAID / OAID          （设备广告标识符）
  ├── IMEI / Android ID           （逐渐受限/不可用）
  ├── Cookie ID                    （Web 端）
  ├── 登录账号 ID                  （App 内登录态）
  ├── 手机号 hash                  （隐私合规下的ID）
  └── 设备指纹                     （多维信息生成的虚拟 ID）

         │
         ▼
┌──────────────────────────────────┐
│  ID Mapping Service              │
│                                  │
│  Cookie_A ──┐                    │
│  IDFA_B  ───┼──→ unified_uid_001 │
│  Login_C ───┘                    │
│                                  │
│  实现: ID-Graph (图存储)          │
│  - 确定性匹配 (同设备登录)        │
│  - 概率性匹配 (设备指纹相似度)    │
└──────────┬───────────────────────┘
           │
           ▼
  用统一 ID 去查询用户画像（Feature Store）
```

业内公司常见做法

| 公司                              | 做法                                                                                     |
|----------------------------------|------------------------------------------------------------------------------------------|
| 阿里（UMID + UTDID）             | 统一设备 ID 体系，覆盖淘宝/支付宝/优酷等全生态；用确定性 ID（登录态）+ 设备指纹构建 ID Graph |
| Meta                             | 强登录态生态，用 Facebook/Instagram 账号做跨设备串联；Privacy-Enhanced Technologies (PETs) 做 hashed 匹配 |
| The Trade Desk (TTD)             | 推出 Unified ID 2.0 (UID2)，基于加密邮箱的开放 ID 体系，替代三方 Cookie                   |
| LiveRamp                         | 行业级 Identity Resolution 服务，RampID 做跨平台人匹配                                     |

**用户的ID 来源**
Web 场景：第三方 Cookie（正在消亡）、Publisher 的第一方 Cookie、登录态的 email hash
App 场景：iOS 的 IDFA（需 ATT 授权）、Android 的 GAID/OAID、App 内自定义的设备 ID
国内场景：OAID（华为/OPPO/vivo 等厂商联盟）、CAID（中国广告协会）、手机号 MD5/SHA256

生产中怎么处理
**ID 映射在生产中分为两个层次：**
层次一：**跨平台 ID 同步（Cookie Sync）**。 这是 RTB 生态中 DSP 和 Exchange 之间的标准操作。OpenRTB User 对象中的 buyeruid 字段就是 Exchange 为买方映射的用户 ID，这个值通常来自 ID 同步过程。 GitHub具体实现是：当用户浏览网页时，Exchange 的 pixel 和 DSP 的 pixel 各自种下 Cookie，然后通过一次 redirect 交换彼此的 Cookie ID，建立映射关系。这个映射表存储在分布式 KV 存储中（如 Aerospike、Redis Cluster），供请求时查询。
层次二：**跨设备 ID Graph**。 大型广告平台（Meta、Google、字节）会维护一张 ID Graph，将同一个人在手机、平板、PC 上的不同 ID 关联起来。构建方式包括：确定性匹配（同一登录账号关联的所有设备）和概率性匹配（基于 IP + UA + 行为模式推断的设备关联）。这张图通常存储在图数据库或定制的分布式存储中，每天离线更新，请求时只做查表。
工程关键点：ID 映射表的规模非常大（数十亿级 KV 对），但每次查询只需要一次点查（GET by key），延迟在 1-3ms。

### unified_uid 广告内部唯一标识

unified_uid 不是某一个原始 ID，而是广告系统内部自己生成和维护的一个统一身份标识，它的作用是把同一个自然人在不同设备、不同平台上的多个原始 ID 关联到一起。

```
一个真实用户可能有这些原始 ID：
├─ 手机上的 IDFA（iOS）
├─ 手机上的 OAID（Android）
├─ PC 浏览器上的 Cookie ID
├─ 登录后的 Login UID
├─ 小程序里的 OpenID
└─ ...

           ┌─────────────────┐
  IDFA ───→│                 │
  OAID ───→│  ID-Mapping     │──→ unified_uid = "U_8a3f9c2d"
Cookie ───→│  Service        │
Login  ───→│                 │
           └─────────────────┘
```

### unified_uid 冷启动

这里就有一些列的问题 : 1. 有原始ID ，但是没有unified_uid 怎么办。 2. 如果没有这些原始ID 怎么办 这就是常见的冷启动问题，我们需要生成新的unified_uid 

**1. 有原始ID ，但是没有unified_uid**
核心原则是：第一次遇到一个从未见过的原始 ID 时，就为它生成一个新的 unified_uid。

```json
广告请求进入，携带原始 ID（比如 device_id = "ABC123"）
  │
  ▼
查 ID-Mapping 存储：device_id "ABC123" → unified_uid ?
  │
  ├─ 命中：返回已有的 unified_uid，结束
  │
  └─ 未命中：这是一个全新设备
       │
       ▼
     生成新的 unified_uid
       │
       ▼
     写入映射关系：device_id "ABC123" → unified_uid "U_xxxx"
       │
       ▼
     返回新的 unified_uid，后续链路正常执行
```

**2. 如果没有这些原始ID 怎么办**

这是当下广告行业最头疼的问题，尤其是 2021 年 iOS 14.5 推出 ATT 之后，整个行业都在被迫重构身份识别体系。

现状 ： 

```json
iOS 端（最严重）：
├─ IDFA：ATT 弹窗后，全球大约只有 20%-35% 的用户允许追踪
├─ IDFV：同一开发者的 App 内可用，跨 App 不行
├─ Cookie：Safari ITP 限制第三方 Cookie，第一方 Cookie 也只有 7 天
└─ IP：iCloud Private Relay 开启后 IP 也被隐藏

Android 端（正在收紧）：
├─ GAID：Google 已宣布逐步弃用
├─ OAID（国内）：目前还能用，但政策在收紧
└─ Cookie：Chrome 第三方 Cookie 虽然多次推迟，但方向不变

Web 端：
├─ 第三方 Cookie：Firefox/Safari 已禁，Chrome 在推 Privacy Sandbox
├─ 浏览器指纹：各大浏览器在主动对抗指纹识别
└─ IP：越来越多的 VPN 和隐私代理
```


**1. 解决方案一：第一方数据体系**

这是目前全行业最重视的方向。核心思路是不依赖第三方标识，靠自己平台的登录体系建立身份。
比如字节跳动内部各个APP打通自己的账号体系，或者天猫淘宝这样的情况

```
具体做法：
├─ 强化登录引导
│   ├─ 用产品价值驱动用户主动登录（不登录就限制功能）
│   ├─ 提供一键登录（手机号验证码、微信/Google 授权登录）
│   └─ 登录后的 login_uid 就是最可靠的 unified_uid 来源
│
├─ 第一方 Cookie / SDK Token
│   ├─ 用户访问你的站点/App 时，你自己种的第一方标识
│   ├─ 不受第三方 Cookie 限制
│   └─ 在你自己的域/App 内始终有效
│
└─ 数据清洁室（Data Clean Room）
    ├─ 广告主和媒体各自把第一方数据加密后放进去
    ├─ 在安全环境中做匹配，双方都看不到对方原始数据
    └─ Google Ads Data Hub、Meta 的 CAPI 都是这个思路
```


**说一下数据清洁室（Data Clean Room） 的核心原理**

| 特性 | Google Ads Data Hub (ADH) | Meta Conversions API (CAPI) |
| :--- | :--- | :--- |
| 本质 | 数据分析平台 (Data Warehouse/Analytics) | 数据传输接口 (Data Pipeline/API) |
| 主要目的 | 深度洞察、自定义归因、隐私安全的研究 | 数据回传、修复丢失的转化信号、优化投放 |
| 数据流向 | 数据汇入 ADH -> 内部 SQL 分析 -> 输出聚合结果/受众 | 你的服务器 -> 直接发送给 Meta 服务器 |
| 隐私处理 | 极度严格：禁止导出行级用户数据，强制聚合 | 灵活：由广告主决定发送哪些字段（需哈希处理 PII） |
| 使用门槛 | 较高（需要 SQL 技能，通常面向大型企业或代理商） | 中等（可通过合作伙伴集成、GTG 服务器或自行开发） |
| 生态系统 | 专注于 Google 生态 (YouTube, Search, Display) | 专注于 Meta 生态 (Facebook, Instagram, WhatsApp) |
| 典型场景 | "我想分析 YouTube 广告对线下销售的长期贡献率" | "我的 iOS 用户购买数据在广告后台少报了 30%，需要补全" |

本质上，之前DSP是通过 广告的标识ID 来实现的媒体（比如APP或者网页）一个用户在媒体侧和DSP平台统一的。 现在使用数据或者接口进行匹配上， 比如 在媒体 一个用户A在广告位xxx上发起了一个广告。 每次侧有这个用户->广告位ID的映射关系，DSP 有，广告位ID->用户的特征的关系。 只要相互链接数据，就可以实现用户追踪了。 

**引申一下 ： 用户画像的数据怎么来**
```
画像数据来源（以穿山甲/字节为例）：

第一来源：字节自有 App 的数据
├─ 如果这个 OAID 在抖音上登录过
│   字节知道这个设备背后的用户在抖音的全部行为
│   搜索、浏览、点赞、购物、直播打赏 ...
│   这些数据极其丰富
└─ 这是字节做联盟广告最大的优势

第二来源：联盟内 SDK 收集的广告交互数据
├─ 这个 OAID 在所有嵌入穿山甲 SDK 的 App 中的广告行为
└─ 覆盖面广，但数据维度有限（只有广告相关的行为）

第三来源：广告主上传的人群包
├─ 广告主可以把自己的用户 ID 列表上传到平台
├─ 平台做 ID 匹配后形成定向人群包
└─ 这些用户即使在联盟流量中也能被精准定向
```

**解决方案二：层层降级+上下文匹配**

这才是真正困难的场景。广告平台会按优先级做层层降级：

```
第一步：尝试概率性 ID 匹配

SDK 上报的参数：
{
  IP: "202.96.134.xx",
  UA: "iPhone14,2/iOS17.2",
  屏幕: "1170x2532",
  语言: "zh-Hans",
  时区: "Asia/Shanghai",
  运营商: "中国移动",
  网络: "WiFi",
  ...
}

广告平台用这些参数组合做概率匹配：
├─ 在过去 N 小时内，有没有一个已知用户的参数组合
│   和当前请求高度相似？
├─ 如果有 → 大概率是同一个人 → 关联到已有画像
├─ 如果没有 → 进入下一步
│
├─ 匹配置信度不同，处理方式不同：
│   ├─ 高置信度（>90%）→ 直接使用完整画像
│   ├─ 中置信度（60%-90%）→ 使用画像但排序阶段降权
│   └─ 低置信度（<60%）→ 放弃匹配，走无 ID 逻辑

准确率：
├─ IP + 设备型号 + OS 版本 组合在短时间窗口内
│   准确率能到 60%-80%
├─ 但同一公司 WiFi 下几十台同型号 iPhone
│   准确率就很差了
└─ 所以这只是个兜底方案，不是主力

第二步：没有匹配上，构建实时临时画像

当完全无法关联到已有画像时：

├─ 生成一个临时 Session ID（这次会话内有效）
│
├─ 基于可用信息做粗粒度推断：
│   ├─ IP → 城市：上海
│   ├─ 设备型号 iPhone 15 Pro Max → 高消费力
│   ├─ 当前 App 是"得到" → 知识付费用户 → 高教育水平
│   ├─ 时间 23:30 → 夜间活跃
│   ├─ 网络 WiFi → 大概率在家
│   └─ 组合起来：上海、高消费力、高学历、夜间活跃
│       虽然粗糙，但已经能做有效的广告筛选了
│
├─ 用群体统计画像补充：
│   ├─ "上海 + iPhone 15 Pro Max + 晚间" 这个群体
│   │   历史上对哪些广告品类点击率高？
│   ├─ 用这个群体的统计特征作为当前用户的"伪画像"
│   └─ 这种做法在业内叫做 Lookalike 思路的变体
│
└─ 在会话内用户的每次广告交互都被 SDK 实时记录
    第一次展示了游戏广告 → 用户没点
    第二次展示了理财广告 → 用户点了
    → 实时更新临时画像：对理财感兴趣
    → 第三次请求时已经能做初步个性化了
```

还有一点，媒体广告主可以主动提供数据

```
联盟广告协议中，媒体可以在广告请求中附带：

├─ 媒体自己的用户 ID（如果用户在媒体 App 登录了）
├─ 当前页面的内容分类
│   如：小说 App 告诉广告平台"用户正在看言情小说"
├─ 用户在媒体内的行为标签
│   如：新闻 App 告诉广告平台"用户常看科技频道"
├─ 用户的基础属性（如果媒体掌握）
│   如：注册时填写的性别、年龄
│
└─ 这些数据通过 SDK 的扩展参数接口传递：
   AdRequest.setUserData({
     gender: "male",
     age_range: "25-30",
     content_category: "romance_novel",
     user_tag: ["frequent_reader", "premium_user"]
   })
```


## 4. 页面/内容语义理解（最复杂的部分）

这是上下文解析中技术含量最高的环节，不同场景差异很大：

**1. 场景 A：Web 页面广告**

```json

输入: page_url = "https://news.example.com/auto/tesla-model-y-review-2024.html"

         │
         ▼
┌──────────────────────────────────────────┐
│  Step 1: URL 级别快速分类                 │
│  - 域名 → 媒体类型 (新闻/电商/工具...)    │
│  - URL 路径关键词提取 (/auto/ → 汽车)     │
│  - 命中 URL → Category 缓存映射表         │
│  → 耗时: <1ms                            │
└──────────┬───────────────────────────────┘
           │ 如果缓存未命中
           ▼
┌──────────────────────────────────────────┐
│  Step 2: 页面内容抓取 + NLP 分析          │
│  - 预先爬虫 / 实时轻量抓取               │
│  - 正文提取 (Readability / Diffbot)      │
│  - 文本分类 → IAB Content Taxonomy       │
│    (28 大类 + 数百子类)                   │
│  - 关键词/实体提取 (NER)                 │
│    → "特斯拉", "Model Y", "电动汽车"     │
│  - 情感分析 (正面评测 vs 负面新闻)        │
│  → 耗时: 异步预处理，结果缓存             │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  Step 3: 品牌安全分类 (Brand Safety)      │
│  - GARM (Global Alliance for             │
│    Responsible Media) 分类框架            │
│  - 是否涉及: 暴力/色情/政治争议/...       │
│  - IAS / DoubleVerify / Oracle(Moat)     │
│    等第三方验证                           │
│  → 输出: brand_safety_level: safe/risky  │
└──────────┬───────────────────────────────┘
           │
           ▼
  page_context:
  ├── iab_category:    [IAB2-2: Auto-SUV]
  ├── keywords:        [特斯拉, Model Y, 电动车, 续航, 评测]
  ├── entities:        [{name: Tesla, type: Brand}, ...]
  ├── sentiment:       positive
  ├── brand_safety:    safe
  └── content_quality: high
```

一些头部企业的做法

| 公司                              | 做法                                                                                     |
|----------------------------------|------------------------------------------------------------------------------------------|
| Google AdSense / Ad Manager      | 大规模页面分类系统；抓取+分类覆盖数十亿页面；实时分类用轻量模型，复杂分类用异步 pipeline；Content Label 体系 |
| IAS (Integral Ad Science)        | 专业做页面级内容分析：语义分类 + 品牌安全 + 可见性；被众多 DSP 集成                         |
| GumGum                           | Contextual Intelligence 代表公司，用 CV + NLP 分析页面图文内容，做上下文定向                |

**2. 场景 B：信息流 / 短视频广告（字节、快手、微信等）**

```
用户正在浏览的内容（非广告）:
  ├── 刚看了一条 "新能源汽车对比" 视频
  ├── 之前看了 "家装设计" 图文
  └── 当前停留在 "数码评测" 频道

         │
         ▼
┌──────────────────────────────────────────┐
│  内容理解 Pipeline (离线 + 近实时)        │
│                                          │
│  视频 → 多模态理解:                       │
│  ├── ASR: 语音转文字                     │
│  ├── OCR: 视频帧文字识别                 │
│  ├── CV:  画面物体/场景识别              │
│  ├── NLP: 标题 + ASR文本 → 分类/标签     │
│  └── 多模态融合 → content_embedding       │
│                                          │
│  文章 → NLP:                             │
│  ├── 分词/NER/关键词                     │
│  ├── 文本分类（多级类目）                 │
│  └── 文本 embedding                      │
└──────────┬───────────────────────────────┘
           │
           ▼
  当前请求的「内容上下文」:
  ├── current_channel:      数码
  ├── recent_content_tags:  [新能源车, 家装, 数码评测]
  ├── **content_embedding:    [0.12, -0.34, 0.78, ...]**
  └── context_ad_category:  [汽车, 3C数码, 家居] ← 适合投放的广告类别
```

一些头部企业的做法

```
| 公司             | 做法                                                                                     |
|------------------|------------------------------------------------------------------------------------------|
| 字节跳动         | 内容理解是核心能力；视频用多模态模型（ASR+OCR+CV+NLP）提取标签和 embedding；广告投放时把用户正在看的内容的 embedding 作为上下文特征输入排序模型 |
| 快手             | 类似；短视频内容理解 + 上下文 embedding；场景特征（「发现页」vs「关注页」vs「直播间」）作为重要上下文 |
| 微信朋友圈广告   | 上下文更偏社交场景：时间段、用户活跃模式、朋友圈浏览深度等作为上下文信号                   |
```

**3. 场景 C：搜索广告**

```
用户搜索: "北京朝阳区 少儿英语培训 哪家好"

         │
         ▼
┌──────────────────────────────────────────┐
│  Query Understanding Pipeline            │
│                                          │
│  1. 分词:                                │
│     [北京, 朝阳区, 少儿, 英语, 培训, 哪家好]│
│                                          │
│  2. 意图识别:                             │
│     intent = commercial (有购买/消费意图)  │
│                                          │
│  3. NER (命名实体识别):                   │
│     location = 北京-朝阳区                │
│     service  = 少儿英语培训               │
│                                          │
│  4. Query 改写/扩展:                      │
│     同义扩展: [儿童英语, 幼儿英语, 英语班] │
│     上位扩展: [教育培训, 语言培训]         │
│                                          │
│  5. Query Embedding:                     │
│     q_emb = [0.23, -0.11, ...]           │
│                                          │
│  6. 行业分类:                             │
│     category = 教育-语言培训-少儿英语      │
└──────────────────────────────────────────┘
```

一些头部企业的做法

| 公司                     | 做法                                                                                     |
|--------------------------|------------------------------------------------------------------------------------------|
| 百度凤巢                 | 最成熟的中文搜索广告 Query 理解系统；分词 → 意图 → NER → Query 改写 → 触发广告关键词匹配（精确/短语/智能匹配） |
| Google Ads               | BERT-based query understanding；broad match 背后是深度语义匹配；近年大幅推广 Performance Max 自动化 |
| 阿里妈妈（直通车）       | 淘宝站内搜索广告；Query → 类目预测 + 属性提取 → 匹配商品/关键词                             |

**注意** ： 在真实的生产环境中，这些上下文信息会统一成64 位向量或者128维度向量，提前植入缓存中，不需要实时计算。 

## 5. 场景与时序信号

用户在页面或者APP中的使用情况和浏览记录信息

```
实时提取:
├── time_of_day:      14:30 (工作日下午)
├── day_of_week:      Wednesday
├── is_holiday:       false
├── session_depth:    第 15 次刷新 (深度用户)
├── session_duration: 已浏览 8 分钟
├── network:          WiFi (可能在室内/家中/办公室)
├── charging_status:  充电中 (可能静止使用)
├── app_usage:        前一个 App 是「大众点评」→ 可能有餐饮需求
└── ad_load:          本次会话已看过 3 条广告 → 调控广告密度
```

## 6. 隐私信号解析

数据怎么来
隐私信号来自多个来源：

CMP（Consent Management Platform）：网页上的 Cookie 弹窗让用户选择后，生成 GDPR Consent String（TCF v2 格式）
iOS ATT 框架：App 弹窗询问用户是否允许追踪，结果通过 app_tracking_authorization_status 字段传递
Publisher 声明：Publisher 可以声明某些请求不应做个性化广告

怎么处理
Google 的 BidRequest 中定义了 NonPersonalizedAdsReason 枚举来标识广告不应做个性化投放的原因——包括 Publisher 声明的非个性化广告请求和 Publisher 要求的限制数据处理等多种情况。 Google
在生产中，隐私信号的解析是一个路由决策过程：系统解析完这些信号后，会产出一个 targeting_mode 字段，它的值决定了下游所有环节的行为边界：
full_targeting：所有定向能力可用（行为定向、重定向、Lookalike 等）
limited_targeting：只能使用有限的数据（如 Google 的 Topics API）
contextual_only：只能使用上下文定向（页面内容、地理位置），不能使用任何用户级别的行为数据

这个字段会被注入到请求上下文中，在定向过滤、召回、竞价等每个环节被检查。

# 特征拼装 

所有解析结果最终汇聚到一个统一的请求上下文对象类似下面这样。 

```json
{
  "device_brand": "Apple",
  "device_model": "iPhone 15",
  "device_price": 7999,
  "os": "iOS",
  "os_ver": "17.0",
  "screen": "1179x2556",
  "network": "WiFi",

  "country": "CN",
  "city": "上海",
  "district": "浦东",
  "biz_circle": "陆家嘴",
  "geohash": "wtw3sm",

  "unified_uid": "u_abc_123",
  "id_type": "login",
  "id_confidence": 0.99,

  "content_category": ["IAB2-2"],
  "content_keywords": ["特斯拉", "电动车"],
  "content_embedding": [0.12, -0.34],
  "brand_safety": "safe",

  "hour": 14,
  "weekday": 3,
  "session_depth": 15,
  "ad_slot_id": "feed_pos_6",
  "ad_format": "native",

  "user_age_bucket": "25-34",
  "user_gender": "M",
  "user_interests": ["汽车", "科技", "旅行"],
  "user_purchase_power": "high",
  "recent_clicks": [
    {
      "ad_id": "x",
      "ts": 1710000000
    }
  ],
  "recent_conversions": [],
}
```

## 