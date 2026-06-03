# k3s 环境安装

使用fodora linux > 

0. 要翻墙，配置下面类似的环境变量

```clash
HTTP_PROXY=http://127.0.0.1:7890
HTTPS_PROXY=http://127.0.0.1:7890
NO_PROXY=registry.k8s.local,harbor.demo.com,proxyhost,localhost,*.vsphere.local,*.vm.demo,*.tanzu.demo,192.168.21.101,127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

```clash
export HTTP_PROXY=http://127.0.0.1:7890
export HTTPS_PROXY=http://127.0.0.1:7890
export NO_PROXY=registry.k8s.local,harbor.demo.com,proxyhost,localhost,*.vsphere.local,*.vm.demo,*.tanzu.demo,192.168.21.101,127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
export HTTP_PROXY=http://192.168.5.6:7890
export HTTPS_PROXY=http://192.168.5.6:7890
```


1. 安装脚本命令 curl -sfL https://get.k3s.io | sh -

注意 ，有的发行版需要移动下配置文件比如 rha2 
配置 ./kube/config -> rke2 配置的默认安装路径是 /etc/rancher/rke2/rke2.yaml 需要移动一下
kubeconfig 文件将写入到 /etc/rancher/k3s/k3s.yaml，由 K3s 安装的 kubectl 将自动使用该文件。

2. 配置k3s http 代理

配置文件地址
/etc/systemd/system/k3s.service.env
/etc/systemd/system/k3s-agent.service.env

K3s 会自动将集群内部 Pod 和 Service IP 范围以及集群 DNS 域添加到 NO_PROXY 条目列表中。你需要确保 Kubernetes 节点本身使用的 IP 地址范围（即节点的公共和私有 IP）包含在 NO_PROXY 列表中，或者可以通过代理访问节点。
```
HTTP_PROXY=http://your-proxy.example.com:8888
HTTPS_PROXY=http://your-proxy.example.com:8888
NO_PROXY=127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```
如果你想在不影响 K3s 和 Kubelet 的情况下为 containerd 配置代理，你可以在变量前加上 CONTAINERD_：
```
CONTAINERD_HTTP_PROXY=http://your-proxy.example.com:8888
CONTAINERD_HTTPS_PROXY=http://your-proxy.example.com:8888
CONTAINERD_NO_PROXY=127.0.0.0/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16
```

host.containers.internal

# 安装 kite k3s 监控面板

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

7. 注意配置一下 kubeconfig 文件
k3s 入到 /etc/rancher/k3s/k3s.yaml中

# helm 安装

> fedora 系统直接 sudo dnf install helm 即可

> 注意一个问题， 就是 .kube/config 这个文件一定要复制过来， helm 是通过这个文件找到配置路径的。 

# 监控系统安装 Prometheus 

kube-prometheus-stack Helm chart 提供了完整的监控解决方案，包括 Prometheus、Alertmanager 和 Grafana。

1. 添加 Prometheus 社区 Helm 仓库

```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

2. 安装 kube-prometheus-stack

```
helm install prometheus prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace
```

# rustfs

添加仓库 helm repo add rustfs https://charts.rustfs.com
更新 helm repo update

