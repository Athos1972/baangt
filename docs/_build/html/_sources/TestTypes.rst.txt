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

No oversimplification
---------------------

Please don't get me wrong. Just because we have a great tool, it doesn't mean that testing will happen by itself. There's
still a lot of expert work needed for Testdesign, Stagedesign, Creation and maintenance of Testsets, creation and
maintenance of test data sets, deployment strategies. ``baangt`` provides efficient ways to work, but work still needs
to be done.