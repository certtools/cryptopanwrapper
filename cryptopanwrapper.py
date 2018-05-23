#!/usr/bin/env python3

# Copyright 2018 by L. Aaron Kaplan <kaplan@cert.at>, all rights reserved
#
# Apache License Version 2.0, January 2004 http://www.apache.org/licenses/
#


import time
import sys
import ipaddress
from ctypes import cdll, c_uint


try:
    from yacryptopan import CryptoPAn as YaCryptoPAn
    have_yacryptopan = True
except:
    print("did not find yacryptopan. Please install it from https://github.com/keiichishima/yacryptopan/")

try:
    from cryptopan import CryptoPan
    have_pycryptopan = True
except:
    print("did not find pycryptopan. Please install it from https://github.com/certtools/pycryptopan/")

try:
    panonymize_lib = cdll.LoadLibrary("cryptopanlib.so")
    have_cryptopanlib = True
except Exception as e:
    print("did not find cryptopanlib.so. Please install it from https://github.com/certtools/cryptopanlib")
else:
    print("loaded cryptopanlib @ %s" % panonymize_lib, file=sys.stderr)


class CryptoPanWrapper():
    """ wrapper class around multiple implementations of CryptoPAN. Offers a single, common interface.
    Currently supports
      * yacryptopan (https://github.com/keiichishima/yacryptopan/)
      * pycryptopan (https://github.com/certtools/pycryptopan/)
      * cryptopanlib (https://github.com/certtools/cryptopanlib)


        >>> cpw = CryptoPanWrapper(b'some-long-32-bytes-key123456789')
        >>> cpw.anonymize('1.2.3.4')
    """

    def __init__(self, key, use="yacryptopan", prefixlen=16):
        """ initialises the CryptPanWrapper class, needs a key as byte string.  """

        assert isinstance(key, bytes), "need to specify a byte string as key to init()"
        self.key = key
        self.lib = use
        self.prefixlen = prefixlen

        try:
            if self.lib == "yacryptopan":
                self.cp = YaCryptoPAn(key)
            elif self.lib == "pycryptopan":
                self.cp = CryptoPan(key)
            elif self.lib == "cpp-cryptopan":
                panonymize_lib.init(key)
                self.anonymize_str = panonymize_lib.anonymize_str
                self.anonymize_str.restype = c_uint
                self.anonymize_int = panonymize_lib.anonymize
                self.anonymize_int.restype = c_uint
            else:
                print("Can't find a suitable cryptopan lib for the CryptoPan wrapper class")
                sys.exit(-1)
        except Exception as e:
            print("could not initialise cryptopan lib: %s" % str(e))

    def anonymize(self, ip):
        if not ip:
            return None

        if self.lib != "cpp-cryptopan":
            return self.cp.anonymize(ip)
        else:
            if isinstance(ip, str):
                return ipaddress.ip_address(self.anonymize_str(ip.encode('utf-8')))
            elif isinstance(ip, int):
                return ipaddress.ip_address(self.anonymize_int(ip))

    def benchmark(self, num_tests=10**4):
        print("  benchmarking %s" % self.lib)
        stime = time.time()
        for i in range(0, num_tests):
            self.anonymize("192.0.2.1")
        dtime = time.time() - stime
        print("  %d anonymizations in %s s" % (num_tests, dtime), file=sys.stderr)
        print("  rate: %f anonymizations /sec " % (num_tests / dtime), file=sys.stderr)
        print()
        return True


if __name__ == "__main__":

    try:
        cp = CryptoPanWrapper("foobar normal string", use="yacryptopan")
    except:
        pass

    print("=" * 78)
    print("sample test for correctness")
    print()
    cp = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="yacryptopan")
    assert(cp.anonymize('192.0.2.1') == '192.0.125.244')
    # assert(cp.anonymize_bin(0xc0000201, version=4) == 3221257716)
    # assert(cp.anonymize('2001:db8::1') == '27fe:8bc7:fee:1e:1e1f:f0fe:f0e1:83fd')
    # assert(cp.anonymize_bin(0x20010db8000000000000000000000001, version=6) == 53161570263948813229648829710638089213)
    cp2 = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="pycryptopan")
    assert(cp2.anonymize('192.0.2.1') == '192.0.125.244')
    cp3 = CryptoPanWrapper(b'32-char-str-for-AES-key-and-pad.', use="cpp-cryptopan")
    # XXX FIXME: this variant does not behave the same way as the others! We are getting other results. Why?
    # assert(cp3.anonymize('192.0.2.1') == '192.0.125.244') XXX FIXME: no correct results yet!
    print("OK")

    print("=" * 78)
    print("starting performance check", file=sys.stderr)
    print()
    cp.benchmark(num_tests=5*10**4)
    cp2.benchmark(num_tests=5*10**4)
    cp3.benchmark(num_tests=5*10**4)
