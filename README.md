# Welcome
This is the current release of baangt - the tool for "Basic And Advanced Next Generation Testing".

## Installation in a virtual environment:
``pip install baangt``

## Installation from GIT-Repository:
``GIT CLONE https://gogs.earthsquad.global/baangt``

#Usage:
##Run the provided Testcase
``Python baangt.py`` will run the Testcase specified in file ``default.json``

##Create your own TestStep:
:
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