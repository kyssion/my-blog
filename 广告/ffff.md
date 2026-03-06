Now I have enough material to give you a thorough answer. "上下文解析"在生产环境中并不是一个单体模块，而是由多个并行或串行的子系统协作完成的。我按照实际的数据流来拆解。

---

## 一、原始请求里到底带了什么

理解上下文解析的第一步，是搞清楚一次广告请求的原始载体长什么样。在程序化广告（RTB）场景下，这个载体就是 **OpenRTB BidRequest**——它是 IAB 定义的行业标准协议，几乎所有主流 Ad Exchange（Google AdX、Xandr、Index Exchange 等）都遵循。一次 RTB 交易始于 Exchange 向 Bidder 发送一个 bid request，它由顶层的 BidRequest 对象、至少一个 impression 对象组成，并可选地包含提供展示上下文的附加对象。

一个真实的 BidRequest JSON 大概长这样（来自公开的 OpenRTB 示例）：

```json
{
  "id": "d4b5c697-...",
  "imp": [{ "id": "1", "banner": {"w": 300, "h": 250}, "bidfloor": 0.5 }],
  "site": {
    "id": "12345",
    "domain": "sitedomain.com",
    "cat": ["IAB25-3"],
    "page": "https://sitedomain.com/page",
    "keywords": "lifestyle, humour"
  },
  "device": {
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 8_1_2 ...) ...",
    "ip": "8.8.8.8",
    "geo": {"lat": 0, "lon": 0, "country": "USA", "region": "CA", "city": "Mountain View"},
    "make": "Apple", "model": "iphone", "os": "iOS", "osv": "8",
    "connectiontype": 2,
    "ifa": "03F..."
  },
  "user": { "id": "57592f...", "buyeruid": "..." }
}
```

可以看到，BidRequest 里包含了 device 对象（UA 字符串、IP、设备型号、OS 版本、连接类型）、geo 对象（国家/地区/城市/经纬度）、site 或 app 对象（域名、页面 URL、IAB 内容分类、关键词），以及 user 对象（用户 ID、buyer UID）。

**上下文解析的任务，就是把这些半结构化的原始字段，解析、补全、映射成下游模型和定向系统能直接使用的标准化特征。**

---

## 二、五条并行的解析子链路

在生产环境中，为了把总延迟控制在个位数毫秒以内，这些子任务通常是**并行**执行的：

### 2.1 设备解析（Device Parsing）

**输入**：User-Agent 字符串 + 可选的 Client Hints（SUA 对象）

**做什么**：从 UA 字符串中提取操作系统（iOS/Android/Windows）、浏览器（Chrome/Safari）、设备型号、是否移动端等信息。业界通用的做法是在服务端解析 UA 字符串，使用正则表达式和 UA 解析库的组合来提取设备型号、操作系统及版本、浏览器及版本、平台类型等信息。

**生产案例**：

Google 的 Authorized Buyers 在 BidRequest 中同时传递传统的 `device.ua` 字符串和结构化的 `device.sua` 对象。其 proto 定义中包含了 `hardware_version`（如 iPhone12,1）、`limit_ad_tracking` 标志位，以及 App Tracking Transparency 状态等字段。之所以引入 SUA，是因为传统 UA 字符串在隐私趋势下被逐步冻结（Chrome 的 User-Agent Reduction），结构化数据是更可靠的替代。

在自有媒体（如抖音、微信朋友圈）场景中，客户端 SDK 会直接上报设备信息，不需要解析 UA 字符串——设备型号、OS 版本、屏幕分辨率、OAID/IDFA 等数据在 SDK 层就已经结构化了。

### 2.2 地理位置解析（Geo Resolution）

**输入**：IP 地址（必选）+ GPS 经纬度（可选，App 场景较多）

**做什么**：将 IP 地址映射为国家、省/州、城市、邮编、运营商（ISP）、连接类型等。

**生产案例**：

行业里的事实标准是 **MaxMind GeoIP**。MaxMind 的 GeoIP 数据可用于个性化地域内容和广告、分析流量、防止网络地理定位问题，数据有多种格式可供集成，包括可下载的本地数据库和通过 API 访问的 Web 服务。MaxMind 基本上创建了 IP 地理定位行业，仍然是其他服务对标的黄金标准，拥有超过 20 年的持续数据库优化，覆盖 99.9999% 的活跃 IP 地址。

在实际部署中，高 QPS 的广告系统会将 MaxMind 数据库（MMDB 格式）加载到本地内存，做纯内存查询，单次查询延迟在亚毫秒级。在 Google 的 OpenRTB 实现中，粗粒度的设备地理位置信息是基于广告请求来源 IP 地址近似估算的，经纬度代表一个圆的中心点，accuracy 字段表示其半径。

对于 App 场景，如果用户授权了 GPS 权限，客户端会上报精确的经纬度，精度可达几十米级。这时系统会优先使用 GPS 数据而非 IP 推断。

### 2.3 用户 ID 映射（Identity Resolution）

