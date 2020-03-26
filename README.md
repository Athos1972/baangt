# Welcome
Please find the full documentation on [ReadTheDocs](https://baangt.readthedocs.io)

# Further reading:
Latest news on http://baangt.org for community edition and http://baangt.com for corporate environments.


 - donwload latest webdrivers in baangt/browserDrivers folder
 - or if you run baangt and execute with TC.Browser = FF, then latest geckodriver will be downloaded.
 
To run selenium grid 4 
```bash
$ java -jar /baangt/browserDrivers/selenium-server-4.0.0-alpha-5.jar standalone
```

Check http://localhost:4444/status

Use to test examples/globals_grid4.json

TC.Browser: REMOTE_V4

TC.BrowserAttributes: {'browserName': 'firefox', 'seleniumGridIp': '127.0.0.1', 'seleniumGridPort': '4444'}