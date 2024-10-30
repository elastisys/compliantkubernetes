---
description: Troubleshooting help for Application Developers on Welkin, the security-hardened Kubernetes distribution
search:
  boost: 2
tags:
  - NIS2 Minimum Requirement (b) Incident Handling
---

# Troubleshooting for Application Developers

Going through these basic troubleshooting steps should help you as an Application Developer identify where a problem may lie. If any of these steps do not give the expected "fine" output, use `kubectl describe` to investigate.

If you are using Lens instead of the `kubectl` command-line interface, clicking through your Deployments and Pods will reveal the same information as the commands given below.

## Is the Kubernetes cluster fine?

All Nodes need to have status `Ready`.

```bash
kubectl get nodes
```

## Are my application Pods fine?

Pods should be `Running` or `Completed`, and fully `Ready` (e.g., `1/1` or `6/6`)?

```bash
kubectl get pods
```

Check your Pods for excessive resource usage:

```bash
kubectl top pod
```

Inspect [application logs](logs.md) and [metrics](metrics.md).

## Are my Deployments fine?

Are all Deployments fine? Deployments should show all Pods Ready, Up-to-date and Available (e.g., `2/2 2 2`).

```bash
kubectl get deployments
```

## Are Helm Releases fine?

All Releases should be `deployed`.

```bash
helm list --all
```

## Are my Certificates fine?

All Certificates needs to be Ready.

```bash
kubectl get certificates
```

## Is the API server healthy?

The command below should return `HTTP/2 200`.

```sh
curl --fail --verbose -k https://$loadbalancer_ip_address:6443/healthz
```

## Are Compliantkubernetes apps services healthy?

All commands below should return `HTTP/2 200`.

```sh
curl --fail --verbose https://dex.$DOMAIN/healthz
curl --fail --verbose https://harbor.$DOMAIN/healthz
curl --fail --verbose https://grafana.$DOMAIN/healthz
curl --fail --verbose https://opensearch.$DOMAIN/
curl --fail --verbose -k https://app.$DOMAIN/healthz  # WC Ingress Controller
```
