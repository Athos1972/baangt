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
5. Confluence

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

Once we have all the necessary things we just need to add them in ``mail.ini`` which must be inside ``ini`` folder.
If you have used windows installer to setup ``baangt`` then it must be inside `C:/Users/{username}/baangt` directory,
else it will be in the root directory of baangt. Once you find the ``ini`` folder their must be a main.ini file inside
it. If it is not their you can make one. Just create a new file name `mail` and extension `ini` which will look like
``mail.ini``. Then you can edit it via any text editor. It should look like.


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

Override mail.ini
=================

There are some cases when we don't want to send reports either in few or in all services. Now to overcome this what we
can do is that we can add the settings directly in globals file. Our program will always first check for settings in
globals file, if it is not their then it will take settings from ``mail.ini``. Here is an example

| **mail.ini**
| [Default]
| sendmailto = example1@gmail.com
| notificationwithattachment = <True or False>
| mswebhook = <MsTeam channel webhook url>
| slackwebhook = <Slack App webhook url>
| telegrambot = <telegram bot access token>
| telegramchannel = <telegram channel name>

| **globals.json**
| {
|     "TC.dontCloseBrowser": "False",
|     "TC.NetworkInfo": "False",
|     "TC.Browser": "Chrome",
|     "TC.BrowserWindowSize": "1024x768",
|     "Stage": "Test",
|     "SendMailTo": "example2@gmail.com, example3@gmail.com",
|     "NotificationWithAttachment": "False",
|     "MsWebHook": "",
|     "SlackWebHook": "",
| }

Now as we can see the we have override Mail, Ms Teams & Slack settings. So now our program will take mails from globals
and as the ``NotificationWithAttachment`` parameter is False it won't attach the xlsx file. ``MsWebHook`` & ``SlackWebHook``
are empty so no report will be sent on those platforms. Here we haven't declared any setting for **Telegram** so the
program will now look for those settings in ``mail.ini`` and send the report as per that settings.

Confluence
==========
We also have functionality to update report in confluence. Reports are updated as page. Along with it we can also attach
original report(.xlsx) file in main page. Main page can consist link to original file, data from "Summary" tab & data
from "Output" tab. Their might also be cases when "Output" tab has too many datas, so we have solution for that too. We
have given you an option to create subpages of data from "Output" tab. You can use this functionality with the help of
global files. Lets see the keywords needed for global file in order to update the report in confluence.

| **globals.json**
| {
|    "Confluence-Base-Url" : "",
|    "Confluence-Space" : "",
|    "Confluence-Username" : "",
|    "Confluence-Password" : "",
|    "Confluence-Rootpage" : "",
|    "Confluence-Pagetitle" : "",
|    "Confluence-Remove_Headers" : "",
|    "Confluence-Uploadoriginalfile" : "",
|    "Confluence-Createsubpagesforeachxxentries" : 0
| }

**Confluence-Base-Url**

``Confluence-Base-Url`` contains the url for your confluence.

**Confluence-Space**

``Confluence-Space`` contains the name of space where page
is to be created.

**Confluence-Username**

``Confluence-Username`` contains your username.

**Confluence-Password**

``Confluence-Password`` contains your password.

**Confluence-Rootpage**

``Confluence-Rootpage`` contains parent page id, this option is optional and in most of the case is not usable, you must
use this option if you want to create the report page as a sub-page to another main page.

**Confluence-Pagetitle**

``Confluence-Pagetitle`` title for the report page.

**Confluence-Remove_Headers**

``Confluence-Remove_Headers`` contains headers from "Output" tab which are not to be considered
while generating report page. Multiple headers should be sperated by comma, e.g. - "header1, header2, header3".

**Confluence-Uploadoriginalfile**

``Confluence-Uploadoriginalfile`` value must be true if you want to upload original xlsx file in main report page.

**Confluence-Createsubpagesforeachxxentries**

``Confluence-Createsubpagesforeachxxentries`` contain integer, when we want to create sub-pages for "Output" tab data
we should input the number of rows present in a subpage, multiple sub-pages are created with the number of rows which
are defined here. e.g. - "Confluence-Createsubpagesforeachxxentries" : 100, here we have given input of maximum 100 data
in a sub-page and suppose if total number of data is 288, then their will be 3 pages containing 1-100, 101-200, 201-288
data.