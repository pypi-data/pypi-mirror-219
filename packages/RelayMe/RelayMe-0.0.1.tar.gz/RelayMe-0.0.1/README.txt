RelayMe
=======

This module is geared towards emailing using email relay services like Breve.

Prerequisites
-------------

This module requires an `EmailSender` instance to be created, which can be passed into the function that sends emails.

The `EmailSender` instance needs a config file key passed in, which should contain the following keys:

- `server`
- `port`
- `sender`
- `username`
- `password`

Here is an example config key:

.. code-block:: python

   'email_sender': {
       'server': 'smtp.example.com',
       'port': 123,
       'sender': 'sender@example.com',
       'username': 'username',
       'password': 'password'
   }

Usage
-----

Here's an example of how to use this module in your code:

.. code-block:: python

   from RelayMe import EmailSender

   sender = EmailSender(config['email_sender'])
   subject = "Hello from the EmailSender module!"
   body = "This is the body of the email."
   recipient = "Jhon.Doe@mail.com"  # (or it can come from a config file where you could list multiple emails)

   sender.send_email(subject, body, recipient)
