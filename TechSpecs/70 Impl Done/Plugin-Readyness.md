# Current situation
baangt classes are well structure and generally follow the principle of separations of concern. Users can easily subclass
existing baangt-classes. Depending on the requirements the user might end up with subclassing a lot of classes and overwrite
a lot of methods.

Each method, that doesn't call super().<method>() means danger of upcoming breaking changes.

Sometimes it would be easier to implement a Plugin than subclassing.

# Aim of this task
Prepare baangt classes and methods for usage of [pluggy](https://pluggy.readthedocs.io/en/latest/). Implement pluggy-entry points in 
* baangt.base.BrowserHandling
* baangt.base.TestRun
* baangt.base.Timing
* baangt.base.ExportResults