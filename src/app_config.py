import os

from lib.kafka_connect import KafkaConsumer, KafkaProducer
from lib.redis import RedisClient


class AppConfig:
    CERTIFICATE_PATH = 'crt/YandexInternalRootCA.crt'
    DEFAULT_JOB_INTERVAL = 25

    def __init__(self) -> None:

        self.kafka_host = str(os.getenv('KAFKA_HOST'))
        self.kafka_port = int(str(os.getenv('KAFKA_PORT')))
        self.kafka_consumer_username = str(os.getenv('KAFKA_CONSUMER_USERNAME'))
        self.kafka_consumer_password = str(os.getenv('KAFKA_CONSUMER_PASSWORD'))
        self.kafka_consumer_group = str(os.getenv('KAFKA_CONSUMER_GROUP'))
        self.kafka_consumer_topic = str(os.getenv('KAFKA_SOURCE_TOPIC'))
        self.kafka_producer_username = str(os.getenv('KAFKA_CONSUMER_USERNAME'))
        self.kafka_producer_password = str(os.getenv('KAFKA_CONSUMER_PASSWORD'))
        self.kafka_producer_topic = str(os.getenv('KAFKA_DESTINATION_TOPIC'))

        self.redis_host = str(os.getenv('REDIS_HOST'))
        self.redis_port = int(str(os.getenv('REDIS_PORT')))
        self.redis_password = str(os.getenv('REDIS_PASSWORD'))

    def kafka_producer(self):
        return KafkaProducer(
            self.kafka_host,
            self.kafka_port,
            self.kafka_producer_username,
            self.kafka_producer_password,
            self.kafka_producer_topic,
            self.CERTIFICATE_PATH
        )

    def kafka_consumer(self):
        return KafkaConsumer(
            self.kafka_host,
            self.kafka_port,
            self.kafka_consumer_username,
            self.kafka_consumer_password,
            self.kafka_consumer_topic,
            self.kafka_consumer_group,
            self.CERTIFICATE_PATH
        )

    def redis_client(self) -> RedisClient:
        return RedisClient(
            self.redis_host,
            self.redis_port,
            self.redis_password,
            self.CERTIFICATE_PATH
        )
