What is a baangt-plugin
=======================

Simply speaking, one baangt-plugin correspond to one class, and the
methods in the class correspond to the implements in the plugin.

how to make a baangt-plugin
===========================

first of all , we need to create a implement class, like this:

::

    import baangt

    from baangt.base.Timing.Timing import Timing

    class TimingHookImpl:
        
        @baangt.hook_impl
        def timing_init(self):
            return Timing()

        @baangt.hook_impl
        def timing_takeTime(self, timingObject, timingName, forceNew=False):
            return timingObject.takeTime(timingName, forceNew)

        @baangt.hook_impl
        def timing_addAttribute(self, timingObject, attribute, value, timingSection=None):
            return timingObject.addAttribute(attribute, value, timingSection)

        @baangt.hook_impl
        def timing_takeTimeSumOutput(self, timingObject):
            return timingObject.takeTimeSumOutput()

        @baangt.hook_impl
        def timing_returnTime(self, timingObject):
            return timingObject.returnTime()

        @baangt.hook_impl
        def timing_returnTimeSegment(self, timingObject, segment):
            return timingObject.returnTimeSegment(segment)

        @baangt.hook_impl
        def timing_resetTime(self, timingObject):
            return timingObject.resetTime()

and then register this implement class in /baangt/\_*init\_*.py:

::

    from baangt.base.Timing.hookImpls import TimingHookImpl

    plugin_manager.register(plugin=TimingHookImpl())

how the baangt-plugin work
==========================

for example, after transfer TestRun to a plugin, we can replace the
code:

::

    from xxx import TestRun
    TestRun()

by

::

    from xxx import plugin_manager
    plugin_manager.hook.testRun_init()

this replacement does not change anything of the result of programme's
execution.

how to replace the existing plugin by your own one
==================================================

for example, if you want to replace the default TestRun plugin,

you can easily change the implement of TestRun by just unregister the
default plugin and register your own one:

::

    plugin_manager.unregister(plugin=default_plugin)
    plugin_manager.register(plugin=my_plugin)

notice that if you don't unregister the old one, two same implements
(with same function name) in two plugins may both execute if you call
the function:

::

    plugin_manager.hook.i_got_two_implements()

the order of the execution follows the FILO (first-in-last-out) rule.

Author: Yuyi Shao
