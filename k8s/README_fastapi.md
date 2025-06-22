This tutorial shows how to set up Fast API and Jaeger tracing
## How-to Guide Fast API

### Start minikube
```shell
minikube start
kubectl create namespace deployed-api
```
Output:
```shell
namespace/deployed-api created
```

### Add the Helm chart
```shell
helm create stroke-api-chart
cd stroke-api-chart
```
Remove unnecessary files:
```shell
rm templates/hpa.yaml templates/tests/* templates/ingress.yaml templates/serviceaccount.yaml
```

### Install API helm chart
```shell
helm install stroke-api-k8s . -n deployed-api
```
Expected output:
```shell
NAME: stroke-api-k8s
LAST DEPLOYED: Mon Jun 16 23:27:51 2025
NAMESPACE: deployed-api
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

## How-to Guide Jaeger

### Add Jaeger helm repo
```shell
helm repo add jaegertracing https://jaegertracing.github.io/helm-charts
helm repo update
mkdir -p jaeger_chart
cd jaeger_chart
helm pull jaegertracing/jaeger --untar
```

### Install Jaeger using Helm
```shell
helm install jaeger-k8s ./jaeger \
  --namespace monitoring \
  -f ./jaeger/jaeger-values.yaml
```
Expected output:
```shell
NAME: jaeger-k8s
LAST DEPLOYED: Mon Jun 16 23:41:20 2025
NAMESPACE: monitoring
STATUS: deployed
REVISION: 1
TEST SUITE: None
```