# Section 8: Writing a Code Injector

This section primarily aims as JS execution.
One of the options is to execute [BeEF](https://beefproject.com/) JS to take control over victim's browser.

```shell
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

Remove NF queue once done:
```shell
iptables --flush
```