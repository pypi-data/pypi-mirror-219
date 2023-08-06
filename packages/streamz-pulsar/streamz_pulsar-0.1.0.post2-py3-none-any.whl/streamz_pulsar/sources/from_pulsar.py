"""
Create custom streamz sources.

Classes:

    from_pulsar
"""
import weakref

import pulsar
from streamz import Stream, Source
from tornado import gen


@Stream.register_api(staticmethod)
class from_pulsar(Source):  # pylint: disable=C0103
    """ Accepts messages from Pulsar

    Uses the pulsar library,
    https://pulsar.apache.org/docs/next/client-libraries-python/


    Parameters
    ----------
    topics: list of str
        Labels of Pulsar topics to consume from
    subscription_name: string
        The name of the subscription
    consumer_params: dict
        Settings to set up the stream, see
        https://pulsar.apache.org/api/python/3.2.x/pulsar.Client.html
        Examples:
        service_url: The Pulsar service url eg: pulsar://my-broker.com:6650/;
        group.id, Identity of the consumer. If multiple sources share the same
        group, each message will be passed to only one of them.
    poll_interval: number
        Seconds that elapse between polling Pulsar for new messages

    Examples
    --------
    >>> import pulsar
    >>> from streamz import Stream
    >>> s = Stream.from_pulsar(
    ...     ['my-topic'],
    ...     subscription_name='my-sub',
    ...     consumer_params={'service_url': 'pulsar://localhost:6650'}
    ...     )
    >>> decoder = s.map(lambda x: x.decode())
    >>> L = decoder.sink_to_list()
    """
    def __init__(
            self,
            topics,
            subscription_name,
            consumer_params,
            poll_interval=0.1,
            **kwargs):
        self.cpars = consumer_params
        self.subscription_name = subscription_name
        self.consumer = None
        self.topics = topics
        self.poll_interval = poll_interval
        super().__init__(**kwargs)

    def do_poll(self):
        if self.consumer is not None:
            try:
                msg = self.consumer.receive(0)
                self.consumer.acknowledge(msg)
            except pulsar._pulsar.Timeout:
                msg = None
            if msg and msg.value():
                return msg.value()

    @gen.coroutine
    def poll_pulsar(self):
        while True:
            val = self.do_poll()
            if val:
                yield self._emit(val)
            else:
                yield gen.sleep(self.poll_interval)
            if self.stopped:
                break
        self._close_consumer()

    def start(self):
        if self.stopped:
            self.stopped = False
            self.client = pulsar.Client(**self.cpars)
            self.consumer = self.client.subscribe(
                self.topics, self.subscription_name)
            weakref.finalize(
                self, lambda consumer=self.consumer: _close_consumer(consumer)
            )
            self.loop.add_callback(self.poll_pulsar)

    def _close_consumer(self):
        if self.consumer is not None:
            consumer = self.consumer
            self.consumer = None
            consumer.unsubscribe()
            consumer._client.close()
        self.stopped = True


def _close_consumer(consumer):
    try:
        consumer.close()
    except RuntimeError:
        pass
