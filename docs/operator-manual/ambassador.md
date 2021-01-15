# Ambassador
Ambassador is an alternative of using nginx as an ingress controller. Ambassador can
be used as an regular ingress controller but also supports more features. It comes with
Its own custom resources which can be used to control traffic to the cluster with
greater precision. For more documentation on ambassador see https://www.getambassador.io/docs/latest/.

## Ambassador in compliantkubernetes

Ambassador can be enabled in compliantkubernetes by setting the config options
```yaml
ambassador:
  enabled: true
nginxIngress:
  enabled: false
```
in the `wc-config.yaml` config file (in the [compliantkubernetes-apps](https://github.com/elastisys/compliantkubernetes-apps)
repository).  It is as of now only available in the workload cluster, but can be extended to the service cluster as well.

Unfortunately ambassador receives traffic on port 8080 and 8443 by default. While the kubernetes clusters receives
traffic on port 80 and 443. To fix this a manual manifest must be applied after the installation is completed.

```yaml
apiVersion: getambassador.io/v2
kind:  Module
metadata:
  name:  ambassador
  namespace: ambassador
spec:
  config:
    service_port: 443
```
This config can not be set in the helm chart and thus needs to be added manually.

## Using ambassador

When ambassador is deployed traffic can be routed either by using an ingress
```yaml
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: test-ingress
  annotations:
    kubernetes.io/ingress.class: ambassador
spec:
  rules:
  - host: test.example.com
    http:
      paths:
      - backend:
          serviceName: test-service
          servicePort: 80
        path: /
```
Or by using the mapping resource.
```yaml
kind: Mapping
apiVersion: getambassador.io/v2
metadata:
  name: test-mapping
spec:
  prefix: /
  service: test-service.namespace
  host: test.example.com
```

## Behind the scenes
When applying compliantkubernetes-apps with ambassador enabled it will install it
with datawires [helm chart](https://github.com/datawire/ambassador-chart/tree/master).

This will install ambassador pods as a daemonset running on each worker node in the cluster.
The daemonset will use the hosts port to direct any incoming traffic on the selected ports (443).
The ambassador will act both as an ingress controller and routing traffic through the custom resources.

All http requests will automatically be re-routed to https requests. If there is no certificates set up
it will automatically fall back to a self signed certificate.

### The ambassador console
If no valid path is added in the request it will fall back to a general ambassador starting page.
From this page you will be routed to the admin console (/edge_stack/admin) and asked to login
with `edgectl` (if you have access to the kubernetes cluster). This console can be used to view
any rules, mappings or config set up with the ambassador resources. OBS, this page will not show
any mappings done through the ingress resource.

### Load balancer
If there is an external Load Balancer pointing on the worker nodes they will have to be configured with
the correct health check. Ambassador does not give a 200 response on the default path `/`. The path ambassador
uses is `/ambassador/v0/check_alive` on port `8877`
