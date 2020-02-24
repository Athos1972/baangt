Agile: Where does ``baangt`` fit in?
====================================

``baangt`` supports all you ever dreamed of - you can start right away with TDD, where you create Test-Cases before you
even write code (Just don't forget to set the test case version number to a future version).

Increment testing is the next logical consequence, where you'll use your test cases defined in the previous step to verify
results from the current sprint. Once run, optimized and stable you'll want to keep the system at least at this good state,
so you'll want to enrich your regression test set with those successful tests from your last sprint.

On the unrelated subject of negative test cases:

    Don't forget how important negative test cases are. Those are test cases, where you **need** the system to stop
    processing, because it is not supposed to accept a value or process or state. ``baangt`` makes this very simple for
    you! Define your parameters as with any other test case and set value of *TC Expected Error* to ``X``. That's it,
    ``baangt`` will be happy, when the testcase fails and raise an error, when the test case is successful.
