Keycloak (self-managed)
===========
# (Picture goes here)

This page will help you succeed in connecting your application to an identity and access management solution Keycloak, which meets your security and compliance requirements.

Keycloak is a widely recognized open-source Identity and Access Management (IAM) solution that provides user authentication and authorization services for applications. It offers a comprehensive set of features, including Single Sign-On (SSO), user federation, and social login support, making it a popular choice for securing applications in a variety of industries. In this guide we outline the necessary steps to configure and deploy a Keycloak instance on a Compliant Kubernetes cluster that is using the [managed PostgreSQL.](https://elastisys.io/compliantkubernetes/user-guide/additional-services/postgresql/) This will provide you with a robust and secure IAM solution to manage user access and authorization for your applications running on Compliant Kubernetes.
## Initial preparation
*Note: This guide assumes that you have managed PostgreSQL as an additional service.*
1. [Create a HNC namespace for Keycloak.](https://elastisys.io/compliantkubernetes/user-guide/namespaces/)
2. [Setup an application database and user in postgreSQL](https://elastisys.io/compliantkubernetes/user-guide/additional-services/postgresql)

3. Take note of the following variables from step 2 for the next section.
- The host of the postgres (PGHOST)
- The user you have created(APP_USER)
- The database you have created(APP_DATABASE)
- The application secret you have created




## Configure Keycloak with managed Postgres

We chose Bitnami's Helm chart for [Keycloak](https://github.com/bitnami/charts/tree/main/bitnami/keycloak) due to its open-source nature, ease of deployment, security optimization, and active maintenance. 
Bitnami is a well known provider of pre-configured, open-source application stacks that simplify deployment and management in various environments, such as Kubernetes. They offer a Helm chart for Keycloak, which streamlines deployment while adhering to Kubernetes best practices for security.

1. Add resource requests(and optionally limits) to the helm chart values.
```
resources:
  limits:
    #cpu: 1000m
    memory: 1000Mi
  requests:
    cpu: 10m
    memory: 400Mi
```
The example provided above serves as a starting point for configuring resource requests and limits for your Keycloak deployment. Be sure to tailor these values to your specific requirements, and monitor your deployment to optimize resource allocation for your unique use case.

2. Configure Keycloak values to use an external database based on the variables noted in the previous step.
```
postgresql:
 enabled: false


externalDatabase:
 host: "<PGHOST>"
 port: 5432
 user: <APP_USER>
 database: <APP_DATABASE>
 existingSecret: "<application-secret"
 existingSecretPasswordKey: "PGPASSWORD"
```

3. Configure your values for production and based on how you will be using Keycloak.
\
a. https://www.keycloak.org/server/configuration-production
\
b. Consider if you should expose Keycloak with an ingress.

4. How will you be using Keycloak?
\
a. [With a reverse proxy?](https://www.keycloak.org/server/configuration-production#_reverse_proxy_in_a_distributed_environment)
\
b. [By securing your applications?](https://www.keycloak.org/docs/latest/securing_apps/index.html)

5. When you have deployed Keycloak you can:
\
[Login as admin and configure realms, users, and clients.](https://www.keycloak.org/getting-started/getting-started-kube)
\
The initial admin user is “user” and the initial admin password will be generated in the secret “keycloak”. This can be customized in the values if you want to generate your own admin password or change admin username.


## Demo?