1. client bidding  android sdk 插件化和配置下发 弱网环境下的降级策略 -> 自定义adn能力了
2. 每个ADN平台维护独立的HTTP连接池 golang 并发请求 ， 
id -> 高性能ID生成器 -> 雪花算法 高性能数组 防止伪共享（False Sharing）：在极端高并发下，队列的 head 和 tail 指针如果处于同一个 CPU 缓存行（Cache Line），会导致多核 CPU 频繁失效缓存。生产级代码通常会在结构体中加入 [56]byte 这样的填充字段（Padding），将它们隔离到不同的缓存行中。
imp -> id 流量方ADX生成的展示 ID 
       bidfloor ->
       tagid ->  

3. 合规隐私 IDFA


https://developers.adnet.qq.com/doc/bidding/server_bidding


写在开头：工作强度9：30-18：30，基本不加班；薪资不压不卡预算；没有管理的位置；公司规模不到100人，有长期稳定赚钱的业务；
要求：技术栈go+想来创业公司+P5-P7级别（P8级别以上不合适，除非特别合适且可以接受IC岗位）
职位描述：
1、负责程序化广告交易系统（DSP/ADX）的核⼼模块设计与开发，包括但不限于：竞价引擎、流量接⼊、策略配置、投放控制、计费与扣费、数据报表等
2、优化⾼并发、低延迟的实时竞价（RTB）链路，保障单机万级QPS下的毫秒级响应
3、参与广告流量的对接与协议适配（支持OpenRTB、各类媒体/ADX私有协议），提升流量接⼊效率与稳定性
4、建设DSP侧的人群定向、预算控制、频次控制、出价策略等基础投放能力
5、负责线上服务的问题排查、性能调优与稳定性建设，保障广告系统高可用
职位要求
1、本科及以上学历，计算机相关专业，3年以上后端开发经验
2、掌握 Go，有良好的并发编程、性能调优与工程规范能力
3、熟悉常见中间件：Redis、Kafka、MySQL、ClickHouse等
4、至少1年以上程序化广告系统开发经验
5、熟悉 DSP 或 ADX 的核心链路与业务逻辑
6、理解 OpenRTB协议，有实际流量对接经验（如穿山甲、优量汇、百青藤、Google ADX等）
7、了解广告竞价的核心策略：如预算平滑、频次控制、人群定向、流量优选等
加分项：
1、有从0到1搭建DSP/ADX系统的经验
2、熟悉广告计费逻辑（CPM/CPC/CPA/OCPM）及实时扣费实现
3、了解机器学习预测模块（CTR/CVR） 与竞价引擎的协同方式
4、有大数据处理经验（Flink/Spark）或广告投放效果分析经验

k8s 服务发现怎么做.
自研 gorouter 调度.



# 1. 百万QPS 请求优化 
1. 智能DNS - 就近原则 anycast 自建 。  LB -> LVS 四层负载均衡+Nginx / OpenResty 七层复杂 -> 简单校验，简单限流。 3. 做到无状态服务集群。广告请求本身必须无状态。，可以水平扩容。 
2.  常见的限流算法-> 1. 分片 2. 滑动 3. 令牌桶 -> 分布式令牌桶、
3. 请求参数标准化 这个问题的核心是要建立统一的请求模型（Unified Ad Request），因为不同 SDK 版本、不同操作系统上报的字段差异很大。  Adapter 模式适配不同来源 --设备信息标准化（IDFA/GAID/OAID 统一映射到内部 device_id，处理 iOS ATT 框架下 IDFA 获取不到的情况）；地理位置标准化（GPS 坐标 → 城市/区县编码，使用 GeoHash 索引加速）；广告位信息标准化（素材尺寸、支持的广告类型、SDK 版本能力映射）。
4. 风控和流量分级 - 高价值流量 普通流量 低价值流量  **数据统计和GBDT** 
5. DSP/AdX 竞价调度（核心难点） 异步并行 + 统一超时的设计 - 问题 1. DSP 竞价超时率很高怎么办？怎么做动态 DSP 选择？ 解决方案是做 DSP 健康度评分 + 动态路由。**给每个 DSP 维护一个滑动窗口的健康度分数（广告位粒度），核心指标包括：超时率（权重最高）、平均出价、竞胜率、广告质量分**。每分钟更新一次评分，评分低于阈值的 DSP 自动降级 — 减少发送的请求量甚至暂时摘除。恢复机制用探针模式：每隔一段时间发少量请求探测，恢复正常后逐步放量。基于滑动窗口统计每个ADN最近N分钟的三个核心指标——平均出价水平、有效响应率、超时率——通过加权评分公式计算出各ADN的请求分配权重。得分高的ADN分配更多请求量，长期低效的ADN自动降权减量。 2. 出价方法 bid sharing ， 一价，二价，bid cache 
6. OpenRTB 协议 ， 关键 请求id, adm -> 广告渲染样式 ， 特殊的东西 ID生成。 sync.pool , sync.atomic
7. 特征召回，索引化处理  -> 比如server bidding 低价，或者一个瀑布流的配置有很多限制，需要做这种东

（1） 召回逻辑
倒排索引结构：
  地域维度:   北京 → [ad_1, ad_5, ad_8, ...]
              上海 → [ad_2, ad_5, ad_9, ...]
  性别维度:   男   → [ad_1, ad_3, ad_7, ...]
  年龄维度:   18-25 → [ad_2, ad_5, ad_6, ...]
  兴趣维度:   游戏  → [ad_1, ad_4, ad_8, ...]

请求（北京,男,20岁,兴趣=游戏）
  → 北京∩男∩18-25∩游戏 → {ad_1} 命中

（2） 匹配 -> 地区，设备，应用xxx -> 序列化成特征+ redis 读、


8. **平台预算扣减** 调价的细粒度是到了广告位粒度的。  deviceID 力度数据量不够，不置信

（1） 减数的方法：  超前领取。 
（2） 价格波动，平台扣减 ，使用 函数分区 。 指数函数或者对数函数 线性函数
（3） 基于反馈动态调价 - 固定规则 。 

9. 传统瀑布流（Waterfall）模式有什么问题？Header Bidding 怎么解决的？

传统 Waterfall 模式下，媒体按优先级依次请求各广告源（先问 A，A 不填再问 B，B 不填再问 C）。这带来两个致命问题：第一，低优先级的广告源即使愿意出更高价，也没机会竞争，因为高优先级的源只要填充就直接拿走了，媒体的收益天花板被人为压低。第二，串行调用导致延迟叠加，每多一层就多几百毫秒。

