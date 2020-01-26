# Current situation
baangt classes are well structure and generally follow the principle of separations of concern. Users can easily subclass
existing baangt-classes. Depending on the requirements the user might end up with subclassing a lot of classes and overwrite
a lot of methods.

Each method, that doesn't call super().<method>() means danger of upcoming breaking changes.

Sometimes it would be easier to implement a Plugin than subclassing.

# Aim of this task
Prepare baangt classes and method for usage of pluggy. Implement pluggy-entry points in 