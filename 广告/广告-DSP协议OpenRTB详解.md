# OpenRTB 2.6 完整 Bid Request
## 完整 Bid Request JSON
```json
{
  "id": "80ce30c53c16e6ede735f123ef6e32361bfc7b22",
  "imp": [
    {
      "id": "1",
      "metric": [
        {
          "type": "viewability",
          "value": 0.85,
          "vendor": "EXCHANGE"
        }
      ],
      "banner": {
        "format": [
          { "w": 300, "h": 250 },
          { "w": 320, "h": 50 }
        ],
        "w": 300,
        "h": 250,
        "btype": [4],
        "battr": [13, 14],
        "pos": 1,
        "mimes": ["image/jpeg", "image/gif", "image/png"],
        "topframe": 1,
        "expdir": [2, 4],
        "api": [3, 5],
        "id": "banner-1",
        "ext": {}
      },
      "video": {
        "mimes": ["video/mp4", "video/x-flv", "application/javascript"],
        "minduration": 5,
        "maxduration": 30,
        "startdelay": 0,
        "maxseq": 3,
        "poddur": 90,
        "protocols": [2, 3, 5, 6],
        "w": 640,
        "h": 480,
        "podid": "pod-001",
        "podseq": 1,
        "plcmt": 1,
        "linearity": 1,
        "skip": 1,
        "skipmin": 15,
        "skipafter": 5,
        "slotinpod": 1,
        "mincpmpersec": 0.02,
        "battr": [13, 14],
        "maxextended": 30,
        "minbitrate": 300,
        "maxbitrate": 1500,
        "boxingallowed": 1,
        "playbackmethod": [1],
        "playbackend": 1,
        "delivery": [2],
        "pos": 1,
        "companionad": [
          {
            "id": "comp-1",
            "w": 300,
            "h": 250,
            "pos": 1,
            "battr": [13, 14],
            "expdir": [2, 4],
            "vcm": 1
          },
          {
            "id": "comp-2",
            "w": 728,
            "h": 90,
            "pos": 1,
            "battr": [13, 14]
          }
        ],
        "api": [1, 2],
        "companiontype": [1, 2],
        "durfloors": [
          { "mindur": 1, "maxdur": 15, "bidfloor": 5.00 },
          { "mindur": 16, "maxdur": 30, "bidfloor": 10.00 }
        ],
        "ext": {}
      },
      "native": {
        "request": "{\"ver\":\"1.1\",\"assets\":[{\"id\":1,\"required\":1,\"title\":{\"len\":90}},{\"id\":2,\"required\":1,\"img\":{\"type\":3,\"wmin\":100,\"hmin\":100}}]}",
        "ver": "1.1",
        "api": [3],
        "battr": [13, 14],
        "ext": {}
      },
      "pmp": {
        "private_auction": 1,
        "deals": [
          {
            "id": "AB-Agency1-0001",
            "bidfloor": 2.50,
            "bidfloorcur": "USD",
            "at": 1,
            "wseat": ["Agency1"],
            "wadomain": ["brand-a.com"],
            "guar": 0,
            "mincpmpersec": 0.05,
            "durfloors": [
              { "mindur": 1, "maxdur": 15, "bidfloor": 3.00 }
            ],
            "ext": {}
          }
        ],
        "ext": {}
      },
      "displaymanager": "MoPub",
      "displaymanagerver": "5.16.0",
      "instl": 0,
      "tagid": "agltb3B1Yi1pbmNyDQsSBFNpdGUY7fD0FAw",
      "bidfloor": 0.50,
      "bidfloorcur": "USD",
      "clickbrowser": 1,
      "secure": 1,
      "iframebuster": ["vendor1.com", "vendor2.com"],
      "rwdd": 0,
      "ssai": 0,
      "exp": 300,
      "qty": {
        "multiplier": 1.0,
        "sourcetype": 2,
        "vendor": "measurementvendor.com",
        "ext": {}
      },
      "dt": 1709712000000,
      "refresh": {
        "refsettings": [
          {
            "reftype": 1,
            "minint": 30,
            "ext": {}
          }
        ],
        "count": 2,
        "ext": {}
      },
      "ext": {}
    }
  ],
  "site": {
    "id": "102855",
    "name": "Awesome News Site",
    "domain": "www.awesomenews.com",
    "cattax": 2,
    "cat": ["IAB12", "IAB12-2"],
    "sectioncat": ["IAB12-2"],
    "pagecat": ["IAB12-2"],
    "page": "https://www.awesomenews.com/news/tech/article123.html",
    "ref": "https://www.google.com/search?q=tech+news",
    "search": "tech news",
    "mobile": 0,
    "privacypolicy": 1,
    "publisher": {
      "id": "pub-8953",
      "name": "Awesome Media Group",
      "cattax": 2,
      "cat": ["IAB12"],
      "domain": "awesomenews.com",
      "ext": {}
    },
    "content": {
      "id": "content-78901",
      "episode": 23,
      "title": "The Future of AI in 2025",
      "series": "Tech Deep Dive",
      "season": "Season 3",
      "artist": "John Smith",
      "genre": "Technology",
      "gtax": 9,
      "genres": ["600", "601"],
      "album": "",
      "isrc": "",
      "producer": {
        "id": "producer-001",
        "name": "Tech Media Inc.",
        "cattax": 2,
        "cat": ["IAB12"],
        "domain": "techmedia.com",
        "ext": {}
      },
      "url": "https://www.awesomenews.com/news/tech/article123.html",
      "cattax": 2,
      "cat": ["IAB12", "IAB19"],
      "prodq": 2,
      "context": 1,
      "contentrating": "G",
      "userrating": "4.5 stars",
      "qagmediarating": 1,
      "keywords": "AI,machine learning,technology,2025",
      "livestream": 0,
      "sourcerelationship": 1,
      "len": 600,
      "language": "en",
      "embeddable": 1,
      "data": [
        {
          "id": "content-data-001",
          "name": "Content Classifier",
          "segment": [
            { "id": "seg-100", "name": "tech_enthusiasts", "value": "high" }
          ]
        }
      ],
      "network": {
        "id": "network-abc",
        "name": "ABC Media Network",
        "domain": "abcmedia.com",
        "ext": {}
      },
      "channel": {
        "id": "channel-tech",
        "name": "ABC Tech Channel",
        "domain": "tech.abcmedia.com",
        "ext": {}
      },
      "ext": {}
    },
    "keywords": "tech,news,AI,startup",
    "inventorypartnerdomain": "contentpartner.com",
    "ext": {}
  },
  "app": null,
  "dooh": null,
  "device": {
    "geo": {
      "lat": 34.0522,
      "lon": -118.2437,
      "type": 1,
      "accuracy": 50,
      "lastfix": 10,
      "ipservice": 3,
      "country": "USA",
      "region": "CA",
      "regionfips104": "",
      "metro": "803",
      "city": "Los Angeles",
      "zip": "90001",
      "utcoffset": -480,
      "ext": {}
    },
    "dnt": 0,
    "lmt": 0,
    "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "sua": {
      "browsers": [
        {
          "brand": "Safari",
          "version": ["17", "0"]
        },
        {
          "brand": "AppleWebKit",
          "version": ["605", "1", "15"]
        }
      ],
      "platform": {
        "brand": "iOS",
        "version": ["17", "0"]
      },
      "mobile": 1,
      "architecture": "arm",
      "bitness": "64",
      "model": "iPhone 15",
      "source": 2,
      "ext": {}
    },
    "ip": "203.0.113.45",
    "ipv6": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
    "devicetype": 4,
    "make": "Apple",
    "model": "iPhone 15",
    "os": "iOS",
    "osv": "17.0",
    "hwv": "iPhone15,4",
    "h": 2556,
    "w": 1179,
    "ppi": 460,
    "pxratio": 3.0,
    "js": 1,
    "geofetch": 1,
    "flashver": "",
    "language": "en",
    "carrier": "VERIZON",
    "mccmnc": "311-480",
    "connectiontype": 6,
    "ifa": "AA000DFE-7416-8477-C70D-291F574D3447",
    "ext": {}
  },
  "user": {
    "id": "55816b39711f9b5acf3b90e313ed29e51665623f",
    "buyeruid": "dsp-user-abc-123456",
    "keywords": "sports,technology,travel",
    "customdata": "base85encodedstringhere",
    "geo": {
      "lat": 34.0195,
      "lon": -118.4912,
      "type": 2,
      "country": "USA",
      "region": "CA",
      "city": "Santa Monica",
      "zip": "90401",
      "ext": {}
    },
    "data": [
      {
        "id": "data-provider-1",
        "name": "BlueKai",
        "segment": [
          { "id": "seg-auto-001", "name": "auto intenders", "value": "", "ext": {} },
          { "id": "seg-travel-002", "name": "frequent travelers", "value": "", "ext": {} }
        ],
        "ext": {}
      },
      {
        "id": "data-provider-2",
        "name": "Lotame",
        "segment": [
          { "id": "seg-age-001", "name": "age_25-34", "value": "25-34", "ext": {} }
        ],
        "ext": {}
      }
    ],
    "consent": "CPXxRfAPXxRfAAfKABENB-CgAAAAAAAAAAYgAAAAAAAA",
    "eids": [
      {
        "inserter": "awesomenews.com",
        "source": "liveramp.com",
        "matcher": "liveramp.com",
        "mm": 1,
        "uids": [
          {
            "id": "XY1000bIVBVah9ium-sZ3ykhPiXQbEcUpn4GjctxSA",
            "atype": 3,
            "ext": {}
          }
        ],
        "ext": {}
      },
      {
        "inserter": "awesomenews.com",
        "source": "uidapi.com",
        "uids": [
          {
            "id": "a]2D(s:7Wq!jZ0h)tp97kOOX",
            "atype": 3,
            "ext": {}
          }
        ],
        "ext": {}
      }
    ],
    "ext": {}
  },
  "test": 0,
  "at": 1,
  "tmax": 150,
  "wseat": ["seat-001", "seat-002"],
  "bseat": [],
  "allimps": 0,
  "cur": ["USD"],
  "wlang": ["en", "zh"],
  "acat": [],
  "bcat": ["IAB25", "IAB7-39", "IAB26"],
  "cattax": 2,
  "badv": ["blockedadvertiser.com", "spammy-brand.com"],
  "bapp": ["com.example.blockedapp"],
  "source": {
    "fd": 0,
    "tid": "txn-abc-123-def-456",
    "pchain": "tag1:abc123:reseller",
    "schain": {
      "complete": 1,
      "ver": "1.0",
      "nodes": [
        {
          "asi": "awesomenews.com",
          "sid": "pub-8953",
          "rid": "bid-request-001",
          "name": "Awesome Media Group",
          "domain": "awesomenews.com",
          "hp": 1,
          "ext": {}
        },
        {
          "asi": "ssp-exchange.com",
          "sid": "12345",
          "rid": "80ce30c53c16e6ede735f123ef6e32361bfc7b22",
          "name": "SSP Exchange",
          "domain": "ssp-exchange.com",
          "hp": 1,
          "ext": {}
        }
      ],
      "ext": {}
    },
    "ext": {}
  },
  "regs": {
    "coppa": 0,
    "gdpr": 0,
    "us_privacy": "1YNN",
    "gpp": "DBABMA~CPXxRfAPXxRfAAfKABENB-CgAAAAAAAAAAYgAAAAAAAA",
    "gpp_sid": [6],
    "ext": {}
  },
  "ext": {}
}
```

