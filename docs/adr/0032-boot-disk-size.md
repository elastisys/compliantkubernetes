# Boot disk size on nodes

- Status: accepted
- Deciders: Cristian Klein, Olle Larsson, Lucian Vlad, Fredrik Liv, Robin Wallace, Pavan Gunda
- Date: 2023-02-14

## Context and Problem Statement

We have often defaulted to using boot disks of 50GB where possible but as of late we have noticed that for some environments this is not sufficient. We also noticed that the available space is commonly filled up by Application Developer container images.
We would like to have same boot disk sizes for all our nodes on all the Infrastructure Providers if possible.
Should we increase the boot disk size to a bigger size?

## Decision Drivers

- We want to best serve the Application Developer needs.
- We want to find a solution which is scalable and minimizes administrator burden.
- We don't want to waste infrastructure.

## Considered Options

- Keep boot disk size to 50Gb but increase the alert threshold and do regular cleanup
- Keep boot disk size to 50Gb and increase boot disk size only where is needed
- Increase the boot disk size to 100GB for all nodes irrespective of node size
- Increase the boot disk size to 100GB only for nodes that are bigger than 4C8GB
- Use local disk of 100GB size for controlplane nodes

## Decision Outcome

Chosen option: Increase the boot disk size to 100GB for all nodes irrespective of node size & Use local disk of 100GB size for controlplane nodes

### Positive Consequences

- There will be more available space for pulling images
- Reduce the number of alerts and ops time
- Improve platform stability and scalability

### Negative Consequences

- We need to replace all existing nodes for our existing environments
- Cost will increase depending on number of nodes and price per GB of storage

## Recommendation to Platform Administrators

- Try to use same VM flavors on all environments
- Use VM flavor with local disk of 100GB or whichever is closest to this size depending on Infrastructure Provider for controlplane nodes.
- For worker nodes use 100GB boot disk size on Infrastructure Providers that allow it and on the ones that we can't use the VM flavor with the closest disk size.

## Links

- [Some recomandations](https://serverfault.com/questions/977871/recommended-disk-size-for-gke-nodes)
