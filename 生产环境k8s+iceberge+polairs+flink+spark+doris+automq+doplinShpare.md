# rke2 安装

官网： https://www.rancher.cn/products/rke2/ 


HTTP_PROXY=http://192.168.5.43:7890
HTTPS_PROXY=http://192.168.5.43:7890
NO_PROXY=registry.k8s.local,harbor.demo.com,proxyhost,localhost,*.vsphere.local,*.vm.demo,*.tanzu.demo,192.168.21.101,127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16

CONTAINERD_HTTP_PROXY=http://192.168.5.43:7890
CONTAINERD_HTTPS_PROXY=http://192.168.5.43:7890
CONTAINERD_NO_PROXY=registry.k8s.local,harbor.demo.com,proxyhost,localhost,*.vsphere.local,*.vm.demo,*.tanzu.demo,192.168.21.101,127.0.0.1/8,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16


helm install rancher rancher-latest/rancher \
  --namespace cattle-system \
  --set hostname=192.168.5.98.sslip.io \
  --set replicas=1 \
  --set bootstrapPassword=Hjvc4e4a...


./kubectl -n cattle-system rollout status deploy/rancher