Client-Side Header Bidding 和 Server-Side Header Bidding 有什么区别？你会怎么选？
这是 Header Bidding 架构层面最核心的决策。
Client-Side（客户端竞价）
优点是 Cookie/设备信息直接可用，Bidder 能精准定向，出价更高。缺点是并发能力受限于客户端环境（浏览器并发连接数限制、手机网络质量差异大），Bidder 数量多了延迟不可控，而且 SDK 体积膨胀影响 App 性能。
Server-Side（服务端竞价）
优点是并发能力强（服务端网络环境好，可以轻松并行调用几十个 Bidder）、延迟可控（统一超时管理）、客户端轻量

移动端（App 场景）几乎都选 Server-Side，因为设备信息（GAID/IDFA）本身就在请求参数里传递

10. server bidding 并行竞价的超时管理策略怎么设计？简单设一个固定超时够吗？

固定超时是最初级的做法，实际需要多层超时 + 自适应超时。
第一层是全局超时（Hard Deadline），比如 100ms，到时间不管谁没返回，用已有结果做决策。这是绝对底线，保护用户体验。
第二层是单 Bidder 超时，每个 Bidder 有独立的超时设置，根据历史表现动态调整。
第三层是自适应超时（核心亮点），对于同一个 Bidder，不同时段、不同网络状况下的响应速度差异很大。用滑动窗口统计每个 Bidder 的 P90/P95 延迟，动态调整它的超时值。

11. Bidder Adapter 层（协议适配） 不同 Bidder 的协议和接口都不一样，怎么做统一适配？

这是 Header Bidding 系统中工程量最大的模块。每个 DSP/AdX 的接口格式、认证方式、字段映射都不同。核心设计是 Adapter Pattern + 插件化。
重点难点在于价格标准化。不同 Bidder 的价格体系差异巨大：有的报 CPM（千次展示价格），有的报单次展示价格；有的用美元，有的用人民币；有的是明文，有的是加密价格（Google 用的是自己的加密方案）。必须统一转换成同一计价单位（通常是微元/次展示）才能公平比较。

12. 竞价决胜引擎 

面试题 5：Header Bidding 场景下一价和二价怎么选？Floor Price 怎么设？
Header Bidding 行业趋势是全面转向一价竞拍（First-Price Auction），原因是 Header Bidding 本身改变了竞价的博弈结构。
在传统 Waterfall + 二价模式下，DSP 的真实出价是占优策略（Vickrey 拍卖理论保证）。但在 Header Bidding 环境下，同一次曝光可能经过多个竞价层（先在 Header Bidding 层比，胜者再和 Ad Server 的直投/合约广告比），二价机制被"嵌套竞价"打破了，DSP 无法判断最终结算价格，反而会倾向于降低出价。一价模式更简单透明：你出多少就付多少。

但一价模式下 DSP 会做 Bid Shading（出价折扣），作为 SSP 侧需要通过 Floor Price 策略来对冲这一点。

13. 响应时长优化（核心难点）

第一段：客户端到服务端的网络延迟（目标 < 20ms）
部署边缘节点，用 CDN Anycast 就近接入。在中国场景下，至少需要华北、华东、华南三个区域。对于移动端，使用长连接而不是每次 HTTP 短连接，省掉 TCP 握手 + TLS 握手的开销（大约省 50-80ms）。  使用http3 QUIC 协议 **https://zhuanlan.zhihu.com/p/655070575**

从 TCP 到 HTTP/2 到 QUIC — 逐层进化
2.1 先搞透 TCP 的瓶颈
面试题 1：TCP 在高性能广告场景下的核心瓶颈是什么？不是说 TCP 可靠吗？
TCP 的可靠性恰恰是它在广告场景下的最大问题。可靠性靠的是重传和确认，而重传和确认需要时间。
瓶颈一：建连延迟
TCP三次握手: 1 RTT (往返时间)
TLS 1.2握手: 2 RTT (ClientHello→ServerHello→密钥交换→Finished)
TLS 1.3握手: 1 RTT (合并了密钥交换步骤)

总建连延迟:
  TCP + TLS 1.2 = 3 RTT
  TCP + TLS 1.3 = 2 RTT
  
假设客户端到服务端RTT=30ms:
  TCP + TLS 1.2 = 90ms  ← 光握手就用掉了竞价预算的60%
  TCP + TLS 1.3 = 60ms  ← 还是太多
瓶颈二：队头阻塞（Head-of-Line Blocking）
TCP 是字节流协议，保证有序交付。如果序列中一个包丢了，后面所有包都要等重传完成才能交给应用层，即使后面的包已经到了。在 HTTP/1.1 里这意味着一个请求卡住了后面所有请求都卡住。
TCP队头阻塞:
  包1 ✓  包2 ✗(丢了)  包3 ✓  包4 ✓  包5 ✓
  
  应用层看到: 包1 ✓ → 等待包2重传... → 等了200ms → 包2补到 → 包3包4包5一起交付
  
  在广告场景:
    → 一个DSP的响应包丢了，其他DSP的响应被TCP层阻塞了
    → 直到超时，所有响应一起失败
瓶颈三：拥塞控制的冷启动
TCP 慢启动从很小的窗口（initcwnd，默认 10 个 MSS ≈ 14KB）开始，指数增长到合适的发送速率。对于广告请求这种小数据量、短周期的通信，每次新连接都要经历慢启动，还没到最佳速率请求就结束了。
java// 服务端TCP内核参数优化（Linux sysctl）
```
public class TcpTuning {
    /*
     * 增大初始拥塞窗口 — 让新连接一开始就能发更多数据
     * 默认10，广告场景建议32-64
     * ip route change default via <gw> initcwnd 32 initrwnd 32
     */
    
    /*
     * 启用TCP Fast Open (TFO) — 在SYN包里携带数据，省1个RTT
     * sysctl -w net.ipv4.tcp_fastopen=3  (客户端+服务端都启用)
     * 
     * 效果: 第二次及以后的连接，建连和首个请求合并
     *   首次: SYN → SYN-ACK(带cookie) → ACK+Data    仍需1RTT建连
     *   后续: SYN+Data(带cookie) → SYN-ACK+Response  建连和请求同时完成 省1RTT
     */
    
    /*
     * 禁用Nagle算法 — 小包立即发送，不等凑满
     * TCP_NODELAY = 1
     * 广告请求通常只有几KB，Nagle会额外等40ms凑包
     */
    
    /*
     * 启用TCP_QUICKACK — 立即发送ACK，不延迟
     * 与TCP_NODELAY配合，减少小包场景的人为延迟
     */
    
    /*
     * 连接复用相关:
     * tcp_tw_reuse = 1      允许TIME_WAIT的连接被新连接复用
     * tcp_max_tw_buckets     控制TIME_WAIT总数（高并发下会爆）
     * tcp_keepalive_time     长连接保活间隔
     */
}
```
2.2 HTTP/2 深度解析
面试题 2：HTTP/2 解决了 HTTP/1.1 的哪些问题？在广告系统里怎么用？
HTTP/2 的三个核心改进，每个都直接命中广告场景的痛点。
改进一：多路复用（Multiplexing）
一条 TCP 连接上可以同时传输多个请求/响应，它们被拆成帧（Frame），通过 Stream ID 标识属于哪个请求，交错传输。
HTTP/1.1（串行或多连接）:
  连接1: [请求A完整传输] → [响应A完整传输] → [请求B...] → [响应B...]
  连接2: [请求C完整传输] → [响应C完整传输]
  连接3: [请求D完整传输] → [响应D完整传输]
  → 6个TCP连接才能并行6个DSP竞价

