Redis Queue
===========

`Redis Queue <https://pypi.org/project/rq/>`


Sending messages asynchronously
-------------------------------

.. code-block:: python

    from redis import Redis
    from rq import Queue

    queue = Queue(connection=Redis())

    result = q.enqueue(
        email.send,
        to=["someone@example.com"],
        subject="Test message",
        body="This is a test message.",
    )


Scheduling receiving of messages
--------------------------------

`RQ Scheduler <https://pypi.org/project/rq-scheduler/>`


.. code-block:: python

    import datetime as dt

    from redis import Redis
    from rq_scheduler import Scheduler

    scheduler = Scheduler(connection=Redis())

    scheduler.schedule(
        scheduled_time=dt.datetime.utcnow(),
        func=email.receive,
        kwargs={"limit": 100},
        interval=300,
        repeat=0,
    )
