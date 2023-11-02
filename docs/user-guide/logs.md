---
description: How to work with logs in Elastisys Compliant Kubernetes, the security-focused Kubernetes distribution.
tags:
- ISO 27001 A.12.4.1 Event Logging
- ISO 27001 A.12.4.3 Administrator & Operator Logs
- ISO 27001 A.16 Information Security Incident Management
---

# Logging

Compliant Kubernetes (CK8s) provides the mechanism to manage your cluster as well as  the lifecycle of thousands of containerized applications deployed in  the cluster. The resources managed by CK8s are expected to be highly distributed with dynamic behaviors. An instance of CK8s cluster  environment involves several components with  nodes that host hundreds of containers that are constantly being spun up and destroyed based on workloads.

When dealing with a large pool of containerized applications and workloads in CK8s, it is imperative to be proactive with continuous monitoring and debugging information in order to observe what is going on the cluster. These information can be seen at the container, node, or cluster level.  Logging as one of the [three pillars of observability](https://www.oreilly.com/library/view/distributed-systems-observability/9781492033431/ch04.html#:~:text=Logs%2C%20metrics%2C%20and%20traces%20are,ability%20to%20build%20better%20systems.) is a crucial element to manage and monitor services and infrastructure. It allows you to track debugging information at different levels of granularity.

## Compliance needs

The requirements to comply with ISO 27001 are stated in ISO [27001:2013](https://www.isms.online/iso-27001/). The annexes that mostly concerns logging are:

- [Annex 12](https://www.isms.online/iso-27001/annex-a-12-operations-security/), article A.12.4.1 "Event Logging" and A.12.4.3 "Administrator and Operator Logs".
- [Annex 16](https://www.isms.online/iso-27001/annex-a-16-information-security-incident-management/) which deals with incident management.

In Compliant Kubernetes, OpenSearch is separate from the production workload, hence it complies with A.12.4.2 "Protection of Log Information". The Infrastructure Provider should ensure that the clock of Kubernetes nodes is synchronized, hence complying with A.12.4.4 "Clock Synchronisation".

## OpenSearch

Raw logs in CK8s are normalized, filtered, and processed by [fluentd](https://www.fluentd.org/) and shipped to [OpenSearch](https://opensearch.org/) for storage and analysis. OpenSearch is derived from the fully open source version of Elasticsearch called  [Open Distro for Elasticsearch](https://logz.io/blog/open-distro-for-elasticsearch/).

OpenSearch provides a powerful, easy-to-use event monitoring and alerting system, enabling you to monitor, search, visualize your data among other things. OpenSearch Dashboards is used as visualization and analysis interface for OpenSearch for all your logs.

## OpenSearch Mappings

OpenSearch organizes data into indexes. Each index is a collection of JSON documents. If you have a set of log lines that you want to add to OpenSearch, you must first convert them to JSON. A simple JSON document for a movie might look like this:

```json
{
  "title": "Forrest Gump",
  "release_date": "1994-07-06"
}
```

When you add the document to an index, OpenSearch adds some metadata, such as the unique document ID:

```json
{
  "_index": "<index-name>",
  "_type": "_doc",
  "_id": "<document-id>",
  "_version": 1,
  "_source": {
    "title": "Forrest Gump",
    "release_date": "1994-07-06"
  }
}
```

Indexes also contain mappings and settings:

- A mapping is the collection of fields that documents in the index have. In this case, those fields are title and release_date.
- Settings include data like the index name, creation date, and number of shards.

You can define how documents and their fields are stored and indexed by creating a mapping. The mapping specifies the list of fields for a document. Every field in the document has a field type, which corresponds to the type of data the field contains. For example, you may want to specify that the `release_date` field should be of type `date`. To learn more, see [Supported field types](https://opensearch.org/docs/latest/field-types/supported-field-types/index/).


### Dynamic mapping

When you index a document, OpenSearch adds fields automatically with dynamic mapping. You can also explicitly add fields to an index mapping.

Let's create an index called **movies**, and add a document :

![Create Index](../img/dynamic_mapping_1.png)

We can see the dynamic mapping of all the document fields :

![Get Mapping](../img/dynamic_mapping_2.png)

And OpenSearch was able to infere that **release_date** is of type **date**, and **title** is of type **text**.

You should be aware that OpenSearch type detection is based on some Internal rules, which by no means will infere the correct type for every field. Let's take this example : 

We will recreate the **movies** index, and add a new field called `duration_minutes`, and wrap the value in quotes:

![Add Fields](../img/dynamic_mapping_3.png)

Let's check the new dynamic mapping

![Get Mapping](../img/dynamic_mapping_4.png)

You can see that OpenSearch choose a type of text for duration, which is technically correct, but it won't be of value especially if we were to run custom queries on the *duration_minutes* field, for example: Get all movies longer than a certain duration .. etc

We can instruct OpenSearch to detect numeric values, by configuring the Index at creation time. Let' recreate the index and enable numeric detection:

![Detect Numeric](../img/dynamic_mapping_5.png)

Checking the dynamic mapping again, we can see that Opensearch was able to detect the numeric, and set the value of field to **long**

![Get Mapping](../img/dynamic_mapping_6.png)

  Although OpenSearch was able to detect the numeric type, **long** in our case is not the best data type, as it is an inefficient use of memory space. A better data type here could be **short**. 

| Field data type | Description                                                      |
|-----------------|------------------------------------------------------------------|
| short           | A signed 16-bit integer. Minimum is −2 <sup>15</sup> . Maximum is 2 <sup>15 − 1</sup>. |
| long            | A signed 64-bit integer. Minimum is −2 <sup>63</sup> . Maximum is 2 <sup>63 − 1</sup>  |

To learn more, see [Numeric field types]https://opensearch.org/docs/latest/field-types/supported-field-types/numeric/)


Dynamic mappings are fine when you're getting started with elasticsearch or when you're working with a new dataset. Once you have a more concrete idea of how you want to use the data, you want to be much more deliberate with your mappings, this is where an explicit mapping will be beneficial.

### Explicit mapping

Explicit mappings allow us to be more precise with our field definitions taking the creative control away from elasticsearch. We describe everything upfront providing the structure of our data and the relevant propeties.

Here is an example where we define explicitly the fields type of an index :

![Explicit Mapping](../img/dynamic_mapping_7.png)

An explicit mapping only bypasses the type inference that elasticsearch does for the fields we provide in the explicit mapping. If we index a document with a field not described in the explicit mapping, elasticsearch will still add that new field to the mapping and infer data type to use.

Let's index a new document containing a new field `producer`: 

![Add new field](../img/explicit_mapping_1.png)

The document gets indexed fine, and the mapping now contains the additional field with type text

![Get Mapping](../img/explicit_mapping_2.png)

But now if start adding all sorts of fields we don't know about, we're going to start having problems, and will probably end up with bad quality data, which will make it more difficult to work with.

There are some options on how to deal when documents contains new fields that were not explicitly defined in the mapping. We can tell Elastisearch to either reject the document completly or we can allow the document to be indexed but ignore fields not in the explicit mapping.

Let's configure the index to reject documents that contains fields not defined in the explicit mapping, to do this we set *dynamic* to *strict*: 

![Strict Dynamic](../img/explicit_mapping_3.png)

If we try now to index a document with a field not in the explicit mapping, we'll get an error :

![Error Dynamic](../img/explicit_mapping_4.png)

This is really handy as it will prevent field count explosion, especially in production environments, as the fields will always be increasing as clients can add documents with previously unmapped fields. 
However this might be too strict in some cases, so an alternative is still to allow the document to be indexed but ignore fields not defined in the explicit mapping. To do this we set dynamic to false :

![Ignore Fields](../img/explicit_mapping_5.png)

Now we won't get an error when we index with the same document, and the field is not in the mapping for the index 

![Get Mapping](../img/explicit_mapping_6.png)

One thing worth mentioning is that while the *producer* field was not indexed, and can't be used for queries, it is still there if we get the document, and the *_source*:

![Source](../img/explicit_mapping_7.png)

While this new field is not usable for queries as said before, but if we saw the need, we can create a new index with the *producer* field in the explicit mapping, then re-index the documents in **movies** index to where the new index is.

### Mapping constraints

There is a limit to the number of fields a mapping can have but it's a limit that can be changed. The default value is a 1000 fields per index. This limit is there to prevent cluster performance issues, as resource utilization increases a lot when you have a large number of fields in an index.

![Fields Limit](../img/explicit_mapping_8.png)

Also, note that new fields can be added to an explicit mapping, but field types cannot be changed. The general pattern here is to create a new index with a new mapping and bring documents over in what's called a re-index operation.

## Visualization using OpenSearch Dashboards
OpenSearch Dashboards is used as a data visualization and exploration tool for log time-series  and aggregate analytics. It offers powerful and easy-to-use features such as histograms, line graphs, pie charts, heat maps, and built-in geospatial support.

When you log into OpenSearch Dashboards, you will start at the home page as shown below.

![OpenSearch Dashboards](../img/osd-home.png)

From here click "Visualize & analyze" to continue and you will be greeted with the options to go forward to either **Dashboard** or **Discover**. Opening the sidebar in the top left will also provide navigation to OpenSearch Dashboards features, and here **Visualize** can be found in addition to the two former two outlined in the page shown below.

![OpenSearch Dashboards Sidebar](../img/osd-sidebar.png)

Since we are concerned with searching logs and their visualization, we will focus on these three features indicated by the red rectangle in the figure above. If you are interested to know more about the rest please visit the [official OpenSearch Dashboards documentation](https://opensearch.org/docs/latest/dashboards/index/).

Before we dive in further, let us discuss the type of logs ingested into OpenSearch. Logs in CK8s cluster are filtered and indexed by fluentd into four categories.

**Application level logs**

  -  **Kubeaudit logs** related to [Kubernetes audits](https://kubernetes.io/docs/tasks/debug/debug-cluster/audit/) to provide security-relevant chronological set of records documenting the sequence of activities that have affected system by individual users, administrators or other components of the system. This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

  -  **Kubernetes logs** that provide insight into CK8s resources such as Nodes, Pods, Containers, Deployments and ReplicaSets. This allows you to observe the interactions between those resources and see the effects that one action has on another. Generally, logs in the CK8s ecosystem can be divided into the cluster level (logs outputted by components such as the kubelet, the API server, the scheduler) and the application level (logs generated by pods and containers). This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

**Platform level logs**

  - **Authlog** includes information about system authorization, along with user logins and the authentication mechanism that were used. Such as SSH access to the Nodes. This is mostly related to the ISO 27001 requirement A.12.4.3 "Administrator and Operator Logs".

  -  **Others** logs other than the above two are indexed and shipped to OpenSearch as *others*. These logs are collected from the Node's [`journald`](https://www.freedesktop.org/software/systemd/man/latest/systemd-journald.service.html) logging system.

!!!note
    **Users** can only view the logs of **kubernetes** and **kubeaudit**. **authlog** and **others** are for Compliant Kubernetes administrators.

Let us dive into it then.

### Data Visualization and Exploration

As you can see in the figure above, data visualization and exploration in OpenSearch Dashboards has three components: **Discover**, **Visualize** and **Dashboard**. The following section describes each components using examples.

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
  1. Click **Create visualization** button located on the top right side of the page.
  1. Select a visualization type, we will use **Pie** here.
  1. Choose an index pattern or saved search name under **New Pie / Choose a source**. You can utilize the search function. We will use the **kubernetes\*** index here.

By default a pie chart with the total number of logs will be provided by OpenSearch Dashboards. Let us divide the pie chart based on the number of logs contributed by each **namespace**. To do that perform the following steps:

  1. Under **Buckets** click **Add** then **Split slices**. See the figure below.

      ![Visualize Bucket](../img/add_bucket.png)

  1. Under **Aggregation** select **Significant Terms** terms. See the figure below.

      ![Visualize Aggregation](../img/aggregation.png)

  1. Under **Field** select **kubernetes.namespace_name.keyword** and under **Size** input **10**. See the figure below.

      ![Visualize Fields](../img/namespace.png)

  1. Click **Update** button located in the bottom right corner.

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
2. Click **Create dashboard** button located on the top right side of the page.
3. Click **Add an existing** link located on the left side.
4. Select the name of the two charts/visualizations that you created above.

The figure below shows the dashboard generated from the above steps showing the two pie charts in a single page.

![Dashboard](../img/dashboard.png)


## Accessing Falco and OPA Logs
To access Falco or OPA logs, go to the  **Discover** panel and write **Falco** or **OPA** on the **search textbox**.  Make sure that  the **Kubernetes** log index category is selected.

The figure below shows  the search result for **Falco** logs.
![Falco logs](../img/falco_log.png)

The figure below shows the search result for **OPA** logs.
![OPA logs](../img/opa_log.png)

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
    Re-indexing requires a lot of permissions, including creating and deleting indices, and changing Index templates. This may interfere with audit logs and [compromise platform security](demarcation.md). Therefore, to ensure platform security, re-indexing can only be performed by Compliant Kubernetes administrators.

## Running Example

<!--user-demo-logs-start-->

The user demo application already includes structured logging: For each HTTP request, it logs the URL, the user agent, etc. Compliant Kubernetes further adds the Pod name, Helm Chart name, Helm Release name, etc. to each log entry.

The screenshot below gives an example of log entries produced by the user demo application. It was obtained by using the index pattern `kubernetes*` and the filter `kubernetes.labels.app_kubernetes_io/instance:myapp`.

![Example of User Demo Logs](../img/user-demo-logs.jpeg)

!!!note
    You may want to save frequently used searches as dashboards. Compliant Kubernetes saves and backs these up for you.

<!--user-demo-logs-end-->

## Exporting logs

At the moment the reporting feature in OpenSearch doesn't work so instead we recommend you to use [elasticsearch-dump](https://github.com/elasticsearch-dump/elasticsearch-dump).

Example of exporting the `kubernetes-*` index pattern to a folder `opensearch-dump`:

```bash
docker pull elasticdump/elasticsearch-dump
mkdir opensearch-dump

# OpenSearch username and password
# This will be handed out from your Compliant Kubernetes administrator
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

- ### kubeaudit
    - All api-requests = Successful API requests
    - Forbid error = Forbidden API requests
    - Client Error = Client error logs
    - Server error = Server error logs
- ### kubernetes
    - error OR denied = Error & denied logs
- ### other
    - error OR critical OR alert OR warning = System logs of priority 1-4
- ### authlog
    - number of authlog seassions = Authlog seassions

## Further Reading

* [OpenSearch](https://opensearch.org/)
* [OpenSearch Dashboards](https://opensearch.org/docs/latest/dashboards/index/)
* [Open Distro for Elasticsearch](https://opendistro.github.io/for-elasticsearch/)
* [Kibana](https://opendistro.github.io/for-elasticsearch-docs/docs/kibana/)
* [Open Distro for Elasticsearch – How Different Is It?](https://logz.io/blog/open-distro-for-elasticsearch/)
* [Fluentd](https://www.fluentd.org/)
