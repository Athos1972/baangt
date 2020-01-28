# Aim
So far via class ```timing``` the durations of webpages are logged. In some performance testing and analysis jobs this
is not enough. Additionally we need the network traffic stored for each request.

# Vision
Activated via TestRun-Parameter or in Globalsettings the network traffic needs to be stored. In `ExportResults` the 
network traffic should be stored in a separate Tab in the output-XLSX (Status, Method, URI, Type, Size, Headers, Params, Response)
for each activity done in the browser

# Implementation idea:
Usage of https://github.com/browserup/browserup-proxy and the corresponding Python Package. Dynamically create a proxy 
for each active browser (and pass the new proxy-URL to the browser in ``baangt.base.BrowserHandling``. 
Read the logs of browserup-proxy after finished requests and store result together with the
```Teststep```. Other ideas welcome.

 