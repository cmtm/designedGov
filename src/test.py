from DG_file import DG_file

privateKey1 = """-----BEGIN RSA PRIVATE KEY-----
MIIEpQIBAAKCAQEA6xySc9Eo/Ula75EurLPLMrfXr2IquSllfPCgNncnn7DG5NJ/
HI3XchTYkiYILWS3FafiVW+CkkcGAVDA5Bv1L5n8qRZiwMxVNDIYY6WPv0HK+VKP
5qeNi2EAPyjsBN6STWHbQp3Bmem/zgdDE62J6qx1fVBnAujA2qCC/x6U4uXRwM0W
QeuUiFPF4kEPb+L3z9xoCyzxNEbLtTuVNMz5j7KZS9n3lAskPMZFeGw2WpnoFN5a
+B/2xdzv19x9HpsTr/zTddkU7XNHhN3zXl9zN1ibmEwHBszmErQcGbAfokbXHs7W
xXKdKHCYPJ8zMFZY6R6u8sA475OT04+/S8FlKwIDAQABAoIBAQCJvLFnvG9hA6qM
kudfMe2nBuEK1F3nIANe0LFrdx71hODgiRkCp25CXUgLRtCfl1NTEomcN7ms7ILu
HlsCyAY6HuJQRNcR0CNScs6rAgFWsLqymdXH8P0RXICCf/zVVXcsclm7iyQygShn
EQYQ7yfPHb2u7n2KzMS+0C4uO8JJse5Pwh1A36bctZmVtyVV88oyBqoIijFQ8MLG
6uLBzSg4NY1F7f0L7DWSrJVzubwsdBKNs+5eRRmMmILqjn5grSPltL6UY92611W0
HBJTLXpziVAJNQ2KaQiv6jlOsIgeipFCBowKVY6WsSF11scehmbZu9fNmJ5vETht
EtEGt41RAoGBAPog7VjLIOK0UtbZVhMYfRmNf49xUMqGnrin/l2knywJwTi3YEMF
ZWaqOhkVJcl/dxhQxn1R/YSL6353MHtNlAeCFjiFZ0zO+Z1SVZ6grkeXSiuxXH2y
akRbdivis1WLVa8JFSRPhFzCOhsPC9nx3/uIO4EeSASmn1O/rGB1eP/3AoGBAPCh
Z5ugICLsZBt1rTxYFXfN8FJzuBs+CeDVKnuiy7UVaCVcYNQHhkyJGuNf058Mm9ZN
RXxdoikjDyTkUrT4VIkuCw/2mjosEf3eFLJcUXOF5NVeKQ95YyGRxtTialI13L3M
MfgDJ8mot+voq34e/nT0X1yMM71xG/5D9D01Tp9tAoGAdpL9cUZ6RH5vduJ453yI
cYCepAV340qGG8unzgSoYFwPeS+VNrBsLYstF47q5ubCMoi4T9h6ckdSUBV4qjtQ
nW6R0iGLouHLe0T4ycYqWE3kH2ppCj12Gwmwr4U8tqTi7aNEnn4DpWV93i331E3R
fJBMhR0xzuKeTTlkIiYOQmkCgYEAld3guoNrIHUcECIlZ8zwafJgN+oMgyMLYfVB
hUkqGDkh6Qr033lkQmyty2kWUxu2Py1XFpL2eSp1tyNhA4cal2mOyD1tZsel2Pgk
6cUnkYyVrfH8HsAaZoD1VgdB8rvLJIZ1pKLKeAVVr1702BMTpeHBNtG3M8irh5vp
FOoLcq0CgYEAvXr/+ZXqs2tAJed1DdXNcHxtmzgpyHTb4mulciRQyVJsSE123l8F
rH99VlxHxYUlgZHu/28tV9LhCfMbBBOICsfnV14T/LpErOPH2unvEOmGYXajMrWG
onwvLPt/juujKaBbjyQc/FseBOFMgedWpa7b7BJJhQtxs6KaKdNApSs=
-----END RSA PRIVATE KEY-----
"""

publicKey1 = """ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDrHJJz0Sj9SVrvkS6ss8syt9evYiq5KWV88KA2dyefsMbk0n8cjddyFNiSJggtZLcVp+JVb4KSRwYBUMDkG/UvmfypFmLAzFU0MhhjpY+/Qcr5Uo/mp42LYQA/KOwE3pJNYdtCncGZ6b/OB0MTrYnqrHV9UGcC6MDaoIL/HpTi5dHAzRZB65SIU8XiQQ9v4vfP3GgLLPE0Rsu1O5U0zPmPsplL2feUCyQ8xkV4bDZamegU3lr4H/bF3O/X3H0emxOv/NN12RTtc0eE3fNeX3M3WJuYTAcGzOYStBwZsB+iRtceztbFcp0ocJg8nzMwVljpHq7ywDjvk5PTj79LwWUr chris@FreeTower
"""
myDG_file1 = DG_file("fakeType", authorId = 0, content = {"fakeEntryA": 65, "fakeEntryB": "helloWorld"})
myDG_file1.addPublicKey(publicKey1)
myDG_file1.sign(privateKey1)