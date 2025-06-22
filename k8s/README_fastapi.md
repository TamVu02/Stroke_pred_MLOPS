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