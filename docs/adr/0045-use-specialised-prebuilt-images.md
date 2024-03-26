# Use specialised prebuilt images

- Status: Accepted
- Deciders: Architecture meeting
- Date: 2024-01-18

## Context and Problem Statement

Some of the upstream images we include relies on package or plugins managers to enable support during runtime for different infrastructure providers.

This is a security concern as a malicious actor could modify the packages or plugins to compromise the workload, and a reliability concern as even a good actor could take down packages which would render the workload unavailable.

To improve both the security and reliability of the platform we should therefore take better control over the workloads it includes to provide the images it needs, without external reliance on packages or plugins.

## Decision Drivers <!-- optional -->

- Improve the security of the platform by preventing malicious packages and plugins to be installed during runtime.
- Improve the reliability of the platform by ensuring required packages and plugins are provided in the images.

## Considered Options

1.  Build specialised images one for all required configurations
1.  Build specialised images one for each required configuration
1.  Build no specialised images

## Decision Outcome

Chosen option 2, since it will improve upon the two issues above and provide each configuration with images using minimal software.

The tagging should follow the following scheme:

```text
<registry>/<repository>/<application>:<application-version>-<variant-identifier><variant-version>
```

With variant matching the configuration variant to support, example different object storage services AWS/S3, OpenStack/Swift, etc., and the version of the plugin supporting it.

Example for Velero with AWS/S3 support:

```text
ghcr.io/elastisys/compliantkubernetes-apps/velero:1.12.3-aws1.8.2
```

The application version should not have any version prefix and the variant identifier and variant version should not have any separator.
This is similar to the version scheme used by the Docker Community and how they identify different base image variants.

### Positive Consequences <!-- optional -->

- Increased control over the software supply chain.
- Increased platform security and reliability.
- Starts the process to better manage, update, and verify images used as part of the platform.

### Negative Consequences <!-- optional -->

- Additional maintenance burden to manage images in addition to charts.
- Departs from the upstream charts and images.

## Pros and Cons of the Options <!-- optional -->

### Option 1: _Build specialised images one for all required configurations_

- Good, removes reliance on external packages and plugins during runtime.
- Bad, requires larger images that might contain vulnerabilities that affect all configurations.
- Bad, requires modifications to upstream images and potentially charts to support it.

### Option 2: _Build specialised images one for each required configuration_

- Good, removes reliance on external packages and plugins during runtime.
- Good, allows minimal images that might isolate vulnerabilities to only affect certain configurations.
- Bad, requires modifications to upstream images and potentially charts to support it.

### Option 3: _Build no specialised images_

- Bad, requires external packages and plugins during runtime.
- Good, allows use of upstream images and charts as is.
