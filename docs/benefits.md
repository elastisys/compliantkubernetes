---
description: Learn how to explore the benefits of the Compliant Kubernetes platform, helping you reach compliance targets as well as agile software development.
---

# Exploring the benefits of Compliant Kubernetes

If you are new to the Compliant Kubernetes project, you are encouraged to carry out your own proof-of-concept using Compliant Kubernetes to get a feel for its features and how it can provide tangible benefit to your application and operations.

The following are suggested aspects to investigate, which also help building an understanding for the platform.

## The application

As a Kubernetes-based platform distribution of software, any containerized application will of course do. However, to get the best possible understanding of the Compliant Kubernetes platform's features, we suggest that your application has:

 - a publicly facing front end part, which connects to
 - a back end business logic application, which connects to
 - a database system.

This will let you explore some of the features that the Compliant Kubernetes platform offers and see how these benefit your needs and workflows.

### Beware: PodSecurityPolicies in place

Be mindful of not trying to start Pods that assume they can run using the root account. In regulated environments, doing this should of course not be permitted, as it needlessly increases your attack surface. So all your applications should run with as few permissions as possible. Add capabilities if you must, but don't try to run as root!

## Compliant Kubernetes benefits to explore

### Integration with your identity provider (IdP) of choice

Since Compliant Kubernetes relies on [Dex](https://github.com/dexidp/dex), it integrates with various identity providers, such as LDAP-based ones (Active Directory), SAML, OpenID Connect, GitHub, and more, including Google accounts. See the whole list of support by looking at [the list of connectors](https://github.com/dexidp/dex). Set it up with your provider of choice to get a feel for how easily it will integrate with your workflow!

### Application and audit logs to Elasticsearch

Your application just needs to write to standard output, as is typical in Kubernetes-based platform. Whatever it writes will be collected and stored in your preconfigured Elasticsearch service that Compliant Kubernetes ships with (OpenDistro for Elasticsearch). Access it from your dashboard!

Check out the audit logs as well, to see that all API actions against the Kubernetes API are logged in Elasticsearch. Perhaps try to carry out administrative tasks with a non-privileged user to see that these are prevented and logged. You can of course set up alerting for this type of event.

### Monitoring data to Prometheus, viewed with Grafana

The Pods of your application will automatically be monitored by Prometheus. Check it out from your dashboard and see the data update.

#### Custom incident alerts in Alertmanager

Create a couple of alerts that make sense for your application based on the data reported into Prometheus. Alertmanager [integrates natively with e.g. Slack and PagerDuty](https://prometheus.io/docs/alerting/latest/configuration/) and also supports a [wide range of additional notification channels](https://www.prometheus.io/docs/operating/integrations/#alertmanager-webhook-receiver) via webhooks so you can try setting up something that makes sense for your operations team.

### Image vulnerability scanning for known threats

Upload your container images to the Compliant Kubernetes Harbor image registry. Verify that scanning takes place, and see if your images are secure.

How about intentionally pushing an image based on some old base image to see the list populate fast!

### Intrusion detection system for unknown threats

Make your application do unsafe things to trigger Falco, the intrusion detection system. Try to write something to the `/etc` directory!

### Policies and automatic enforcement

Compliant Kubernetes integrates with the [Open Policy Agent](https://www.openpolicyagent.org/) (OPA), which helps enforce policies automatically. Such policies can prevent e.g. the use of default passwords when connecting to databases, or configuration errors such as deploying a non-vetted Pod to production.

Set up a policy that makes sense for your application and watch as OPA immediately stops violations to these policies to occur. It catches API requests to the Kubernetes API before they can touch resources in the cluster.

### Network isolation/segregation

Set up standard Kubernetes [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) such that all inbound and outbound traffic is restricted to that which is necessary for the application to work, and other traffic is specifically denied:

 - only the front end is publicly exposed;
 - the front end can only initiate connections to the back end;
 - the back end can only be connected to from the front end (no other components running in other namespaces);
 - the back end only gets to initiate connections to the database and to the known external endpoints;
 - nothing besides the back end application gets to connect to the database; and
 - the database may never initiate connections to anything on its own.

Doing this shows that not only do you have network isolation/segregation up and running, but also, you have significantly reduced your attack surface. Should code get exploited in either component, it will still be limited in what damage it can do to the overall system.

### Automatic certificate management

Of course your publicly exposed front end should support (only?) encrypted traffic. Set up the cert-manager to give your exposed service a certificate issued by Let's Encrypt.
