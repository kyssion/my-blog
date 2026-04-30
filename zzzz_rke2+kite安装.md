#  rke2 安装

环境linux -> fedora43

1. 官网 : https://docs.rke2.io/ 
2. 注意配置代理 , 上面这个脚本可能会有网络问题

```shell
export HTTP_PROXY=http://192.168.5.43:7890
export HTTPS_PROXY=http://192.168.5.43:7890
```

3. 安装的时候会生成一个systemd服务 ->  /usr/lib/systemd/system/rke2-server.service
4. 配置服务的代理： vim /usr/lib/systemd/system/rke2-server.env ，并添加下面的代理配置

```shell
HTTP_PROXY=http://192.168.5.43:7890
HTTPS_PROXY=http://192.168.5.43:7890
NO_PROXY=registry.k8s.local,harbor.demo.com,proxyhost,localhost,*.vsphere.local,*.vm.demo,*.tanzu.demo,192.168.21.101,127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

5. 等待服务启动就安装成功

6. 配置 ./kube/config -> rke2 配置的默认安装路径是 /etc/rancher/rke2/rke2.yaml 需要移动一下

```shell
sudo cp /etc/rancher/rke2/rke2.yaml ~/.kube/config
```

# kite 安装

kite 是 k8s 操作系统的控制面板，可以方便的管理yaml等配置

kite github 官网： https://github.com/kite-org/kite/tree/main

1. 源码编译安装 
git clone https://github.com/kite-org/kite.git

2. 配置golang proxy  -> go env -w GOPROXY=https://goproxy.cn,direct

3. 配置npm国内仓库registry -> npm config set registry https://registry.npmmirror.com/

4. clone下来之后 安装pnpm , 因为这个项目构架脚本使用的pnpm

```shell
npm install -g pnpm
```

5. 然后使用脚本构建 

```shell
make deps
make build
```

6. 然后运行 ./kite 就能运行

# 可监控性 grafana + prometheus-stack

使用helm 安装 配置文件如下

```yaml
# ==========================================
# 单节点 K8s 全功能监控栈（终极无遗漏版）
# ==========================================

# --- 全局存储类 ---
# 如果你有 local-path / nfs / openebs，取消注释：
global:
  storageClass: "local-path"

# ==========================================
# 1. Prometheus Operator（核心调度器）
# ==========================================
prometheusOperator:
  enabled: true
  # 单节点减少 webhook patch job 资源占用
  admissionWebhooks:
    enabled: true
    patch:
      enabled: true
      resources:
        requests:
          cpu: 50m
          memory: 64Mi
        limits:
          cpu: 100m
          memory: 128Mi
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

# ==========================================
# 2. Prometheus Server（核心时序库 + 对外主接口）
# ==========================================
prometheus:
  enabled: true
  service:
    type: NodePort
    nodePort: 30090
  
  prometheusSpec:
    replicas: 1
    retention: 15d
    retentionSize: "20GB"
    enableAdminAPI: true
    # 单节点：取消反亲和性，允许全部调度到同一节点
    podAntiAffinity: ""
    
    # 关键：允许抓取所有命名空间的 ServiceMonitor / PodMonitor / Rule
    # 这样外部看板才能看到整个集群的完整指标
    serviceMonitorSelectorNilUsesHelmValues: false
    podMonitorSelectorNilUsesHelmValues: false
    ruleSelectorNilUsesHelmValues: false
    
    serviceMonitorSelector: {}
    podMonitorSelector: {}
    ruleSelector: {}
    
    serviceMonitorNamespaceSelector: {}
    podMonitorNamespaceSelector: {}
    ruleNamespaceSelector: {}
    
    # 持久化
    storageSpec:
      volumeClaimTemplate:
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 30Gi
          storageClassName: local-path
    
    # 资源
    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 2000m
        memory: 4Gi
    
    # Thanos sidecar：单节点对象存储留空，仅保留组件位
    thanos:
      objectStorageConfig: null

# ==========================================
# 3. Alertmanager（告警中心）
# ==========================================
alertmanager:
  enabled: true
  service:
    type: NodePort
    nodePort: 30093
  
  # 基础告警路由（避免 alertmanager 启动报错）
  config:
    global:
      resolve_timeout: 5m
    route:
      group_by: ['alertname', 'namespace']
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 12h
      receiver: 'null'
      routes:
        - receiver: 'null'
          matchers:
            - alertname =~ "Info.*|Watchdog"
    receivers:
      - name: 'null'
  
  alertmanagerSpec:
    replicas: 1
    podAntiAffinity: ""
    storage:
      volumeClaimTemplate:
        spec:
          accessModes: ["ReadWriteOnce"]
          resources:
            requests:
              storage: 5Gi
          storageClassName: local-path
    resources:
      requests:
        cpu: 100m
        memory: 256Mi
      limits:
        cpu: 500m
        memory: 512Mi