HTTP/2（多路复用）:
  一条连接:
    [A帧1][C帧1][B帧1][A帧2][D帧1][C帧2][B帧2]...
    所有请求在一条连接上交错传输
  → 1个TCP连接搞定所有DSP（当然实际会用几条做冗余）
在广告系统中，Ad Server 到每个 DSP 只需要维护 1-2 条 TCP 连接（而非 HTTP/1.1 时代的几十条），大幅降低连接管理的复杂度和内存消耗。
改进二：头部压缩（HPACK）
HTTP 头部在广告请求里占比可观（Cookie、Accept、各种 X-Header），而且相邻请求的头部高度相似。HPACK 用静态表（61 个常见 header）+ 动态表（连接上出现过的 header）+ Huffman 编码压缩。
压缩效果:
  典型广告竞价请求头(HTTP/1.1): ~800字节
  HPACK压缩后(HTTP/2):          ~150字节    节省约80%
  
  百亿次请求 × 650字节节省 = 每天省约6TB出站带宽
改进三：服务端推送（Server Push）
服务端在客户端请求一个资源时，主动推送相关资源。在广告场景用得不多，但有一个巧妙用法：Ad Server 返回广告响应的同时，主动推送该广告的素材预加载提示，让客户端提前开始下载素材。
面试题 3：HTTP/2 的多路复用解决了 HTTP 层的队头阻塞，但 TCP 层的队头阻塞还在吗？
还在。这是面试中区分候选人是否真正理解协议栈层次的关键题目。
HTTP/2 的多路复用让多个 Stream 在一条 TCP 连接上并行，HTTP 层不再有队头阻塞。但所有 Stream 共享同一条 TCP 连接，TCP 层仍然保证字节有序交付。如果 TCP 层丢了一个包，所有 Stream 的数据都被阻塞，直到重传完成。
HTTP/2 + TCP 的队头阻塞问题:

Stream 1 (DSP-A响应): [帧1] [帧2] [帧3]
Stream 2 (DSP-B响应):       [帧1] [帧2]
Stream 3 (DSP-C响应): [帧1]       [帧2] [帧3]

TCP字节流: [S1帧1][S3帧1][S2帧1][S1帧2][S3帧2][S2帧2][S1帧3][S3帧3]
                            ↑
                         这个包丢了

结果: S1帧2之后的所有帧（包括S3帧2、S2帧2等）都要等这个包重传
      即使S3帧2已经到了接收端内存里，TCP也不会交给HTTP/2层
      → Stream 3被Stream 2的丢包连累了
在弱网环境下（比如 SDK 到 Ad Server 的移动网络），丢包率 2-5% 是常态。2% 丢包率下 HTTP/2 的性能可能比 HTTP/1.1 的 6 条并行连接还差，因为 HTTP/1.1 各连接独立，一条连接丢包不影响其他连接。
这就是 QUIC 诞生的直接动因。

2.3 QUIC 深度解析
面试题 4：QUIC 的核心设计思想是什么？相比 TCP+TLS+HTTP/2 解决了哪些问题？
QUIC 的设计哲学是把传输层和加密层融为一体，在用户态实现，彻底解决 TCP 的历史包袱。
协议栈对比:

传统:                          QUIC:
┌──────────┐                  ┌──────────┐
│  HTTP/2  │                  │  HTTP/3  │
├──────────┤                  ├──────────┤
│   TLS    │                  │   QUIC   │  ← 传输+加密一体化
├──────────┤                  │  (UDP上) │
│   TCP    │                  ├──────────┤
├──────────┤                  │   UDP    │  ← 只借UDP的端口复用和校验和
│   IP     │                  ├──────────┤
└──────────┘                  │   IP     │
                              └──────────┘
QUIC 解决的四个核心问题：
问题一：0-RTT 建连
TCP+TLS 1.3 首次连接: 2 RTT (TCP握手1RTT + TLS握手1RTT)
QUIC 首次连接:        1 RTT (密钥交换和连接建立合并)
QUIC 恢复连接:        0 RTT (用缓存的会话密钥直接发数据)

0-RTT的意义:
  假设RTT=30ms
  TCP+TLS: 60ms建连 + 请求 = 90ms才开始传数据
  QUIC 0-RTT: 0ms建连 + 请求 = 30ms就开始传数据
  → 在广告场景省了60ms，这几乎是竞价预算的40%
QUIC 0-RTT 流程:

首次连接 (1-RTT):
  Client → Server: Initial (ClientHello + 传输参数)
  Server → Client: Initial (ServerHello) + Handshake (证书+Finished) + 1-RTT数据
  Client → Server: Handshake (Finished) + 1-RTT数据
  → 从第二个包开始就能携带应用数据

恢复连接 (0-RTT):
  Client → Server: Initial (ClientHello + 恢复票据) + 0-RTT数据(应用请求!)
  Server → Client: Initial + Handshake + 1-RTT数据(应用响应!)
  → 客户端第一个包就带了应用层请求，无需等待握手完成
问题二：消除队头阻塞
QUIC 的每个 Stream 有独立的流控和重传逻辑。一个 Stream 丢包只影响该 Stream，其他 Stream 不受影响。
QUIC多Stream独立传输:

Stream 1: [包1] [包2] [包3]    ← 包2丢了，只有Stream 1等重传
Stream 2: [包1] [包2]          ← 正常交付，不受影响
Stream 3: [包1] [包2] [包3]    ← 正常交付，不受影响

对比TCP上的HTTP/2:
  所有Stream共享一个字节流 → 一个包丢了全部阻塞
在广告场景中，Ad Server 并行调用 5 个 DSP 用 5 个 QUIC Stream，DSP-C 的响应包丢了只影响 DSP-C，DSP-A、B、D、E 的响应正常返回参与竞价。这在丢包率 2% 的移动网络环境下差异巨大。
问题三：连接迁移
TCP 连接由四元组（源 IP、源端口、目标 IP、目标端口）标识。手机从 WiFi 切到 4G，IP 变了，连接就断了，要重新三次握手 + TLS 握手。
QUIC 用 Connection ID 标识连接，和 IP/端口无关。IP 变了，Connection ID 不变，连接无缝迁移。
TCP (WiFi → 4G切换):
  WiFi连接: 192.168.1.5:12345 → server:443  [活跃]
  切换4G...
  WiFi连接: [断开，TCP重置]
  4G新连接: 10.0.0.1:54321 → server:443     [重新握手，60ms+]
  
