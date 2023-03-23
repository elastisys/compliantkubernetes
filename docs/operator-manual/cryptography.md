---
tags:
- MSBFS 2020:7 4 kap. 9 §
- ISO 27001 A.10 Cryptography
- HIPAA S47 - Access Control - Encryption and Decryption - § 164.312(a)(2)(iv)
---
# Use of Cryptography

Compliant Kubernetes recommends the ECRYPT-CSA "near term use".
The key cryptographic parameters are listed below.

## Recommended Strengths

| Cryptographic Structure  | Size |
|--------------------------|------|
| Symmetric                |  128 |
| Factoring Modulus        | 3072 |
| Discrete Logarithm       |  256/3072 |
| Elliptic Group           |  256 |
| Hash                     |  256 |

## Recommended Algorithms

| Function             | Algorithm              |
|----------------------|------------------------|
| Block Ciphers        | AES<br/>Camellia<br/>Serpent |
| Hash Functions       | SHA-2 (256, 384, 512, 512/256)<br />SHA-3 (256, 384, 512, SHAKE128, SHAKE256)<br />Whirlpool (512)<br />BLAKE (256, 584, 512) |
| Public Key Primitive | RSA (>3072) <br/> DSA (>256/3072) <br/> ECDSA (>256) |

!!!note
    For HTTPS traffic, Compliant Kubernetes uses [TLS 1.3](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.3).
    TLS 1.3 mandates [forward secrecy](https://en.wikipedia.org/wiki/Forward_secrecy).
    In other words, an attacker cannot decrypt past HTTPS transmissions even if the TLS certificate (private key) is compromised.

    Compliant Kubernetes uses RSA 2048 when provisioning HTTPS certificates, which is lower than the present recommendation.
    However, these certificates have a short expiration time of 3 months.
    Hence, given the forward secrecy of TLS 1.3 and the short expiration time, **usage of RSA 2048 for HTTPS certificates does not add a security risk.**

## Further Reading

* [ECRYPT–CSA D5.4 Algorithms, Key Size and Protocols Report (2018)](https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5ba203b9b&appId=PPGMS)
* [BlueCrypt Cryptographic Key Length Recommendation](https://www.keylength.com/en/3/)