---

## 逐层、逐字段解析

---

### 一、顶层对象：BidRequest

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"80ce30c5..."` | **必填。** 本次竞价请求的唯一标识，由 Exchange 生成。用于后续日志追踪、响应匹配。Exchange 可以对不同 DSP 发送不同的 ID。 |
| `imp` | `[...]` | **必填。** 展示机会数组（Impression），至少包含 1 个 `Imp` 对象。每个 Imp 代表页面上一个可竞价的广告位。 |
| `site` | `{...}` | **推荐。** 网站信息。当流量来自浏览器网页时使用。与 `app`、`dooh` 三者互斥，一个请求中只能出现其中一个。 |
| `app` | `null` | **推荐。** App 信息。本例为网页流量，故为 null。若为 App 流量则填充此对象。 |
| `dooh` | `null` | DOOH（数字户外广告）对象。本例不涉及户外广告，故为 null。 |
| `device` | `{...}` | **推荐。** 用户设备信息，包含硬件、操作系统、地理位置、运营商等。 |
| `user` | `{...}` | **推荐。** 用户信息，包含用户 ID、人群标签、隐私同意状态等。 |
| `test` | `0` | 是否测试模式。0 = 正式竞价（产生计费），1 = 测试模式（不计费）。默认 0。 |
| `at` | `1` | 拍卖类型。1 = **第一价格拍卖**（胜出者按自己出价支付），2 = 第二价格拍卖（按次高价 +0.01 支付）。默认 2。500 以上为 Exchange 自定义。 |
| `tmax` | `150` | Exchange 允许 DSP 返回响应的最长时间（毫秒），包含网络延迟。超时视为放弃出价。本例允许 150ms。 |
| `wseat` | `["seat-001", "seat-002"]` | 席位白名单。只允许列表中的买方席位（广告主/代理商）参与竞价。与 `bseat` 不可同时使用。 |
| `bseat` | `[]` | 席位黑名单。被屏蔽的买方席位。本例为空，表示不通过黑名单限制。 |
| `allimps` | `0` | Exchange 能否保证本次请求包含了页面上所有可用广告位。0 = 否/未知，1 = 是。用于 Roadblocking（包场投放）。 |
| `cur` | `["USD"]` | 允许的出价货币列表，使用 ISO-4217 代码。本例只接受美元。 |
| `wlang` | `["en", "zh"]` | 允许的创意语言白名单，使用 ISO-639-1 代码。本例允许英文和中文创意。 |
| `acat` | `[]` | 允许的广告主类别白名单。与 `bcat` 互斥，只应出现一个。本例为空。 |
| `bcat` | `["IAB25", "IAB7-39", "IAB26"]` | 被屏蔽的广告类别黑名单。本例屏蔽了"非标准内容"、"极限运动"和"非法内容"等类别。 |
| `cattax` | `2` | 指定 `bcat`/`acat` 使用的分类体系。2 = IAB Content Taxonomy 2.0。默认 1（Taxonomy 1.0）。 |
| `badv` | `["blockedadvertiser.com", ...]` | 被屏蔽的广告主域名黑名单。这些广告主的创意不会被接受。 |
| `bapp` | `["com.example.blockedapp"]` | 被屏蔽的应用 bundle ID 黑名单。 |
| `source` | `{...}` | 请求来源信息，用于描述上游决策实体（如 Header Bidding 场景）。 |
| `regs` | `{...}` | 法规与隐私合规信息，包含 COPPA、GDPR、CCPA 等标志。 |
| `ext` | `{}` | Exchange 扩展字段。各平台可自定义私有字段。 |

---

### 二、Source 对象（请求来源）

| 字段 | 值 | 说明 |
|------|-----|------|
| `fd` | `0` | 最终决策方。0 = Exchange 自身决策，1 = 上游系统决策（如 Header Bidding 中由 Publisher Ad Server 决策）。 |
| `tid` | `"txn-abc-123-def-456"` | 交易 ID。在多方参与的同一次竞价中（如多个 Exchange），此 ID 必须保持一致，用于跨系统关联。 |
| `pchain` | `"tag1:abc123:reseller"` | TAG Payment ID 链，遵循 TAG Payment ID Protocol v1.0 语法，用于支付链路追踪。 |
| `schain` | `{...}` | **SupplyChain 对象**，描述从 Publisher 到当前 Exchange 的完整供应链路。详见下方。 |

#### SupplyChain 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `complete` | `1` | **必填。** 供应链是否完整。1 = 包含从原始 Publisher 到当前发送者的所有节点。0 = 不完整。 |
| `ver` | `"1.0"` | **必填。** Supply Chain 规范版本号。 |
| `nodes` | `[...]` | **必填。** 按顺序排列的供应链节点数组。第一个节点是最初的库存持有者（Publisher），最后一个是发送此请求的实体。 |

#### SupplyChainNode 对象（每个节点）

| 字段 | 值 | 说明 |
|------|-----|------|
| `asi` | `"awesomenews.com"` | **必填。** 广告系统的标准域名（SSP/Exchange 的域名），应与 ads.txt 中使用的域名一致。 |
| `sid` | `"pub-8953"` | **必填。** 该广告系统中卖方/转售方的账户 ID，通常对应 `publisher.id`。最长 64 字符。 |
| `rid` | `"bid-request-001"` | 该卖方发出的 OpenRTB Request ID。 |
| `name` | `"Awesome Media Group"` | 该节点对应的公司名称。如果已在 sellers.json 中存在，则不需要包含。 |
| `domain` | `"awesomenews.com"` | 该实体的业务域名。如果已在 sellers.json 中存在，则不需要包含。 |
| `hp` | `1` | 是否参与资金流转。1 = 该节点参与支付链（上游 `asi` 向 `sid` 付款），0 = 不参与。v1.0 中应始终为 1。 |

---

### 三、Regs 对象（法规与合规）

| 字段 | 值 | 说明 |
|------|-----|------|
| `coppa` | `0` | 是否受美国 COPPA（儿童在线隐私保护法）约束。0 = 否，1 = 是。若为 1，则不应收集 13 岁以下儿童的个人信息。 |
| `gdpr` | `0` | 是否受欧盟 GDPR 约束。0 = 否，1 = 是，省略 = 未知。 |
| `us_privacy` | `"1YNN"` | 美国隐私字符串（CCPA）。格式为 4 位：版本号 + 是否有"选择退出销售通知" + 用户是否选择退出 + LSPA 协议。`1YNN` 表示：版本 1，有通知，用户未选择退出，未签署 LSPA。 |
| `gpp` | `"DBABMA~CPXx..."` | Global Privacy Platform（全球隐私平台）的同意字符串，统一携带各地区隐私合规信号。 |
| `gpp_sid` | `[6]` | GPP 中适用于本次交易的章节 ID 数组。6 通常表示 US National（美国全国隐私法规）。 |

---

### 四、Imp 对象（展示机会）

> 每个 Imp 对象描述一个可竞价的广告位。一个 Bid Request 可包含多个 Imp。

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"1"` | **必填。** 本次展示在请求中的唯一标识，通常从 1 开始递增。DSP 在响应时通过 `impid` 引用此 ID。 |
| `metric` | `[...]` | 展示相关的量化指标数组，如历史可视率、点击率等，辅助 DSP 决策。 |
| `banner` | `{...}` | Banner 广告位信息。存在此对象表示该广告位接受 Banner 类型的出价。 |
| `video` | `{...}` | 视频广告位信息。存在此对象表示该广告位接受视频类型的出价。 |
| `native` | `{...}` | 原生广告位信息。存在此对象表示该广告位接受原生广告类型的出价。 |
| `pmp` | `{...}` | 私有交易市场信息。包含预先约定的 Direct Deal。 |
| `displaymanager` | `"MoPub"` | 负责渲染广告的 SDK/中介平台名称。在移动和视频场景中推荐填写。 |
| `displaymanagerver` | `"5.16.0"` | 渲染 SDK 的版本号。 |
| `instl` | `0` | 是否为插屏/全屏广告。0 = 否，1 = 是。 |
| `tagid` | `"agltb3B1Yi..."` | 用于发起竞价的广告位标识或广告标签 ID。可用于 Debug 和买方优化。 |
| `bidfloor` | `0.50` | 底价（最低出价），以 CPM 计。低于此价格的出价不被接受。默认 0。 |
| `bidfloorcur` | `"USD"` | 底价货币类型，ISO-4217 代码。默认 USD。此字段设定了 Imp 内所有底价的默认货币。 |
| `clickbrowser` | `1` | 点击创意后打开的浏览器类型（仅 App 内）。0 = 内嵌 WebView，1 = 系统原生浏览器（如 Safari）。 |
| `secure` | `1` | 是否要求创意素材和标记使用 HTTPS。0 = 不要求，1 = 要求。省略则未知，但可假设支持 HTTP。 |
| `iframebuster` | `["vendor1.com", "vendor2.com"]` | Exchange 支持的 iframe buster 供应商列表。 |
| `rwdd` | `0` | 用户是否因观看广告而获得奖励。0 = 否，1 = 是（如激励视频广告）。 |
| `ssai` | `0` | 服务端广告插入（SSAI）状态。0 = 未知，1 = 全部客户端，2 = 素材服务端拼接但追踪像素客户端触发，3 = 全部服务端。 |
| `exp` | `300` | 竞价到实际展示之间可能经过的秒数（建议值）。DSP 可据此评估创意的时效性。 |
| `qty` | `{...}` | 展示数量乘数信息（主要用于 DOOH/CTV 场景），表示一次购买实际产生的展示次数。 |
| `dt` | `1709712000000` | 预计展示实际发生的时间戳（Unix 毫秒）。常用于 DOOH 场景。 |
| `refresh` | `{...}` | 广告位自动刷新信息。包含刷新机制和已刷新次数。 |

