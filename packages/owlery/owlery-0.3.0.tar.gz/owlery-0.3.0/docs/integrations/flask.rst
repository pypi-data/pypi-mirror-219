.. currentmodule:: owlery.integrations.flask

Flask
=====

Integrate messaging in your Flask application and configure messaging managers and services based on your Flask
:doc:`configuration handling <flask:config>`.


Configuration
-------------

=============== ===============================================================
Key             Description
=============== ===============================================================
OWLERY_SUPPRESS Suppress sending of messages, defaults to ``app.testing``.
=============== ===============================================================


To configure each service on each manager, the extension expects one of more configuration keys of the form:

``OWLERY_{MANAGER}_{SERVICE}_{KEY}``


where ``MANAGER`` is the uppercase form of the ``name`` passed to the manager in the
:meth:`init_manager <Owlery.init_manager>` method and ``SERVICE`` would be the uppercase form of the ``name`` passed to
the service in the :meth:`register <owlery.services.ServiceManager.register>` or if no name is passed, ``DEFAULT``.


The following configuration key is required:

``OWLERY_{MANAGER}_{SERVICE}_CLS``


An example configuration:

.. code-block:: python

    OWLERY_EMAIL_DEFAULT_CLS = "owlery.services.email.smtp.SMTP"
    OWLERY_EMAIL_DEFAULT_HOST = "localhost"
    OWLERY_EMAIL_DEFAULT_PORT = 25


Once you configure the extension and manager, for example:

.. code-block:: python

    from owlery.integrations.flask import Owlery
    from owlery.services.email import EmailManager

    from .app import app

    owlery = Owlery(app)

    email = owlery.init_manager(EmailManager, name="email")


The previous configuration will result in roughly the following:

.. code-block:: python

    from owlery.services.email.smtp import SMTP

    email.register(SMTP, host="localhost", port=25)


Initializing the extension
--------------------------

To initialize the integration, instantiate the :class:`Owlery` class and pass the ``app`` instance:

.. autoclass:: Owlery


or you can use the :doc:`application factory pattern <flask:patterns/appfactories>` and
:meth:`init_app <Owlery.init_app>`:

.. automethod:: Owlery.init_app


.. code-block:: python

    owlery = Owlery()

    # ... later in your application factory function after configuration

    owlery.init_app(app)


Initialize service manager
--------------------------

To initialize a :doc:`service-manager` we use the :meth:`init_manager <Owlery.init_manager>` instead, this will
initialize the manager and configure the services based on the application configuration.

.. automethod:: Owlery.init_manager


Register media helper
---------------------

Some services require an external URL to send attachments and media, you can register an endpoint to expose these
attachments using your Flask application:

.. automethod:: Owlery.register_media_url


WhiteNoise
~~~~~~~~~~

If you are using the `WhiteNoise <https://github.com/evansd/whitenoise>`_ library to serve your static files, you can
also serve your media attachments. After configuring WhiteNoise you can call the
:meth:`configure_whitenoise <Owlery.configure_whitenoise>` method:

.. automethod:: owlery.integrations.flask.Owlery.configure_whitenoise


Register webhooks
-----------------

Your services may use webhooks to receive messages and status callbacks, you can register all these endpoints on your
Flask application or :class:`Blueprint <flask.Blueprint>`:

.. automethod:: Owlery.register_webhooks


API Reference
-------------

.. autoclass:: owlery.integrations.flask.Owlery
    :members:
    :noindex:
