# Learn Python and Ethical Hacking From Scratch

This project is a fork of [Learn Python and Ethical Hacking From Scratch](https://github.com/PacktPublishing/Learn-Python-and-Ethical-Hacking-From-Scratch),
published by Packt in combination with the same [video course on Udemy](https://www.udemy.com/course/learn-python-and-ethical-hacking-from-scratch).

# NOTES
## Scapy / kamene

To learn functions, execute something like:
```python
import kamene.all as scapy
scapy.ls(scapy.ARP)
```

-----

To fix "WARNING: can't import layer ipsec: cannot import name 'gcd' from 'fractions' (/usr/lib64/python3.10/fractions.py)",
replace `from fractions import gcd` with `from math import gcd` in ipsec.py file.
