# To be updated based on this communication happened on 17.3.2020 on freelancer.com chat:

ok, I would like to go task.
https://gogs.earthsquad.global/athos/baangt/src/master/TechSpecs/30%20Ready/PYSIMPLEGUI_UI_ADDITONS_1.md


I do was thinking to improve the Global Settings configuration from the first day.

Below is my suggestion for Baangt framework as per standard guidelines:
1> UI should not force to remember all keywords to User. All choices and their meaning should be visible in the form of DropDown, ComboBox, Checkbox.



2> Easy way to Save / Load /Export Settings.

Please check a reference Settings from TWS gateway, which I am very impressed with UI and easy management.
https://gogs.earthsquad.global/athos/baangt/src/master/TechSpecs/30%20Ready/PYSIMPLEGUI_UI_ADDITONS_1.md
Here you can see,User can see all possible settings and their explanation.
So a NOOB user can understand easily how each setting activation and deactivation can affect the execution.
User Avatar
I was thinking to implement global settings via GUI Menu Box, which would load globals.json file and activate or deactivate necessary options.

For settings which require True/False, we can use it as checkbox.
For variable which require selected options like exportFilesBasePath we will use BROWSE directory function.

These are example for improvement.
Please let me know your views.
Yes, that's great indeed. The different configurations need to load and save the settings. The entry screen should still be as clean and simple as possible (the way it is now before you klick "Details").
Is this possible as pysimpleGui or do we need switch to QT?
We will stick to PySimpleGui, as moving to QT will force Tester to install QT for their OS along with pyQT.


But we can't ignore the performance of QT. Since it is compiled and will be more faster than python.
?
User Avatar
Now I need to collect all possible settings we can do in Globals.json file, so that we can include all at single place.
Where I can look for?
Easy. Just a sec.
User Avatar
ok
https://baangt.readthedocs.io/en/latest/ParametersConfigFile.html
and after first chapter here: https://baangt.readthedocs.io/en/latest/Developer.html
let me check
ok, I got all settings.
So here is my workflow:
--> Keep the existing methods to import globals.json settings as it is without affecting its features.
--> When user will click on "Details". It will switch to Settings Menu.
--> This can be accessed via File> Properties>Preferences

Currently "Properties" submenu is not working or not implemented.
--> All settings like "Rlease", "TC.slowExecution" will be implemented internally. And User can see necessary settings automatically activated/deactivated based on globals.json file.

(We will have to provide explanation for both Developer as well as Tester perspective. So Documentation will be updated).


--> If user make any changes in configuration, it will not implemented unless "Apply" Button is clicked.( We will add the button "Apply","OK","Cancel" to handle each case).

--> On Apply, The globals settings will be override with new settings.

--> on Close or Ok, the User will be switched to Main Screen.
User Avatar
How's that?
Sounds good. I'm thinking to have a JSON-File with the available parameters, datatype and Mouseover-Texts rather than hardcoded in the screen. What do you think?
Ok, So that json-file can be updated in future for new functionality. Mouseover-Texts will be used as hints to tell how this setting works.

It will be like, updating a Json object( Initially with all available settings) with another Json file(here, globals.json).

And User will see all settings activated or deactivated at single places. So that he/she can modify based on the requirement.
User Avatar
?
I'd see the ui parameters JSON as something different than the globals.json. Ultimately of course the settings, that were chosen in the UI will be written to the Globals-File(s). But the definition, which elements, which data types, which mouse-over-texts will not be in globals.json.
User Avatar
okay. I think if we will implement settings like we have done for Address Create (singleton class). and globals.json file will activate and deactivate necessary settings.

what I am trying to think is that.
1> A baangtsettings.json file which store details of each settings as dictionary object.

Suppose, Release Variable. It will be stored like.

{"variableName":"Release","hint":"set particular version to test ":,"type":"Input Box","value":"","displayText":"Current Release"}

Similar like we process form field.

And in globals.json file,
if there is Release=0.1.dev



It will update above dictionary object as:

{"variableName":"Release","hint":"insert particular release here":,"type":"Text","value":"0.1.dev
"}

So, We will store other variables also.

And in UI it will be diplayed based upon input Type. like, if "type":"bool", we will display setting as checkbox. Example
TC.Network
.

"variableName":"TC.Network
","hint":"Enable / Disable network statistics":,"type":"Bool","value":"False", "displayText":"EnableNetwork"}

So, Each settings will have keys ["variableName","hint","type","value","displayText"]

variableName --> mapped to global settings file
hint ---> Display text
type ---> to display as checkbox, inputBox
value ---> This is the field that will be updated for each Globals.json file
displayText ---> This will be displayed on Frontend to User.


This is my plan. May be you have better than this, I would like to know as well.
Value should be able to have a json-element for dropdown-values. Other than that it's pretty much exactly what I thought about!
User Avatar
ok, so for dropdown, it will be like <select> tag with <option>
Yes, sounds good

# Scope of this enhancement

UI has currently just very basic functionality. Enhancements are needed in the following areas:

## More comfortable handling of Global Parameters
Right now in baangt.UI.UI when you chose any global*.JSON the parameters and values from this file are displayed. 
4 empty lines are added to give the user a chance to add more parameters/values. In long configuration files, this
leads to an overflowing window.

### Solution approach
Keep the global parameters/values in a sorted dict. Keep for instance 10 parameter/value-pairs on the UI (just as
parameter-01, value-01, parameter-02, value-02 and so on). Add a vertical scroll-bar on the UI (if there are more 
than 10 parameters (including the 4 empty ones)). 

In the initialization loop over the first 10 entries of the globals-Dict and fill in parameter-01, value-01 until 
parameter-10 and value-10. 

When the user scrolls on the vertical scroll-bar, e.g. to position 4: Read the globals-Dict from position 4. Fill in
UI-Element parameter-01 with parameter 4 from globals-Dict, value-01 with value 4 from globals-Dict, and so on.

## Global Parameters as dropdown with additional values:
Right now the user must know the allowed parameter names in order to tune the globals-file. That's not ideal. It would
be better if at least standard values are in a dropdown and only customer specific values must be known.

### Solution approach:
For empty entries (Currently 4 at the end of the list):
Change the Parameter-fields in the UI to be Dropdowns. Have a method to set the default entries. Enable manual 
addition of values by the user. 

For filled entries:
No dropdown. Instead show a "delete"-Button for each row. After pressing the delete-button remove the entry and reload
the Window (hide/unhide on Mac doesn't really work. It destroys the layout. Reloading works well)