---
description: How to work with logs in Welkin, the security-focused Kubernetes distribution.
search:
  boost: 2
tags:
  - ISO 27001 A.12.4.1 Event Logging
  - ISO 27001 A.12.4.3 Administrator & Operator Logs
  - ISO 27001 A.16 Information Security Incident Management
  - NIST SP 800-171 3.1.13
  - NIST SP 800-171 3.12.3
---

# Logging

Welkin provides the mechanism to manage your cluster as well as the lifecycle of thousands of containerized applications deployed in the cluster. The resources managed by Welkin are expected to be highly distributed with dynamic behaviors. A Welkin environment involves several components with nodes that host hundreds of containers that are constantly being spun up and destroyed based on workloads.

When dealing with a large pool of containerized applications and workloads in Welkin, it is imperative to be proactive with continuous monitoring and debugging information in order to observe what is going on in the cluster. This information can be seen at the container, node, or cluster level. Logging as one of the [three pillars of observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html#:~:text=Logs%2C%20metrics%2C%20and%20traces%20are,ability%20to%20build%20better%20systems.) is a crucial element to manage and monitor services and infrastructure. It allows you to track debugging information at different levels of granularity.

## Compliance needs

The requirements to comply with ISO 27001 are stated in ISO [27001:2013](https://www.isms.online/iso-27001/). The annexes that mostly concerns logging are:

- [Annex 12](https://www.isms.online/iso-27001/annex-a-12-operations-security/), article A.12.4.1 "Event Logging" and A.12.4.3 "Administrator and Operator Logs".
- [Annex 16](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/) which deals with incident management.

In Welkin, OpenSearch is separate from the production workload, hence it complies with A.12.4.2 "Protection of Log Information". The Infrastructure Provider should ensure that the clock of Kubernetes nodes is synchronized, hence complying with A.12.4.4 "Clock Synchronisation".

## OpenSearch

Raw logs in Welkin are normalized, filtered, and processed by [Fluentd](https://www.fluentd.org/) and shipped to [OpenSearch](https://opensearch.org/) for storage and analysis. OpenSearch is derived from the fully open source version of Elasticsearch called [Open Distro for Elasticsearch](https://logz.io/blog/open-distro-for-elasticsearch/).

OpenSearch provides a powerful, easy-to-use event monitoring and alerting system, enabling you to monitor, search and visualize your data among other things. OpenSearch Dashboards is used as a visualization and analysis interface for OpenSearch for all your logs.

## Visualization using OpenSearch Dashboards

OpenSearch Dashboards is used as a data visualization and exploration tool for log time-series and aggregate analytics. It offers powerful and easy-to-use features such as histograms, line graphs, pie charts, heat maps, and built-in geospatial support.

When you log into OpenSearch Dashboards, you will start at the home page as shown below.

![OpenSearch Dashboards](../img/osd-home.png)

From here click "Visualize & analyze" to continue and you will be greeted with the options to go forward to either **Dashboard** or **Discover**. Opening the sidebar in the top left will also provide navigation to OpenSearch Dashboards features, and here **Visualize** can be found in addition to the former two, as outlined in the page shown below.

![OpenSearch Dashboards Sidebar](../img/osd-sidebar.png)

Since we are concerned with searching logs and their visualization, we will focus on these three features indicated by the red rectangle in the figure above. If you are interested to know more about the rest please visit the [official OpenSearch Dashboards documentation](https://opensearch.org/docs/latest/dashboards/index/).

Before we dive in further, let us discuss the type of logs ingested into OpenSearch. Logs in Welkin cluster are filtered and indexed by Fluentd into four categories.

**Application level logs**:

- **Kubeaudit logs** related to [Kubernetes audits](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/) to provide a security-relevant chronological set of records documenting the sequence of activities that have affected the system by individual users, administrators or other components of the system. This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

- **Kubernetes logs** that provide insight into Welkin resources such as Nodes, Pods, Containers, Deployments and ReplicaSets. This allows you to observe the interactions between those resources and see the effects that one action has on another. Generally, logs in the Welkin ecosystem can be divided into the cluster level (logs outputted by components such as the kubelet, the API server, the scheduler) and the application level (logs generated by pods and containers). This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

**Platform level logs**:

- **Authlog** includes information about system authorization, along with user logins and the authentication mechanism that were used. Such as SSH access to the Nodes. This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

- **Others** logs other than the above two are indexed and shipped to OpenSearch as _others_. These logs are collected from the Node's [`journald`](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) logging system.

!!!note

    **Users** can only view the logs of **kubernetes** and **kubeaudit**. **authlog** and **others** are for Platform Administrators.

Let us dive into it then.

### Data Visualization and Exploration

As you can see in the figure above, data visualization and exploration in OpenSearch Dashboards has three components: **Discover**, **Visualize** and **Dashboard**. The following section describes each component using examples.

!!!note

    These following examples were created for Open Distro for Elasticsearch and Kibana, however the user experience is the same when using OpenSearch Dashboards.

#### Discover

The **Discover** component in OpenSearch Dashboards is used for exploring, searching and filtering logs.

Navigate to **Discover** as shown previously to access the features provided by it. The figure below shows a partial view of the page that you will get under **Discover**.

![Discover](../img/discover.png)

As you can see in the above figure, the **kubeaudit** index logs are loaded by default. If you want to explore logs from another index, please select the right index under the dropdown menu marked _log index category_.

To appreciate the searching and filtering capability, let us get data for the following question:

- **Get all logs that were collected for the past 20 hours in host 172.16.0.3 where the responseStatus reason is notfound**

We can use different ways to find the answer for the question. Below is one possible solution.

1. Write **sourceIPs: 172.16.0.3** in the **search textbox**.

1. Click **Add Filter** and select **responseStatus.reason** and **is** under **field** and **Operator** dropdown menus respectively. Finally, enter
    **notfound** under **Value** input box and click **Save**. The following figure shows the details.

    ![Discover Filter](../img/discover_filter.png)

1. Click the part that is labelled **Time** in the **Discover** figure from the beginning of this section, then enter **20** under the input box and select **hours** in the dropdown menu. Make sure that you are under the **Relative** tab. Finally, click **update**. The following figure shows how to set the hours. Note that the data will be automatically updated as time passes to reflect the past 20 hours from the current time.

    ![Discover Time](../img/discover_hours.png)

Once you are done, you will see a result similar to the following figure.

![Kibana](../img/discover_filter_hours_result.png)

#### Visualize

The **Visualize** component in OpenSearch Dashboards can be used to create different visualizations. Let us create a couple of visualizations.

To create visualizations:

1. Open the sidebar and click **Visualize** under OpenSearch Dashboards.
1. Click the **Create visualization** button located on the top right side of the page.
1. Select a visualization type, we will use **Pie** here.
1. Choose an index pattern or saved search name under **New Pie / Choose a source**. You can utilize the search function. We will use the `kubernetes*` index here.

By default a pie chart with the total number of logs will be provided by OpenSearch Dashboards. Let us divide the pie chart based on the number of logs contributed by each `namespace`. To do that perform the following steps:

1. Under **Buckets** click **Add** then **Split slices**. See the figure below.

    ![Visualize Bucket](../img/add_bucket.png)

1. Under **Aggregation** select **Significant Terms** terms. See the figure below.

    ![Visualize Aggregation](../img/aggregation.png)

1. Under **Field** select `kubernetes.namespace_name.keyword` and under **Size** input `10`. See the figure below.

    ![Visualize Fields](../img/namespace.png)

1. Click the **Update** button located in the bottom right corner.

The final result will look like the following figure.

![Visualize Namespace Pie](../img/namespace_pie.png)

Please save the pie chart as we will use it later.

Let us create a similar pie chart using `host` instead of `namespace`. The chart will look like the following figure.

![Visualize Host Pie](../img/host_pie.png)

#### Dashboard

The **Dashboard** component in OpenSearch Dashboards is used for organizing related visualizations together.

Let us bring the two visualizations that we created above together in a single dashboard.

To do that:

1. Open the sidebar and click **Dashboard** under OpenSearch Dashboards.
1. Click **Create dashboard** button located on the top right side of the page.
1. Click **Add an existing** link located on the left side.
1. Select the name of the two charts/visualizations that you created above.

The figure below shows the dashboard generated from the above steps showing the two pie charts in a single page.

![Dashboard](../img/dashboard.png)

### Refresh field list for index pattern

When new fields are indexed in OpenSearch they are not immediately available for query in OpenSearch Dashboards. This unavailability can also happen to once queryable older fields, but with the reason being different e.g. some kind of issue occurred.

If you find fields missing from a selected index pattern, you can try to refresh the field list for the particular index pattern by:

1. Open the sidebar and click **Dashboards Management** under Management.
1. Click **Index patterns** in the top left side.
1. Click the index pattern you want to refresh e.g. **kubernetes***.<!-- markdownlint-disable-line MD044 -->
1. Click **Refresh field list.** which is the refresh icon located at the top right side of the page.
1. Finally click **Refresh** and the fields would hopefully be queryable again.

If this didn't help with the missing fields, you can contact your Platform Administrator for additional assistance.

## Accessing Falco and OPA Logs

To access Falco or OPA logs, go to the **Discover** panel and write **Falco** or **OPA** in the **search textbox**. Make sure that the **Kubernetes** log index category is selected.

The figure below shows the search result for **Falco** logs.
![Falco logs](../img/falco_log.png)

The figure below shows the search result for **OPA** logs.
![OPA logs](../img/opa_log.png)

## OpenSearch Mappings

An index mapping specifies the structure of the data within that index, listing all the fields and their data types.

Mappings can be created:

1. Dynamically by OpenSearch
1. Explicitly on index creation
1. Using [Templates](https://opensearch.org/docs/latest/im-plugin/index-templates/)

For example, if you index an integer field without pre-defining the mapping, OpenSearch sets the mapping of that field as long.

Importantly, a field can only be of _one_ type, sending data of another type can result in a _mapping conflict_ and data being rejected.

In Welkin, index mappings are dynamically created from the data you send in.
To set explicit mappings, reach out to your Platform Administrator.
A mapping conflict occurs when you try to send data into a field that already has a mapping created but the data doesn't meet the same type (date, integer, string, etc.)

A very short example of index mapping is displayed and commented below:

```json
{
  "movies": {                         # Index name we're looking at
    "mappings": {
      "properties": {
        "release_date": {             # The release_date field is of
          "type": "date"              # date format allowing for time based
        },                            # searching, eg between 1970 and 2000
        "title": {                    # The title field stores the title,
          "type": "text",             # and is of type text,
          "fields": {                 # and also a keyword
            "keyword": {              # less than 256 bytes in length
              "type": "keyword",      # the default limit is to avoid
              "ignore_above": 256     # excessive disk/memory usage
            }
          }
        }
      }
    }
  }
}
```

To learn more, see [Configuring OpenSearch Mappings](../operator-manual/opensearch-mappings.md).

## Handling Mapping Conflicts

If you get the following error:

```error
Mapping conflict! A field is defined as several types (string,
integer, etc) across the indices that match this pattern. You may still
be able to use these conflict fields in parts of Kibana, but they will
be unavailable for functions that require Kibana to know their type.
Correcting this issue will require re-indexing your data.
```

This means that your application has changed the type of a field in your structured logs. For example, say version A of your application logs the HTTP request path in `request`. Later, version B logs the HTTP request path in `request.path` and the HTTP verb in `request.verb`. Essentially, `request` has changed from string to dictionary.

As a first step, review your application change management policy to reduce the chance of a log field changing type.

Second, ask your administrator to re-index the affected indices.

!!!note

    Re-indexing requires a lot of permissions, including creating and deleting indices, and changing Index templates. This may interfere with audit logs and [compromise platform security](demarcation.md). Therefore, to ensure platform security, re-indexing can only be performed by Platform Administrators.

## Running Example

<!--user-demo-logs-start-->

The user demo application already includes structured logging: For each HTTP request, it logs the URL, the user agent, etc. Welkin further adds the Pod name, Helm Chart name, Helm Release name, etc. to each log entry.

The screenshot below gives an example of log entries produced by the user demo application. It was obtained by using the index pattern `kubernetes*` and the filter `kubernetes.labels.app_kubernetes_io/instance:myapp`.

![Example of User Demo Logs](../img/user-demo-logs.jpeg)

!!!note

    You may want to save frequently used searches as dashboards. Welkin saves and backs these up for you.

<!--user-demo-logs-end-->

## Exporting logs

At the moment the reporting feature in OpenSearch doesn't work so instead we recommend you to use [elasticsearch-dump](https://github.com/elasticsearch-dump/elasticsearch-dump).

!!! elastisys "For Elastisys Managed Services Customers"

    Elasticsearch-dump is not enabled by default, but can be requested by filing a [service ticket](https://elastisys.atlassian.net/servicedesk/).

Example of exporting the `kubernetes-*` index pattern to a folder `opensearch-dump`:

```bash
docker pull elasticdump/elasticsearch-dump
mkdir opensearch-dump

# OpenSearch username and password
# This will be handed out from your Welkin administrator
OPENSEARCH_USERNAME="your-username"
OPENSEARCH_PASSWORD="your-password"

# Your domain that is used for your cluster.
# This is the same as the one you are using for your other services (grafana, harbor, etc.)
DOMAIN="your-domain"

docker run --rm -ti -v $(pwd)/opensearch-dump:/tmp elasticdump/elasticsearch-dump \
  --input="https://${OPENSEARCH_USERNAME}:${OPENSEARCH_PASSWORD}@opensearch.ops.${DOMAIN}/kubernetes-*" \
  --type=data \
  --output=/tmp/opensearch-dump.json \
  --searchBody='{"query":{......}}'
```

For more examples and how to use the tool, read the documentation [in the repo](https://github.com/elasticsearch-dump/elasticsearch-dump#use).

## Log review dashboard

This dashboard can be viewed to get a quick overview of the cluster's state.

![Log review dashboard](../img/log-review-dashboard.png)

- ### Kubeaudit

    - All API-Requests = Successful API requests
    - Forbid Error = Forbidden API requests
    - Client Error = Client error logs
    - Server Error = Server error logs

- ### Kubernetes

    - error OR denied = Error & denied logs

- ### Other

    - error OR critical OR alert OR warning = System logs of priority 1-4

- ### Authlog

    - number of authlog sessions = Authlog sessions

## Further Reading

- [OpenSearch](https://opensearch.org/)
- [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/index/)
- [Fluentd](https://www.fluentd.org/)
