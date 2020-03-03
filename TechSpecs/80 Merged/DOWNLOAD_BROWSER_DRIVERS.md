# Result
If the browser drivers (Chromedriver, Geckodriver) for the current operating system can't be found in 
`Path(os.getcwd()).joinpath("browserDrivers")` download latest Chromedriver and Geckodriver and unpack them, so that the application can use them.

# Implementation
In class `baangt.base.BrowserHandling.BrowserDriver` in Method `createNewBrowser` call a new method to identify, whether the browserDrivers are in the expected location and if not, download them accordingly.