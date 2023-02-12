# Section 7: Writing a DNS Spoofer

See [interceptor.pdf](interceptor.pdf)

# NOTES
## net_cut
This script is used to capture traffic by `Kali` VM from **another VM**.
Enable NF queue on `Kali` VM before running Python script:
```shell
iptables -I FORWARD -j NFQUEUE --queue-num 0
```

Remove NF queue once done:
```shell
iptables --flush
```

## dns_spoof
This script is used to capture traffic by `Kali` VM from itself.
Enable NF queue on `Kali` VM before running Python script:
```shell
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

Remove NF queue once done:
```shell
iptables --flush
```