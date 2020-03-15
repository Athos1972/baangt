Asynchronous vs. Canon tests
============================

Abstract
--------

Whenever you can't grab the verification of your test assumption right away, you're in an **asynchronous** scenario. When
you have an End2End-Scenario where this happens in more than one steps, you could consider setting up a test Canon.
Borrowed from music, a test canon will start with one test case until the halt condition is reached. Once the case can
continue (e.g. because a trigger arrived), the canon will not only continue to run the first test case in it's second
step but also start a new initial sequence of the same test case.

-------

Isn't everything asynchronous?
------------------------------

By nature basically every test is asynchronous, because we always wait for a reaction of the System under test. In most
cases, we're talking about Microseconds up to a few seconds. You'll not do anything special with waiting times up to
a few seconds. As you run anyway 50 or 500 parallel sessions, it doesn't really matter. But what if we need to wait
for e.g. 10 Minutes, 30 Minutes, 8 hours?

Polling vs. Events
^^^^^^^^^^^^^^^^^^

**Polling** means to have your currently active test case poll repeatedly for an event in a more or less fixed timely
interval. That's nice for smaller waiting periods and smaller installations. When you run with 500 parallel sessions and
you query a service every 500 ms for a specific answer you could create unrealistic load to that service. You're also
consuming resources of your test environment, which are then not available for other tasks. For ``baangt`` we recommend
to use polling for expected short waiting times (several seconds up to minutes) - but that's not a hard rule. YMMV.

**Events** (aka Callbacks) are the opposite. Your test case pauses and doesn't do anything until an external trigger
appears. Of course callbacks are more difficult to implement as you not only need to query a service repeatedly, but first
implement a callback service as well as the call to the callback service (even when it's done via Kafka or Redis). It's
another component, that needs to be written, tested and maintained.

Deep dive on test Canons
------------------------

What is a test Canon? They are basically the same concept as a canon in music

    From Wikipedia_:

    In music, a canon is a contrapuntal (counterpoint-based) compositional technique that employs a melody with **one or**
    **more imitations** of the melody played after a given duration (e.g., quarter rest, one measure, etc.). from Wikipedia_

.. _Wikipedia: https://en.wikipedia.org/wiki/Canon_(music)
.. _Youtube: https://www.youtube.com/watch?v=S9MN2WeqFY8

See the music canon in action on Youtube_

How does it apply to testing processes?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Imagine the following (simplified) test case sequence (in combination with a mainframe or SAP-System):

#. Create material master data in Backend. Validate: Material available in online shop (asynchronous)
#. Create sales order. Validate: Increased demand in material resource planning (batch)
#. Create delivery and shipping. Validate: Reduced stock of materials (asynchronous)
#. Create invoice. Validate: Invoice amount posted to A/R (batch)
#. Create payment. Validate: Open item closed (batch)
#. Create goods return. Validate: Special quality stock increased (asynchronous)
#. Create credit note. Validate: Amount of credit note in A/P (batch)
#. Create outgoing payment. Validate: Open item closed

In this example there are 4 batch processes, that we need to wait for before we can tell, whether the whole E2E-Scenario
works. Without any measures this means to wait for 5 days until we have a test result. Real use cases are not that simple and would
take longer. Back in the days when there was a month of User acceptance test (UAT) this was fine. Now with always shorter
release cycles you can't survive without new approaches.

How the test Canon works
^^^^^^^^^^^^^^^^^^^^^^^^

========================  = = = = = = = = =
Canons and                D A Y S / E X E C
------------------------  - - - - - - - - -
Teststeps                 1 2 3 4 5 6 7 8 9
========================  = = = = = = = = =
Canon 1 - Teststep 1 + 2  X
Canon 1 - Teststep 3 + 4    X
Canon 2 - Teststep 1 + 2    X
Canon 1 - Teststep 5          X
Canon 2 - Teststep 3 + 4      X
Canon 3 - Teststep 1 + 2      X
Canon 1 - Teststep 6 + 7        X
Canon 2 - Teststep 5            X
Canon 3 - Teststep 3 + 4        X
Canon 4 - Teststep 1 + 2        X
Canon 1 - Teststep 8              X
Canon 2 - Teststep 6 + 7          X
Canon 3 - Teststep 5              X
Canon 4 - Teststep 3 + 4          X
Canon 5 - Teststep 1 + 2          X
Canon 2 - Teststep 8                X
Canon 3 - Teststep 6 + 7            X
Canon 4 - Teststep 5                X
Canon 5 - Teststep 3 + 4            X
Canon 6 - Teststep 1 + 2            X
Canon 3 - Teststep 8                  X
Canon 4 - Teststep 6 + 7              X
Canon 5 - Teststep 5                  X
Canon 6 - Teststep 3 + 4              X
Canon 7 - Teststep 1 + 2              X
Canon 4 - Teststep 8                    X
Canon 5 - Teststep 6 + 7                X
Canon 6 - Teststep 5                    X
Canon 7 - Teststep 3 + 4                X
Canon 8 - Teststep 1 + 2                X
Canon 5 - Teststep 8                      X
Canon 6 - Teststep 6 + 7                  X
Canon 7 - Teststep 5                      X
Canon 8 - Teststep 3 + 4                  X
Canon 9 - Teststep 1 + 2                  X

========================  = = = = = = = = =

How it fits all together
------------------------

In ``baangt`` we have test case status ``paused`` for conditions of longer asynchronous waiting times. Each test case has
a unique identifier, that enables external callbacks or triggers to resume a certain test case after it was paused and
the precondition for continuation was met.

Prerequisites to run test canons in ``baangt``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* implement the triggers which will call ``baangt`` service "resumeTestCase" with the unique ID of a test case
* baangtDB (onsite, in the cloud or serverless)