QUIC (WiFi → 4G切换):
  WiFi连接: CID=abc123
  切换4G... IP从192.168.1.5变成10.0.0.1
  QUIC: 同一个CID=abc123，继续传输，应用层无感知
  延迟: 0ms (连接没断)
这对移动端广告 SDK 特别重要——用户在地铁里频繁切换基站，如果每次切换都要重建连接，广告请求的失败率会很高。

用户态实现，快速迭代
TCP 在内核里，改一个拥塞控制算法要等内核版本更新，再等运营商/厂商推送。QUIC 在用户态（应用层），更新一个 App 版本就能部署新的拥塞控制算法。Google 就是通过 Chrome 更新，在几周内就把 QUIC 的拥塞控制从 Cubic 换成了 BBR。
面试题 5：QUIC 用 UDP，UDP 不可靠啊，怎么保证数据不丢？
这是高频误解题。QUIC 不是"用 UDP 传数据然后祈祷不丢"，QUIC 自己在用户态实现了完整的可靠传输机制（确认、重传、流控、拥塞控制），比 TCP 的还精细。
UDP 在这里只是一个"端口复用 + 校验和"的薄壳。QUIC 选择建在 UDP 上而不是直接建在 IP 上，唯一原因是中间的 NAT/防火墙普遍允许 UDP 通过，如果用一个全新的传输层协议号，绝大多数网络设备会直接丢弃。
QUIC自己实现的可靠性机制:

1. 包级别确认 (ACK Frames)
   每个包有唯一的Packet Number（严格递增，不复用）
   接收方用ACK Frame告知哪些包收到了
   比TCP的seq/ack更精确（TCP的序列号可能因重传而模糊）

2. 独立重传
   丢了哪个包就重传哪个包，不影响其他Stream的包
   重传包有新的Packet Number（不是TCP那样重用序列号）
   → 可以精确测量RTT（不会像TCP那样因重传歧义测不准）

3. 前向纠错 (FEC，可选)
   发送方额外发少量冗余包
   接收方可以从其他包恢复丢失的包，不需要等重传
   适合延迟敏感场景（广告就是）

4. 流控 (Flow Control)
   连接级 + Stream级 双层流控
   比TCP更精细，避免一个Stream占满整个连接的缓冲区
