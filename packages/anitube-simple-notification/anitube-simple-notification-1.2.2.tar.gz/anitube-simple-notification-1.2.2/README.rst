Anitube Simple Notification
===========================

Anitube Simple Notification is a application made for getting
notification when a content is updated on the web-site (anitube.in.ua).

Usage
=====

In application folder create file with name ``config.toml``. If a value
is wrong, then a error will be shown. If there no value or a wrong value
then it will be default.

Example of a config file for all options:

.. code:: toml

   POSTERS = true
   WAITING_PERIOD = 3600
   URLS = [
     "https://anitube.in.ua/4110-chainsaw-man.html",
     "https://anitube.in.ua/4010-overlord-iv.html",
     "https://anitube.in.ua/4097-mob-varyat-100-3-sezon.html",
     "https://anitube.in.ua/4087-spy-x-family-part-2.html",
   ]

The last comma of the urls list can be ommited.

Run the program by one of the commands:

.. code:: shell

   python3 main.py
   python main.py

Author
======

Kostiantyn Klochko (c) 2022-2023

Donation
========

Monero:
8BCZr3LaciDZUwNUbC8M5gNZTtnPKoT9cMH95YcBoo2k8sg4qaxejYL4Qvp6V21ViqMHj5sHLiuRwhMYxHTVW1HUNAawV6c
|image1|

License
=======

Under GNU GPL v3 license

.. |image1| image:: ./img/monero.png
