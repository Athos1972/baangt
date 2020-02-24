Stop testing software...
========================

... only. Also and foremost test business functionality. In today's semi-agile and agile environments we fortunately improved testing
in all stages of the development process. Nobody would dream to deliver software without unit-tests, service tests and
consumer driven contract testing is hip and most companies even have (more or less) End-2-End (E2E) tests. Nevertheless
we still see loads of bugs once the software reaches production.

These bugs slow us down. They cost millions of hours every day, that could be spent on more productive things. A bug,
that is found in production is much more harmful to an organization than a bug found (ideally) in DEV-Environment or
in QA/Final QA-Stages. I'm not talking about the reputation of the organization - that's a different story alltogether. No,
I'm talking about the fixing cost.

Chances are, the bug was created longer than 3 months ago. Maybe the developer isn't here anymore, even if he is, he won't
know the faulty code by heart, meaning he'll have to spend some time figuring out, what's wrong. These switching costs are
one of the main effort drivers for bug fixing costs.

Secondly - a production bug needs to be treated with priority. The assigned Developer will stash his current work, checkout
production code, reconfigure Dev-Environment. Depending on the IDE and the overall complexity, this might take only
a few minutes, but it adds to the overall costs.

Another important factor, that can cost days, weeks or months of additional effort is when fixing the bug needs
migrations for instance in already posted data. Separate functionalities need to be written to identify the effected
records, determine the correct values, the wrong value and decide, how to cope with the delta between those two. Such
situations can get messy and you wish you had chosen another career path, when in the middle of this.

How to improve the situation
----------------------------

Even when you have simple and easy to solve bugs from production, they still cost you more than when you had found them
in earlier stages. And there's still this reputation thing with your users or customers.

To improve the situation you'll definitely want to use realistic test data, if possible cases from production for your
regression tests and in most cases also for your progression tests. You'll also move your focus from technichal aspects
of testing to pure business functionality. You'll create many realistic test data combinations and let them run.

We once searched for quite some time for performance optimization possibilities until we found out, that the test case
itself was flawed. It produced a demand situation for a specific material that would never happen in a productive
system, because all the customer order tests were mainly ordering this one material number, when in reality the customer
had 10.000s of materials. Don't be like our past. Be better.

Realistic testdata combinations might also mean, that you have to create multiple sets of realistic master data for your
test cases. Sometimes that's hard, because masterdata might be maintained on a remote master system and you might not
have access to that. But it's so worth the trouble in the long run.

FK The gold is on the street
----------------------------

Once you're in production your bug tickets are an invaluable source of wisdom, on how to improve testing. Majority of the
tickets will hopefully be about user errors, wrong passwords, unknown "Works as designed"-Situations, and things like that.

The remaining tickets are the gold. Dig them up (usually we'd have a JIRA-Filter and a classification in the defects),
look what came in since your last release and once fixed, analyse, how you can adjust your test set in order to avoid the
current and similar error situations. Look deep into the root cause of why this defect or error wasn't discovered before.
Once you're clear on the reasons (multiple reasons are very common, once you have a mature test set) add test data
combinations, that will detect those problems upfront.

If you follow this procedure I guarantee, that in 1-4 months you'll see a sharp decline in production defects as
day by day and week by week you'll catch more problems in previous stages and your production will become rock-stable.

