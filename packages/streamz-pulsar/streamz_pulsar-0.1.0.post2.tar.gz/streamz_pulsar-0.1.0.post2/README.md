# Pulsar plugin for Streamz

This a plugin for [Streamz](https://github.com/python-streamz/streamz) that adds stream
nodes for writing and reading data from/to Pulsar.

## 🛠 Installation

Latest stable version is available on PyPI

```sh
pip install streamz_pulsar
```

Latest development version can be installed from git repo

```sh
pip install git+https://github.com/MarekWadinger/streamz_pulsar
```

## ⚡️ Quickstart

To start working with streamz_pulsar, follow these 3 steps:

### 1. Run a standalone Pulsar cluster locally

```sh
docker run -it -p 6650:6650 -p 8000:8080 --mount source=pulsardata,target=/pulsar/data --mount source=pulsarconf,target=/pulsar/conf apachepulsar/pulsar:latest bin/pulsar standalone
```

### 2. Create a consumer

The following example creates a consumer with the `my-sub` subscription name on the `my-topic` topic, receives incoming messages, prints the content and ID of messages that arrive, and acknowledges each message to the Pulsar broker.

```python
import pulsar
from streamz import Stream

s = Stream.from_pulsar(
    ['my-topic'],
    subscription_name='my-sub',
    consumer_params={'service_url': 'pulsar://localhost:6650'}
    )

s.map(lambda x: x.decode())
L = s.sink_to_list()

s.start()
while True:
    try:
        if L:
            print(L.pop(0))
    except pulsar.Interrupted:
        print("Stop receiving messages")
        break
```

### 3. Create a producer

The following example creates a Python producer for the `my-topic` topic and sends 10 messages on that topic:

```python
from streamz import Stream

source = Stream()
producer_ = source.to_pulsar(
    'my-topic',
    producer_config={'service_url': 'pulsar://localhost:6650'}
    )

for i in range(3):
    source.emit(('hello-pulsar-%d' % i).encode('utf-8'))

producer_.stop()
producer_.flush()

```