```

第二段：请求处理阶段（目标 < 5ms）
预解析和预计算。在连接建立时就缓存好设备信息、用户画像等，不要等请求来了再现查。用对象池避免 GC 抖动（广告请求对象频繁创建销毁，GC 是延迟尖刺的主要来源）。  **广告 cache** ： 注意这里哈 ，sdk联动的时候要注意token或者其他的标签要一致。 

14. 请求压缩与预计算
Bid Request 的 JSON 体可能有 2-5KB，对于高频调用来说序列化/反序列化的开销不可忽略。优化手段：使用 Protobuf 替代 JSON（体积减少 60%，序列化速度快 5-10 倍）；对于支持 OpenRTB 的 Bidder，提前构建好请求模板，每次只填充变化的字段。

但是有利有弊把。 portobuf 

15. Header Bidding 的竞价结果怎么做到透明可审计？
这是商业层面极其重要但工程上容易被忽视的点。Bidder（DSP）接入 Header Bidding 后最大的顾虑就是"我不知道自己为什么输了"。
需要建设完整的 Auction Log + Bid Landscape 系统。

16. 竞价系统的id 体系   GAID/IDFA/OAID 

如果你是 Bidder（DSP），你怎么应对一价竞拍下的 Bid Shading？
这是反过来站在买方的视角。Bid Shading 的核心是预测市场价格的"清算价"（Market Clearing Price），然后出一个略高于清算价的价格，而不是出自己真实的估价。通常用 Censored Regression 模型 — 输入特征是广告位、时段、竞争度等，输出是预测的清算价。"Censored" 是因为你只能观测到自己赢了时的结算价（赢了才知道第二高价），输了的数据是缺失的（右删失），需要用生存分析的方法处理。  --- Censored Regression 模型

17. ？？？怎么防止 Bidder 窥探其他 Bidder 的出价？
在 Server-Side 架构下这天然做到了 — 所有 Bidder 的出价只有 SSP 看得到。但 Win Notice 中会携带结算价，Bidder 可以据此推断竞争情况。防护手段：Win Notice 中的价格做加密传输（Google 使用双重加密，用 Bidder 专属的密钥加密结算价），Loss Notice 只告知"你输了"但不透露赢家的价格。

18. 底价（Floor Price）到底在优化什么？为什么不直接设成 0 或者设得很高？

设成 0：所有出价都能赢，填充率 100%，但大量低价广告涌入拉低 eCPM，DSP 也会逐渐学到"这个媒体便宜"，越出越低（Race to Bottom）。设得很高：只有高价广告能赢，单次收益高，但大量请求无人填充，总收益反而下降。

E[Revenue] = 请求量 × FillRate(f) × AvgSettlementPrice(f)

其中 f = floor price
- FillRate(f)：底价越高，填充率越低，单调递减
- AvgSettlementPrice(f)：底价越高，成交均价越高，单调递增
- 两者乘积存在一个最优点 f*


┌──────────────────────────────────────────────────────────────────────┐
│                        动态底价系统全景                                │
│                                                                      │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────────────┐  │
│  │  数据采集层  │───>│  特征工程层   │───>│      模型层              │  │
│  │             │    │              │    │  ┌──────────────────┐   │  │
│  │ · 竞价日志  │    │ · 历史统计特征│    │  │ 离线模型(小时级) │   │  │
│  │ · Win/Loss  │    │ · 实时流特征  │    │  │  Survival Model  │   │  │
│  │ · 市场信号  │    │ · 上下文特征  │    │  └────────┬─────────┘   │  │
│  │ · 用户行为  │    │ · 竞争态势特征│    │           │ 基准底价     │  │
│  └─────────────┘    └──────────────┘    │  ┌────────▼─────────┐   │  │
│                                         │  │ 在线调整(秒级)    │   │  │
│                                         │  │  实时供需修正     │   │  │
│                                         │  └────────┬─────────┘   │  │
│                                         └───────────┼─────────────┘  │
│                                                     │                │
│  ┌──────────────────────────────────────────────────▼──────────────┐ │
│  │                      决策与安全层                                 │ │
│  │  底价输出 → 置信度检查 → 安全兜底 → AB实验分流 → 最终底价         │ │
│  └──────────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────┘


面试题 1：底价算法需要哪些数据？竞价日志里最关键的字段是什么？
底价算法依赖的核心数据是竞价日志（Auction Log），但和普通的请求日志不同，底价算法需要的是完整的出价分布，不仅要知道谁赢了出了多少，还要知道谁输了出了多少、谁没出价、谁超时了。
```
javapublic class AuctionRecord {
    // === 请求维度 ===
    String requestId;
    long   timestamp;
    String slotId;            // 广告位
    String adFormat;          // banner/interstitial/rewarded/native
    String appId;
    String deviceType;        // phone/tablet
    String os;                // iOS/Android
    String country;
    String region;
    int    hourOfDay;
    int    dayOfWeek;
    
    // === 竞价维度（核心） ===
    long   floorPrice;        // 本次设定的底价
    int    bidderCount;       // 参与竞价的Bidder数
    int    bidResponseCount;  // 实际返回出价的Bidder数
    
    List<BidDetail> bids;     // 所有出价明细（含被底价过滤的）
    
    // === 结果维度 ===
    boolean filled;           // 是否填充
    long    winningBid;       // 胜出价
    long    settlementPrice;  // 实际结算价
    long    revenue;          // 实际收入
    
    @Data
    static class BidDetail {
        String bidderId;
        long   bidPrice;          // 原始出价
        boolean belowFloor;       // 是否低于底价被过滤
        boolean timedOut;         // 是否超时
        long   latencyMs;
    }
}
```
这里有个非常关键的数据问题——删失数据（Censored Data）。
当底价设为 5 元时，出价 3 元、4 元的 Bidder 被过滤掉了，我们知道它们出价低于 5 元，但不知道它们具体出了多少。更严重的是，有些 Bidder 看到底价高于自己的预算，直接不出价了（连 bid response 都没有），我们甚至不知道它们本来愿意出多少。这就像医学试验中"病人中途退出"一样，是一种右删失。这个问题决定了后面模型选型必须能处理 **censored data**。

todo 为啥不适用机器学习预测出价呢？ 

特征可以分成四大类，每类解决不同的问题。
一、历史统计特征（回答"这个广告位值多少钱"）
slotId + timeWindow → 
  hist_ecpm_7d:     过去7天eCPM均值
  hist_ecpm_1d:     过去1天eCPM均值  
  hist_fill_rate_7d: 过去7天填充率
  hist_bid_density:  平均每次竞价收到几个出价
  hist_price_p25/p50/p75: 出价分布的分位数
  hist_win_rate_by_bidder: 各Bidder的历史胜率
二、实时供需特征（回答"现在市场热不热"）
最近5分钟/15分钟/1小时的滑动窗口 →
  rt_qps:           当前请求量（供给侧热度）
  rt_fill_rate:     实时填充率（需求侧响应）
  rt_avg_bid:       实时平均出价
  rt_bidder_count:  当前活跃Bidder数
  rt_timeout_rate:  Bidder超时率（网络问题信号）
  rt_bid_trend:     出价趋势（过去15分钟 vs 过去1小时的eCPM比值）
三、上下文特征（回答"这个具体请求值多少"）
请求级别 →
  hour_of_day:      小时（广告出价有明显日内周期）
  day_of_week:      星期几（工作日vs周末差异大）
  device_type:      设备类型（iOS通常比Android出价高20-30%）
  os_version:       系统版本（新系统用户价值更高）
  geo_tier:         地域分级（一线城市 vs 下沉市场）
  connection_type:  网络类型（WiFi vs 4G/5G）
  app_category:     App分类
  user_freq:        用户当天已看广告次数（频次越高价值越低）
四、竞争态势特征（回答"竞争格局是什么样的"）
  active_bidder_set: 当前在线的Bidder集合（某大DSP下线了，竞争减弱）
  bidder_budget_signal: Bidder预算消耗信号（月底预算冲量，出价会上升）
  seasonal_factor:  节日/大促因素（双11、黑五，广告主预算集中释放）
  inventory_scarcity: 库存稀缺度（该广告位最近请求量是否偏低）

19. 模型选型与算法设计

方法一：出价分布建模（Bid Landscape）
核心思想是先建模"在没有底价干预时，Bidder 的出价分布是什么样的"，然后在这个分布上做数学优化找最优底价。
如果知道出价分布 P(bid)，那么：
  给定底价 f，
    填充率 = P(max_bid > f) = 1 - CDF(f)
    条件均价 = E[max_bid | max_bid > f]
    期望收益 = RequestVolume × (1-CDF(f)) × E[max_bid | max_bid > f]
  
  对 f 求导令其为0，解出最优 f*
但前面说了，出价数据是删失的。解法是用**生存分析（Survival Analysis）**来建模。
python# 用Kaplan-Meier / Cox比例风险模型 处理删失数据
# 把"出价"类比为"生存时间"，"低于底价被过滤"类比为"删失事件"
```
import lifelines
import numpy as np

class BidLandscapeModel:
    """
    将出价建模为生存分析问题：
    - "生存时间" = 出价金额
    - "事件发生" = 出价被观测到（高于底价）
    - "删失" = 出价未被观测到（低于底价，只知道 bid < floor）
    """
    
    def fit(self, auction_records):
        # 构建生存分析数据
        durations = []     # "生存时间" = 出价或底价
        observed = []      # 是否被观测到
        
        for record in auction_records:
            for bid in record.bids:
                if bid.below_floor:
                    # 删失数据：只知道出价 < floor，用floor作为删失时间
                    durations.append(record.floor_price)
                    observed.append(0)  # censored
                else:
                    # 完整观测：知道确切出价
                    durations.append(bid.bid_price)
                    observed.append(1)  # observed
        
        # Kaplan-Meier估计出价的生存函数 S(f) = P(bid > f)
        self.kmf = lifelines.KaplanMeierFitter()
        self.kmf.fit(durations, event_observed=observed)
        
        return self
    
    def find_optimal_floor(self, request_features):
        """在估计的出价分布上搜索最优底价"""
        
        # S(f) = P(max_bid > f) ≈ 填充率
        survival_func = self.kmf.survival_function_
        
        best_floor = 0
        best_revenue = 0
        
        # 网格搜索（实际生产中用更高效的优化方法）
        for f in np.arange(0.01, 50.0, 0.01):  # 遍历候选底价
            fill_rate = self._get_survival_prob(f)
            # 条件期望：E[bid | bid > f]
            conditional_mean = self._get_conditional_mean(f)
            expected_revenue = fill_rate * conditional_mean
            
            if expected_revenue > best_revenue:
                best_revenue = expected_revenue
                best_floor = f
        
        return best_floor
```
这个方法的优势是可解释性强，劣势是对高维特征的建模能力有限（KM 是非参数方法，维度高了估计不准）。


方法二：基于梯度提升树的分段优化（工业界主流）
思路是把连续的底价决策离散化成分桶，转化为分类或排序问题。
```
pythonimport lightgbm as lgb
import numpy as np

