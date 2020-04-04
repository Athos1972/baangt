Agile: Where does ``baangt`` fit in?
====================================

``baangt`` supports all your agile mindset ever dreamed of - you can start right away with TDD, where you create Test-Cases before you
even write code (Just don't forget to set the test case version number to a future version).

Increment testing is the next logical consequence, where you'll use your test cases defined in the previous step to verify
results from the current sprint. Once run, optimized and stable you'll want to keep the system at least at this good state,
so you'll want to enrich your regression test set with those successful tests from your last sprint.

On the unrelated subject of negative test cases:

    Don't forget how important negative test cases are. Those are test cases, where you **need** the system to stop
    processing, because it is not supposed to accept a value or process or state. ``baangt`` makes this very simple for
    you! Define your parameters as with any other test case and set value of *TC Expected Error* to ``X``. That's it,
    ``baangt`` will be happy, when the testcase fails and raise an error, when the test case is successful.


In CDCT and Service tests (parts of the testing pyramid) you'll use the API functions of ``baangt`` to
ensure stable and proper outcome from your (micro-)services.

Finally in E2E-Testing ``baangt`` will help you to organize and keep track of your complex E2E-Scenarios where
you might start with mainframe or SAP-Systems to create master data, then change to WEB to use the created master
data in your frontend test cases and finally call some APIs to verify results in the backend systems were as expected.

We can do that with every software, what's so special about baangt?
-------------------------------------------------------------------

Thanks for asking. Well, you might be able to achieve that with expensive software like Tricentis Tosca or HP Runner, but
think again. How long does it take you to transfer information from business department via IT-Guys to the test automation
planners, experts, implementers and testers? Is the test case still relevant by then?

With ``baangt`` being free and open source and mostly depending on MS Excel you don't have expensive nor complex
client installation procedures. Everybody in your organization can record test cases and run them for validation
by themselves. You'll still want to keep your skilled guys in central test automation or central test management, but
how much faster will they be? How much better will your regression test rate be and how much more motivated will the whole
organization be, when things start to move faster than they're now (if you're still moving at all)?

Anything missing? Let us know! Interested? Go for it!
