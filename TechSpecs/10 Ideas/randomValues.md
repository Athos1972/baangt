# Provision of intelligent random values

## Aim

In Test data creation despite having often very specific test data requirements to facilitiate reproducable outcome both
in exploratory testing but also in regression testing sometimes we want random values.

Example:
* Names of business partners
* Random text

We want to provide an easily accessable feature for users of ```baangt``` to deal with this requirement without needing
to develop code.

## Implementation

Implement a class (RandomValues), activity (Random) in API and SimpleFormat as well as variable replacement (``$(RANDOM)``). 
The implementation of the activity and variable replacement needs to be done in ``TestStepMaster``.

### Class RandomValues

Parameters for the class should be none in init, and the following in Method ``retrieveRandomValue``:
* RandomizationType (default: "String". Other values: Int)
* Min (default: 3)
* Max (default: 10)

### Acitvity "Random"

Parameters of the activity ``Random`` are defined in field ``value`` with JSON-Format (e.g. ``{Type:String,Min:5,Max:40}``) 
and must be mapped to the method parameters (Type->RandomizationType, Min->Min, Max->Max).

In this case the return value must be stored to testDataDict into the variable defined in column ``value2`` 

### Variable replacement

When ``$(RANDOM)`` is used in e.g. Activitiy ``SETTEXT`` in the column "Value", then we should execute method
``retrieveRandomValue``. The logic must also be implemented in ``TestStepMaster`` in method ```replaceVariables``` 

### Randomization
Implement one String and one Integer generation of random values and return according to length definition in Min/Max.

### Storing 

## Scope / DOD
* Implementation provided (in line with coding standards and PEP-8 conformity)
* Functional test executed and passed (in this case it means to also create a new simpleXLS-Format where both ways (Activity = Random or variable replacement) can bet tested)
* Enhance existing documentation in docs-Folder in RST-Format
    * in this case in simpleExample.rst and SimpleAPI.rst
* Unit-Tests in tests-folder providing reasonable coverage of the provided functionality
* git Commit to feature branch and PullRequest on Gogs created