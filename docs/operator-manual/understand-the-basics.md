# Understand the Basics

Welkin is a platform which significantly reduces the cognitive load on the application team.
However, this means that you the platform administrator are taking over some of that complexity.
Before you can operate Welkin, you need to understand the basics.
This section provides some useful links to build up this understanding.

- Linux administration
    - We recommend [Linux Foundation Certified System Administrator (LFCS)](https://training.linuxfoundation.org/certification/linux-foundation-certified-sysadmin-lfcs/)
    - [Ansible](https://docs.ansible.com/)
- Containers
    - We recommend [Containers Fundamentals (LFS253)](https://training.linuxfoundation.org/training/containers-fundamentals/)
- Kubernetes administration
    - We recommend [Certified Kubernetes Administrator (CKA)](https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/)
- Kubernetes networking
    - We recommend [Introduction to Cilium (LFS146)](https://training.linuxfoundation.org/training/introduction-to-cilium-lfs146/)
    - NOTE: In Welkin, we use Calico as a CNI, however, the basic CNI concepts are the same.
    - [Ingress Controllers](https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/)
    - [NGINX Ingress Controller](https://github.com/kubernetes/ingress-nginx?tab=readme-ov-file)
- Helm
    - We recommend [Managing Kubernetes Applications with Helm (LFS244)](https://training.linuxfoundation.org/training/managing-kubernetes-applications-with-helm-lfs244/)
- Metrics observability
    - [Prometheus](https://prometheus.io/docs/introduction/overview/)
    - [Thanos](https://thanos.io/tip/thanos/design.md/)
- Logs observability
    - [Fluentd](https://www.fluentd.org/)
        - [S3 plugin for Fluentd](https://docs.fluentd.org/output/s3)
        - [Opensearch plugin for Fluentd](https://github.com/fluent/fluent-plugin-opensearch)
    - [OpenSearch](https://opensearch.org/docs/latest/)
- Container registries and container vulnerability scanning
    - [Harbor](https://goharbor.io/)
    - [Trivy](https://trivy.dev/v0.57/)
- Kubernetes security hardening
    - We recommend [Certified Kubernetes Security Specialist (CKS)](https://training.linuxfoundation.org/certification/certified-kubernetes-security-specialist/)
    - [Pod Security Standards](https://kubernetes.io/docs/concepts/security/pod-security-standards/)
    - [Falco](https://falco.org/)
    - [Kured](https://kured.dev/)
    - [OpenPolicyAgent and Gatekeeper](https://open-policy-agent.github.io/gatekeeper/website/docs/)
    - [OpenID](https://en.wikipedia.org/wiki/OpenID)
    - [Dex](https://dexidp.io/)
- Kubernetes backups
    - [Velero](https://velero.io/)
    - [Rclone](https://rclone.org/)
- [Argo CD](https://argo-cd.readthedocs.io/en/stable/getting_started/)

Platform administration, in particular on-call, can be stressful.
Therefore, familiarize yourself with:

- [OODA loop](https://en.wikipedia.org/wiki/OODA_loop), in particular, make sure you **always orient yourself** before deciding what to do, especially at 2am.
- [The Site Reliability and Software Engineering Soft Skills That Matter Most](https://blogs.cisco.com/security/the-site-reliability-and-software-engineering-soft-skills-that-matter-most)