**输入**：请求中携带的各种 ID（Cookie ID、IDFA、OAID、设备指纹等）

**做什么**：将这些异构 ID 统一映射到系统内部的唯一用户标识（Unified ID），以便后续检索用户画像。

**生产案例**：

OpenRTB 的 User 对象中，`buyeruid` 是 Exchange 为买方映射的用户 ID，除非买卖双方有事先约定，否则这个值通常来自 ID 同步（Cookie Sync）过程。

在国内平台（如巨量引擎、腾讯广告）上，这一步更多是 OAID/CAID/手机号哈希等多 ID 的归一化。跨设备、跨 App 的 ID 打通（ID Graph）是这一步最复杂的部分——需要维护一张大规模的映射表来关联同一个人在不同设备和 App 上的 ID。

### 2.4 页面/内容语义解析（Content Classification）

**输入**：页面 URL、域名、页面关键词、页面正文（部分场景）

**做什么**：判断广告将要出现在什么类型的内容旁边——这既服务于定向投放（如投放到体育类页面），也服务于品牌安全（如避免出现在暴力内容旁边）。

**生产案例**：

这个领域有两层做法：

**第一层：Exchange 侧的标准分类。** 在 OpenRTB 中，Publisher 会在 `site.cat` 字段中声明页面的 IAB 内容分类（如 `IAB25-3` = 时尚）。但这个分类是 Publisher 自己打的，粒度粗、更新慢，可信度有限。

**第二层：第三方验证公司的深度分析。** 这是目前行业的主流做法。IAS 使用先进的上下文技术、机器学习和多媒体分类来实时评估内容，其专利的认知语义技术使用 NLP 来动态理解上下文的细微差别，包括情感和情绪分析。DoubleVerify 的 Universal Content Intelligence 引擎利用 AI 技术分析视频、图片、音频、语音、文本和链接，将信息分类到超过 100 个类别中供品牌选择屏蔽。

在 IAS 的实际运营中，关键词仅占买方开放网络流量中被屏蔽或标记的展示的 0.25%，绝大部分分类决策已经由 AI 驱动的全页面上下文分析完成。

在自有媒体平台上（如抖音信息流），内容语义分析更为深入——系统在内容发布阶段就已经用 NLP/CV 模型完成了文本分类、视频标签提取、情感分析等，这些标签直接存入内容索引，广告请求时只需查表，不需要实时分析。字节跳动的系统建立在内容分析和用户标签挖掘的基础之上，需要对内容和用户都进行标签提取，内容分析包括文本分析、图像分析和视频分析。

### 2.5 网络环境与隐私信号解析

**输入**：连接类型、隐私相关字段（GDPR consent string、CCPA 信号、ATT 状态等）

**做什么**：判断用户的网络环境（WiFi/4G/5G 影响素材选择——弱网环境下不应投放大尺寸视频广告），以及解析隐私合规信号以决定哪些定向能力可用。

Google 的 BidRequest 中包含了 `NonPersonalizedAdsReason` 枚举，标识广告不应做个性化投放的原因（如 Publisher 声明、用户隐私偏好等），以及 `limit_ad_tracking` 和 `app_tracking_authorization_status` 字段。

这些信号直接决定了下游的"定向过滤"环节能使用什么粒度的定向能力——如果用户处于 GDPR 严格限制下或 iOS ATT 拒绝追踪，系统只能使用上下文定向，不能使用行为定向。

---

## 三、解析结果怎么输出

所有子链路的解析结果最终汇聚成一个**标准化的 Feature Map**，类似：

```
request_features = {
  device_os: "iOS",
  device_model: "iPhone14,2",
  screen_size: "1170x2532",
  connection: "WiFi",
  geo_country: "CN",
  geo_province: "guangdong",
  geo_city: "shenzhen",
  geo_source: "GPS",          // GPS vs IP推断
  unified_user_id: "u_abc123",
  page_category: ["IAB19-6", "IAB19-18"],   // 科技-手机
  page_sentiment: "positive",
  brand_safety_level: "safe",
  privacy_mode: "full_targeting",  // vs limited vs contextual_only
  network_carrier: "China Mobile",
  time_of_day: 14,
  day_of_week: 5,
  ...
}
```

这个 Feature Map 会被后续的每一个环节消费：定向过滤用它匹配广告主的投放条件，召回用它做向量化检索的 query 构建，粗排/精排用它作为模型输入特征的一部分。

---

## 四、工程上的关键约束

整个上下文解析环节在生产中面临一个硬约束：**总延迟不能超过 5~10ms**。因为整条广告链路的端到端预算通常在 50~100ms 以内，留给上下文解析的窗口极其有限。

所以你会看到几个共性的工程选择：MaxMind 数据库加载到本地内存而非远程调用；UA 解析用预编译的正则引擎；页面语义分类在内容发布时预计算而非请求时实时分析；多个子链路并行执行而非串行瀑布。这些设计都是为了在极短时间内把原始请求翻译成模型和业务规则能理解的标准化语言。