---
description: How to work with log-based alerting in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
  - ISO 27001 A.16 Information Security Incident Management
---

# OpenSearch Alert

The alerting feature notifies you when data from one or more OpenSearch indices meets certain conditions. For example, you might want to notify a Slack channel if your application logs more than five HTTP 404 errors in one hour/minute, or you might want to page a developer if no new documents have been indexed in the past 20 minutes.

Alerting features have been enabled by default in Elastisys Compliant Kubernetes as of version 0.19.X

## OpenSearch Alert Demo

To use OpenSearch alerting feature, it involves two steps described below.

1.  **Create Notifications Channel** - A reusable location for the information that you want the monitor to send out after being triggered. Supported locations are Amazon Chime, Email, Slack, or custom webhook.
1.  **Create Monitor** - A job that runs on a defined schedule and queries OpenSearch indices. The results of these queries are then used as input for one or more triggers (Conditions that, if met, generate alerts).

When you log into **OpenSearch Dashboards**, you will start at the home page as shown below.

![OpenSearch Dashboards](../img/osd-home.png)

From here click **Visualize & analyze** to continue and you will be greeted with the options to go forward to either **Dashboard** or **Discover**. Opening the sidebar in the top left will also provide navigation to **OpenSearch Dashboards Plugins**, and here **Alerting** and **Notifications** can be found in the page shown below.

![OpenSearch Alert Sidebar](../img/osd-alerting-sidebar.png)

**Step 1 - Create Notification Channel**:

We start with creating a notification channel, which enables sending messages directly to a designated Slack channel.

- Go to **Notifications** page, then **Channels** tab as shown below.

  ![OpenSearch Notification Channels](../img/osd-notifications-channels-tab.png)

- Click on **Create channel**

- Fill in **Channel details**

  ![OpenSearch Notification](../img/add-notifications-channel.png)

  - **Name** - Name of the destination - for example **user-demo-404-slack-notify**
  - **Channel type** - choose **Slack**
  - **Slack webhook URL** - Create a Slack Webhook following [Slack documentation](https://api.slack.com/messaging/webhooks). Paste the webhook URL

- Test that the Slack integration works by clicking **Send test message** button and check if you receive a test message in your Slack Channel.

  ![OpenSearch Notification Test](../img/notifications-channel-slack-test.png)

- Finally, save the Notification channel by clicking **Create** button.

  ![OpenSearch Monitor Create](../img/create-channel-button.png)

Next, we can proceed with creating a monitor that will use our newly created channel.

**Step 2 - Create Monitors**:

- Go to **Alerting** page, then **Monitors** tab as shown below.

  ![OpenSearch Notification Channels](../img/osd-alerting-monitors-tab.png)

- Click on **Create monitor** button

- Fill in **Monitor details**

  ![OpenSearch Monitor 1](../img/monitor-creation-1.png)

  - **Monitor name** - Name of the monitor, for example **user-demo-404-error**
  - **Monitor type** - Select **Per query monitor** - For more information check OpenSearch documentation on [Monitor types](https://opensearch.org/docs/latest/observing-your-data/alerting/monitors/#monitor-types)
  - **Schedule** - How often to monitor, for example, to check every 1 minute, set:
    - **Frequency** - **By interval**
    - **Run every** - **1 Minutes**
  - **Data source**

    - **Index** where your logs are stored, for instance, **kubernetes\*** (per default, Compliant Kubernetes will store all application logs indices that match the **kubernetes\*** index pattern)

    - **Time field** should be set to **@timestamp**

- Continue with **Query** details

  ![OpenSearch Monitor 2](../img/monitor-creation-2.png)

  - **Metrics** - optional
  - **Time range for the last** - Time frame of data the plugin should monitor - **1 minute(s)**
  - **Data filter** - **status-code is 404**

- Continue with **Triggers** details

  ![OpenSearch Trigger](../img/trigger.png)

  - **Trigger name** - Name of the trigger - **404-error occurred >5 times in last 1 minute**
  - **Severity level** - Select the severity level **1(Highest)**
  - **Trigger condition** - Select the condition according to your applications - **IS ABOVE 5**

- Continue with **Actions** details

  ![OpenSearch Action](../img/action.png)

  - Create an action with name, destination and customized message notification accordingly.
  - Test the action by clicking **Send test message** and check if you receive a test message in your Slack Channel.

    ![OpenSearch Test Trigger](../img/trigger-notification-slack-test.png)

- Finally click **Create** button to complete the creation of the monitor.

  ![OpenSearch Monitor Create](../img/create-monitor-button.png)

- You can see the status of the monitor under **Alerting > Monitors > user-demo-404-error** as shown below.

  ![OpenSearch Monitor View](../img/monitor-view.png)

**Test alert notification to Slack**:

- Demo application deployed and users get 404 errors many times (5 is the condition set before) as shown below.

  ![OpenSearch User Request](../img/404-user-request.png)

- We get the Slack notifications as shown below.

  ![OpenSearch Slack Notify](../img/slack-notify.png)

- Users can view the alert status under the **Alerting** tab as shown below and accordingly take the required action.

  ![OpenSearch Alert List](../img/alert-list.png)

- Users can **acknowledge** the alerts under the **Alerting** tab as shown below.

  ![OpenSearch Acknowledge Alert](../img/acknowledge-alert.png)

## Alert state

- **Active** - The alert is ongoing and unacknowledged. Alerts remain in this state until you acknowledge them, delete the trigger associated with the alert, or delete the monitor entirely.
- **Acknowledged** - Someone has acknowledged the alert, but not fixed the root cause.
- **Completed** - The alert is no longer ongoing. Alerts enter this state after the corresponding trigger evaluates to false.
- **Error** - An error occurred while executing the trigger—usually the result of a bad trigger or destination.
- **Deleted** - Someone deleted the monitor or trigger associated with this alert while the alert was ongoing.

You can find the more information about [OpenSearch alerting](https://opensearch.org/docs/latest/monitoring-plugins/alerting/index/) by following the link.
