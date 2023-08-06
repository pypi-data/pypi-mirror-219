from kafka import KafkaProducer, KafkaConsumer

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockKafkaProducer, MockKafkaConsumer
from .models import KafkaTopic


class KafkaProducerFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockKafkaProducer()

    @staticmethod
    def _return_client():
        return KafkaProducer(
            bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
            sasl_mechanism="SCRAM-SHA-256",
            security_protocol="SASL_SSL",
            sasl_plain_username=SETTINGS.KAFKA_USERNAME,
            sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
        )


class KafkaConsumerFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockKafkaConsumer()

    @staticmethod
    def _return_client():
        consumer = KafkaConsumer(
            bootstrap_servers=[SETTINGS.KAFKA_BOOTSTRAP_SERVER],
            sasl_mechanism="SCRAM-SHA-256",
            security_protocol="SASL_SSL",
            sasl_plain_username=SETTINGS.KAFKA_USERNAME,
            sasl_plain_password=SETTINGS.KAFKA_PASSWORD,
            auto_offset_reset="earliest",
            group_id="default",
        )
        consumer.subscribe(KafkaTopic.get_all_topics())
        return consumer
