Troubleshooting
===============

## I have no clue where to start

### Is the Kubernetes clusters doing fine?

All Nodes need to have status `Ready`.

```bash
kubectl get nodes
```

### Are my application Pods fine?

Pods should be `Running` or `Completed`, and fully `Ready` (e.g., `1/1` or `6/6`)?

```bash
kubectl get pods
```

Check your Pods for excessive resource usage:

```bash
kubectl top pod
```

Inspect [application logs](../logs) and [metrics](../metrics).

### Are my Deployments fine?

Are all Deployments fine? Deployments should show all Pods Ready, Up-to-date and Available (e.g., `2/2 2 2`).

```bash
kubectl get deployments
```

### Are Helm Releases fine?

All Releases should be `deployed`.

```bash
helm list --all
```

### Are my Certificates fine?

All Certificates needs to be Ready.

```bash
kubectl get certificates
```
