---
description: Learn how to explore the benefits of the Compliant Kubernetes platform, helping you reach compliance targets as well as agile software development.
---

# Getting Started with Compliant Kubernetes

This documentation includes a user demo application which allows you to quickly explore the benfits of Compliant Kubernetes. The provided artifacts, including Dockerfile and Helm Chart, allow you to quickly get started on your journey to become an agile organization with zero compromise on compliance with data protection regulations.

## Install Prerequisites

{%
    include "user-guide/setup.md"
    start="<!--user-demo-setup-start-->"
    end="<!--user-demo-setup-end-->"
%}

## Prepare Your Application

{%
    include "user-guide/prepare.md"
    start="<!--user-demo-overview-start-->"
    end="<!--user-demo-overview-end-->"
%}

## Push Your Application Container Images

{%
    include "user-guide/registry.md"
    start="<!--user-demo-registry-start-->"
    end="<!--user-demo-registry-end-->"
%}

## Deploy your Application

{%
    include "user-guide/kubernetes-api.md"
    start="<!--user-demo-kubernetes-api-start-->"
    end="<!--user-demo-kubernetes-api-end-->"
%}

## Search on Application Logs

{%
    include "user-guide/logs.md"
    start="<!--user-demo-logs-start-->"
    end="<!--user-demo-logs-end-->"
%}

## Monitor your Application

{%
    include "user-guide/metrics.md"
    start="<!--user-demo-metrics-start-->"
    end="<!--user-demo-metrics-end-->"
%}

## Alert on Application Metrics

{%
    include "user-guide/alerts.md"
    start="<!--user-demo-alerts-start-->"
    end="<!--user-demo-alerts-end-->"
%}

## Back up Application Data

{%
    include "user-guide/backup.md"
    start="<!--user-demo-backup-start-->"
    end="<!--user-demo-backup-end-->"
%}