class GBDTFloorPriceModel:
    """
    核心思路：
    1. 将历史数据按不同底价分桶，统计每个桶的收益
    2. 用GBDT学习 features → 最佳底价桶 的映射
    """
    
    def __init__(self):
        # 底价候选桶：[0.5, 1.0, 1.5, 2.0, ..., 30.0]（单位元CPM）
        self.floor_buckets = np.arange(0.5, 30.5, 0.5)
        self.model = None
    
    def prepare_training_data(self, auction_logs):
        """
        关键：利用同一广告位在不同时段设过不同底价的历史数据，
        构建"底价→收益"的因果关系样本。
        """
        X, y = [], []
        
        # 按 (slotId, hour, contextGroup) 分组
        for group_key, records in group_by_context(auction_logs):
            features = extract_features(records)
            
            # 对每个底价桶，用历史数据估算该底价下的期望收益
            revenue_by_bucket = {}
            for bucket_floor in self.floor_buckets:
                # 筛选底价在这个桶附近的历史记录
                nearby_records = [r for r in records 
                                  if abs(r.floor_price - bucket_floor) < 0.5]
                if len(nearby_records) < 30:  # 样本太少，跳过
                    continue
                
                fill_rate = np.mean([r.filled for r in nearby_records])
                avg_revenue = np.mean([r.revenue for r in nearby_records 
                                       if r.filled])
                revenue_by_bucket[bucket_floor] = fill_rate * avg_revenue
            
            if revenue_by_bucket:
                # 标签 = 使收益最大化的底价桶
                best_bucket = max(revenue_by_bucket, key=revenue_by_bucket.get)
                best_bucket_idx = np.searchsorted(self.floor_buckets, best_bucket)
                X.append(features)
                y.append(best_bucket_idx)
        
        return np.array(X), np.array(y)
    
    def train(self, X, y):
        train_data = lgb.Dataset(X, label=y)
        params = {
            'objective': 'multiclass',
            'num_class': len(self.floor_buckets),
            'metric': 'multi_logloss',
            'learning_rate': 0.05,
            'num_leaves': 63,
            'feature_fraction': 0.8,
            'bagging_fraction': 0.8,
        }
        self.model = lgb.train(params, train_data, num_boost_round=500)
    
    def predict(self, features):
        """返回最优底价"""
        probs = self.model.predict(features.reshape(1, -1))[0]
        best_idx = np.argmax(probs)
        return self.floor_buckets[best_idx]
```
方法三：强化学习（Contextual Bandit / RL）
把底价设定建模为一个序贯决策问题——每次请求来了选一个底价（action），观察到收益（reward），更新策略。
面试题 5：为什么底价优化适合用 Bandit/RL？和监督学习的本质区别是什么？
核心区别在于探索-利用困境（Exploration-Exploitation Dilemma）。
监督学习假设训练数据的分布是固定的，但底价场景下，你选择的底价本身会改变你观测到的数据分布（底价设高了，你就看不到低出价的样本了）。这就是 Bandit 问题的经典设定——你的决策影响了你的观测。
具体来说：Exploitation 是根据当前知识选择预期收益最高的底价。Exploration 是偶尔尝试其他底价，收集更多信息来更新认知。如果只做 Exploitation，可能陷入局部最优（比如你一直设 5 元底价效果还行，但永远不知道设 3 元可能总收益更高，因为填充率大幅提升）。
```
pythonimport numpy as np
from collections import defaultdict

class ContextualBanditFloorPrice:
    """
    Contextual Thompson Sampling for Floor Price Optimization
    
    - Context: 请求特征（广告位、时段、设备等）
    - Arms: 离散的底价候选值
    - Reward: 该次竞价的实际收益（未填充则为0）
    """
    
    def __init__(self, floor_candidates, context_dim):
        self.floors = floor_candidates  # [0.5, 1.0, 1.5, ..., 25.0]
        self.n_arms = len(floor_candidates)
        
        # 每个arm维护一个贝叶斯线性回归模型
        # 参数：均值向量 mu_a，精度矩阵 Lambda_a
        self.mu = {a: np.zeros(context_dim) for a in range(self.n_arms)}
        self.Lambda = {a: np.eye(context_dim) for a in range(self.n_arms)}
        self.sigma2 = 1.0  # 噪声方差先验
        
    def select_floor(self, context):
        """Thompson Sampling: 从每个arm的后验分布中采样，选最大的"""
        sampled_rewards = {}
        
        for a in range(self.n_arms):
            # 从后验 N(mu_a, sigma2 * Lambda_a^{-1}) 中采样 theta
            cov = self.sigma2 * np.linalg.inv(self.Lambda[a])
            theta_sample = np.random.multivariate_normal(self.mu[a], cov)
            sampled_rewards[a] = context @ theta_sample
        
        best_arm = max(sampled_rewards, key=sampled_rewards.get)
        return self.floors[best_arm], best_arm
    
    def update(self, arm, context, reward):
        """观察到收益后更新后验分布"""
        x = context.reshape(-1, 1)
        self.Lambda[arm] += x @ x.T / self.sigma2
        self.mu[arm] = np.linalg.inv(self.Lambda[arm]) @ (
            self.Lambda[arm] @ self.mu[arm] + x.flatten() * reward / self.sigma2
        )
    
    def select_floor_with_epsilon_decay(self, context, total_steps):
        """
        工业实践中更常用 epsilon-greedy + decay，比纯TS更稳定
        """
        epsilon = max(0.02, 0.2 * (0.999 ** total_steps))  # 从20%探索逐渐衰减到2%
        
        if np.random.random() < epsilon:
            # 探索：随机选一个底价（但不完全随机，在当前最优附近扰动）
            best_arm = self._get_greedy_arm(context)
            perturbed_arm = best_arm + np.random.choice([-2,-1,0,1,2])
            return self.floors[np.clip(perturbed_arm, 0, self.n_arms-1)]
        else:
            # 利用：选当前预期收益最高的
            return self.floors[self._get_greedy_arm(context)]
