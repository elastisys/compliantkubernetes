# Operator Manual Overview

This manual is for Compliant Kubernetes operators.

Operators can be described via the following user stories:

* As an operator I want to manage the life cycle of *multiple* Compliant Kubernetes clusters.
  * Create cloud infrastructure (on supported clouds).
  * Bootstrap a Compliant Kubernetes cluster on pre-existing infrastructure.
  * Upgrade a Compliant Kubernetes cluster to a new Kubernetes version.
  * Migrate workload and data from one Compliant Kubernetes cluster to another.
  * Decommission a Compliant Kubernetes cluster (including cloud infrastructure if applicable).
  * Handle multiple clusters running different versions in a safe way.
* As an operator I want to re-configure a Compliant Kubernetes cluster.
  * Add or remove nodes.
  * Modify control plane options (e.g. feature gates, authentication settings and log level).
* As an operator I want to perform day 2 operations.
  * Backup and restore a Compliant Kubernetes cluster, including workload and data.
  * Patch any included software with minimal downtime.
  * Rotate credentials.
* As an operator I want to share management of a cluster with other operators in a safe and convenient way.
* As an on-call operator I want to be alerted when abnormal activity is detected, suggesting a pending intrusion.
* As an on-call operator I want to be alerted when the Compliant Kubernetes cluster is unhealthy.
* As an on-call operator I do *not* want to be alerted because of user workload issues or mistakes.
* As an on-call operator I want "break glass" to investigate and recover an unhealthy Compliant Kubernetes cluster.
