# Rclone and Encryption adheres Cryptography Policy

- Status: Accepted
- Deciders: Arch Meeting
- Date: 2023-05-04

## Context and Problem Statement

Compliant Kubernetes can be configured to replicate the primary backup to a secondary backup on a second object storage. Under the hood, this is performed using `rclone`. Such replication improves disaster recovery and mitigates ransomware attacks.

However, this second object storage sometimes needs to be on a different Infrastructure Provider and/or in a different country.
In such cases, it is desirable to make the secondary backup completely opaque to the Infrastructure Provider, so that they do not count as a new data sub-processor.

Is `rclone`'s encryption sufficient for our purposes? Does it comply with the recommended [cryptography policy](../operator-manual/cryptography.md)?

## Decision Drivers

- We want to maintain Platform security and stability.
- We want to find a solution which is scalable and minimizes Platform Administrator burden.
- We want to best serve the Application Developers.
- We want to make the Platform Administrator life easier.
- We want to avoid Infrastructure Provider dependent implementation sprawl.

## Considered Options

1. Use `rclone` to replicate the data from our `primary` Infrastructure Provider to `secondary` public Infrastructure Provider on a second object storage.

    - `Good`, because it supports our goals of data redundancy, privacy, compliance, and cross-infrastructure-provider flexibility.
    - `Bad`, because in some jurisdictions and regulatory frameworks, Infrastructure Providers might be considered data sub-processors, which could impose additional requirements and compliance obligations.

1. Use `rclone` to replicate the data from our primary region to secondary region (outside Sweden) within the same public Infrastructure Provider on a second object storage.

    - `Good`, because it supports our goals of data redundancy, resilience, disaster recovery preparedness, privacy, compliance, encrypted data transfer, and cross-region accessibility.

1. Use `rclone` to replicate the data from our `primary` Infrastructure Provider to `secondary` Compliant Infrastructure Provider on a second object storage.

    - We investigated this with Infrastructure Providers, but found that there is no good way to enable communication between public Infrastructure Provider object storage and compliant Infrastructure Provider object storage.

1. Do nothing and accept the risk of data loss.

    - `Bad`, because not implementing data replication leaves our services vulnerable to data loss in case of hardware failures, system errors, or accidental deletions, and recovery options become limited.

## Decision Outcome

Chosen option:

- Use `rclone` to replicate the data from our primary region to secondary region (outside Sweden) within the same public Infrastructure Provider on a second object storage.

- As a result, and as per the [ECRYPT-CSA report](https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5ba203b9b&appId=PPGMS), We concluded that the `Salsa20` and `Poly1305` ciphers comply with our use of the [Cryptography Policy](./../operator-manual/cryptography.md) and we can use the encryption feature in `rclone` for our replication strategy.

### Positive Consequences

- We have `Data Redundancy` and `Resilience` that provides a safeguard against data loss due to hardware failures, natural disasters, or other unforeseen events.
- We don't increase the operational complexity.
- We avoid security theatre.

## Recommendations to Platform Administrators

- Platform Administrator should encrypt the backups before sending to an off-site location outside of Sweden and use the encryption feature in `rclone` which adheres to our [cryptography policy](../operator-manual/cryptography.md).

## Links

- [XSalsa20 with 192-bit nonce](https://en.wikipedia.org/wiki/Salsa20#XSalsa20_with_192-bit_nonce)
- [ECRYPT-CSA report](https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5ba203b9b&appId=PPGMS)
- [Configuration Encryption](https://rclone.org/docs/#configuration-encryption)
- [secretbox](https://pkg.go.dev/golang.org/x/crypto/nacl/secretbox)