```

# RL 做底价在生产环境中最大的坑是什么？
三个核心坑。
第一个是探索的成本。探索意味着你要故意设"可能不是最优的"底价，这会直接损失收入。在广告系统里每个百分点的收入都很敏感，产品和商务会问"为什么这段时间 eCPM 掉了"。所以探索比例必须严格控制（通常 2%-5%），而且只能在低价值流量上做探索，高价值流量用 exploitation。
第二个是延迟反馈。设了底价后，真正的收益要等到广告展示、甚至点击/转化后才能确认。Reward 的延迟从毫秒到小时不等。需要设计好 reward attribution 机制。
第三个是非平稳环境。广告市场是高度动态的——节假日、大促、DSP 预算变化、竞品上下线都会改变出价分布。模型必须有遗忘机制（滑动窗口或指数衰减），不能让半年前的数据还在影响今天的决策。


20. DSP 会反向利用你的底价策略吗？怎么防？
这是底价系统中最容易被忽视但最深刻的问题。底价和出价本质上是一个博弈过程，DSP 是理性的 agent，它们会试图学习和利用你的底价模式。
博弈场景一：底价试探（Floor Probing）
DSP 故意交替出高价和低价，观察哪些被接受哪些被过滤，逆向推断你的底价。一旦知道底价是 3 元，它就把出价从 5 元降到 3.1 元。
防御：在底价上增加随机扰动。
javapublic long addNoise(long baseFloor) {
    // 在基准底价上加 ±10% 的均匀随机扰动
    double noiseFactor = 0.9 + Math.random() * 0.2;  // [0.9, 1.1]
    return (long)(baseFloor * noiseFactor);
}
博弈场景二：出价压缩（Bid Compression）
如果 DSP 发现你的底价总是跟着它们的出价降，它们就会集体缓慢降低出价，把底价"带"下来。
防御：底价的下调速度要有阻尼——可以快速上调但缓慢下调，而且设置绝对下限。
java// 底价的非对称调整：上调快，下调慢
public long adjustWithDamping(long currentFloor, long suggestedFloor) {
    if (suggestedFloor > currentFloor) {
        // 上调：允许一步到位
        return suggestedFloor;
    } else {
        // 下调：每次最多降5%，防止被Bidder带节奏
        long maxDrop = (long)(currentFloor * 0.05);
        return Math.max(suggestedFloor, currentFloor - maxDrop);
    }
}
博弈场景三：选择性退出
某大 DSP 威胁"你底价太高我就不参与了"，试图迫使你降低底价。
这其实是商业博弈而非纯技术问题。但技术上可以做的是：监测每个 Bidder 的参竞率变化趋势，如果某 Bidder 的参竞率在底价调整后显著下降，系统自动生成预警报告给商务团队，量化"这个 Bidder 退出带来的收入影响是多少"，辅助商业决策。

21. 冷启动设计 ： 三步走：先用同类广告位的均值做初始底价，然后 Bandit 探索 2-3 天快速收集数据，最后切换到正式模型。探索期接受 10-15% 的收益损失换取数据

22. 长连接优化深度方案
面试题 6：广告系统的长连接架构怎么设计？SDK 端和 Server 端分别需要注意什么？
广告系统涉及两种长连接：SDK → Ad Server（上行长连接）和 Ad Server → DSP（下行长连接）。两者的优化策略完全不同。
3.1 SDK → Ad Server 长连接
设计目标:
  - 减少建连开销（百亿请求如果每次都新建连接，光握手就扛不住）
  - 弱网环境下保持连接存活
  - 支持服务端主动推送（预加载、配置下发）

```
public class SdkConnectionManager {
    
    // === 连接建立策略 ===
    
    /**
     * 多协议降级策略：
     * 优先QUIC → 降级HTTP/2 → 兜底HTTP/1.1长连接
     */
    public Connection createConnection(String host) {
        // 第一步：尝试QUIC (0-RTT)
        try {
            QuicConnection quic = quicClient.connect(host, 443);
            if (quic.isReady()) return quic;
        } catch (Exception e) {
            // QUIC可能被企业防火墙/运营商UDP QoS封掉
            metrics.record("quic_fallback");
        }
        
        // 第二步：降级HTTP/2
        try {
            Http2Connection h2 = http2Client.connect(host, 443);
            if (h2.isReady()) return h2;
        } catch (Exception e) {
            metrics.record("h2_fallback");
        }
        
        // 第三步：兜底HTTP/1.1 + Keep-Alive
        return http11Client.connect(host, 443);
    }
    
    // === 心跳保活策略 ===
    
    /**
     * 智能心跳：不是固定间隔，而是根据NAT超时动态调整
     * 
     * 不同运营商NAT超时不同:
     *   移动4G: ~5分钟
     *   联通4G: ~3分钟  
     *   WiFi路由器: ~10分钟
     *   某些公网NAT: ~1分钟
     * 
     * 固定心跳间隔要么太频繁（费电费流量），要么太稀疏（连接被NAT干掉）
     */
    private long heartbeatIntervalMs;
    
    public void startAdaptiveHeartbeat() {
        // 初始心跳间隔: 4分钟（保守起步）
        heartbeatIntervalMs = 4 * 60 * 1000;
        
        // 探测算法：二分法找NAT超时边界
        // 成功了就拉长间隔，失败了就缩短
        scheduleHeartbeat(() -> {
            boolean success = sendPing();
            if (success) {
                // 连接还活着，下次试更长间隔
                heartbeatIntervalMs = Math.min(
                    heartbeatIntervalMs + 30_000, // +30秒
                    MAX_HEARTBEAT_INTERVAL          // 上限10分钟
                );
            } else {
                // 连接已死，重连，缩短间隔
                reconnect();
                heartbeatIntervalMs = Math.max(
                    heartbeatIntervalMs - 60_000, // -60秒
                    MIN_HEARTBEAT_INTERVAL          // 下限30秒
                );
            }
        });
    }
    
    // === 断线重连策略 ===
    
    /**
     * 指数退避 + 抖动，避免雷群效应
     * （服务端重启后，百万客户端同时重连会打爆服务端）
     */
    private int reconnectAttempt = 0;
    
