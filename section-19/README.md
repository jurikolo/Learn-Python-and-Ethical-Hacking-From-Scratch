# Section 19: Writing a Vulnerability Scanner

Read more about BeautifulSoup here: [link](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

To be able to use XSS vulnerabilities, go to Metasploit VM and modify file `/var/www/dvwa/dvwa/include/dvwaPage.inc.php`.
Replace `security` cookie from "high" to "medium".

To test XSS, navigate to [DVWA XSS_R](http://172.16.43.139/dvwa/vulnerabilities/xss_r/) webpage and type something like this in a form:
```html
<scrIpt>alert('test')</sCript>
```

If it doesn't work, review if security is set to "medium". You may need to change in security tab: [link](http://172.16.43.139/dvwa/security.php).