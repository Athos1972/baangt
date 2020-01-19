# Welcome
This is the current release of baangt: "Basic And Advanced Next Generation Testing".

## Installation in a python virtual environment:
Depending on your virtual environment something along these lines:
```
conda create baangt
conda activate baangt
pip install baangt
```

## Installation from GIT-Repository:
Clone the repository: ``GIT CLONE https://gogs.earthsquad.global/baangt``

Then fire up your favorite virtual environment, e.g. 
`CONDA create baangt`, activate it, e.g. `CONDA activate baangt` and install the necessary requirements: `pip install -r requirements.txt` and you're good to go.

##Usage:
``baangt`` can be used for API, oData V2/V4, Browser (Chrome, Firefox, Safari, IE and more) Testing based on a common data layer. As complex as this sounds, as easy is it to start with, give it a try!
##Preparation:
You need at least a data- and a sequence definition file (example: `DropsSimple.xlsx` in the root folder of `baangt`).
##Run the Testcase
``Python baangt.py --run="DropsSimple.xlsx"`` will execute the testcases defined in the file (login to drops-app, recycle a product)
##Receive the results
You'll find the output file in the folder `1testoutput` as XLSX with a summary of duration, successful vs. non-successful testcases and a second tab with details for each looped testcase.
##Awesome, but not enough?
You're deeply impressed by the simplicity of the solution, but want MORE? We've got you covered. The second example shows the same outcome with much greater flexibility. For the second execution you'll use DropsTestRunDefinition.xlsx-File. You can see, that there are more Tabs than in the first example, for instance can you specify which datafile and tabname(s) to use for execution of a testrun, which lines from the datafile to skip/run, which browser to use and much more.
Calling ``baangt.py`` is still same simple:
`Python baangt.py --run="DropsTestRunDefinition"`. Again you'll find an excel sheet in the folder `1Testoutput`.
##Nice(r), but how about a real life example?
You're right. Nobody can test his application with 5 datafields and 1 business process. 

Real life regression tests often span multiple applications (thus we use TestCaseSequence), many business processes (the testcases) and each of them in countless variations (datafile with usage of TestStepSequences). 
No matter, how complex the application under test is, the start is always a Testrun definition. 

Btw. try `python baangt.py` without parameters to start the UI. It should run on Mac, Windows and all major Linux-Distributions with X11 
##Still want more? Create your own TestStepClass:
Every once in a while the TestStep-Definition via XLSX or the database will not be enough for your use-case. You can easily subclass whatever you need and still use the rest of the framework.
```
from baangt.TestStep import TestStepMaster

class myTestStep(TestStepMaster):
    def execute():
        self.driver.goToURL("http://www.google.com")
        self.driver.findByAndSetText(xpath='//input[@type="text"]', value='baangt')
        self.driver.findByAndClick(xpath='(//input[contains(@type,'submit')])[3]')

```

That's it. All the rest is taken care of by baangt. You'll also receive a nice export file showing timing information for your TestCase.

You can subclass any other functionality, that doesn't fully fit your needs (IBAN-Generation, Browser-Handling, Timing) and also create your own Assertion-classes (for instance if you need to receive data from a Host-System or RFC/SOAP-Connection, which is not natively supported by ``baangt.py``). Of course you'd only re-implement methods, that you need to enrich and consume everything else from the framework.

##Browser related knowledge
###Setting, which browser to start
* Method 1:
Set the browser in the Testrun Definition (either in XLSX in Tab `TestCase` in the column `Browser` or in JSON:

```
  "dontCloseBrowser": "True",
  "TC.Browser": "CHROME"
``` 
)

* Method 2:
Set the browser in the `globals.json` file to overwrite any settings of the testrun definition.
```
  "dontCloseBrowser": "True",
  "TC.Browser": "CHROME"
``` 
Then call `baangt.py` as usual:

`python baangt.py --run="someRunNameXLSXorJSON" --globals='mynewGlobals.json'`

###Starting browser in Headless Mode:
Either in XLSX or in JSON on level TestCase set the BrowserOptions as follows:

`{'HEADLESS': 'True'}`

#Further reading:
Please see latest news on http://baangt.org for community edition and http://baangt.com for corporate environments.