    public void reconnect() {
        long baseDelay = 1000; // 1秒起步
        long maxDelay = 60_000; // 最长60秒
        
        long delay = Math.min(baseDelay * (1L << reconnectAttempt), maxDelay);
        // 加随机抖动：delay * [0.5, 1.5]
        long jitteredDelay = (long)(delay * (0.5 + Math.random()));
        
        scheduleReconnect(jitteredDelay);
        reconnectAttempt++;
    }
}
```

3.2 Ad Server → DSP 长连接
```
javapublic class DspConnectionPool {
    
    /**
     * 每个DSP维护独立连接池
     * HTTP/2下每条连接可以多路复用，所以不需要很多条
     */
    private final Map<String, ConnectionPool> dspPools = new ConcurrentHashMap<>();
    
    public void initPool(DspConfig dsp) {
        ConnectionPool pool = ConnectionPool.builder()
            .host(dsp.getHost())
            .port(dsp.getPort())
            .protocol(Protocol.H2)        // HTTP/2
            .minConnections(2)             // 最少保持2条（冗余）
            .maxConnections(10)            // 最多10条
            .maxConcurrentStreams(100)      // 每条连接最多100个并行Stream
            .connectTimeout(50)            // 建连超时50ms
            .idleTimeout(300_000)          // 空闲5分钟关闭
            .build();
        
        // 预热：服务启动时就建好连接，不等第一个请求来
        pool.warmUp(dsp.getMinConnections());
        
        dspPools.put(dsp.getId(), pool);
    }
    
    /**
     * 连接健康检查：后台定期检测
     */
    @Scheduled(fixedRate = 10_000) // 每10秒
    public void healthCheck() {
        dspPools.forEach((dspId, pool) -> {
            pool.getConnections().forEach(conn -> {
                if (!conn.isActive()) {
                    pool.remove(conn);
                    pool.createNew(); // 补充新连接
                    return;
                }
                
                // HTTP/2 PING帧检测连接活性
                long pingStart = System.nanoTime();
                boolean pongReceived = conn.sendPing(Duration.ofMillis(500));
                long pingLatency = (System.nanoTime() - pingStart) / 1_000_000;
                
                if (!pongReceived) {
                    conn.markUnhealthy();
                    pool.remove(conn);
                    pool.createNew();
                } else {
                    conn.updateLatency(pingLatency);
                }
            });
        });
    }
    
    /**
     * 智能选连接：不是随机选，而是选延迟最低、负载最轻的
     */
    public Connection acquireConnection(String dspId) {
        ConnectionPool pool = dspPools.get(dspId);
        
        return pool.getConnections().stream()
            .filter(Connection::isHealthy)
            .min(Comparator.comparingInt(conn -> 
                // 权重 = 当前活跃Stream数 × 2 + 最近平均延迟（归一化）
                conn.getActiveStreams() * 2 + (int)(conn.getAvgLatencyMs() / 10)
            ))
            .orElseGet(() -> pool.createNew());
    }
}
```

23. 混合比价引擎（体现核心技术深度）
这是最值钱的部分，要讲出"混合"的难度。

"难点在于Bidding和瀑布流的决策逻辑本质不同——Bidding是实时竞价、动态价格，瀑布流是预设eCPM的固价排序。我需要把这两种模式统一到一个决策流程里。"
"具体做法是：并发阶段，对所有支持Bidding的ADN同时发起竞价请求；归并阶段，把返回的 bidprice 和瀑布流中各层的固定eCPM放到同一个优先级队列里做统一排序。这里有个关键设计——瀑布流的固价节点本质上是一个'保底价占位'，Bidding返回的实时价格可以插入到瀑布流的任意层级之间，实现动态穿插。"
"这样的好处是：Bidding ADN多的时候，大部分流量通过实时竞价拿到更高价格；Bidding ADN少或者超时的时候，瀑布流兜底保证填充率不掉。"

24. 连接池设计
不要只说"维护连接池"，要讲为什么要按平台隔离，以及你怎么调参。

"首先，连接池必须按ADN平台做物理隔离，不能共用一个全局池。原因很现实——假设平台A突然出现服务端抖动，响应变慢，如果共用连接池，A的慢连接会逐步把池子里的可用连接占满，导致正常的平台B、C也拿不到连接，形成级联阻塞。隔离之后，A出问题只影响A自己的池子，其他平台完全不受影响，这是故障隔离的基本原则。"


"每个平台的连接池参数也不一样，核心依据是该平台的流量配额和响应特征。比如某个平台QPS配额高、响应快（P99在50ms以内），那它的池子可以小一些，因为连接周转率高；另一个平台响应偏慢但出价高，池子就要大一些，避免并发高峰时排队等连接。这些参数不是拍脑袋定的，我们通过监控每个平台的连接等待时间、活跃连接数、连接创建频率来持续调优。"


"另外还有一个容易忽略的细节：空闲连接回收策略。如果空闲时间设太短，高峰来的时候要频繁建连，TCP握手+TLS握手的开销会突增延迟；设太长，又会浪费内存和文件描述符，甚至可能被对端服务器主动断开后我们这边还不知道，用到的时候才发现是死连接。我的做法是结合平台侧的keep-alive策略来设——比如对方服务器的keep-alive timeout是60s，我们就设50s，在对方关闭之前主动回收，避免用到半关闭连接。"

25. 动态ADload

开场定位

"前面两个模块解决的是'怎么拿到最高出价'，这个模块解决的是'给用户看多少广告才是最优的'。本质上是一个收入和用户体验的博弈问题——广告展示越多收入越高，但过度展示会伤害留存。我设计的动态AdLoad系统就是在这两者之间找到动态平衡点，同时配合全链路性能优化把广告加载耗时从600ms降到100ms。"


模块1：动态AdLoad调控
先讲"为什么不能用固定规则"

"最初的方案是静态频控——比如每个用户每天最多看30条广告，每个广告位每小时最多请求5次。问题很明显：一个高活跃用户一天刷3小时，30条广告在第1小时就花完了，后面2小时的变现机会全浪费了；一个低活跃用户一天只打开1次App，给他5条就够了但系统按照30条的预算预留了资源。静态规则无法区分用户价值，等于用一个均值策略应对一个高方差人群。"

再讲你的多维信号决策模型

"我的思路是把频控从'固定规则'升级为'动态预算分配'。每个用户每次广告请求进来，系统会实时计算一个AdLoad Score，决定这次请求加载几条广告、是否触发频控拦截。"


"这个Score的输入信号有几个维度："


"用户活跃度：基于用户最近7天的DAU天数、单日平均使用时长、本次会话已持续时长，判断该用户还剩多少'可变现库存'。高活跃用户库存充足，可以适当克制，均匀分布广告展示，避免集中轰炸；低活跃用户可能随时离开，要抓住当前机会适度增加展示密度。"


"会话深度：用户进入App后的第1分钟和第30分钟，展示广告的策略应该不同。刚进入时用户耐心最高、内容消费意愿强，这时候频繁插广告会拉高跳出率；随着会话加深，用户进入惯性浏览状态，对广告的容忍度反而提高。所以AdLoad随会话深度做非线性递增——前3分钟保守，中间正常，深度会话适度激进。"


"广告位场景权重：开屏广告和信息流原生广告的侵入感完全不同。开屏广告频控要严格——一天超过3次用户就会烦；信息流原生广告融入内容流，频控可以适当宽松。不同广告位有独立的权重系数。"


"历史填充率与eCPM的反馈闭环：如果某个时段某类用户的广告填充率低（意味着ADN没有合适的广告库存），加大请求量只会增加无效请求、浪费耗时，这时候系统应该自动收缩AdLoad。反过来，如果eCPM正处在高位（比如电商大促期间），说明广告主在抢量，这时候适度提高AdLoad能显著增收。"


### todo
**一个快速验证的起步方案**
如果想快速跑通，最精简的路径是：对竞价取 log，用 LightGBM 做回归，loss 用 Huber（对异常值鲁棒），评估指标用 MAE 和 MAPE。先把 baseline 跑出来，再逐步加特征、拆两阶段、尝试分位数回归。
需要我帮你写一个具体的建模代码框架吗？**

路径 分位数回归 + 收益最大化搜索（收益曲线） + 机器学习 GBDT（LightGBM） + 强化学习 强化学习 / Bandit（最前沿）