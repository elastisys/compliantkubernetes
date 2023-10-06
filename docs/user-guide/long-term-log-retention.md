---
tags:
- HIPAA S48 - Audit Controls - § 164.312(b)
- GDPR Art. 17 Right to erasure ("right to be forgotten")
---
# Long-term log retention

Compliant Kubernetes by default sets an retention of 30 days for logs.
Many regulators, including Swedish Healthcare, require a minimum of 5 year log retention.

This is not provided at the platform level by Compliant Kubernetes as it runs the risk of GDPR non-complicance.
Logs may include sensitive information like personal data, which requires that the the retention scheme is designed together with application-specific knowledge to ensure compliance.
Specifically, this includes that the retention scheme ensures that erased personal data can not be accidentally restored, as per [Art. 17 GDPR Right to erasure (‘right to be forgotten’)](https://gdpr.fan/a17).

Using application-specific knowledge would also make it possible to reduce the amount of logs stored, by filtering out so only the required logs are kept.
Minimising the kept data, storage costs and storage management.

##  Exporting logs for long-term storage

To enable long-term log retention we instead recommend using [Elasticdump](https://github.com/elasticsearch-dump/elasticsearch-dump).
This tool can export logs from OpenSearch within Compliant Kubernetes on a per document basis in either CSV or JSON format, allowing other tools to process the logs and ship them somewhere else.
It can also perform transformations, compress using Gzip, and write them into a file or send them to S3 object storage.

Using this tool, along with the REST API of OpenSearch, then it is possible to create scripts to export logs for long-term storage using a Kubernetes CronJob.
Down below are some examples how to discover indices to export from OpenSearch, some commands to use with Elasticdump, and an example Dockerfile and some Kubernetes manifests.

## Accessing OpenSearch

!!!info

	To access OpenSearch contact your Compliant Kubernetes administrator and ask them to create a user with suitable permissions listed here below.

This is the permissions required for the OpenSearch API snippets and the permissions required by Elasticdump:

```yaml
cluster_permissions:
- cluster_monitor
- indices:data/read/scroll
- indices:data/read/scroll/clear
index_permissions:
- index_patterns:
  - '*'
  allowed_actions:
  - indices:admin/aliases/get # Can be omitted when aliases is not used
  - indices:monitor/*
- index_patterns:
  - kubernetes*
  allowed_actions:
  - indices:admin/get
  - indices:admin/mappings/get
  - indices_monitor
  - read
  - search
```

With `${DOMAIN}` set to the domain of your environment, the variables then needed to connect the becomes:

```bash
export OS_PROTOCOL="https"
export OS_ENDPOINT="opensearch.ops.${DOMAIN}"
export OS_USERNAME="<provided-by-admin>"
export OS_PASSWORD="<provided-by-admin>"

# The index pattern we want to export, normally "kubernetes*"
export OS_PATTERN="kubernetes*"
```

!!!important

	These variables will be used later on in the example snippets.

## Discovering aliases and indices

In OpenSearch logs are stored into *indices*.
These indices are managed in a way that will limit them both in time and size, to make them more manageable.
Each index typically represents a days worth of logs, but if the size of the index exceeds a set threshold a new one will be created to limit their maximum size.

The indices are all grouped within index *aliases*, a sort of virtual index that behind the scenes link to other indices.
This allows one to read from all indices and write to one designated write index, all using the same name.

Since only the write index can change one method to select indices for exporting into log-term storage is to only export the read indices.
This way there is no need to check and update indices in case they've changed since the previous export run, simplifying the export logic.

!!!example "Example: List all indices using a pattern"

	```bash
	# call as: get_indices <pattern>
	get_indices() {
		pattern="$1"

		res="$(curl -u "${OS_USERNAME}:${OS_PASSWORD}" -XGET "${OS_PROTOCOL}://${OS_ENDPOINT}/_cat/indices?h=index")"

		if echo "${res}" | grep "error" >&2; then
			exit 1
		elif echo "${res}" | grep "fail" >&2; then
			exit 1
		else
			echo "${res}" | sed -n "/${pattern}/p" | sort
		fi
	}
	```

	This will generate a list of all indices within OpenSearch for the specified pattern.

	The pattern accept regex used by `sed` and should in most instances be `kubernetes*` to only include the application logs indices.

!!!example "Example: List all write indices using a pattern"

	```bash
	# call as: get_write_index <pattern>
	get_write_index() {
		pattern="$1"

		res="$(curl -u "${OS_USERNAME}:${OS_PASSWORD}" -XGET "${OS_PROTOCOL}://${OS_ENDPOINT}/_cat/aliases?h=alias,index,is_write_index")"

		if echo "${res}" | grep "error" >&2; then
			exit 1
		elif echo "${res}" | grep "fail" >&2; then
			exit 1
		else
			echo "${res}" | grep "true" | sed -n "/${pattern}/p" | awk '{print $2}' || true
		fi
	}
	```

	This will generate a list of all write indices within OpenSearch for the specified pattern.

	The pattern accept regex used by `sed` and should in most instances be `kubernetes*` to only include the application logs alias.

	Since the pattern only should only match a single alias, and since each alias can only have a single write index, the output should be validated that it at most only contains one index.

Using these two example functions we can now fetch the indices for a pattern and find the write index for any matching alias, meaning we can iterate over them, filter out the write index, and perform our backup:

!!!example "Example: Iterating over indices, filtering out the write index, and perform export action"

	```bash
	indices=$(get_indices "${OS_PATTERN}")
	write_index=$(get_write_index "${OS_PATTERN}")

	for index in ${indices}; do
		if [ "${index}" = "${write_index}" ]; then
			continue # skipping as it is the write index
		fi

		perform_export "${index}"
	done
	```

For more complex tasks checkout [the OpenSearch REST API reference](https://opensearch.org/docs/latest/opensearch/rest-api/index/).

## Exporting indices

With Elasticdump it is possible to export logs out to the console, to file, or to S3.
In these example snippets we well export them to S3.
To be able to do some management functions we will also use [s3cmd](https://github.com/s3tools/s3cmd), most importantly to be able to check for existing exports.

Using S3 both for Elasticdump and s3cmd will require the following variables:

```bash
export S3_BUCKET="<bucket>"
export S3_REGION="<region>"
export S3_ENDPOINT="<region-endpoint>"
export S3_FORCE_PATH_STYLE="<false|true>" # Generally "false" for AWS and Exoscale, else "true"
export AWS_ACCESS_KEY_ID="<access-key>"
export AWS_SECRET_ACCESS_KEY="<secret-key>"

if [ "$S3_FORCE_PATH_STYLE" = "true" ]; then
	export S3_BUCKET_ENDPOINT="${S3_ENDPOINT}"
else
	export S3_BUCKET_ENDPOINT="%(bucket)s.${S3_ENDPOINT}"
fi
```

!!!important

	These variables will be used later on in the example snippets.

!!!example "Example: Export entire index to S3"

	```bash
	# With ${index} set to the index to export.
	elasticdump \
		--input "${OS_PROTOCOL}://${OS_USERNAME}:${OS_PASSWORD}@${OS_ENDPOINT}/${index}" \
		--output "s3://$S3_BUCKET/${index}.json.gz" \
		--s3Region ${S3_REGION} \
		--s3Endpoint ${S3_ENDPOINT} \
		--s3ForcePathStyle ${S3_FORCE_PATH_STYLE} \
		--s3Compress \
		--concurrency 40 \
		--concurrencyInterval 1000 \
		--intervalCap 20 \
		--limit 1000
	```

	This process will take a while depending on the size of the index.
	By default it will not try to delete, replace or update any resources, so this must be enabled using the [appropriate flags](https://github.com/elasticsearch-dump/elasticsearch-dump#options) or it should be managed by other means like s3cmd.

	!!!caution
		If this process is aborted it will leave multipart uploads after itself that should be cleared, else they will still use storage on the S3 service!

		These can be listed and then removed with s3cmd:
		```bash
		s3cmd \
			--host=${S3_ENDPOINT} \
			--host-bucket=${S3_BUCKET_ENDPOINT} \
			multipart "s3://${S3_BUCKET}"

		s3cmd \
			--host=${S3_ENDPOINT} \
			--host-bucket=${S3_BUCKET_ENDPOINT} \
			abortmp "s3://${S3_BUCKET}/<multipart-upload-path>" "<multipart-upload-id>"
		```

In the example above only certain logs can be exported by adding a query using [OpenSearch Query DSL](https://opensearch.org/docs/latest/opensearch/query-dsl/index/) with the `--searchBody '<query>'` flag.
This way it is possible to filter on certain labels to only export logs for a particular namespace, deployment, or even using identifier within structured logs.
An example for a specific namespace would be:
```json
{
	"query": {
		"term": {
			"kubernetes.namespace_name": "production"
		}
	}
}
```
Since the Query DSL is in JSON format it must be properly quoted or escaped to keep its format, preferably the whitespace should be stripped before sending it as an argument to Elasticdump.

!!!example "Example: Putting it all together"

	```bash
	# call as: perform_export <index>
	perform_export() {
		index="$1"

		check="$(s3cmd "--host=${S3_ENDPOINT}" "--host-bucket=${S3_BUCKET_ENDPOINT}" ls "s3://${S3_BUCKET}/${index}.json.gz"
		if [ -n "${check}" ]; then
			return # skipping as it is already exported
		fi

		# Just as an example
		query='{"query": {"term": {"kubernetes.namespace_name": "production"}}}'

		elasticdump \
			--input "${OS_PROTOCOL}://${OS_USERNAME}:${OS_PASSWORD}@${OS_ENDPOINT}/${index}" \
			--output "s3://$S3_BUCKET/${index}.json.gz" \
			--s3Region ${S3_REGION} \
			--s3Endpoint ${S3_ENDPOINT} \
			--s3ForcePathStyle ${S3_FORCE_PATH_STYLE} \
			--s3Compress \
			--concurrency 40 \
			--concurrencyInterval 1000 \
			--intervalCap 20 \
			--limit 1000 \
			--searchBody "${query}"
	}
	```

## Deploying CronJobs

The simplest way to prepare this for deployment is to build a container image including Bash, Elasticdump and s3cmd, and set up a CronJob to run this on a preferred schedule.

Here are some examples of how to build and deploy them:

!!!example "Example: Containerfile / Dockerfile"

	```Dockerfile
	FROM docker.io/library/ubuntu:jammy

	ARG DEBIAN_FRONTEND=noninteractive
	ARG TZ=Etc/UTC

	RUN apt update && \
		apt install -y --no-install-recommends ca-certificates curl npm s3cmd && \
		apt clean -y && \
		rm -rf /var/lib/apt

	RUN npm install elasticdump@v6.88.0 -g

	CMD ["elasticdump"]
	```

!!!example "Example: Kubernetes resources"

	```yaml
	---
	apiVersion: v1
	kind: ConfigMap
	metadata:
	  name: export-script
	data:
	  script.sh: |-
	    <bash-script>
	---
	apiVersion: v1
	kind: Secret
	metadata:
	  name: export-secret
	type: Opaque
	stringData:
	  # OpenSearch
	  OS_PROTOCOL: "${OS_PROTOCOL}"
	  OS_ENDPOINT: "${OS_ENDPOINT}"
	  OS_USERNAME: "${OS_USERNAME}"
	  OS_PASSWORD: "${OS_PASSWORD}"
	  OS_PATTERN: "${OS_PATTERN}"
	  # S3
	  S3_BUCKET: "${S3_BUCKET}"
	  S3_REGION: "${S3_REGION}"
	  S3_ENDPOINT: "${S3_ENDPOINT}"
	  S3_BUCKET_ENDPOINT: "${S3_BUCKET_ENDPOINT}"
	  S3_FORCE_PATH_STYLE: "${S3_FORCE_PATH_STYLE}"
	  AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
	  AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
	---
	apiVersion: batch/v1
	kind: CronJob
	metadata:
	  name: export
	spec:
	  schedule: <schedule> # example "@daily"
	  concurrencyPolicy: Forbid
	  jobTemplate:
	    spec:
	      template:
	        metadata:
	          labels:
	            app: log-export
	        spec:
	          automountServiceAccountToken: false
	          restartPolicy: Never
	          containers:
	            - name: export
	              image: <image>
	              command:
	                - /scripts/script.sh
	              envFrom:
	                - secretRef:
	                    name: export-secret
	              resources:
	                requests:
	                  cpu: 500m
	                  memory: 500Mi
	                limits:
	                  cpu: 1000m
	                  memory: 750Mi
	              securityContext:
	                runAsNonRoot: true
	                capabilities:
	                  drop:
	                    - ALL
	              volumeMounts:
	                - name: script
	                  mountPath: /scripts
	                  readOnly: true
	          securityContext:
	            runAsNonRoot: true
	            runAsGroup: 65534
	            runAsUser: 65534
	            fsGroup: 65534
	          volumes:
	            - name: script
	              configMap:
	                name: export-script
	                defaultMode: 0777
	```

For more information about CronJobs checkout the Kubernetes [documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/) and [reference](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/cron-job-v1/) about the subject.
