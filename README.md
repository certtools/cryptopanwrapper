# CryptoPanWrapper


This is a simple wrapper class around the following libraries:

  * [pycryptopan](https://github.com/certtools/pycryptopan)
  * [yacryptopan](https://github.com/keiichishima/yacryptopan/)
  * [cryptopanlib](https://github.com/certtools/cryptopanlib)

## Crypto-PAn

Crypto-PAn stands for Cryptograpy-based prefix preserving Anonymization.
Quoting from [the original site]():

"This is an implementation of the cryptography based prefix-preserving trace
anonymization technique described in "Prefix-Preserving IP Address
Anonymization: Measurement-based Security Evaluation and a New Cryptography-
based Scheme" authored by Jun Xu, Jinliang Fan, Mostafa Ammar and Sue Moon.
In this implementation, we use Rijndael cipher(AES algorithm) as underlying
pseudorandom function. "

**Note**: technically speaking, what Crypto-PAn does, is actually **pseudonymization** of IP addresses.
Since every IP address is mapped uniquely (1-1) onto another IP address (via AES encryption).
So, for all purposes of [GDPR](), Crypto-PAn does **pseudonymization**. However, the original paper called it anonymization.
We will use these two terms within this page synonimously (although it's actually wrong).

## Implementations

Currently there are many implementations of the Crypto-PAn Algorithm:

 * [pycryptopan](https://github.com/certtools/pycryptopan)
 * [yacryptopan](https://github.com/keiichishima/yacryptopan/)
 * [the original C++](https://www.cc.gatech.edu/computing/Telecomm/projects/cryptopan/)
 * [David Stott's Lucent Tech C++](https://www.cc.gatech.edu/computing/Networking/projects/cryptopan/lucent.shtml). This one is very fast since it uses the AES NI Intel Instruction.
 * [opencores](https://opencores.org/project/cryptopan_core) implemenation. Requires hardware but is blazingly fast.
 * ... (probably some more)...


## The CryptoPanWrapper

This code wraps the differnet implementations and especially makes using David Stott's Lucent implementation useable via Python.

How to use it?
```python

>>> from  CryptoPanWrapper import CryptoPanWrapper
>>> cp = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="yacryptopan")
>>> cp.anonymize('192.0.2.1') == '192.0.125.244')
>>> cp2 = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="pycryptopan")
>>> assert(cp2.anonymize('192.0.2.1') == '192.0.125.244')
>>> cp3 = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="cpp-cryptopan")
>>> cp3.anonymize('192.0.2.1')
...

```
