"""
Create custom streamz sinks.

Classes:

    to_pulsar
"""
import pulsar
from streamz import Stream, Sink
from streamz_pulsar.base import PulsarNode


@Stream.register_api()
class to_pulsar(PulsarNode, Sink):  # pylint: disable=C0103
    """ Writes data in the stream to Pulsar

    This stream accepts a string or bytes object. Call ``flush`` to ensure all
    messages are pushed. Responses from Pulsar are pushed downstream.

    Parameters
    ----------
    topic : string
        The topic which to write
    producer_config : dict
        Settings to set up the stream, see
        https://pulsar.apache.org/api/python/3.2.x/pulsar.Client.html
        Examples:
        service_url: The Pulsar service url eg: pulsar://my-broker.com:6650/

    Examples
    --------
    >>> from streamz import Stream
    >>> source = Stream()
    >>> producer_ = source.to_pulsar(
    ...     'pulsar://localhost:6650'
    ...     'my-topic'
    ...     )  # doctest: +SKIP
    >>> for i in range(3):
    ...     source.emit(('hello-pulsar-%d' % i).encode('utf-8'))
    """
    def __init__(
            self,
            upstream,
            service_url,
            topic,
            producer_config={},
            **kwargs):

        self.topic = topic
        self.client = pulsar.Client(service_url)
        self.producer = self.client.create_producer(
            self.topic, **producer_config)

        kwargs["ensure_io_loop"] = True
        super().__init__(upstream, **kwargs)
        self.stopped = False
        self.polltime = 0.2
        self.futures = []

    def update(self, x, who=None, metadata=None):
        self.producer.send(x)

    def flush(self):
        self.producer.flush()