#### Metric 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `type` | `"viewability"` | **必填。** 指标类型，由 Exchange 定义并预先发布给 DSP。本例为"可视率"。 |
| `value` | `0.85` | **必填。** 指标值。概率类指标取值范围 0.0–1.0。本例表示 85% 的历史可视率。 |
| `vendor` | `"EXCHANGE"` | **推荐。** 指标来源。`EXCHANGE` 表示由 Exchange 自身提供。也可以是第三方监测供应商名称。 |

#### Qty 对象（展示乘数）

| 字段 | 值 | 说明 |
|------|-----|------|
| `multiplier` | `1.0` | **必填。** 如果购买此广告位，将产生多少个计费展示。例如 DOOH 屏幕一次展示可能被 14.2 个人看到。 |
| `sourcetype` | `2` | **推荐。** 乘数测量来源类型。参考 AdCOM 中的 DOOH Multiplier Measurement Source Types 枚举。 |
| `vendor` | `"measurementvendor.com"` | 当 `sourcetype` 存在且值为 1 时必填。提供测量的供应商顶级域名。 |

#### Refresh 对象（广告位刷新）

| 字段 | 值 | 说明 |
|------|-----|------|
| `refsettings` | `[...]` | 刷新设置数组。描述广告位自动刷新的触发方式和间隔。 |
| `count` | `2` | 自上次页面加载以来，该广告位已刷新的次数。本例表示已刷新 2 次。 |

#### RefSettings 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `reftype` | `1` | 自动刷新的触发类型。参考 AdCOM 中的 Auto Refresh Triggers 枚举。1 通常表示基于时间的自动刷新。 |
| `minint` | `30` | 最小刷新间隔（秒）。广告创意至少渲染 30 秒后才会刷新到下一个创意。 |

---

### 五、Banner 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `format` | `[{"w":300,"h":250}, {"w":320,"h":50}]` | **推荐。** 允许的尺寸列表。每个 Format 对象代表一种可接受的宽高组合。 |
| `w` | `300` | 精确宽度（设备独立像素 DIPS）。当没有 Format 对象时推荐使用。 |
| `h` | `250` | 精确高度（设备独立像素 DIPS）。 |
| `btype` | `[4]` | 被屏蔽的 Banner 类型。4 = iframe 类型被屏蔽。 |
| `battr` | `[13, 14]` | 被屏蔽的创意属性。13 = 用户交互式广告，14 = 弹窗式广告。参考 AdCOM Creative Attributes 枚举。 |
| `pos` | `1` | 广告位在屏幕上的位置。1 = 首屏（Above the Fold）。参考 AdCOM Placement Positions 枚举。 |
| `mimes` | `["image/jpeg", "image/gif", "image/png"]` | 支持的 MIME 类型列表。 |
| `topframe` | `1` | Banner 是否在顶层框架中（非 iframe 内）。0 = 否，1 = 是。 |
| `expdir` | `[2, 4]` | 允许的展开方向。2 = 向右，4 = 向下。参考 AdCOM Expandable Directions 枚举。 |
| `api` | `[3, 5]` | 支持的 API 框架。3 = MRAID-1，5 = MRAID-2。参考 AdCOM API Frameworks 枚举。 |
| `id` | `"banner-1"` | Banner 对象的唯一 ID。当 Banner 作为 Video 的伴随广告时推荐使用。 |
| `vcm` | *(出现在 companionad 中)* | 伴随广告渲染模式（仅用于 Video 伴随广告场景）。0 = 与视频同时展示，1 = 视频结束后展示（End-Card）。 |

#### Format 对象（允许的尺寸）

| 字段 | 值 | 说明 |
|------|-----|------|
| `w` | `300` | 宽度（DIPS）。 |
| `h` | `250` | 高度（DIPS）。 |
| *(可选)* `wratio` | - | 宽度比例（用于 Flex Ads 弹性广告）。 |
| *(可选)* `hratio` | - | 高度比例。 |
| *(可选)* `wmin` | - | 以比例表示尺寸时的最小宽度。 |

---

### 六、Video 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `mimes` | `["video/mp4", ...]` | **必填。** 支持的视频 MIME 类型。 |
| `minduration` | `5` | 最短视频时长（秒）。与 `rqddurs` 互斥。 |
| `maxduration` | `30` | 最长视频时长（秒）。与 `rqddurs` 互斥。 |
| `startdelay` | `0` | 广告开始播放的延迟（秒）。0 = 前贴片（Pre-roll），>0 = 中贴片的延迟秒数，-1 = 通用中贴片，-2 = 通用后贴片。 |
| `maxseq` | `3` | 动态视频广告 Pod 中允许的最大广告数量。 |
| `poddur` | `90` | 动态视频广告 Pod 的总时长（秒）。指整个广告时段的长度，而 `minduration`/`maxduration` 约束的是单条广告。 |
| `protocols` | `[2, 3, 5, 6]` | 支持的视频协议。2 = VAST 2.0，3 = VAST 3.0，5 = VAST 2.0 Wrapper，6 = VAST 3.0 Wrapper。 |
| `w` | `640` | 视频播放器宽度（DIPS）。 |
| `h` | `480` | 视频播放器高度（DIPS）。 |
| `podid` | `"pod-001"` | 标识该展示机会属于哪个 Ad Pod。同一请求中共享相同 `podid` 的 Imp 属于同一个 Pod。 |
| `podseq` | `1` | 该 Ad Pod 在内容流中的顺序位置。参考 AdCOM Pod Sequence 枚举。 |
| `plcmt` | `1` | 视频展示位置类型（替代已废弃的 `placement`）。1 = In-Stream（贴片广告）。参考 AdCOM Plcmt Subtypes - Video 枚举。 |
| `linearity` | `1` | 线性/非线性要求。1 = 线性（如贴片广告，占据全部播放器），2 = 非线性（如覆盖式广告）。 |
| `skip` | `1` | 是否允许跳过。0 = 不可跳过，1 = 可跳过。 |
| `skipmin` | `15` | 总时长超过此秒数的视频才可以被跳过。本例表示 15 秒以上的视频才能跳过。 |
| `skipafter` | `5` | 视频播放多少秒后才出现跳过按钮。本例为播放 5 秒后可跳过。 |
| `slotinpod` | `1` | 卖方保证该广告在 Pod 中的位置。1 = 第一个位置，2 = 最后一个位置。参考 AdCOM Slot Position in Pod。 |
| `mincpmpersec` | `0.02` | 每秒最低 CPM。动态 Pod 中按视频时长计算的底价。 |
| `battr` | `[13, 14]` | 被屏蔽的创意属性（同 Banner）。 |
| `maxextended` | `30` | 允许的最大延长播放时长（秒）。0 = 不允许延长，-1 = 无限制。本例允许超出 maxduration 最多 30 秒。 |
| `minbitrate` | `300` | 最低码率（Kbps）。 |
| `maxbitrate` | `1500` | 最高码率（Kbps）。 |
| `boxingallowed` | `1` | 是否允许 4:3 内容在 16:9 播放器中加黑边。0 = 不允许，1 = 允许。 |
| `playbackmethod` | `[1]` | 播放方式。1 = 页面加载时自动播放有声。建议只使用数组第一个元素。 |
| `playbackend` | `1` | 触发播放结束的事件。参考 AdCOM Playback Cessation Modes。 |
| `delivery` | `[2]` | 支持的传输方式。2 = 渐进式下载（Progressive）。1 = 流式（Streaming）。 |
| `pos` | `1` | 广告位在屏幕上的位置。1 = 首屏。 |
| `companionad` | `[...]` | 伴随广告（Banner）数组。VAST 规范中定义的与视频配套展示的 Banner 广告。 |
| `api` | `[1, 2]` | 支持的 API 框架。1 = VPAID 1.0，2 = VPAID 2.0。 |
| `companiontype` | `[1, 2]` | 支持的伴随广告类型。1 = 静态资源，2 = HTML 资源。参考 AdCOM Companion Types。 |
| `durfloors` | `[...]` | 按视频时长分段的底价数组。不同时长的创意有不同的最低出价。 |

#### DurFloors 对象（按时长的底价）

| 字段 | 值 | 说明 |
|------|-----|------|
| `mindur` | `1` | 时长范围下限（秒）。缺失则下限无约束。 |
| `maxdur` | `15` | 时长范围上限（秒）。缺失则上限无约束。`mindur` 和 `maxdur` 至少有一个。 |
| `bidfloor` | `5.00` | 该时长范围内创意的最低 CPM 出价。例如 1-15 秒的视频，底价为 $5 CPM。 |

---

### 七、Native 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `request` | `"{\"ver\":\"1.1\",...}"` | **必填。** 遵循 OpenRTB Native Ads API 规范的请求载荷（JSON 编码字符串）。包含所需的原生广告资产（标题、图片、描述等）。 |
| `ver` | `"1.1"` | **推荐。** Native Ads API 规范版本，便于高效解析。 |
| `api` | `[3]` | 支持的 API 框架。3 = MRAID-1。 |
| `battr` | `[13, 14]` | 被屏蔽的创意属性。 |

---

### 八、Pmp 对象（私有交易市场）

| 字段 | 值 | 说明 |
|------|-----|------|
| `private_auction` | `1` | 是否为私有竞拍。0 = 所有出价均接受，1 = 仅接受 deals 中指定席位的出价。 |
| `deals` | `[...]` | Deal 数组，包含适用于此展示的具体交易条款。 |

#### Deal 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"AB-Agency1-0001"` | **必填。** 交易唯一标识。买卖双方预先协商的 Deal ID。 |
| `bidfloor` | `2.50` | 此 Deal 的专属底价（CPM）。可能高于或低于 Imp 级别的底价。 |
| `bidfloorcur` | `"USD"` | Deal 底价货币。此字段独立于 `Imp.bidfloorcur`，不继承，若未指定则默认 USD。 |
| `at` | `1` | 此 Deal 的拍卖类型。1 = 第一价格，2 = 第二价格，3 = `bidfloor` 即为约定的固定价格。可覆盖 BidRequest 级别的 `at`。 |
| `wseat` | `["Agency1"]` | 允许参与此 Deal 的买方席位白名单。 |
| `wadomain` | `["brand-a.com"]` | 允许参与此 Deal 的广告主域名白名单。 |
| `guar` | `0` | 是否为保量交易（Guaranteed Deal）。0 = 否，1 = 是（DSP 必须出价）。 |
| `mincpmpersec` | `0.05` | 每秒最低 CPM（仅用于视频/音频 Deal）。 |
| `durfloors` | `[...]` | 按时长的底价数组（用于视频/音频 Deal）。 |

---

### 九、Site 对象（网站信息）

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"102855"` | **推荐。** Exchange 分配的站点 ID。 |
| `name` | `"Awesome News Site"` | 站点名称（可由 Publisher 要求使用别名）。 |
| `domain` | `"www.awesomenews.com"` | 站点域名。 |
| `cattax` | `2` | 站点分类使用的分类体系。2 = IAB Content Taxonomy 2.0。 |
| `cat` | `["IAB12", "IAB12-2"]` | 站点的内容分类数组。IAB12 = 新闻，IAB12-2 = 科技新闻。 |
| `sectioncat` | `["IAB12-2"]` | 当前栏目的内容分类。 |
| `pagecat` | `["IAB12-2"]` | 当前页面的内容分类。 |
| `page` | `"https://www.awesomenews.com/..."` | 展示广告的当前页面完整 URL。 |
| `ref` | `"https://www.google.com/..."` | 引导用户来到当前页面的来源页（Referrer URL）。 |
| `search` | `"tech news"` | 导致用户来到当前页面的搜索词。 |
| `mobile` | `0` | 站点是否已针对移动端优化布局。0 = 否，1 = 是。 |
| `privacypolicy` | `1` | 站点是否有隐私政策。0 = 否，1 = 是。 |
| `publisher` | `{...}` | Publisher 信息（详见下方）。 |
| `content` | `{...}` | 当前页面的内容信息（详见下方）。 |
| `keywords` | `"tech,news,AI,startup"` | 描述站点的关键词（逗号分隔）。与 `kwarray` 互斥。 |
| `inventorypartnerdomain` | `"contentpartner.com"` | 库存合作方域名。当站点所有者与内容所有者之间存在库存共享时使用。内容所有者的域名应在站点所有者的 ads.txt 中声明为 `inventorypartnerdomain`。 |

#### Publisher 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"pub-8953"` | Exchange 分配的卖方 ID。每个 ID 只能映射到一个收款实体。对应 Exchange 的 sellers.json 中的 `seller_id`。 |
| `name` | `"Awesome Media Group"` | 卖方名称。 |
| `cattax` | `2` | 分类体系。 |
| `cat` | `["IAB12"]` | Publisher 的内容分类。 |
| `domain` | `"awesomenews.com"` | Publisher 的最高级域名。 |

#### Content 对象（内容信息）

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"content-78901"` | Publisher 提供的内容唯一 ID。 |
| `episode` | `23` | 集数。 |
| `title` | `"The Future of AI in 2025"` | 内容标题。 |
| `series` | `"Tech Deep Dive"` | 所属系列/节目名。 |
| `season` | `"Season 3"` | 季度。 |
| `artist` | `"John Smith"` | 内容创作者/艺术家。 |
| `genre` | `"Technology"` | 内容类型/流派。 |
| `gtax` | `9` | genre 分类使用的分类体系。9 = Content Category Taxonomy 3.1。 |
| `genres` | `["600", "601"]` | 基于 gtax 指定分类体系的流派 ID 数组。 |
| `producer` | `{...}` | 内容制作方信息（可能不同于 Publisher，如联合供稿场景）。 |
| `url` | `"https://..."` | 内容 URL。 |
| `cattax` | `2` | 内容分类体系。 |
| `cat` | `["IAB12", "IAB19"]` | 内容分类。IAB19 = 技术与计算。 |
| `prodq` | `2` | 制作质量。参考 AdCOM Production Qualities 枚举。2 = 专业制作。 |
| `context` | `1` | 内容上下文类型。1 = 视频。参考 AdCOM Content Contexts 枚举。 |
| `contentrating` | `"G"` | 内容分级（如 MPAA 电影分级）。G = 适合所有人。 |
| `userrating` | `"4.5 stars"` | 用户对内容的评分。 |
| `qagmediarating` | `1` | 按 IQG 标准的媒体分级。1 = 所有受众。参考 AdCOM Media Ratings 枚举。 |
| `keywords` | `"AI,machine learning,..."` | 描述内容的关键词。 |
| `livestream` | `0` | 是否为直播。0 = 非直播，1 = 直播。 |
| `sourcerelationship` | `1` | 内容来源关系。0 = 间接（如联合供稿），1 = 直接（Publisher 即内容所有者）。 |
| `len` | `600` | 内容时长（秒）。适用于视频或音频内容。本例为 10 分钟。 |
| `language` | `"en"` | 内容语言，ISO-639-1 代码。 |
| `embeddable` | `1` | 内容是否可嵌入（如可嵌入的视频播放器）。0 = 否，1 = 是。 |
| `data` | `[...]` | 附加内容数据（来自不同数据源的额外信息）。 |
| `network` | `{...}` | 内容所在的电视/媒体网络信息。 |
| `channel` | `{...}` | 内容所在的频道信息。 |

##### Network 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"network-abc"` | Publisher 分配的网络唯一 ID。 |
| `name` | `"ABC Media Network"` | 网络名称（如 "ABC"、"CBS" 等电视网络）。 |
| `domain` | `"abcmedia.com"` | 网络的主域名。建议使用 PSL+1 级域名以便 DSP 归一化定向。 |

##### Channel 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"channel-tech"` | Publisher 分配的频道唯一 ID。 |
| `name` | `"ABC Tech Channel"` | 频道名称（如 "MTV"、"CNN" 等具体频道）。 |
| `domain` | `"tech.abcmedia.com"` | 频道的主域名。 |

##### Producer 对象（内容制作方）

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"producer-001"` | 内容制作方 ID。在联合供稿场景中有用。 |
| `name` | `"Tech Media Inc."` | 制作方名称。 |
| `domain` | `"techmedia.com"` | 制作方的最高级域名。 |

---

### 十、Device 对象（设备信息）

| 字段 | 值 | 说明 |
|------|-----|------|
| `geo` | `{...}` | **推荐。** 设备当前地理位置（通常 = 用户当前位置）。 |
| `dnt` | `0` | **推荐。** 浏览器的 Do Not Track 标志。0 = 允许追踪，1 = 不追踪。 |
| `lmt` | `0` | **推荐。** 限制广告追踪信号（iOS/Android 系统级）。0 = 不限制，1 = 限制。 |
| `ua` | `"Mozilla/5.0 (iPhone;..."` | 浏览器原始 User-Agent 字符串。如果客户端支持 UA Client Hints 且 `sua` 存在，DSP 应优先使用 `sua`，因为 `ua` 可能被冻结或精简。 |
| `sua` | `{...}` | **结构化 User Agent 信息**（基于 User-Agent Client Hints），比 `ua` 更准确。详见下方。 |
| `ip` | `"203.0.113.45"` | 最接近设备的 IPv4 地址。 |
| `ipv6` | `"2001:0db8:..."` | 最接近设备的 IPv6 地址。 |
| `devicetype` | `4` | 设备类型。4 = 手机。参考 AdCOM Device Types 枚举。（1=移动/平板, 2=PC, 3=CTV, 4=手机, 5=平板, 6=连接设备, 7=机顶盒） |
| `make` | `"Apple"` | 设备制造商。 |
| `model` | `"iPhone 15"` | 设备型号。 |
| `os` | `"iOS"` | 操作系统。 |
| `osv` | `"17.0"` | 操作系统版本。 |
| `hwv` | `"iPhone15,4"` | 硬件版本号。 |
| `h` | `2556` | 屏幕物理高度（像素）。 |
| `w` | `1179` | 屏幕物理宽度（像素）。 |
| `ppi` | `460` | 屏幕每英寸像素数。 |
| `pxratio` | `3.0` | 物理像素与设备独立像素的比率（Retina 屏通常为 2.0 或 3.0）。 |
| `js` | `1` | 是否支持 JavaScript。0 = 不支持，1 = 支持。 |
| `geofetch` | `1` | 地理定位 API 是否对 Banner 中的 JS 代码可用。0 = 否，1 = 是。 |
| `flashver` | `""` | Flash 版本（现代设备已不再支持，通常为空）。 |
| `language` | `"en"` | 浏览器语言，ISO-639-1。 |
| `carrier` | `"VERIZON"` | 运营商/ISP 名称。 |
| `mccmnc` | `"311-480"` | 移动国家码-移动网络码。"311-480" 代表美国 Verizon。反映 SIM 卡归属网络，不随漫游变化。 |
| `connectiontype` | `6` | 网络连接类型。6 = 蜂窝网络-4G。参考 AdCOM Connection Types 枚举。 |
| `ifa` | `"AA000DFE-7416-..."` | 广告标识符（IDFA/GAID），明文传输。用于跨应用用户识别和频次控制。 |

#### UserAgent（sua）对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `browsers` | `[{"brand":"Safari","version":["17","0"]}, ...]` | **推荐。** 浏览器品牌和版本信息数组。来源于 Sec-CH-UA-Full-Version-List 头。 |
| `platform` | `{"brand":"iOS","version":["17","0"]}` | **推荐。** 操作系统/执行平台的品牌和版本。来源于 Sec-CH-UA-Platform 头。 |
| `mobile` | `1` | 是否为移动设备。1 = 移动端，0 = 桌面端。来源于 Sec-CH-UA-Mobile 头。 |
| `architecture` | `"arm"` | 设备 CPU 架构（如 "x86"、"arm"）。来源于 Sec-CH-UA-Arch 头。 |
| `bitness` | `"64"` | 设备位数（如 "64"）。来源于 Sec-CH-UA-Bitness 头。 |
| `model` | `"iPhone 15"` | 设备型号。来源于 Sec-CH-UA-Model 头。 |
| `source` | `2` | 数据来源类型。参考 AdCOM User-Agent Source 枚举。0 = 未知，1 = UA Client Hints (低熵)，2 = UA Client Hints (高熵)，3 = 从 UA 字符串解析。 |

#### BrandVersion 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `brand` | `"Safari"` | **必填。** 品牌标识，如 "Chrome"、"Safari"、"iOS"、"Windows"。 |
| `version` | `["17", "0"]` | 版本号组件数组，按层级降序排列（主版本、次版本、修订号...）。 |

#### Geo 对象（地理位置）

| 字段 | 值 | 说明 |
|------|-----|------|
| `lat` | `34.0522` | 纬度，-90.0 到 +90.0。负值表示南纬。 |
| `lon` | `-118.2437` | 经度，-180.0 到 +180.0。负值表示西经。本例为洛杉矶。 |
| `type` | `1` | 位置数据来源。1 = GPS/设备定位服务，2 = IP 地址推断，3 = 用户提供。推荐在传递 lat/lon 时填写。 |
| `accuracy` | `50` | 定位精度（米）。推荐在 type=1 时填写。本例表示 50 米精度。 |
| `lastfix` | `10` | 距上次定位成功已过的秒数。设备可能缓存位置数据。 |
| `ipservice` | `3` | 当 type=2 时使用的 IP 定位服务商。参考 AdCOM IP Location Services 枚举。 |
| `country` | `"USA"` | 国家代码，ISO-3166-1-alpha-3。 |
| `region` | `"CA"` | 区域代码，ISO-3166-2。美国使用 2 字母州代码。CA = 加利福尼亚。 |
| `metro` | `"803"` | Google Metro 代码（类似 Nielsen DMA，但不完全相同）。803 = 洛杉矶。 |
| `city` | `"Los Angeles"` | 城市名，使用联合国贸易与运输地点代码（UN/LOCODE）。 |
| `zip` | `"90001"` | 邮政编码。 |
| `utcoffset` | `-480` | 与 UTC 的时差（分钟）。-480 = UTC-8（太平洋标准时间）。 |

---

### 十一、User 对象（用户信息）

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"55816b397..."` | Exchange 侧的用户 ID（通常来自 Exchange 自己的 Cookie）。应在合理时间内保持稳定，以支持频次控制和重定向。 |
| `buyeruid` | `"dsp-user-abc-123456"` | **DSP 侧的用户 ID**，由 Exchange 通过 Cookie Sync（ID 同步）映射得到。DSP 收到后可直接用于人群匹配。 |
| `keywords` | `"sports,technology,travel"` | 描述用户兴趣的关键词。与 `kwarray` 互斥。 |
| `customdata` | `"base85encodedstringhere"` | Exchange Cookie 中设置的 DSP 自定义数据。必须使用 base85 Cookie 安全字符编码。 |
| `geo` | `{...}` | 用户的**家庭位置**（不一定是当前位置）。与 Device.geo 含义不同。 |
| `data` | `[...]` | 附加用户数据数组，来自不同的第三方数据源（DMP）。 |
| `consent` | `"CPXxRf..."` | 当 GDPR 生效时，包含 IAB TCF（Transparency and Consent Framework）的同意字符串。 |
| `eids` | `[...]` | 扩展标识符数组，支持多个第三方身份识别提供商。 |
| `yob` | *(已废弃)* | 出生年份。在 OpenRTB 2.6 中已被标记为 DEPRECATED。 |
| `gender` | *(已废弃)* | 性别。在 OpenRTB 2.6 中已被标记为 DEPRECATED。 |

#### Data 对象（第三方数据）

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"data-provider-1"` | 数据提供商的 Exchange 专属 ID。 |
| `name` | `"BlueKai"` | 数据提供商名称。 |
| `segment` | `[...]` | Segment 数组，包含来自该数据源的具体数据值（键值对）。 |

#### Segment 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"seg-auto-001"` | 数据段 ID（由数据提供商定义）。 |
| `name` | `"auto intenders"` | 数据段名称。本例表示"汽车购买意向人群"。 |
| `value` | `""` | 数据段值的字符串表示。本例为空。 |

#### EID 对象（扩展标识符）

| 字段 | 值 | 说明 |
|------|-----|------|
| `inserter` | `"awesomenews.com"` | 导致此 ID 被添加的实体的标准域名。对于 Publisher 来说应与 site/app 域名匹配。 |
| `source` | `"liveramp.com"` | ID 的标准来源域名（身份识别提供商的域名）。 |
| `matcher` | `"liveramp.com"` | 提供 `mm` 中定义的匹配方法的技术方。为空时默认等于 `source`。 |
| `mm` | `1` | 匹配方法。参考 AdCOM ID Match Methods 枚举。 |
| `uids` | `[...]` | 来自该来源的用户 ID 数组。 |

#### UID 对象

| 字段 | 值 | 说明 |
|------|-----|------|
| `id` | `"XY1000bIVB..."` | 用户标识符字符串。 |
| `atype` | `3` | User Agent 类型（ID 的来源类型）。3 = 通常表示 Person-based ID（如 LiveRamp RampID）。参考 AdCOM Agent Types 枚举。强烈建议设置此字段。 |

---

### 十二、总结：对象之间的层级关系

```
BidRequest
├── id, test, at, tmax, cur, wseat, bseat, allimps, wlang, bcat, badv, bapp, cattax, acat
│
├── source
│   ├── fd, tid, pchain
│   └── schain
│       ├── complete, ver
│       └── nodes[] → (asi, sid, rid, name, domain, hp)
│
├── regs
│   └── coppa, gdpr, us_privacy, gpp, gpp_sid
│
├── imp[] (至少1个)
│   ├── id, bidfloor, bidfloorcur, secure, instl, tagid, rwdd, ssai, exp, dt
│   ├── metric[] → (type, value, vendor)
│   ├── banner → (format[], w, h, btype, battr, pos, mimes, topframe, expdir, api)
│   ├── video → (mimes, minduration, maxduration, protocols, w, h, skip, ...)
│   │   ├── companionad[] → Banner 对象
│   │   └── durfloors[] → (mindur, maxdur, bidfloor)
│   ├── audio → (类似 video)
│   ├── native → (request, ver, api, battr)
│   ├── pmp
│   │   └── deals[] → (id, bidfloor, at, wseat, wadomain, guar, ...)
│   ├── qty → (multiplier, sourcetype, vendor)
│   ├── refresh → refsettings[] → (reftype, minint)
│   └── displaymanager, displaymanagerver, clickbrowser, iframebuster
│
├── site (或 app 或 dooh，三选一)
│   ├── id, name, domain, cat, page, ref, search, mobile, privacypolicy
│   ├── publisher → (id, name, domain, cat)
│   ├── content
│   │   ├── id, title, series, season, episode, genre, genres, len, language, ...
│   │   ├── producer → (id, name, domain)
│   │   ├── network → (id, name, domain)
│   │   ├── channel → (id, name, domain)
│   │   └── data[] → segment[] → (id, name, value)
│   └── inventorypartnerdomain
│
├── device
│   ├── ua, sua → (browsers[], platform, mobile, architecture, bitness, model, source)
│   ├── ip, ipv6, devicetype, make, model, os, osv, hwv, h, w, ppi, pxratio
│   ├── js, geofetch, language, carrier, mccmnc, connectiontype, ifa, dnt, lmt
│   └── geo → (lat, lon, type, accuracy, country, region, metro, city, zip, utcoffset)
│
└── user
    ├── id, buyeruid, keywords, customdata, consent
    ├── geo → (lat, lon, type, country, region, city, zip)
    ├── data[] → segment[] → (id, name, value)
    └── eids[] → (inserter, source, matcher, mm, uids[] → (id, atype))
```

---

### 十三、关键设计要点

1. **`imp` 中可以同时包含 `banner`、`video`、`native`**，表示该广告位接受多种类型的创意，但一次出价只能选择其中一种类型。

2. **`site`、`app`、`dooh` 三者互斥**，一个请求中只能出现一个，分别对应网页、应用、数字户外三种流量类型。

3. **所有对象都有 `ext` 字段**，用于各 Exchange 传递私有扩展信息。实际对接中 ext 字段非常重要。

4. **`bidfloor` 可出现在多个层级**：Imp 级别设置默认底价，Deal 级别可覆盖，DurFloors 按时长进一步细分底价。

5. **用户标识有多层体系**：`user.id`（Exchange Cookie ID）→ `user.buyeruid`（DSP Cookie ID，通过 Cookie Sync 建立映射）→ `user.eids`（第三方统一 ID，如 LiveRamp、UID2.0 等）。

6. **`sua` 优先于 `ua`**：由于浏览器正在逐步冻结/精简 UA 字符串，结构化的 `sua`（基于 Client Hints）是更准确的设备信息来源。

7. **OpenRTB 2.6 已废弃的字段**：`user.yob`、`user.gender`、`video.sequence`、`video.placement`、各种设备哈希 ID（`didsha1`、`didmd5` 等）。


# OpenRTB 2.6 完整 Bid Response 示例

## 一、完整 Bid Response JSON

