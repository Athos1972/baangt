# Situation

In UI (baangtIA.py without any parameters opens the simple starter UI) there's a button with text "Import Katalon Recorder". 
On pressing the button another pySimpleGui Window opens. In this window one can import (from clipboard) the exported result
from Katalon Recorder (= Plugin in Chrome/FF to record browser interaction) and translate the contents to ```baangt``` format.

On "Save as"-Button a new XLSX Testrun-Definition in Simple format is created. All Teststeps from the recording are included
in the XLSX.

This works quite well. But it's not pretty (the UI) and the functionality is not complete or at least hard to use: 

In order to use the resulting
XLSX, the users have to do tedious manual steps (Create variable names (=columns) in tab "data", move entered data from TestStep into
tab "data" into each column and finally replace cells in column "Value" of TestSteps with the variable names, they just
created (=the columns in tab "Data")).

# Aim

When a recording is imported, all Values should be extracted as columns in the data-tab. For instance, if you have a recording

```markdown
gotoUrl | http://franzi.com 
Click   | //@ID='Button1'
SetText | //@ID='TextInput2' | testTextTestText
```

right now we translate this into correct simpleFormat, but we'll copy the value "testTextTestText" into the field "value"
of the Teststep. This is not practical. Users will have entered this text just as an example and want to use a variable to
dynamically replace this fixed text.

We shall extract all those variables, store them as columns in the Tab ```data```, set the field "Value" of the TestStep
to the variable name (e.g. ```$(TextValue1)```) and store the value from the recording in the proper field of the tab data in Line 1.

We shall do the same for Clicks. Create column "Button<n>" in tab data, set the testStepActivity to "ClickIF" and place 
column-name in the Value-field of the TestStep (e.g. ``$(Button001)``)

From the above example the tab data would look as follows:

```
Url               | Button001 | TextValue1       |
http://franzi.com |   X       | testTextTestText |
```

The Tab ```TestStepExecution``` would look as follows:

```
Activity  | LocatorType | Locator             | Value 
GOTOURL   |             |                     | $(Url) <-- Column in tab 'data'
CLICKIF   | XPATH       | //*[@id=Button1]    | $(Button001)   <-- Column in tab 'data'
SETTEXT   | XPATH       | //*[@id=TextInput2] | $(TextValue1) <-- Column in tab 'data'
```

# UI

If you have any suggestions, how to improve the UI of the Katalon Recorder Import dialogue, please get in contact.

# Test

Create unit tests for new functionality