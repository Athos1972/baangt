Bugs in Production - what are they?
===================================

We all hate bugs in production. They're a pain for everybody. Devs, Management, Customers, Infrastructure. Given a
big enough scale many departments are effected by a single bug. That costs dearly and can be avoided in most cases.

In this article we'll look at real bugs, that managed to reach production and see, if proper testing could have avoided
these bugs.

#1 a lot of wrong shoes in wrong places
---------------------------------------

Task:
^^^^^
A new algorithm for a large shoe producer was built. The aim was to predict how many of which shoes will be sold in which
areas, deliver from the central warehouse to regional distribution centers, optimize loading of trucks to dispatch pallets
to local stores (e.g. load pallets for the last shop on the tour first into the truck).

The result:
^^^^^^^^^^^
Let's put it like this: Chaos. Not like "Chaos! We've a record in the database missing". No, more like "Chaos: Trucks all
over the place are carrying wrong shoes to the wrong stores. It will take months to sort this out". Chaos. Alone the cost
for the truck loads being brought back, repacked, reshipped would have paid 10 more testers, let alone missed sales.

What happened:
^^^^^^^^^^^^^^
The algorithm was developed based on old/incomplete data and old data structure. The testers worked on a small region
and only with one model of shoes, as creating all the test data manually was time consuming and given the short time, they tested, how it would work in 1 shop.
It worked well. In the algorithm itself only one ``clear`` was missing.

How this could have been prevented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
With intelligent test automation testers could have created more sample data in less time (e.g. record 1 shoe model,
then alter the parameters of the test case and automatically create a reasonable number of shoe models).

#2 A sudden wealth
------------------

Task:
^^^^^
Company A buys company B. A quick win to reduce costs and merge applications is to let invoicing and cash flows run on
Company A. 60k contracts. Monthly invoicing. What could go wrong?

The result:
^^^^^^^^^^^
First, there were more bounced direct debits as in other months. Well, X-Mas time, people overspent for presents. All good, right?
Well, no. A few days in after the "successful" first step of the merger, first level support showed an increased number of
calls, mostly furious people, who were charged 10 to 100 times their usual monthly fee - often via direct debit and that
during X-Mas time. If that's not a SUPER-GAU, then what is? News papers got tips and printed accordingly about the scandal,
when a multinational corporation robs from working class people who now don't have any means to by presents for their kids. Great!
"What could go wrong?" --> That!

What happened:
^^^^^^^^^^^^^^
One date field mapped wrongly in the interface between the invoicing application and the contract application. ``BEGINNDATE``
vs ``LASTPAYDATE``. The error was in there since the first test on final quality system. It was found and fixed in 10 minutes.

Test data was complex to be created and proper data from production couldn't be copied (lots of reasons, GDPR was not one of them).
Testers created contracts by themselves and created max backdated to beginning of the year. Then, in order to save the hussle of having to create too many new contracts manually,
they started invoicing on a monthly basis, different than the batch job setting in production, which would take all open
items and collect using the appropriate payment method.

How could this have been prevented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Test data was too complex to be created. Unrealistic manually created test data is the worst. It gives you false security when in reality you're totally blind.


#3 You don't pay - we tow your car!
-----------------------------------

Task:
^^^^^
In many million records of business partners find duplicates, move contracts from the duplicates to a main account,
flag duplicates for deletion.

    Simple, clean. In and out in 60 minutes.

The result:
^^^^^^^^^^^
Cars were towed and unregistered. Collection agents doing their jobs but at people who actually paid their bills.

What happened:
^^^^^^^^^^^^^^

All went well, the task was completed in record time, tested all combinations of possible partner data, all good. Wonderful!
But. The task and the tests were done on the system, that deals with business partners. With every duplicate found in the
partner system the contract system was informed about the new partner number, which replaces the old number on a specific
contract. In collection system the payment went to the new partner number. Unfortunately the unsettled amounts were also
cleared with the new number and the unsettled amount on the old partner number remained open forever. Thanks to the automatic
dunning process including escalation cars were towed - as according to the system - these folks didn't pay their bills.

How could this have been prevented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Honestly, that's a tough one, even if you have great test coverage and full scope E2E-Tests in place. Which normal company
would go to the length of creating bank payment interface to see, that the unsettled amount wasn't cleared? Of course, a
senior solution architect could have foreseen this outcome.

#4 Material master records - what are they for anyway?
------------------------------------------------------

Task:
^^^^^
A table on Oracle SQL exploded because customer added too many fields into the table. Whatever. Other tables had also
reached similar sizes, so transform those fields into key/value-pairs and store in a separate table with reference to the
other tables. 10 tables, a few million records, easy going. 4 hours tops. A little testing on FQA, then run over the weekend
in production.

The outcome:
^^^^^^^^^^^^

Material master records are pretty important for a production company. Not as important as customers, but pretty important.
After this job, they didn't have any (while 1000s of interface records from suppliers and customers were coming in). The fix
was provided within a few hours from a coincidentally setup parallel system, but this could have gone very bad.

What happened:
^^^^^^^^^^^^^^

Functionality was tested. Functionality worked fine (new table was filled with data and displayed and linked properly). Clearing
of the data fields also worked perfectly, but was a bit overmotivated. Everything except the key field was cleared. One
code line changed and it worked. There were practically no tests - because "What could go wrong on such a quick fix?".

How could this have been prevented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Even the simplest functional test would have immediately thrown an error. All Unit-Tests were OK and for this customer
there are (were) no functional tests.

# What are these chemical elements anyway?
------------------------------------------

Task:
^^^^^
Upgrade a mass spectrometer to latest firmware. Come ooon, that's a job for a junior!

The outcome:
^^^^^^^^^^^^

Just a few 100k bugs of wrongly melted raw material. Nobody harmed, no outside consequences (by chance only!).

What happened:
^^^^^^^^^^^^^^

Before the update, the spectrometer had fixed decimal places in a number. After the update, decimal places were floating.
The interface with the material robot, who'd add missing raw material into a boiling soup of metal based on the chemical analysis, was used to fixed decimal
places and thus went wild on adding different components to compensate for each result of the mass spectrometer. Luckily
after 30 hours of boiling the shift supervisor understood that something is wrong

How could this have been prevented:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First it looks like it's an easy one, but it's not. A pure technical test would have not found that problem. If one would mock
away the spectrometer in the first place, it would also not show up. The only way to find that, would have been to
test the output of the spectrometer with a reference material against the output after the update. But that's nothing,
that can be automated.

Summary
-------

Most of the severe bugs described here could have been found easily, others not so easy. In any case, every bug that
was found on lower stages and never reaches production is much cheaper for the whole organization, so get ready to use
``baangt`` to increase test coverage and subsequently overall quality!