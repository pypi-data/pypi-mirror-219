RelayMe
=======

0.0.6
-----

This module is geared towards emailing using email relay services.

Prerequisites
-------------

First, to install RelayMe, open your command prompt and run the following command:

.. code-block:: shell

   pip install RelayMe

Second, this module requires a `SenderConfig` instance to be created in your code, which can be passed into the function that sends emails.

The `SenderConfig` instance needs a config file key to be passed in, which should contain the following keys:

- `server`
- `port`
- `sender`
- `username`
- `password`
- `subject`
- `header`
- `footer`

(Case doesn't matter, but spelling is important. The keys could also be named 'Server', 'PORT', 'UserName', etc.)

(The order doesn't matter either. The keys can be in any order you like.)

(Also the 'username' and 'password' keys are optional if your relay service doesn't require a user name and pass word to authenticate.)

Here is an example config key:

.. code-block:: python

   'EmailConfig': {
       'server': 'smtp.example.com',
       'port': 123,
       'sender': 'sender@example.com',
       'username': 'username',
       'password': 'password',
       'subject": "Hello from the SenderConfig module!",
       'header": "This is the header",
       'footer': "This is the footer"
   }

Usage
-----

Here's an example of how to use this module in your code:

.. code-block:: python

   from RelayMe import SenderConfig

   sender = SenderConfig(config["EmailConfig"])

   body = "This is the body of the email."
   recipient = "John.Doe@mail.com"  # (or it can come from a config file where you could list multiple emails)

   sender.send_email(body, recipient)
