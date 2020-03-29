# Provision of intelligent random values

## Aim

In Test data creation despite having often very specific test data requirements to facilitiate reproducable outcome both
in exploratory testing but also in regression testing sometimes we want random values.

Example:
* Names of business partners
* Random text

We want to provide an easily accessible feature for users of ```baangt``` to deal with this requirement without needing
to develop code.

## Implementation

Implement a class (RandomValues), activity (Random) in API and SimpleFormat as well as variable replacement (``$(RANDOM)``). 
The implementation of the activity and variable replacement needs to be done in ``TestStepMaster``.

### Class RandomValues

Parameters for the class should be none in init, and the following in Method ``retrieveRandomValue``:
* RandomizationType (default: "String". Other values: Int)
* Min (default: 3)
* Max (default: 10)

### Activity "Random"

Parameters of the activity ``Random`` are defined in field ``value`` with JSON-Format (e.g. ``{Type:String,Min:5,Max:40}``) 
and must be mapped to the method parameters (Type->RandomizationType, Min->Min, Max->Max).

In this case the return value must be stored to testDataDict into the variable defined in column ``value2``

### Variable replacement

When ``$(RANDOM)`` is used in e.g. Activitiy ``SETTEXT`` in the column "Value", then we should execute method
``retrieveRandomValue``. The logic must also be implemented in ``TestStepMaster`` in method ```replaceVariables```. 

Also in variable replacement additional parameters can be mentioned, e.g. ``$(RANDOM{Min:10,Max:60})`` 

### Randomization
Implement one String and one Integer generation of random values and return according to length definition in min/max.

### Storing 
In Activity "Random" we need to store the resulting value in the field given in ```value2``` from the TestStep.

## Example File
An example File with explanations can be found in folder ``Examples``, filename ``Random.xlsx``

## Scope / DOD (including effort estimation)
* Implementation provided (in line with coding standards and PEP-8 conformity) (2 hours)
* Functional test executed and passed (theoretically if values from ``Random.xlsx`` work, this should be enough) (1 hour)
* Enhance existing documentation in docs-Folder in RST-Format (0,5 hours)
    * in this case in simpleExample.rst and SimpleAPI.rst
* Unit-Tests in tests-folder providing reasonable coverage (e.g. 80%) of the provided functionality (1 hour)
* git commit to feature branch and pull request on Gogs created (no additional effort)