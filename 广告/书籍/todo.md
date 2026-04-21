1. 通过 device_id → cookie → phone_hash 等多级映射，将跨端设备归一到同一用户。

2.  Flink 窗口聚合 (滑动/滚动窗口) 
离线特征 (T+1): Hive SQL → Spark ETL → 写入 Tair/Redis。覆盖 90%+ 基础画像，每天凌晨全量/增量更新。

3. 特征存储应该还有版本