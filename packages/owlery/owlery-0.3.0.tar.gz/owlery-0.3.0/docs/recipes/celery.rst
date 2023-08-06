Celery
======

`Celery <http://celeryproject.org/>`


Sending messages asynchronously
-------------------------------

.. code-block:: python

    from .celery import app

    @app.task
    def send(**kwargs):
        return manager.send(**kwargs)


.. code-block:: python

    result = send.s(
        to=["someone@example.com"],
        subject="Test message",
        body="This is a test message.",
    )


Scheduling receiving of messages
--------------------------------

.. code-block:: python

    from .celery import app

    @app.task
    def receive(limit=100):
        return manager.receive(limit=limit)

    @app.on_after_configure.connect
    def setup_periodic_task(sender, **kwargs):
        sender.add_periodic_task(
            300.0, receive.s(limit=100), name='receive messages'
        )