```yaml
replicaCount: 1

# ✅ 吸收：固定镜像版本
image:
  rustfs:
    repository: rustfs/rustfs
    tag: "1.0.0-beta.1"       # ← 固定版本
    pullPolicy: IfNotPresent
  initImage:
    repository: busybox
    tag: "stable"
    pullPolicy: IfNotPresent

mode:
  standalone:
    enabled: true
  distributed:
    enabled: false

secret:
  existingSecret: ""
  rustfs:
    access_key: rustfsadmin
    secret_key: "14159265jkl"

config:
  rustfs:
    volumes: ""
    address: ":5052"
    console_enable: "true"
    console_address: ":5053"
    log_level: "info"
    region: "us-east-1"
    obs_log_directory: "/logs"
    obs_environment: "production"
    domains: "s3.rustfs.k3s"
    ec:
      storage_class_standard: ""
    log_rotation:
      size: 100
      time: day
      keep_files: 7
    metrics:
      endpoint: true # 支持指标导出
      endpoint: "/metrics"
    
service:
  type: NodePort
  endpoint:
    port: 5052
  console:
    port: 5053

livenessProbe:
  enabled: true
  httpGet:
    path: /health
    port: 5052
    scheme: HTTP
  initialDelaySeconds: 30
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3

readinessProbe:
  enabled: true
  httpGet:
    path: /health/ready
    port: 5052
    scheme: HTTP
  initialDelaySeconds: 10
  periodSeconds: 5
  timeoutSeconds: 3
  successThreshold: 1
  failureThreshold: 3

ingress:
  enabled: true
  className: "traefik"
  # ✅ 吸收：显式指定 Traefik entrypoint
  annotations:
    traefik.ingress.kubernetes.io/router.entrypoints: web
  hosts:
    - host: s3.rustfs.k3s
      paths:
        - path: /
          pathType: Prefix
  tls:
    enabled: false

mtls:
  enabled: false

# ✅ 吸收：调度约束全部清空，单机更稳
affinity: {}
topologySpreadConstraints: []
nodeSelector: {}
tolerations: []

storageclass:
  name: local-path
  dataStorageSize: 2000Gi
  logStorageSize: 10Gi

pdb:
  create: false

# 先关只读根文件系统，排查完再开
containerSecurityContext:
  capabilities:
    drop:
      - ALL
  readOnlyRootFilesystem: false
  allowPrivilegeEscalation: false
  runAsNonRoot: true

resources:
  requests:
    cpu: 500m
    memory: 1Gi
  limits:
    cpu: "2"
    memory: 4Gi
```

helm 安装命令 
helm install rustfs rustfs/rustfs   --namespace rustfs   --create-namespace   -f rustfs-values.yaml
helm upgrade rustfs rustfs/rustfs   --namespace rustfs   --create-namespace   -f rustfs-values.yaml

卸载命令 

```shell
# 先卸载
helm uninstall rustfs -n rustfs

# 再手动删除 PVC（数据会丢失！）
kubectl delete pvc -n rustfs -l app.kubernetes.io/name=rustfs

# 最后删除 namespace（最彻底）
kubectl delete namespace rustfs
```


podman安装 rustfs

```docker
docker run -d \
  --name rustfs_container \
  -p 19000:9000 \
  -p 19001:9001 \
  -v /opt/rustfs/data:/data\
  -e RUSTFS_ACCESS_KEY=rustfsadmin \
  -e RUSTFS_SECRET_KEY=rustfsadmin \
  -e RUSTFS_CONSOLE_ENABLE=true \
  -e RUSTFS_ADDRESS=:9000 \
  rustfs/rustfs:latest \
  /data
```

```podman
podman run -d   --name rustfs_container   -p 19000:9000   -p 19001:9001   -v /opt/rustfs/data:/data:Z,U   -v /opt/rustfs/logs:/logs:Z,U   -e RUSTFS_ACCESS_KEY=rustfsadmin   -e RUSTFS_SECRET_KEY=rustfsadmin   -e RUSTFS_CONSOLE_ENABLE=true   -e RUSTFS_ADDRESS=0.0.0.0:9000   docker.io/rustfs/rustfs:latest   /data
```
注意podman 挂载容器的时候因为linuxSE的问题，会有权限问题，这里使用ZU 参数解决。具体的内容可以搜索相关的文档 还有一个参数叫做 --userns=keep-id 这个也可以解决



export LAKEKEEPER__PG_DATABASE_URL_READ="postgres://postgres:14159265jkl@127.0.0.1:5432/catalog_database"
export LAKEKEEPER__PG_DATABASE_URL_WRITE="postgres://postgres:14159265jkl@127.0.0.1:5432/catalog_database"
export LAKEKEEPER__PG_ENCRYPTION_KEY="14159265jkl"

EfMXQMWIfKxatUW4favL
DBSadlajFmzspGeQVHjUv51MstX1h6w8mZtl9jib


JOPgw8UyjT662xhz6q4c
HhxHDtoZenBqMFgQngBpcX4NB6zRgo5PsHK7OxAG
k3s 安装 lakekeeper

helm repo add lakekeeper https://lakekeeper.github.io/lakekeeper-charts/
helm install lakekeeper lakekeeper/lakekeeper --namespace lakekeeper   --create-namespace
