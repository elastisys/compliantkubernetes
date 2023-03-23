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
    Compliant Kubernetes might use RSA 2048 when provisioning certificates via cert-manager and LetsEncrypt, which is lower than ECRYPT-CSA recommends for near-term use.
    There is ongoing discussions to use RSA 4096 in website certificates (see discussions on [LetsEncrypt's own R3 certificate](https://community.letsencrypt.org/t/why-does-let-s-encrypt-r3s-cert-use-lower-rsa-than-the-root-cert/189339)).
    Given that the certificate expires after 3 months, we assessed that this situation is **okay for now**.

    The Compliant Kubernetes closely follows developments and discussions in the field and will take action when required.

## Further Reading

* [ECRYPT–CSA D5.4 Algorithms, Key Size and Protocols Report (2018)](https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5ba203b9b&appId=PPGMS)
* [BlueCrypt Cryptographic Key Length Recommendation](https://www.keylength.com/en/3/)
