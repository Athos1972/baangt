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
Right now the user must know the allowed parameter names in order to tune the globals-file. That's not ideal. 

### Solution approach:
For empty entries (Currently 4 at the end of the list):
Change the Parameter-fields in the UI to be Dropdowns. Have a method to set the default entries. Enable manual 
addition of values by the user. 

For filled entries:
No dropdown. Instead show a "delete"-Button for each row.