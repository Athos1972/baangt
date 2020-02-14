Types of tests
==============

No matter if your organization is agile or waterfall oriented or follows one of the many hybrid variants. Sooner or later
you'll have an increment - an outcome from your software developers or customizers. You paid for it. You want it in production.
But will it work? Will there be any unwanted side effects to existing functionality?

Increment testing
-------------------

Usually an increment is tested manually by human testers who are not identical with the developers.

Depending on maturatiy of your organization and many other factors, the testers will be more or less clearly instructed,
what to test. They might have written business requirements and deduct the test cases themselves. In ideal setups they
were part of the development lifecycle, know the deviations from original requirements, pitfalls and workarounds and can
adjust their test expectation accordingly.

Unless you're in a greenfield situation where the whole system landscape needs to be tested and retested for months or years
your Testers will focus on testing the increment - not so much the existing functionality, which used to work fine already.

Use ``baangt`` already in preparation of this test phase. Create all the test cases, that you plan to execute. Create all
the data combinations, that you'll want to have tested. Once the functionality is there, record the most complex scenario
in the recorder. Instead of testing 100s of cases manually, you'll need only one recording and the prepared dataset. Start
the TestRunExecution, sit back and wait for the results. Simple like that.

Heartbeat and Alive-Testing
---------------------------
Alive-Testing is usually done with just one quick test case in all stages (Dev, Pre-Quality and Quality-System). It will
show general availability of the landscape and applications running on it. Alive-Tests with some APIs could run for instance
every 5 minutes.

Heartbeat tests are a smaller subset of regression tests. E.g. if you have 10.000 testcases in regression tests, you'd
use a few hundred for heartbeat tests. They'd usually run a few times per day on Pre-Quality- and once per day on
Quality-System) and of course in the build pipeline.

Regression testing
------------------

If you followed through on Increment testing imagine the joy of the next release! You'll have the increment tested and run
all test cases of previous increments as well. That's called regression testing. If you did everything well use the results
of regression tests and increment tests as rock-solid base for your decision whether to move on to production or not.

Performance testing
-------------------

So you did regression and increment tests, moved to production and receive countless complaints from users, that the
performance of the system is too slow. Additionally there are now bugs that appear due to timeout situations. Damn.

    **What happened?**

You tested only for functionality, but not for load. With a few simple adoptions to your test cases you can simulate any
number of users. To achieve realistic performance testing you'll need more hardware for testing than for regression and
increments. But you'll use the same tool: ``baangt``.

As of today (Jan 2020) ``baangt`` does not provide infrastructure monitoring. In order to analyze the results of your
performance tests you'll need additional tools, but ``baangt`` will give indications, which components or which functionalities
need a closer look by your experts.

End to End (E2E) Testing
------------------------

Whenever you have more than one system/microservice dealing with a process, you'll need E2E-Testing. Of course E2E-Tests
are more complex than just running test cases against one functionality and compare results to the expected values and
behaviour. In larger organizations you'll want to have E2E-Regression tests before you release increments to production.
``baangt`` follows a structure of TestCaseSequences where you combine multiple single Testcases into one Sequence, which
is exactly tailored to run E2E Tests.

Lifecycle tests of business objects
-----------------------------------
Lifecycle tests come in basically two variations, but can be combined - depending on the requirements of the business.
Many industries deal with objects, that follow a certain (long) life cycle. The life cycle can go over years or decades.
These tests are complex and cost a lot of time and effort.

Time travel tests
^^^^^^^^^^^^^^^^^

Often companies have "Time travel" system landscapes, where they
create copies of the whole system landscape (or large parts of the core systems), change the system time on all servers
and run tests subsequently with different dates. ``baangt`` does not support this type of testing out of the box. But
we provide a functionality to "Pause" Testcase and TestCaseSequence execution. You can easily subclass the corresponding
master classes and create your own mechanism, when to pause a Testcase or TestCaseSequence.

Cradle to the grave
^^^^^^^^^^^^^^^^^^^

Another common form of lifecycle tests. In this case the system time remains basically the same, but the test cases are
created in a sequence to follow the birth of an object until it's deletion. This might be a material, which get's created,
production recipe created, work planned, sales contract and order created, produced, delivered, invoiced, paid and
revenue calculated. In service industries C2G-Tests are designed around a customer. ``baangt`` fully supports complex
testcaseSequences running on multiple technologies (Web, API, etc.) also in asynchronous scenarios, for instance if you
need to wait for nightly batch processing of a mainframe.

No oversimplification
---------------------

Please don't get me wrong. Just because we have a great tool, it doesn't mean that testing will happen by itself. There's
still a lot of expert work needed for Testdesign, Stagedesign, Creation and maintenance of Testsets, creation and
maintenance of test data sets, deployment strategies. ``baangt`` provides efficient ways to work, but work still needs
to be done.