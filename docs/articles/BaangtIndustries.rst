``baangt`` In Industries
=========================

``baangt`` is versatile and useful for producers and consumers of software from all walks of life. Some industries though
have specific needs, that are especially well addressed by ``baangt`` out of the box.

``baangt`` in Banking
---------------------

Banks often have large system landscapes, diversified customers and products. It often looks like each individual
customer has it's own set of parameters and business processes within the bank`s organization. KYC-Initiatives,
PEP/FATCA compliance and a lot of regulatory demands must be fulfilled. On the other hand apps and online banking bring
direct communications with end customers. It's nearly impossible to test all processes in all combinations before a new
increment is released to production.

This huge complexity and vast amounts of test cases make it an ideal environment for ``baangt`` to shine! Closer
collaboration between IT-Departments and business people helps to avoid misunderstandings and find different interpretations
of requirements early in the process - and long before reaching production systems.

Creating test cases in simple Excel sheets and communicating based on those expected results will streamline test
processes and support project organizations to deliver better results in shorter time.

Insurance and ``baangt``
------------------------

Insurance is like banking on steroids - at least when it comes to complexity of the products, processes and system
landscapes. Due to the variety of products (Life, P&C, Health, Car/Automotive) and the completely different processes
for each of the product lines testing in insurance companies is complex and challenging. As in many other industries
trends of recent years like off-shoring, near-shoring and outsourcing lead to less understanding of the business needs
by service providers but also to less understanding of the underlying complexity when service providers extend or change
existing code bases, which makes testing even more important as side-effects are more likely than back in the days when
the internal IT people of the company knew exactly what they were dealing with.

Business departments especially during the last 5 years, but also for the next 5-10 years face challenges due to
overaged work force. Companies manage to bring in young talents to take over the responsibility of insurance
products development and maintenance of existing product landscape. At the same time they are competing on a global market,
operating inside a strictly defined legal range of options, need to cut costs and innovate products to fit modern customer
needs.

In this challenging, complex environment ``baangt`` helps by providing a simple yet powerful option for business
experts to define, maintain and run their test cases. This option eliminates prolonged misunderstandings between
IT-People and business department, increasing velocity for both sides and at the same time improves overall system
stability, reduces TCO (Total Cost of Ownership) and enables organizations to have faster time to market - a parameter
very important in todays dynamic insurance landscape.

Production with ``baangt``
--------------------------

Now we're talking about companies, who use machinery of all kind and production optimization flows to produce high quality
goods at competitive prices. The more flexible your machinery and the more steps a production cycle includes between
customer order and paid invoice, the greater the need for ``baangt``, assuming that as many steps as possible are
automated.

While in banking and insurance it's very common to have complete copies of system landscapes for development, migration
and test, this rarely is the case in production companies - given that the various robots and machinery are usually
running in shifts 24/7. Common approaches for those companies to update their landscape are planned downtimes (e.g.
"Easter-" or "Christmas break") when they stop production, upgrade all parts/software as planned and then slowly restart.

Other production companies take down "lines" (a more or less logical group of machines, that perform a sequence of work),
often only for a few hours for upgrade processes. The secret to successful testing strategies in such environments is to
mock.

    **Mocking** is a technique in test automation, where we replace actual interfaces with synthetic data.

When we plan a large scale system upgrade we also test in variations of what might happen. E.g. the upgrade on Unit 6
will brick the engine, so we'll have to reset Unit 6 to it's previous conditon, while the rest of the plant is upgraded
as originally planned. Will this work? If you have to guess whether this (not so uncommon) set-back will jeopardize the
whole upgrade of a plant and cause additional unplanned 2 weeks downtime, Millions of losses for the company, workers
who can't earn money for their families, etc. and **you** are in charge, then you didn't do a great job. With ``baangt``
you'd have used old and new mocks or stubs of those interfaces. Depending on the test results, you'd either have informed
management about the elevated risk when the upgrade of Unit 6 goes wrong, or you'd be very relaxed because instead of
guessing and hoping, you'd **know**, how the failed upgraded will influence the overall upgrade of the plant.

Key takeaway
------------
``baangt`` is no silver bullet, nor does it do the work for you. Using ``baangt`` may actually cause more work on the
short run, in case you didn't automate any critical processes so far.

The more variables in your business processes and/or products, the more you should have a look at ``baangt``.







