Installation
============

There are various ways to install and use ``baangt`` depending on your requirements and setup.

Run the executables
-------------------

Installing the executables for your operating system (MacOS, Windows, Ubuntu) is simple. Head over to
https://github.com/Athos1972/baangt-executables select the archive for your operating system,
download to your local computer and unzip.

In the new folder you'll find ``baangt`` executable. Click on it and explore examples in ``/examples`` folder.

There's also a video on Youtube: https://www.youtube.com/watch?v=25wdwElMlH4 and an article with more background
information in the blog: https://www.baangt.org/4-ways-to-install-baangt-on-macos-windows-and-linux/

Install from sources
--------------------

Install sources from GIT (Please adjust to your virtual environment as per your preferences

::

    git clone https://gogs.earthsquad.global/athos/baangt
    cd baangt
    pip3 install -r requirements.txt
    python3 baangtIA.py

Docker
------
Install from GIT:

::

    git clone https://gogs.earthsquad.global/athos/baangt-Docker
    cd baangt-Docker
    make build
    make run

then use your preferred VNC-Client with ``vnc://localhost:5902``. Unless you changed the default password, the
password is ``password`` .

Install PIP-Package
------------------------
If you're planning to implement subclassing and you don't want to contribute to this open source project you can also
use the pip package:

::

    pip install baangt