import json
from kafka import KafkaProducer, KafkaConsumer

from getajob.vendor.kafka.models import KafkaTopic, BaseKafkaMessage
from getajob.config.settings import SETTINGS

from .client_factory import KafkaProducerFactory, KafkaConsumerFactory
from .authentication import generate_kafka_jwt


class KafkaProducerRepository:
    def __init__(self, producer: KafkaProducer = KafkaProducerFactory.get_client()):  # type: ignore
        # The client provides a producer that is already connected
        self.producer = producer

    def publish(self, topic: KafkaTopic, message: BaseKafkaMessage) -> None:
        message_token = generate_kafka_jwt(
            SETTINGS.KAFKA_USERNAME, SETTINGS.KAFKA_JWT_SECRET
        )
        self.producer.send(
            topic.value,
            json.dumps(message.dict(), default=str).encode("utf-8"),
            headers=[("authorization", message_token.encode("utf-8"))],
        )

    def disconnect(self):
        self.producer.flush()
        self.producer.close()


class KafkaConsumerRepository:
    def __init__(self, consumer: KafkaConsumer = KafkaConsumerFactory.get_client()):  # type: ignore
        # The client provides a consumer that is already connected and subscribed to topics
        self.consumer = consumer

    def poll(
        self, timeout: int = 100, max_records: int = 20, update_offsets: bool = True
    ) -> None:
        self.consumer.poll(timeout, max_records, update_offsets)

    def disconnect(self) -> None:
        self.consumer.close()
