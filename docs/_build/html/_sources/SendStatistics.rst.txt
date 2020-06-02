**************
SendStatistics
**************

While running tests on ``baangt`` we might need to share the report to multiple persons in a team. To do this one might
have to be present in front of screen and wait for completion of the test. But to overcome this issue we have added a
functionality in ``baangt`` to send the reports in various platform automatically, thus you don't need to waste your
time in front of screen just for waiting of completion, our program will take care of that.

Their are 4 different services where we can send test reports. They are:

1. Email
2. Ms Teams
3. Slack
4. Telegram

Lets first discuss things we need to use this services in our program one by one.

**Note :- If you don't need to use any service from the following you just skip that part**

Email
=====

We don't need anything(except recipients email ids).

Ms Teams
========

We need webhook url of Ms Teams channel where we need to send reports. If you need any help in getting webhook url you can
refer to this link:- https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/connectors-using#setting-up-a-custom-incoming-webhook

Slack
=====

We need incoming webhook url for the app which has permission to post message in your group. For further assistance you
can refer to "`Set up Incoming Webhooks`" section of https://slack.com/intl/en-in/help/articles/115005265063-Incoming-webhooks-for-Slack

Telegram
========

To send message in telegram channel we need channel username and a bot's HTTP API token who has administrator privilage
in your channel.

First, to get username of the channel you can simply go to info section of your channel where you will find invite link
which will look like `t.me/your_channel_username` here your_channel_username is what we need.

Now to get HTTP API token of bot, first we need to create a bot. To create a new bot you need to search for `@botfather` in
telegram. If you are first time user of BotFather then you will see an introduction and a start button in the bottom. If
you don't see start button but seeing a text area in bottom you can just type ``/start`` then to create a new bot you
have to select or type ``/newbot`` after that it will ask a name for your bot. You can name it anything but I for best
practice we will use `ChannelName bot` after that it will ask a username for your bot which must be unique and the
username must end with `bot` word so we can use `ChannelName_bot` after sending this you should get a congratulations
message which means your bot is created. In this congratulation message you will get `HTTP API access token` we will
need this further in our program.

Our next step is to add the bot in our channel as administrator. Please visit this link for further assistance :-
https://stackoverflow.com/a/33497769/8784795

Configuring Baangt
==================

Once we have all the necessary things we just need to add them in ``main.ini`` which must be inside ``ini`` folder.
If you have used windows installer to setup ``baangt`` then it must be inside `C:/Users/{username}/baangt` directory,
else it will be in the root directory of baangt. Once you find the ``ini`` folder their must be a main.ini file inside
it. If it is not their you can make one. Just create a new file name `main` and extension `ini` which will look like
``main.ini``. Then you can edit it via any text editor. It should look like.


| [Default]
| sendmailto = <email>
| notificationwithattachment = <True or False>
| mswebhook = <MsTeam channel webhook url>
| slackwebhook = <Slack App webhook url>
| telegrambot = <telegram bot access token>
| telegramchannel = <telegram channel name>

Configurations of mail:- ``sendmailto`` and ``notificationwithattachment`` are the settings for email. ``sendmailto``
can contain single recipients or multiple recipients which would look like.
**sendmailto = example1@xyz.com, example2@xyz.com, example3@xyz.com** inshort they should be comma seperated.
**notificationwithattachment** should be True if you want to send xlsx result file as attachment in the mail else it
should be False.

Configuration of MsTeam:- ``mswebhook`` takes single or multiple(comma seperated as above) webhook url and will send
report in them.

Configuration of Slack:- ``slackwebhook`` takes single or multiple(comma seperated as above) webhook url and will send
report in them.

Configurations of Telegram:- ``telegrambot`` and ``telegramchannel`` are the settings for telegram. ``telegrambot`` will
take single value containing API token of bot. ``telegramchannel`` may contain single or multiple(comma seperated as
above) username of channels. Make sure that all the channels have this bot as administrator.

**Note:- If you don't need to use any of the service out of these four, you can just leave their settings empty**