from streamz import Stream


class PulsarNode(Stream):
    """Base class for Pulsar stream nodes.

    Parameters
    ----------

    client_params: dict
        Will be passed to ``pulsar-py`` client instance. Defaults to None.
    """

    def __init__(self, *args, subscription_name: str = None, **kwargs):
        self._params = subscription_name
        super().__init__(*args, **kwargs)