```json
{
  "id": "80ce30c53c16e6ede735f123ef6e32361bfc7b22",
  "bidid": "resp-abc-20250306-001",
  "cur": "USD",
  "customdata": "dGhpcyBpcyBjdXN0b20gZGF0YQ",
  "seatbid": [
    {
      "seat": "seat-advertiser-A",
      "group": 0,
      "bid": [
        {
          "id": "bid-001",
          "impid": "1",
          "price": 9.43,
          "nurl": "https://dsp.example.com/win?bid=${AUCTION_BID_ID}&imp=${AUCTION_IMP_ID}&price=${AUCTION_PRICE}&cur=${AUCTION_CURRENCY}&seat=${AUCTION_SEAT_ID}&min=${AUCTION_MIN_TO_WIN}&mbr=${AUCTION_MBR}",
          "burl": "https://dsp.example.com/billing?bid=${AUCTION_BID_ID}&imp=${AUCTION_IMP_ID}&price=${AUCTION_PRICE}&ts=${AUCTION_IMP_TS}&mult=${AUCTION_MULTIPLIER}",
          "lurl": "https://dsp.example.com/loss?bid=${AUCTION_BID_ID}&imp=${AUCTION_IMP_ID}&reason=${AUCTION_LOSS}&min=${AUCTION_MIN_TO_WIN}",
          "adm": "<div id=\"ad-container\"><a href=\"https://brand-a.com/landing?click_id=abc123\" target=\"_blank\"><img src=\"https://cdn.dsp.example.com/creatives/banner_300x250_campaign111.jpg\" width=\"300\" height=\"250\" alt=\"Ad\"/></a><img src=\"https://dsp.example.com/impression?price=${AUCTION_PRICE}&id=${AUCTION_ID}\" width=\"1\" height=\"1\" style=\"display:none;\"/></div>",
          "adid": "pre-approved-ad-314",
          "adomain": ["brand-a.com"],
          "bundle": "",
          "iurl": "https://cdn.dsp.example.com/creatives/preview/campaign111_thumb.jpg",
          "cid": "campaign111",
          "crid": "creative-banner-300x250-v2",
          "tactic": "retargeting-q1-2025",
          "cattax": 2,
          "cat": ["IAB2-1", "IAB2-2"],
          "attr": [1, 2, 7],
          "apis": [3, 5],
          "protocol": 0,
          "qagmediarating": 1,
          "language": "en",
          "dealid": "AB-Agency1-0001",
          "w": 300,
          "h": 250,
          "wratio": 0,
          "hratio": 0,
          "exp": 300,
          "dur": 0,
          "mtype": 1,
          "slotinpod": 0,
          "ext": {}
        }
      ],
      "ext": {}
    },
    {
      "seat": "seat-advertiser-B",
      "group": 0,
      "bid": [
        {
          "id": "bid-002",
          "impid": "1",
          "price": 7.50,
          "nurl": "https://dsp.example.com/win?bid=${AUCTION_BID_ID}&price=${AUCTION_PRICE}",
          "burl": "https://dsp.example.com/billing?bid=${AUCTION_BID_ID}&price=${AUCTION_PRICE}",
          "lurl": "https://dsp.example.com/loss?bid=${AUCTION_BID_ID}&reason=${AUCTION_LOSS}",
          "adm": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<VAST version=\"3.0\">\n  <Ad id=\"video-ad-567\">\n    <InLine>\n      <AdSystem version=\"2.0\">DSP Ad Server</AdSystem>\n      <AdTitle><![CDATA[Brand B Video Ad]]></AdTitle>\n      <Impression><![CDATA[https://dsp.example.com/vast/impression?price=${AUCTION_PRICE}]]></Impression>\n      <Creatives>\n        <Creative id=\"1\" sequence=\"1\">\n          <Linear>\n            <Duration>00:00:15</Duration>\n            <TrackingEvents>\n              <Tracking event=\"start\"><![CDATA[https://dsp.example.com/track?event=start]]></Tracking>\n              <Tracking event=\"complete\"><![CDATA[https://dsp.example.com/track?event=complete]]></Tracking>\n            </TrackingEvents>\n            <VideoClicks>\n              <ClickThrough><![CDATA[https://brand-b.com/promo]]></ClickThrough>\n            </VideoClicks>\n            <MediaFiles>\n              <MediaFile delivery=\"progressive\" bitrate=\"800\" width=\"640\" height=\"480\" type=\"video/mp4\">\n                <![CDATA[https://cdn.dsp.example.com/creatives/video_brand_b.mp4]]>\n              </MediaFile>\n            </MediaFiles>\n          </Linear>\n        </Creative>\n      </Creatives>\n    </InLine>\n  </Ad>\n</VAST>",
          "adid": "pre-approved-ad-567",
          "adomain": ["brand-b.com"],
          "bundle": "",
          "iurl": "https://cdn.dsp.example.com/creatives/preview/video_brand_b_thumb.jpg",
          "cid": "campaign222",
          "crid": "creative-video-15s-v1",
          "tactic": "awareness-campaign-2025",
          "cattax": 2,
          "cat": ["IAB1-1"],
          "attr": [6, 16],
          "apis": [1, 2],
          "protocol": 3,
          "qagmediarating": 1,
          "language": "en",
          "dealid": "",
          "w": 640,
          "h": 480,
          "exp": 120,
          "dur": 15,
          "mtype": 2,
          "slotinpod": 0,
          "ext": {}
        },
        {
          "id": "bid-003",
          "impid": "2",
          "price": 3.00,
          "nurl": "https://dsp.example.com/win?bid=${AUCTION_BID_ID}&price=${AUCTION_PRICE}",
          "burl": "https://dsp.example.com/billing?bid=${AUCTION_BID_ID}&price=${AUCTION_PRICE}",
          "lurl": "https://dsp.example.com/loss?bid=${AUCTION_BID_ID}&reason=${AUCTION_LOSS}",
          "adm": "{\"native\":{\"ver\":\"1.1\",\"link\":{\"url\":\"https://brand-b.com/native-landing\",\"clicktrackers\":[\"https://dsp.example.com/track?event=click\"]},\"imptrackers\":[\"https://dsp.example.com/track?event=impression&price=${AUCTION_PRICE}\"],\"assets\":[{\"id\":1,\"title\":{\"text\":\"Discover Brand B's Latest Innovation\"}},{\"id\":2,\"img\":{\"url\":\"https://cdn.dsp.example.com/creatives/native_main_1200x627.jpg\",\"w\":1200,\"h\":627}},{\"id\":3,\"data\":{\"value\":\"Brand B - Innovating the Future\"}}]}}",
          "adid": "pre-approved-ad-890",
          "adomain": ["brand-b.com"],
          "iurl": "https://cdn.dsp.example.com/creatives/preview/native_brand_b_thumb.jpg",
          "cid": "campaign222",
          "crid": "creative-native-feed-v1",
          "cattax": 2,
          "cat": ["IAB1-1"],
          "attr": [],
          "qagmediarating": 1,
          "language": "en",
          "w": 0,
          "h": 0,
          "mtype": 4,
          "ext": {}
        }
      ],
      "ext": {}
    }
  ],
  "ext": {}
}
```

---

## 二、No-Bid 响应示例

当 DSP 决定不出价时，有两种标准方式：

### 方式一：HTTP 204 No Content（推荐，最节省带宽）

直接返回空响应体，HTTP 状态码为 204。

### 方式二：返回包含 nbr 原因码的 BidResponse

```json
{
  "id": "80ce30c53c16e6ede735f123ef6e32361bfc7b22",
  "nbr": 2
}
```

| nbr 值 | 含义 |
|--------|------|
| 0 | 未知错误 |
| 1 | 技术错误 |
| 2 | 无效请求 |
| 3 | 已知爬虫/蜘蛛 |
| 4 | 可疑的非人类流量 |
| 5 | 被代理/防火墙/机器人过滤 |
| 6 | 不支持的设备类型 |
| 7 | 被屏蔽的 Publisher 或站点 |
| 8 | 不匹配的用户（无法识别的用户） |
| 9 | 每日用户达到频次上限 |
| 10 | 每日预算已用完 |

---

## 三、逐层、逐字段解析

---

### 3.1 顶层对象：BidResponse

| 字段 | 示例值 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `id` | `"80ce30c5..."` | string | **必填** | 对应的 Bid Request 的 ID。DSP 必须原样回传此 ID，Exchange 据此将响应与请求关联。用于日志追踪和匹配。 |
| `seatbid` | `[...]` | object array | 出价时必填 | SeatBid 对象数组。每个 SeatBid 代表一个"席位"（买方实体）的出价集合。如果要出价，至少需要 1 个 SeatBid，其中至少包含 1 个 Bid。 |
| `bidid` | `"resp-abc-..."` | string | 可选 | DSP 自行生成的响应追踪 ID。如果指定了此值，Exchange 在后续 Win Notice 中可以通过 `${AUCTION_BID_ID}` 宏回传此 ID。用于 DSP 侧的日志关联。 |
| `cur` | `"USD"` | string | 可选 | 出价使用的货币，ISO-4217 字母代码。默认为 `"USD"`。一个 BidResponse 中所有出价必须使用相同货币。 |
| `customdata` | `"dGhpcyBpcyB..."` | string | 可选 | DSP 可以通过此字段在 Exchange 的 Cookie 中设置自定义数据。必须使用 base85 Cookie 安全字符编码。主要用于在后续请求中通过 `user.customdata` 回传。 |
| `nbr` | *(仅 no-bid 时使用)* | integer | 可选 | 不出价原因码。仅在不出价时返回。参考 OpenRTB 3.0 的 No-Bid Reason Codes 枚举列表。 |
| `ext` | `{}` | object | 可选 | DSP 特有的扩展字段。各平台可自定义私有字段。 |

**关键规则**：
- 如果要出价 → 必须包含 `seatbid` 数组且其中有至少一个 bid
- 如果不出价 → 返回 HTTP 204（无内容），或返回仅含 `id` 和 `nbr` 的 BidResponse
- 格式错误的响应或不含实际 bid 的响应也会被视为不出价

---

### 3.2 SeatBid 对象

一个 BidResponse 可以包含多个 SeatBid，分别代表不同买方席位的出价。

| 字段 | 示例值 | 类型 | 必填 | 说明 |
|------|--------|------|------|------|
| `bid` | `[...]` | object array | **必填** | Bid 对象数组，至少包含 1 个 Bid。每个 Bid 对应请求中的一个展示机会。**同一个 SeatBid 中的多个 Bid 可以对应同一个 imp**，这样可以提高胜出概率（因为 Exchange 会代替 Publisher 执行广告主黑名单等过滤）。 |
| `seat` | `"seat-advertiser-A"` | string | 可选 | 买方席位 ID，代表出价方的身份（如广告主、代理商）。该 ID 需要买卖双方预先协商。Exchange 会据此进行席位级别的权限控制和报告。 |
| `group` | `0` | integer | 可选 | 分组竞价标志。**0 = 展示可以被单独赢得**（默认），即这个席位愿意赢得其中任何一个展示；**1 = 展示必须作为一个整体赢得或失去**，即要么全赢，要么全不要（Roadblocking 场景）。 |
| `ext` | `{}` | object | 可选 | DSP 特有的扩展字段。 |

**业务场景说明**：
- 当 `group=0` 时（默认），Exchange 对每个 bid 独立评估，DSP 可能赢得其中一部分展示
- 当 `group=1` 时，Exchange 必须将所有 bid 视为一组，全部胜出才分配给该席位（适用于品牌想包下整个页面所有广告位的场景）

---

