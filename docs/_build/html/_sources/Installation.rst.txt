Installation
============

There are various ways to install and use ``baangt`` depending on your requirements and setup.

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
    Make build
    Make run

then use your preferred VNC-Client with ``vnc://localhost:5902``. Unless you changed the default password, the
password is ``password`` .

Install PIP-Package
------------------------
If you're planning to implement subclassing you can also use the pip package:

::

    pip install baangt