# Azure Encryption-at-Rest for Object Storage and Block Storage

- Status: Accepted
- Deciders: Arch Meeting
- Date: 2024-02-22

## Context and Problem Statement

Elastisys has introduced Azure as a new Infrastructure Provider and wants to ensure that all data is protected with encryption-at-rest, following our established security practices.

According to the previous [ADR-0041-encryption-at-rest](./0041-encryption-at-rest.md), we decided to rely on the infrastructure Provider for encryption-at-rest to reduce complexity and leverage built-in security features.

With Azure, we need to determine how to best implement encryption-at-rest for both object storage and VM-level disk storage.

- What options does Azure provide to ensure data is encrypted effectively?
- How do we align these options with our security policies and existing operational practices?
- How can we ensure compliance with our established standards while minimizing operational overhead?

## Decision Drivers

- We want alignment with our existing ADR-0041: Encryption-at-Rest
- We want to maintain platform security and stability.
- We want to avoid operational complexity.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.

## Considered Options

1. For Object Storage, Use Service-Side Encryption with Microsoft-Managed Key & For VM-Level, Use Azure Disk Storage Server-Side Encryption (Both enabled by default).

1. For Object Storage, Use Service-Side Encryption with Microsoft-Managed Key plus Double Encryption & For VM-Level, Use Azure Disk Storage Server-Side Encryption with Microsoft-Managed Key.

1. For Object Storage, Use Service-Side Encryption with Customer-Managed Key & For VM-Level, Use Azure Disk Storage Server-Side Encryption with Customer-Managed Key (Requires Azure Managed service called Azure Disk Encryption Set).

## Decision Outcome

**Chosen Option:** Option 1: Use Azure's default service-side encryption with Microsoft-managed keys for object storage and Azure Disk Storage Server-Side Encryption for VM-level disks.

When deciding on the best encryption method for VM-level disk storage in Azure, we considered four main options: Azure Disk Storage Server-Side Encryption, Encryption at Host, Azure Disk Encryption (ADE) and Confidential disk encryption.

Each option offers different levels of control, security, and operational complexity.
For more comparisons, you can refer [here](https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview#comparison).

We selected **Azure Disk Storage Server-Side Encryption** for VM-level disk storage because it provides a balance of strong security, ease of use, compliance, operational efficiency, and cost-effectiveness.

This approach aligns with our strategy to leverage infrastructure Provider capabilities for encryption-at-rest, as outlined in [ADR 0041: Encryption-at-Rest](./0041-encryption-at-rest.md), while avoiding the complexities and potential performance drawbacks associated with other encryption methods.

### Positive Consequences

- Aligns with our decision [ADR 0041: Encryption-at-Rest](./0041-encryption-at-rest.md) to rely on the infrastructure Provider for encryption, reducing the need for custom encryption solutions.
- Maintains simplicity by leveraging Azure's default encryption settings, reducing complexity for Platform Administrators and Application Developers.
- Provides strong encryption-at-rest using [256-bit AES](./../ciso-guide/cryptography.md), meeting the security requirements without additional operational overhead.
- Avoids additional costs associated with managing customer-managed keys or implementing extra encryption layers.
- No significant performance impact, as Azure optimizes encryption and decryption processes.

### Negative Consequences

- Using Microsoft-managed keys might not meet the requirements for some organizations that need full control over their encryption keys.
- Some customers might feel less secure using Microsoft-managed keys instead of managing their own keys.

## Pros and Cons of the Options <!-- optional -->

### Option 1

- Good, because it aligns with our ADR 0041 which follows the established decision to rely on infrastructure Provider encryption, ensuring consistent security practices.
- Good, because it provides encryption-at-rest using 256-bit AES encryption, aligning with Elastisys' [cryptography](./../ciso-guide/cryptography.md) policy.
- Good, because encryption is enabled by default, requiring no additional configuration, reducing setup complexity.
- Bad, because it relies on Microsoft-managed keys, limiting control over key management, which might not be suitable for all organizations.

### Option 2

- Good, because it protects sensitive data with two layers of encryption with two different key, ensuring data remains secure even if one layer is compromised.
- Bad, because double encryption requires additional setup and configuration, increasing the complexity and operational burden on Platform Administrators and Application Developers.
- Bad, because double encryption can introduce performance overhead due to the extra encryption and decryption processes, potentially impacting application performance and resource utilization.

### Option 3

- Good, because customer have full Control Over Encryption Keys.
- Bad, because it increases the operational burden on customer as need to manage the entire lifecycle of encryption keys, including rotation, backup, and recovery.
- Bad, because it doesn't align with our previous [ADR 0041: Encryption-at-Rest](./0041-encryption-at-rest.md).

## Links

- [ADR-0041](./0041-encryption-at-rest.md)
- [Azure-storage-service-side-encryption](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json#client-side-encryption-for-blobs-and-queues)
- [disk-encryption-overview](https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview)
- [cryptography](./../ciso-guide/cryptography.md)
- [Double encryption](https://learn.microsoft.com/en-us/azure/storage/common/storage-service-encryption?toc=%2Fazure%2Fstorage%2Fblobs%2Ftoc.json&bc=%2Fazure%2Fstorage%2Fblobs%2Fbreadcrumb%2Ftoc.json#doubly-encrypt-data-with-infrastructure-encryption)
- [comparison](https://learn.microsoft.com/en-us/azure/virtual-machines/disk-encryption-overview#comparison)