# ==========================================
# 4. Grafana（可视化 + 外部看板对接）
# ==========================================
grafana:
  enabled: true
  service:
    type: NodePort
    nodePort: 30030
  adminPassword: admin123
  
  persistence:
    enabled: true
    type: pvc
    size: 10Gi
    storageClassName: local-path
  
  resources:
    requests:
      cpu: 100m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi
  
  # 核心：允许外部看板通过 iframe / API 免登录接入
  grafana.ini:
    server:
      root_url: "%(protocol)s://%(domain)s:%(http_port)s/"
    security:
      allow_embedding: true
      cookie_samesite: disabled
    auth.anonymous:
      enabled: true
      org_name: Main Org.
      org_role: Viewer
    # 如需跨域，可补充：
    # security:
    #   cors_origin: "*"

# ==========================================
# 5. kube-state-metrics（K8s 对象指标）
# ==========================================
kubeStateMetrics:
  enabled: true

kube-state-metrics:
  enabled: true
  resources:
    requests:
      cpu: 50m
      memory: 128Mi
    limits:
      cpu: 200m
      memory: 256Mi

# ==========================================
# 6. Node Exporter（宿主机指标，DaemonSet）
# ==========================================
nodeExporter:
  enabled: true

prometheus-node-exporter:
  enabled: true
  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 128Mi

# ==========================================
# 7. Prometheus Adapter（custom.metrics.k8s.io）
# ==========================================
prometheusAdapter:
  enabled: true
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 250m
      memory: 256Mi

# ==========================================
# 8. kubeApiServer（API Server 指标 —— 之前遗漏！）
# ==========================================
kubeApiServer:
  enabled: true
  tlsConfig:
    insecureSkipVerify: false
  serviceMonitor:
    enabled: true
    jobLabel: component
    selector:
      matchLabels:
        component: apiserver
        provider: kubernetes

# ==========================================
# 9. CoreDNS（集群 DNS 指标 —— 之前遗漏！）
# ==========================================
coreDns:
  enabled: true
  service:
    port: 9153
    targetPort: 9153
    selector:
      k8s-app: kube-dns
  serviceMonitor:
    enabled: true

# ==========================================
# 10. K8s 核心组件 ServiceMonitor
# ==========================================
kubelet:
  enabled: true
  serviceMonitor:
    enabled: true

kubeControllerManager:
  enabled: true
  endpoints: []

kubeScheduler:
  enabled: true
  endpoints: []

kubeProxy:
  enabled: true
  endpoints: []

kubeEtcd:
  enabled: true
  endpoints: []
  service:
    enabled: true
    port: 2379
    targetPort: 2379
  serviceMonitor:
    enabled: true
    scheme: https
    insecureSkipVerify: true
    # 单节点 etcd 证书挂载后，可改为 verify 模式：
    # tlsConfig:
    #   caFile: /etc/prometheus/secrets/etcd-certs/ca.crt
    #   certFile: /etc/prometheus/secrets/etcd-certs/client.crt
    #   keyFile: /etc/prometheus/secrets/etcd-certs/client.key

# ==========================================
# 11. 告警规则全量启用
# ==========================================
defaultRules:
  create: true
  rules:
    alertmanager: true
    etcd: true
    configReloaders: true
    general: true
    k8s: true
    kubeApiserverAvailability: true
    kubeApiserverBurnrate: true
    kubeApiserverHistogram: true
    kubeApiserverSlos: true
    kubeControllerManager: true
    kubelet: true
    kubeProxy: true
    kubePrometheusGeneral: true
    kubePrometheusNodeRecording: true
    kubernetesApps: true
    kubernetesResources: true
    kubernetesStorage: true
    kubernetesSystem: true
    kubeSchedulerAlerting: true
    kubeSchedulerRecording: true
    kubeStateMetrics: true
    network: true
    node: true
    nodeExporterAlerting: true
    nodeExporterRecording: true
    prometheus: true
    prometheusOperator: true

# ==========================================
# 12. Thanos Ruler（联邦告警评估，单节点关闭）
# ==========================================
thanosRuler:
  enabled: false

# ==========================================
# 13. Windows 监控（无 Windows 节点，关闭）
# ==========================================
windowsMonitoring:
  enabled: false
```