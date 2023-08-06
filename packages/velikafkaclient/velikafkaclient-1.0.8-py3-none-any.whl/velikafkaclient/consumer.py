import json

from aiokafka import AIOKafkaConsumer

from .eventregistration import kafka_topic_events
from .exceptions import InvalidEventTopicException, InvalidEventStructure
from .killer import KafkaClientGracefulKiller


class AsyncKafkaConsumer:

    def __init__(self, bootstrap_servers, group_id=None):
        self.kafka_topic_events = kafka_topic_events
        self.client = None
        self.bootstrap_servers = bootstrap_servers
        self.group_id = group_id
        self.subscriptions = dict()
        self.topics = set()
        self.killer = KafkaClientGracefulKiller(self)

    async def start(self):
        if self.client is not None:
            raise Exception("Consumer already started, stop before starting again <3")
        self.client = AIOKafkaConsumer(
            *list(self.topics),
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id
        )
        await self.client.start()

    async def stop(self):
        if self.client is None:
            raise Exception("Consumer is not started, start before stopping <3")
        await self.client.stop()
        self.client = None

    def subscribe(self, topic, handler):
        self.subscriptions[topic.value] = handler
        self.topics.add(topic.value)

    async def consume(self):
        async for msg in self.client:
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.value)
            if msg.topic not in self.kafka_topic_events.topic_event_models:
                raise InvalidEventTopicException(f"Topic {msg.topic} not found")
            topic_event_model = self.kafka_topic_events.topic_event_models[msg.topic]
            try:
                decoded_msg = msg.value.decode('utf-8')
                data = json.loads(decoded_msg)
                msg_event = topic_event_model(**data)
                handler = await self.subscriptions[msg.topic](msg_event)
                print(handler)
            except Exception as e:
                # TODO add proper exception handling
                raise InvalidEventStructure(f"Invalid event structure {str(msg.value)} for topic {msg.topic}")
