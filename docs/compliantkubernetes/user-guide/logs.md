# Logging

Compliant Kubernetes (CK8s) provides the mechanism to manage your cluster as well as  the lifecycle of thousands of containerized applications deployed in  the cluster. The resources managed by CK8s are expected to be highly distributed with dynamic behaviors. An instance of CK8s cluster  environment involves several components with  nodes that host hundreds of containers that are constantly being spun up and destroyed based on workloads.

When dealing with a large pool of containerized applications and workloads in CK8s, it is imperative to be proactive with continuous monitoring and debugging information in order to observe what is going on the cluster. These information can be seen at the container, node, or cluster level.  Logging as one of the [three pillars of observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html#:~:text=Logs%2C%20metrics%2C%20and%20traces%20are,ability%20to%20build%20better%20systems.) is a crucial element to manage and monitor services and infrastructure. It allows you to track debugging information at different levels of granularity.

## Compliance needs

The requirements to comply with ISO 27001 are stated in ISO [27001:2013](https://www.isms.online/iso-27001/). The annexes that mostly concerns logging are:

- [Annex 12](https://www.isms.online/iso-27001/annex-a-12-operations-security/), article A.12.4.1 "Event Logging" and A.12.4.3 "Administrator and Operator Logs".
- [Annex 16](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/) which deals with incident management.

In Compliant Kubernetes, OpenSearch is separate from the production workload, hence it complies with A.12.4.2 "Protection of Log Information". The cloud provider should ensure that the clock of Kubernetes nodes is synchronized, hence complying with A.12.4.4 "Clock Synchronisation".

## OpenSearch

Raw logs in CK8s are normalized, filtered, and processed by [fluentd](https://www.fluentd.org/) and shipped to [OpenSearch](https://opensearch.org/) for storage and analysis. OpenSearch is derived from the fully open source version of Elasticsearch called  [Open Distro for Elasticsearch](https://logz.io/blog/open-distro-for-elasticsearch/).

OpenSearch provides a powerful, easy-to-use event monitoring and alerting system, enabling you to monitor, search, visualize your data among other things. OpenSearch Dashboards is used as visualization and analysis interface for OpenSearch for all your logs.

!!!note
    Compliant Kubernetes v0.18 and earlier used Open Distro for Elasticsearch, providing fully open source versions of Elasticsearch and Kibana. This project has now reached end of life and continues through OpenSearch, replacing Elasticsearch with OpenSearch and Kibana with OpenSearch Dashboards. Although a big change for the project, it still remains highly compatible and with minor differences in features and user experience.

## Visualization using OpenSearch Dashboards
OpenSearch Dashboards is used as a data visualization and exploration tool for log time-series  and aggregate analytics. It offers powerful and easy-to-use features such as histograms, line graphs, pie charts, heat maps, and built-in geospatial support.

When you log into OpenSearch Dashboards, you will start at the home page as shown below.

![OpenSearch Dashboards](../img/osd-home.png)

From here click "Visualize & analyze" to continue and you will be greeted with the options to go forward to either **Dashboard** or **Discover**. Opening the sidebar in the top left will also provide navigation to OpenSearch Dashboards features, and here **Visualize** can be found in addition to the two former two outlined in the page shown below.

![OpenSearch Dashboards Sidebar](../img/osd-sidebar.png)

Since we are concerned with searching logs and their visualization, we will focus on these three features indicated by the red rectangle in the figure above. If you are interested to know more about the rest please visit the [official OpenSearch Dashboards documentation](https://opensearch.org/docs/latest/dashboards/index/).

Before we dive in further, let us discuss the type of logs ingested into OpenSearch. Logs in CK8s cluster are filtered and indexed by fluentd into three categories:

  1. **Kubeaudit logs** related to [Kubernetes audits](https://kubernetes.io/docs/tasks/debug-application-cluster/audit/) to provide security-relevant chronological set of records documenting the sequence of activities that have affected system by individual users, administrators or other components of the system.
This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

  1. **Kubernetes logs** that provide insight into CK8s resources such as nodes, Pods, containers, deployments and replica sets. This allows you to observe the interactions between those resources and see the effects that one action has on another. Generally, logs in the CK8s ecosystem can be divided into the cluster level (logs outputted by components such as the kubelet, the API server, the scheduler) and the application level (logs generated by pods and containers).
This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

  1. **Others** logs other than the above two are indexed and shipped to OpenSearch as *others*. Such logs are basically your application level logs.
This is mostly related to the ISO 27001 requirement A.12.4.1 "Event Logging".

Let us dive into it then.

### Data Visualization and Exploration

As you can see in the figure above, data visualzation and exploration in OpenSearch Dashboards has three components: **Discover**, **Visualize** and **Dashboard**. The following section describes each components using examples.

!!!note
    These following examples were created for Open Distro for Elasticsearch and Kibana, however the user experience is the same when using OpenSearch Dashboards.

#### Discover

The **Discover** component in OpenSearch Dashboards is used for exploring, searching and filtering logs.

Navigate to **Discover** as shown previously to access the features provided by it. The figure below shows partial view of the page that you will get under **Discover**.

  ![Discover](../img/discover.png)

As you can see in the above figure, the **kubeaudit** index logs are loaded by default. If you want to explore logs from either of the other two log indices please select the right index under the dropdown menu marked *log index category*.

To appreciate the searching and filtering capability, let us get data for the following question:

 **Get all logs that were collected for the past 20 hours in host 172.16.0.3 where the responseStatus reason is notfound**

 We can use different ways to find the answer for the question. Below is one possible solution.

  1.  Write **sourceIPs: 172.16.0.3**  in the **search textbox**.

  1. Click **Add Filter** and select **responseStatus.reason** and **is** under **field** and **Operator** dropdown menus respectively. Finally, enter
**notfound** under **Value** input box and click **Save**. The following figure shows the details.

      ![Discover Filter](../img/discover_filter.png)

  1. To enter the 20 hours, click part that is labelled **Time** in the **Discover** figure above, then enter **20** under the input box and select **hours** in the dropdown menu. Make sure that you are under **Relative** tab. Finally, click **update**. The following figure shows how to set the hours. Note that the data will be automatically updated as time passes to reflect the past 20 hours data from the current time.

      ![Discover Time](../img/discover_hours.png)

Once you are done, you will see a result similar to the following figure.

![Kibana](../img/discover_filter_hours_result.png)



#### Visualize

The **Visualize** component in OpenSearch Dashboards is to create different visualizations. Let us create a couple of visualizations.

To create visualizations:

  1. Open the sidebar and click **Visualize** under OpenSearch Dashboards.
  2. Click **Create visualization** link located on the top right side of the page.
  3. Select a visualization type, we will use **Pie** here.
  4. Choose the index name or saved query name, if any,  under **New Pie / Choose a source**. We will use the **Kubernetes** index here.

By default a pie chart with the total number of logs will be provided by OpenSearch Dashboards. Let us divide the pie chart based on the number of logs contributed by each **namespace**. To do that perform the following steps:

  1. Under **Buckets** click **add** then **Split Slices**. See the figure below.

      ![Visualize Bucket](../img/add_bucket.png)

  1. Under **aggregation** select **Significant Terms** terms. see the figure below.

      ![Visualize Aggregation](../img/aggregation.png)

  1. Select **Kubernetes.namespace_name.keyword** under **field**. See the figure below.

      ![Visualize Fields](../img/namespace.png)

The final result will look like the following figure.

![Visualize Namespace Pie](../img/namespace_pie.png)

Please save the pie chart as we will use it later.

Let us create a similar pie chart using **host** instead of **namespace**. The chart will look like the following figure.

![Visualize Host Pie](../img/host_pie.png)

#### Dashboard

The **Dashboard** component in OpenSearch Dashboards is used for organizing related visualizations together.

Let us bring the two visualizations that we created above together in a single dashboard.

To do that:

1. Open the sidebar and click **Dashboard** under OpenSearch Dashboards.
2. Click **Create Dashboard** link located on the top right side of the page.
3. Click **Add existing** link located on the left side.
4. Select the name of the two charts/visualizations that you created above.

The figure below shows the dashboard generated from the above steps showing the two pie charts in a single page.

![Dashboard](../img/dashboard.png)


## Accessing Falco and OPA Logs
To access Falco or OPA logs, go to the  **Discover** panel and write **Falco** or **OPA** on the **search textbox**.  Make sure that  the **Kubernetes** log index category is selected.

The figure below shows  the search result for **Falco** logs.
![Falco logs](../img/falco_log.png)

The figure below shows the search result for **OPA** logs.
![OPA logs](../img/opa_log.png)

## Running Example

<!--user-demo-logs-start-->

The user demo application already includes structured logging: For each HTTP request, it logs the URL, the user agent, etc. Compliant Kubernetes further adds the Pod name, Helm Chart name, Helm Release name, etc. to each log entry.

The screenshot below gives an example of log entries produced by the user demo application. It was obtained by using the index pattern `kubernetes*` and the filter `kubernetes.labels.app_kubernetes_io/instance:myapp`.

![Example of User Demo Logs](/compliantkubernetes/img/user-demo-logs.jpeg)

!!!note
    You may want to save frequently used searches as dashboards. Compliant Kubernetes saves and backs these up for you.

<!--user-demo-logs-end-->

## Further Reading

* [OpenSearch](https://opensearch.org/)
* [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/index/)
* [Open Distro for Elasticsearch](https://opendistro.github.io/for-elasticsearch/)
* [Kibana](https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/)
* [Open Distro for Elasticsearch – How Different Is It?](https://logz.io/blog/open-distro-for-elasticsearch/)
* [Fluentd](https://www.fluentd.org/)
