---
tags:
  - MSBFS 2020:7 4 kap. 9 §
  - ISO 27001 A.10 Cryptography
  - HIPAA S47 - Access Control - Encryption and Decryption - § 164.312(a)(2)(iv)
  - NIST SP 800-171 3.13.10
  - NIST SP 800-171 3.13.11
  - NIS2 Minimum Requirement (h) Cryptography
---

# Use of Cryptography

Welkin recommends the ECRYPT-CSA "near term use".
The key cryptographic parameters are listed below.

## Recommended Strengths

| Cryptographic Structure | Size     |
| ----------------------- | -------- |
| Symmetric               | 128      |
| Factoring Modulus       | 3072     |
| Discrete Logarithm      | 256/3072 |
| Elliptic Group          | 256      |
| Hash                    | 256      |

## Recommended Algorithms

| Function             | Algorithm                                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Block Ciphers        | AES<br/>Camellia<br/>Serpent                                                                                                  |
| Hash Functions       | SHA-2 (256, 384, 512, 512/256)<br />SHA-3 (256, 384, 512, SHAKE128, SHAKE256)<br />Whirlpool (512)<br />BLAKE (256, 584, 512) |
| Public Key Primitive | RSA (>3072) <br/> DSA (>256/3072) <br/> ECDSA (>256)                                                                          |

## Recommended Implementation

Ubuntu 22.04 already generates SSH and GPG keys conforming to this recommendation, as evidenced below:

```console
$ ssh-keygen
Generating public/private rsa key pair.
[...]
+---[RSA 3072]----+
|           o+.=++|
|           +o..= |
|        = =...o  |
|       O @.    o |
|      . S +.  . .|
|       + B  .. .E|
|      . O o ..o  |
|       o + +o... |
|          +oo=o  |
+----[SHA256]-----+
$ gpg --generate-key
gpg (GnuPG) 2.2.27; Copyright (C) 2021 Free Software Foundation, Inc.
[...]
pub   rsa3072 2023-03-24 [SC] [expires: 2025-03-23]
      41E32D8838ADA81B4D57333E79797753D349F087
uid                      Cristian Klein <cristian.klein@example.com>
sub   rsa3072 2023-03-24 [E] [expires: 2025-03-23]
```

## Notes on HTTPS Traffic

For HTTPS traffic, Welkin allows either [TLS 1.2](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.2) or [TLS 1.3](https://en.wikipedia.org/wiki/Transport_Layer_Security#TLS_1.3).
TLS 1.3 mandates [forward secrecy](https://en.wikipedia.org/wiki/Forward_secrecy).
TLS 1.2 makes forward secrecy optional, however, the [default cipher list](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#ssl-ciphers) in Welkin prioritizes algorithms that provide perfect forward secrecy.
In brief, **you can rely on forward secrecy with most browsers in use today**.

Forward secrecy addresses the "store now, decrypt later" attack.
In essence, an attacker cannot decrypt past HTTPS transmissions even if the TLS certificate (private key) is compromised.

Welkin uses RSA 2048 when provisioning HTTPS certificates, which is lower than the present recommendation.
However, these certificates have a short expiration time of 3 months.
Hence, with short certificate expiration time and forward secrecy, **usage of RSA 2048 for HTTPS certificates does not add a security risk.**

We recommend you to regularly run the [Qualys SSL Server Test](https://www.ssllabs.com/ssltest/) against the application HTTPS endpoints to make sure encrypted-in-transit sufficiently protects your data.
At the time of this writing, Welkin receives A+ overall rating.

## Further Reading

- [ECRYPT–CSA D5.4 Algorithms, Key Size and Protocols Report (2018)](https://ec.europa.eu/research/participants/documents/downloadPublic?documentIds=080166e5ba203b9b&appId=PPGMS)
- [BlueCrypt Cryptographic Key Length Recommendation](https://www.keylength.com/en/3/)
- [Ingress NGINX SSL Ciphers](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#ssl-ciphers)
- [Mozilla SSL recommendations](https://wiki.mozilla.org/Security/Server_Side_TLS)
- [Forward secrecy](https://en.wikipedia.org/wiki/Forward_secrecy)
