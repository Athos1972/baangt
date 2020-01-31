Why your production sucks and how to fix it
===========================================

Sounds familiar? When you sort your defects/incident list for the next sprint, you abandon priority concept (1, 2, 3)
and start experimenting with negative numbers? -1, -2 -3? Your sprint capacity is full before you even reach priority 0?

Each day/week when you're supposed to ship the most important hotfixes to production you suddenly beome religious and pray
intensively for 30 minutes? But the universe doesn't listen to you and 30 Minutes after deployment hell breaks loose
because you again bricked the production?

First of all: **Breathe!** Help is right here!

Changing your religion will not improve your situation (unless you go "all-in",
start as a full-time monk and leave software development forever.). **You are not alone**. I can't come up with trustworthy
numbers, but I'd guess that at any given second of the day at least 1000 people pray for good deployment results or are
at least worried about the current deployment (and the next. And the next.). It's
a phenomenon that we had already in the 1990s, just the impact back then was never as huge as it is today. There existed
manual fallback processes in all companies. Nobody "needed" the IT. If you had a bad deployment and needed to rollback and it
took one week to do so, it wasn't the end of the world, the company or you.

Today is different. Well, I'm pretty sure even if facebook is down for a week, the world would still turn. And facebook
facebook wouldn't cease to exist. I'm not so sure about a few 1000 people, who'd be responsible for the mess though.

Well, let's not focus on what could happen (and usually happens because Murphy's a very special friend to many people in
IT), but rather see, what we can do about it.

    We all know, that there's test automation, which should theoretically give us enough insight on lower stages before we move to Production.

Tricentis Tosca is the market leader and has been around for a few decades. So have the solutions from
HP and many others. As good as these tools are, in order to gain value from them you better follow certain processes, none of
which would be suitable for your business department or your developers. So both parties, who are in pain when deployments
don't work have a direct interface to the tool, that should help them. There are test-engineers, test-planners, test-designers,
test-executors and most probably repalled DevOps involved in the automation testing, but not the business department and not
the developers. That's critical from my point of view, because those processes build a barrier, that prohibits automation testing
to fulfill it's potential in todays organizations.

Enter: ``baangt``. Leightweight, fast, simple. Easy to use for business deparments, fast and flexible for developers (they
even get to play around with beloved JSON-Files) and mature enough for established Delivery organizations to fulfill their
needs of reporting and integration.

Before you try every sect on the planet give ``baangt`` a try. If set-up and used properly, this tool has a good chance
to make your life better and easier.

Great. You're still reading. Before you try to convince your manager about the tool, let's see some common resistance patterns
and how to overcome them.

.. list-table::

    * - Resistance
      - Assistance
    * - ``Sunken Costs``. We just renewed the license for <whatever>. I'll look like a fool when we've a better tool for free!
      - ``baangt`` can be integrated via API-Interface to all "professional" software. You don't need to kick out all your automation people. Get familiar with ``baangt`` and see, how you like it. Whenever your next renewal period for the license of the professional software comes up, you might even have an additional fact for reasoning
    * - ``Security Audit``. You know, how hard it is to convince people from internal IT department to deploy a new piece of software
      - ``baangt`` is open source and has little dependencies. ``baangt`` can be run in a Docker environment for execution, while testcase management happens in Excel. Shouldn't take them too long to approve ``baangt`` because they can review every aspect of the application
    * - ``not another tool``. We've already too much on our plate with the whole CD/CI-Stuff, K8s, Eclipse, IntelliJ and everything else!
      - Exactly. One more reason to bring around simple, reliable test results. How else will we ever know, whether the latest build will crash production or not?
    * - ``Test engineers can never be replaced by people from business department``.
      - If you give them a simple enough tool (how about an Excel sheet?) and the outlook to receive a more reliable production stage, you'd be amazed to what lengths those people from business department can go! Just give it a try - it doesn't cost anything.
