---
description: How to configure your Identity Provider (IdP) for Single Sign-on (SSO) use in Compliant Kubernetes
tags:
  - HSLF-FS 2016:40 4 kap. 2 § Styrning av behörigheter
  - MSBFS 2020:7 4 kap. 5 §
  - NIST SP 800-171 3.1.1
  - NIST SP 800-171 3.3.2
---

# Prepare your Identity Provider (IdP)

!!! elastisys "For Elastisys Managed Services Customers"

    Please follow these steps to configure your IdP so that we can connect a new Compliant Kubernetes environment to it.

    To share credentials with Elastisys, please use our [YoPass service](https://yopass.elastisys.com).

    If you get stuck, get in touch with your contact person at Elastisys.

To help you comply with various data protection regulations, Compliant Kubernetes only allows access to service endpoints (i.e., Kubernetes API, Harbor, Grafana and OpenSearch) via an IdP.
Your organization's IdP acts as the single point to decide who gets access to what.

This page describes how to configure Google Identity and Azure Active Directory so that Platform Administrators can connect a Compliant Kubernetes environment to them.
Note, however, that Compliant Kubernetes supports any OpenID-compatible IdP, including GitHub and GitLab.

This page show what information you need to send to Platform Administrators and where to find it.

## Azure Active Directory (AD)

!!! note

    As of August 2023, Azure Active Directory is Becoming Microsoft Entra ID.

1. Sign in to the [Azure portal](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app).
1. Search for and select **Azure Active Directory**.
1. Under Manage, select App registrations > New registration.
1. Under Supported account types pick **Accounts in any organizational directory (Any Azure AD directory – Multitenant)**.
1. Under **Redirect URI** select **web** and insert the Dex URL that Platform Administrators provided. This is generally `https://dex.$DOMAIN/callback`.
    If unsure, ask your Platform Administrators.
1. Go to **Overview** and note down the **application ID**.
1. Create a secret by going to **Certificates & secrets**.
1. Select the tab **Client secret** and click **New client secret**.
1. Set **expiry date** to **24 months**.
1. For improved security, navigate to **Properties** and note down **the tenant ID**. This limits who can authenticate to your Compliant Kubernetes environment.
1. Decide the **name of the Azure AD group** that should have admin privileges in the environment.
1. Securely send, e.g., via [YoPass](https://yopass.elastisys.com), the following information to your Platform Administrators:
    <!-- markdownlint-enable ol-prefix -->
    <!-- markdownlint-enable list-marker-space -->

    - tenant ID;
    - application ID;
    - client secret;
    - admin group.

### Further Reading

- [Quickstart: Register an application with the Microsoft identity platform](https://learn.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app)
- [Dex: Authentication through Microsoft](https://dexidp.io/docs/connectors/microsoft/)

## Google

!!! important

    Some steps can only be done by an administrator account for a managed Google service,such as Google Workspace or Cloud Identity. (See [this Google support page](https://support.google.com/a/answer/6375836?hl=en-GB).)

1. Go to [Google Cloud -- Credentials](https://console.cloud.google.com/apis/credentials).
1. Create a new project through the top menu.
1. In the new project, go to **OAuth consent screen** on the left side menu and create an internal consent screen.
1. Go to **Enabled APIs & services** on the left side menu and then click **+ ENABLE APIS AND SERVICES**.
1. Search for **Admin SDK API** and enable the API.
1. Go back to **Credentials** on the left side menu.
1. Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
1. Select **Web Application** for **Application type**, give it a suitable name.
1. Set the **Authorized redirect URIs** to the Dex URL provided by your Administrators.
    This is generally `https://dex.$DOMAIN/callback`.
    If unsure, ask your Platform Administrators.
1. Finally, securely send, e.g., via [YoPass](https://yopass.elastisys.com), the following information to your Platform Administrators:

    - client ID;
    - client secret.

To set up groups follow these steps, note that steps 16-18 below can only be done by an administrator.

<!-- The sane_lists Markdown extension will make sure the list starts from 11. -->
<!-- markdownlint-disable ol-prefix -->
<!-- markdownlint-disable list-marker-space -->

11. Go to [Google Cloud -- Service accounts](https://console.cloud.google.com/iam-admin/serviceaccounts?orgonly=true).
12. Make sure that you are in the same project that you created previously (see top menu).
13. Click on **+ CREATE SERVICE ACCOUNT** and give it a suitable name.
14. Note down the **Unique ID** of the service account as you will need it soon.
15. Go to the newly created service account and then under the **KEYS** tab click **ADD KEY** and create a new key of type **JSON**. Save the JSON file for the end.
16. You need to give the service account read access to groups. Go to the [Google admin console](https://admin.google.com).
17. Navigate through the menu to **Security > Access and data control > API Controls** and click **Manage Domain Wide Delegation** and then **Add New**.
18. In the **Client ID** field put the **Unique ID** of the service account from step 4. and in the **Oauth Scopes** field enter this scope: `https://www.googleapis.com/auth/admin.directory.group.readonly`.
19. Decide on the name of the Google group that should have admin privileges in the Compliant Kubernetes environment.
20. Finally, securely send, e.g., via [YoPass](https://yopass.elastisys.com), the following information to your Platform Administrators:
    <!-- markdownlint-enable ol-prefix -->
    <!-- markdownlint-enable list-marker-space -->

    - the JSON file you downloaded;
    - admin group you decided on.

### Further Reading

- [Dex: Authentication Through Google](https://dexidp.io/docs/connectors/google/)
- [Google Identity: OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect)

## OpenID Providers

Compliant Kubernetes should be compatible with any OpenID provider, although full compatibility cannot be guaranteed.

The general instructions are as follows:

1. Check that your IdP is OpenID compatible. You can check this by pointing your browser to: `https://$YOUR_IDP_DOMAIN/.well-known/openid-configuration`. If you get a well-formed JSON page, then your provider is OpenID compatible.
1. Register an application with your OpenID provider. The callback or redirect URL is provided by your Administrators.
    This is generally `https://dex.$DOMAIN/callback`.
1. Allow at least the following scopes: `openid`, `email`, `groups`, `profile`.
1. Securely send, e.g., via [YoPass](https://yopass.elastisys.com), the following information to your Platform Administrators:

- the IdP domain, i.e., `$YOUR_IDP_DOMAIN` which you used in step 1;
- client ID;
- client secret.

### Further Reading

- [Dex: Authentication Through and OpenID Connect Provider](https://dexidp.io/docs/connectors/oidc/)
- [GitLab as OpenID Connect identity provider](https://docs.gitlab.com/ee/integration/openid_connect_provider.html)
- [JumpCloud: SSO with OIDC](https://jumpcloud.com/support/sso-with-oidc)