### 3.3 Bid 对象（核心）

Bid 对象是整个响应中最重要的部分，代表 DSP 对某个展示机会的具体出价。

#### 3.3.1 必填字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `id` | `"bid-001"` | string; **必填** | DSP 生成的出价唯一 ID。用于日志追踪。Exchange 不直接使用此 ID，但 DSP 内部需要它来匹配 Win/Loss Notice。 |
| `impid` | `"1"` | string; **必填** | 对应 Bid Request 中 `imp.id` 的值。**这是将出价与具体展示机会关联的关键**。DSP 必须确保此值与请求中某个 Imp 的 id 完全匹配。 |
| `price` | `9.43` | float; **必填** | 出价金额，以 **CPM**（每千次展示成本）表示。虽然类型是 float，但**强烈建议使用整数数学处理货币**（如 Java 的 BigDecimal），以避免浮点精度问题。注意：实际交易是按单次展示计费，CPM 只是计价单位。 |

#### 3.3.2 通知 URL 字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `nurl` | `"https://dsp.example.com/win?..."` | string | **Win Notice URL**。当 DSP 赢得竞价时，Exchange 会调用此 URL 通知 DSP 胜出。URL 中可以包含替换宏（如 `${AUCTION_PRICE}`）。**重要**：Win Notice 表示赢得了竞拍，但**不一定代表广告已投放、已被用户看到、或已产生计费**。另外，nurl 的响应体也可以用于返回广告素材标记（Markup）。 |
| `burl` | `"https://dsp.example.com/billing?..."` | string | **Billing Notice URL**。当胜出的出价变为**可计费**状态时，Exchange 调用此 URL。什么构成"可计费"由 Exchange 的业务策略决定（如广告已投放到设备、已可见等）。**最佳实践**：burl 的触发应尽可能在服务端进行，且尽可能靠近 Exchange 记录收入的时间点，以减少双方的数据差异。对于 VAST 视频，IAB 规定 VAST Impression 事件才是正式的计费信号，burl 应同时触发。 |
| `lurl` | `"https://dsp.example.com/loss?..."` | string | **Loss Notice URL**。当 Exchange 确定该出价未胜出时调用。可包含 `${AUCTION_LOSS}` 宏来传递失败原因码，以及 `${AUCTION_MIN_TO_WIN}` 宏传递最低胜出价。注意：Exchange 的政策可能不支持 Loss Notice，或不披露胜出方的结算价格（此时宏会被替换为空字符串）。 |

#### 3.3.3 广告素材字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `adm` | `"<div>...</div>"` 或 VAST XML 或 Native JSON | string | **广告素材标记（Ad Markup）**。如果出价胜出，此字段中的内容即为要展示给用户的广告。可以是 HTML（Banner）、VAST XML（视频/音频）、Native JSON（原生广告）。如果同时指定了 `adm` 和 `nurl` 返回内容，**`adm` 优先**。其中也可以包含替换宏（如 `${AUCTION_PRICE}` 用于追踪像素）。 |
| `adid` | `"pre-approved-ad-314"` | string | 预先审核通过的广告 ID。如果 Exchange 有创意预审机制，DSP 可以引用已审核通过的广告 ID，加速素材审核流程。 |

**素材投放的两种方式**（详见规范 Section 4.3）：

| 方式 | 机制 | 优点 | 缺点 |
|------|------|------|------|
| **Markup on Win Notice** | `adm` 为空，素材通过 `nurl` 的响应体返回 | 节省带宽（只有胜出时才传输素材）；提供额外决策点 | 多一次 HTTP 调用，增加投放失败风险 |
| **Markup in Bid** | 素材直接放在 `adm` 中 | 降低因 Win Notice 调用失败导致的"弃权"（forfeit）风险；Exchange 可并发处理 | 带宽消耗更大 |

#### 3.3.4 广告主与质量检查字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `adomain` | `["brand-a.com"]` | string array | 广告主域名列表。**用于 Publisher 的广告主黑名单检查**。可以是数组以支持轮播创意。部分 Exchange 要求只包含一个域名。这是 Exchange 判断广告是否被 Publisher 屏蔽的关键字段。 |
| `bundle` | `""` | string | 如果广告推广的是一个 App，填写该 App 的商店 ID。Google Play 使用包名（如 `com.foo.mygame`），Apple App Store 使用数字 ID。CTV 参考 OTT/CTV App Identification Guidelines。 |
| `iurl` | `"https://cdn.dsp.example.com/..."` | string | **不含缓存清除参数的素材预览图 URL**。此图应能代表该广告系列的内容，供 Exchange 或 Publisher 进行广告质量/安全审核。 |
| `cid` | `"campaign111"` | string | 广告系列（Campaign）ID。用于广告质量检查，`iurl` 应能代表此 Campaign 下所有创意的内容。 |
| `crid` | `"creative-banner-300x250-v2"` | string | 创意（Creative）ID。用于广告质量检查，标识具体的创意版本。 |
| `tactic` | `"retargeting-q1-2025"` | string | 策略（Tactic）ID。允许买方标记出价所使用的投放策略，便于向 Exchange 报告。具体含义由买卖双方预先约定。 |

#### 3.3.5 创意分类与属性字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `cattax` | `2` | integer | 创意分类使用的分类体系。2 = IAB Content Taxonomy 2.0。默认 1。参考 AdCOM Category Taxonomies 枚举。 |
| `cat` | `["IAB2-1", "IAB2-2"]` | string array | 创意的 IAB 内容分类。Exchange 据此检查是否与 Publisher 屏蔽的类别冲突（对应 Bid Request 中的 `bcat`）。 |
| `attr` | `[1, 2, 7]` | integer array | 创意属性集合。描述创意的特征，如是否自动播放音频、是否可展开等。参考 AdCOM Creative Attributes 枚举。Exchange 会与 Bid Request 中的 `battr` 对比，被屏蔽的属性会导致出价被拒绝。常见值包括：1=音频自动播放, 2=音频用户触发, 6=视频贴片自动播放, 7=弹出窗口, 13=用户交互式, 14=弹窗式, 16=可跳过视频。 |
| `apis` | `[3, 5]` | integer array | 该素材支持的 API 框架列表。如果未列出某 API 则假定不支持。3 = MRAID-1, 5 = MRAID-2。参考 AdCOM API Frameworks 枚举。替代了已废弃的 `api` 字段。 |
| `api` | *(已废弃)* | integer | 已废弃，使用 `apis` 代替。 |
| `protocol` | `3` | integer | 视频/音频素材使用的响应协议。3 = VAST 3.0。参考 AdCOM Creative Subtypes - Audio/Video 枚举。仅在素材为视频或音频类型时有意义。 |
| `qagmediarating` | `1` | integer | 按 IQG（Inventory Quality Guidelines）标准的创意媒体分级。1 = 所有受众, 2 = 12岁以上, 3 = 成人内容。参考 AdCOM Media Ratings 枚举。 |
| `language` | `"en"` | string | 创意语言，ISO-639-1 代码。非标准代码 `"xx"` 可用于无语言内容的创意（如只有公司 Logo 的 Banner）。与 `langb` 互斥。 |
| `langb` | *(未使用)* | string | 创意语言，IETF BCP 47 格式。与 `language` 互斥。 |

#### 3.3.6 交易与尺寸字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `dealid` | `"AB-Agency1-0001"` | string | **对应 Bid Request 中 `deal.id` 的值**。当此出价是基于私有交易市场（PMP）的预先约定条款时填写。Exchange 会验证此 Deal ID 是否存在于请求中、出价是否满足 Deal 的底价和其他条款。 |
| `w` | `300` | integer | 创意宽度（设备独立像素 DIPS）。Exchange 会与请求中的 Banner/Video 尺寸要求进行匹配检查。 |
| `h` | `250` | integer | 创意高度（设备独立像素 DIPS）。 |
| `wratio` | `0` | integer | 以比例表示的相对宽度。Flex Ads（弹性广告）时必填。 |
| `hratio` | `0` | integer | 以比例表示的相对高度。Flex Ads 时必填。 |

#### 3.3.7 时长与类型字段

| 字段 | 示例值 | 类型 | 说明 |
|------|--------|------|------|
| `exp` | `300` | integer | DSP 愿意等待的竞拍到实际展示之间的最大秒数。如果超过此时间广告仍未展示，DSP 可能认为该展示已过期。应与 Bid Request 中的 `imp.exp` 配合使用。 |
| `dur` | `15` | integer | 视频或音频创意的时长（秒）。本例中第二个 bid 的视频时长为 15 秒。对于 Banner 类型通常为 0 或不设置。 |
| `mtype` | `1` | integer | **创意素材的类型标识**，用于让 Exchange 正确地将素材与 Bid Request 中 Imp 下的对应子对象关联。**1 = Banner, 2 = Video, 3 = Audio, 4 = Native**。这是 OpenRTB 2.6 新增的重要字段。 |
| `slotinpod` | `0` | integer | 指定此出价仅适用于视频/音频 Ad Pod 中的特定位置。0 = 任意位置（默认），1 = 第一个位置，2 = 最后一个位置。参考 AdCOM Slot Position in Pod 枚举。 |

---

## 四、替换宏（Substitution Macros）详解

替换宏是 OpenRTB 中极为重要的机制。DSP 在 `nurl`、`burl`、`lurl` 以及 `adm` 中嵌入宏，Exchange 在实际调用时将宏替换为真实数据。

| 宏 | 说明 | 使用场景 |
|-----|------|---------|
| `${AUCTION_ID}` | Bid Request 的 ID（来自 `BidRequest.id`） | 所有通知 URL 和素材中 |
| `${AUCTION_BID_ID}` | Bid Response 的 ID（来自 `BidResponse.bidid`） | Win/Loss/Billing Notice |
| `${AUCTION_IMP_ID}` | 被赢得的展示 ID（来自 `imp.id`） | Win/Billing Notice |
| `${AUCTION_SEAT_ID}` | 出价方的席位 ID | Win Notice |
| `${AUCTION_AD_ID}` | DSP 希望投放的广告 ID（来自 `bid.adid`） | Win Notice |
| `${AUCTION_PRICE}` | **结算价格**，使用与出价相同的货币和单位（CPM） | **最重要的宏**，用于所有通知 URL 和素材追踪像素 |
| `${AUCTION_CURRENCY}` | 出价使用的货币（显式或隐式），仅用于确认 | Win/Billing Notice |
| `${AUCTION_MBR}` | 市场出价比率 = 结算价 / 出价价格 | Win Notice |
| `${AUCTION_LOSS}` | 失败原因代码（参考 Loss Reason Codes 枚举） | **仅用于 Loss Notice** |
| `${AUCTION_MIN_TO_WIN}` | 赢得竞拍所需的最低出价 | Win/Loss Notice |
| `${AUCTION_MULTIPLIER}` | 实际赢得的展示数量乘数（用于 DOOH/CTV 确认） | Billing Notice |
| `${AUCTION_IMP_TS}` | 展示实际发生的 Unix 时间戳（毫秒） | Billing Notice |

