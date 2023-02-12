# Section 8: Writing a File Interceptor

## replace_downloads
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
