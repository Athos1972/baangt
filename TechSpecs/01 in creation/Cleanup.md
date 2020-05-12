# Aim

After longer or intense use of baangt a lot of files accumulate, that the user might no longer need. 

This functionality shall provide a convenient way to get rid of those files.

- Logs
- Screenshots
- Temp Downloads

User shall have an option to state age of the files, that shall be deleted. 31 is default. 0 will delete all files.

# Functional specification

We need a class, integration in baangt CLI and baangt UI.

## CLI
* New parameter ```--cleanup <days>```.
* Then call class Cleanup

## UI
* New button ```cleanup```. Popup to ask for how many days. Default 31.
* Then call class Cleanup

## Class
* Have a method for each type of files:
    * Logs
    * Screenshots
    * Temp Downloads
* Provide method ``clean_all``, which calls all the other methods.

# DoD
* Class implemented
* CLI method implemented and tested
* UI button implemented and tested
* Unit-Tests for class created
* Documentation updated