### 宏编码

为安全目的，可以对宏值进行编码。语法：`${MACRO_NAME:X}`，其中 X 是编码算法代码（需双方约定）。

例如：`${AUCTION_PRICE:B64}` — 表示使用 Base64 编码结算价格。

### 最佳实践

- 测试或广告质量审核时，如果宏值未知，应替换为 `"AUDIT"`
- Exchange 到 DSP 之间的直接通信（如 Win Notice）通常不需要编码
- 当价格信息通过设备浏览器中的追踪像素传递时，建议使用编码以防止泄露

---

## 五、`${AUCTION_MIN_TO_WIN}` 宏的特殊规则

此宏的替换值取决于出价结果：

### 第一价格拍卖示例（底价 $0.85）

| 出价 | 结果 | `${AUCTION_PRICE}` | `${AUCTION_MIN_TO_WIN}` |
|------|------|---------------------|--------------------------|
| $1.00 | 胜出 | $1.00 | $0.90（追平第二名所需价格） |
| $0.90 | 落败 | 空字符串 | $1.00（追平胜出者所需价格） |
| $0.80 | 落败（低于底价） | 空字符串 | $1.00 |
| 无效出价 | 被拒 | N/A | 空字符串 |

### 第二价格拍卖示例（结算价 = 次高价 + $0.01）

| 出价 | 结果 | `${AUCTION_PRICE}` | `${AUCTION_MIN_TO_WIN}` |
|------|------|---------------------|--------------------------|
| $1.00 | 胜出 | $0.91 | $0.90（追平第二名所需价格） |
| $0.90 | 落败 | 空字符串 | $0.91（追平胜出者结算价所需价格） |
| $0.80 | 落败 | 空字符串 | $0.91 |
| 无效出价 | 被拒 | N/A | 空字符串 |

Exchange 也可能因隐私策略等原因选择用空字符串替换这些宏。

---

## 六、三种广告类型的 adm 格式对比

### 6.1 Banner（HTML Markup）

```html
<div id="ad-container">
  <a href="https://brand.com/landing" target="_blank">
    <img src="https://cdn.dsp.com/banner_300x250.jpg"
         width="300" height="250" alt="Ad"/>
  </a>
  <!-- 展示追踪像素，包含结算价格宏 -->
  <img src="https://dsp.com/impression?price=${AUCTION_PRICE}"
       width="1" height="1" style="display:none;"/>
</div>
```

对应 Bid 中 `mtype=1`。

### 6.2 Video（VAST XML）

```xml
<?xml version="1.0" encoding="utf-8"?>
<VAST version="3.0">
  <Ad id="video-ad-567">
    <InLine>
      <AdSystem>DSP Ad Server</AdSystem>
      <AdTitle>Brand Video Ad</AdTitle>
      <Impression>
        <![CDATA[https://dsp.com/impression?price=${AUCTION_PRICE}]]>
      </Impression>
      <Creatives>
        <Creative>
          <Linear>
            <Duration>00:00:15</Duration>
            <MediaFiles>
              <MediaFile delivery="progressive" type="video/mp4"
                         width="640" height="480" bitrate="800">
                <![CDATA[https://cdn.dsp.com/video.mp4]]>
              </MediaFile>
            </MediaFiles>
          </Linear>
        </Creative>
      </Creatives>
    </InLine>
  </Ad>
</VAST>
```

对应 Bid 中 `mtype=2`，`protocol` 指定 VAST 版本。

### 6.3 Native（JSON String）

```json
{
  "native": {
    "ver": "1.1",
    "link": {
      "url": "https://brand.com/native-landing",
      "clicktrackers": ["https://dsp.com/track?event=click"]
    },
    "imptrackers": [
      "https://dsp.com/track?event=impression&price=${AUCTION_PRICE}"
    ],
    "assets": [
      {"id": 1, "title": {"text": "Ad Title Here"}},
      {"id": 2, "img": {"url": "https://cdn.dsp.com/native_main.jpg", "w": 1200, "h": 627}},
      {"id": 3, "data": {"value": "Brand Tagline"}}
    ]
  }
}
```

注意在 Bid 中 `adm` 是 JSON 字符串（需要转义），对应 `mtype=4`。

---

## 七、对象层级关系总览

```
BidResponse
├── id                   ← 必填，回传 BidRequest.id
├── bidid                ← DSP 自定义的响应追踪 ID
├── cur                  ← 出价货币（默认 USD）
├── customdata           ← 写入 Exchange Cookie 的自定义数据
├── nbr                  ← 不出价原因码（仅 no-bid 时使用）
│
└── seatbid[]            ← 按席位分组的出价集合
    ├── seat             ← 买方席位 ID（广告主/代理商）
    ├── group            ← 是否要求整组赢得（0=单独, 1=整组）
    │
    └── bid[]            ← 具体出价列表
        │
        ├── 【必填字段】
        │   ├── id       ← 出价唯一 ID
        │   ├── impid    ← 对应请求中的 imp.id
        │   └── price    ← 出价金额（CPM）
        │
        ├── 【通知 URL】
        │   ├── nurl     ← Win Notice URL（含宏）
        │   ├── burl     ← Billing Notice URL（含宏）
        │   └── lurl     ← Loss Notice URL（含宏）
        │
        ├── 【素材内容】
        │   ├── adm      ← 广告素材标记（HTML/VAST/Native JSON）
        │   └── adid     ← 预审核广告 ID
        │
        ├── 【质量检查】
        │   ├── adomain  ← 广告主域名（黑名单检查）
        │   ├── bundle   ← 推广 App 的商店 ID
        │   ├── iurl     ← 素材预览图 URL
        │   ├── cid      ← Campaign ID
        │   ├── crid     ← Creative ID
        │   └── tactic   ← 策略 ID
        │
        ├── 【分类与属性】
        │   ├── cattax   ← 分类体系
        │   ├── cat      ← 创意内容分类
        │   ├── attr     ← 创意属性（如自动播放、可跳过等）
        │   ├── apis     ← 支持的 API 框架
        │   ├── protocol ← 视频协议（VAST 版本）
        │   ├── qagmediarating ← IQG 媒体分级
        │   └── language ← 创意语言
        │
        ├── 【交易与尺寸】
        │   ├── dealid   ← PMP Deal ID
        │   ├── w / h    ← 创意宽高
        │   └── wratio / hratio ← Flex Ads 宽高比
        │
        └── 【时长与类型】
            ├── exp      ← 最大等待时间（竞拍到展示）
            ├── dur      ← 视频/音频时长（秒）
            ├── mtype    ← 素材类型（1=Banner, 2=Video, 3=Audio, 4=Native）
            └── slotinpod ← Pod 中的位置偏好
```

---

## 八、Bid Response 与 Bid Request 的对应关系

理解响应如何与请求关联是实现 OpenRTB 的关键：

```
BidRequest                          BidResponse
─────────                          ────────────
id: "req-001"          ───────────→ id: "req-001"         (必须一致)

imp[0].id: "1"         ───────────→ bid.impid: "1"        (出价引用展示)

imp[0].pmp.deals[0]
  .id: "Deal-ABC"      ───────────→ bid.dealid: "Deal-ABC" (引用 Deal)

imp[0].bidfloor: 0.50  ───────────→ bid.price: 9.43       (必须 ≥ bidfloor)

imp[0].banner          ───────────→ bid.mtype: 1          (标识素材类型)
  .battr: [13,14]      ───────────→ bid.attr: [1,2,7]     (不能包含被屏蔽的属性)

imp[0].banner
  .w: 300, .h: 250     ───────────→ bid.w: 300, .h: 250   (尺寸匹配)

bcat: ["IAB25"]        ───────────→ bid.cat: ["IAB2-1"]    (不能包含被屏蔽的类别)

badv: ["blocked.com"]  ───────────→ bid.adomain: ["ok.com"](不能包含被屏蔽的域名)

at: 1 (第一价格)        ───────────→ ${AUCTION_PRICE}=bid价格 (结算方式)
```

---

## 九、关键设计要点

1. **`id` 必须回传请求的 ID**：`BidResponse.id` 必须与 `BidRequest.id` 完全一致，这是 Exchange 关联请求与响应的唯一依据。

2. **一个 Bid 只能出一种类型**：虽然请求中同一个 Imp 可以同时包含 Banner、Video、Native，但每个 Bid 只能选择其中一种类型，并通过 `mtype` 字段标识。

3. **同一展示可以收到多个出价**：同一个 SeatBid 中或不同 SeatBid 中的多个 Bid 可以引用同一个 `impid`，这样可以提高胜出概率。

4. **`adm` 优先于 `nurl` 返回的素材**：如果两者都包含广告素材标记，Exchange 使用 `adm` 中的内容。

5. **宏替换发生在 Exchange 侧**：DSP 只需在 URL 和 adm 中嵌入宏模板，Exchange 在实际调用时完成替换。

6. **价格使用 CPM 但交易按单次展示**：`price` 字段是 CPM 值，但实际只购买一次展示。例如 `price=9.43` 表示每千次展示 $9.43，实际单次展示成本为 $0.00943。

7. **不出价的最优方式是 HTTP 204**：比返回空的 BidResponse 更节省带宽。但如果想告知 Exchange 不出价的原因，可以返回仅含 `nbr` 的 BidResponse。

8. **`burl` 和 `nurl` 的区别**：`nurl` 告知"你赢了"（用于调整竞价算法），`burl` 告知"该计费了"（用于实际扣款）。两者触发时机可能不同。

9. **OpenRTB 2.6 重要新增字段**：`mtype`（创意类型标识）、`apis`（替代废弃的 `api`）、`slotinpod`（Pod 位置偏好）、`dur`（视频时长）。