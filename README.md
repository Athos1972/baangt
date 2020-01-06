# Welcome
This is the current release of baangt: "Basic And Advanced Next Generation Testing".

## Installation in a virtual environment:
``pip install baangt``

## Installation from GIT-Repository:
Clone the repository: ``GIT CLONE https://gogs.earthsquad.global/baangt``

Then fire up your favorite virtual environment, e.g. 
`CONDA create baangt`, activate it, e.g. `CONDA activate baangt` and install the necessary requirements: `pip install -r Requirements.txt` and you're good to go.

## Installation from DOCKER Hub:
## Fire up your own Docker:

#Usage:
###Preparation:
You need a datafile (example: `DropsTestExample.xlsx) and a Testrun definition as Excel-Sheet (example `DropsTestRunDefinition.xlsx`). Alternatively provide the definition of the testrun as JSON.
##Run the Testcase
``Python baangt.py --run="DropsTestRunDefinition.xlsx`` will run the Testcase specified in file ``Franzi.xlsx``.
##Process
Depending on your TestRun or TestCaseSequence settings one or more browsers (Firefox, Chrome, Safari, Internet Explorer) will start (visible or hidden) and execute the steps defined in the definition of the testrun. An output file (XLSX) consisting of "baangt_" + Testrun-Name + Date and Time will be created.
##Create your own TestStep:
Every once in a while the TestStep-Definition via XLSX or the database will not be enough for your use-case. You can easily subclass whatever you need and still use the rest of the framework.
```
from baangt.TestStep import TestStepMaster

class myTestStep(TestStepMaster):
    def execute():
        self.driver.goToURL("http://www.google.com")
        self.driver.findByAndSetText(xpath='//input[@type='text']', value='baangt')
        self.driver.findByAndClick(xpath='(//input[contains(@type,'submit')])[3]')

```
 That's it. All the rest is taken care of by baangt. You'll also receive a nice export file showing timing information for your TestCase.

#Further reading:
Please see latest news on http://baangt.org for community edition and http://baangt.com for corporate environments