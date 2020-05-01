# Aim

Have a UI for Proxy server maintenance. Users should not have to work inside JSON-files.

# Prerequisites

Proxy-Servers are currently in JSON File proxies.json in /baangt. 

# Implementation

In baangt UI (pyQT5) create a new action button "Proxies". 

* On click of this button, open a new window with a table display, header for the columns of the table and buttons:
    * Button "OK" - save result to JSON and close the screen. Return back to main screen
    * Button "Exit" - don't save.
* Load contents of proxies.json.
    * The columns should arrange themselves dynamically according to the attributes in the JSON-Entries. 
      Currently those attributes (all string unless otherwise mentioned) are:
         * IP
         * Port
         * Type (either SOCKS or HTTPS - but UI shall not check validity)
         * User
         * Password
         * UsedCount (int)
         * ErrorCount (int)
    * Next to each line, there shall be a button "Test". Alternatively a marked line from the grid shall be used and
      Test-Button shall be on the bottom of the window.
         * If the button is clicked, call method "testProxy" of class "ProxyRotate". If result is ```true``` display
           "Proxy test successful". If result is not boolean display f"Proxy not reached: {result_from_call}"          
             
# DoD
 
* Part of the UI delivered in a separate branch to gig repository on Gogs-Server
* Unit-Test coverage (in folder /tests) of 80% (for all committed/changed methods) 
* no critical linter errors or warnings (PEP-8 conformity of the code)