import json
from datetime import datetime
from logging import Logger

from lib.kafka_connect import KafkaConsumer, KafkaProducer
from lib.redis import RedisClient
from stg_loader.repository.stg_repository import StgRepository


class StgMessageProcessor:
    def __init__(self, kafka_consumer: KafkaConsumer, kafka_producer: KafkaProducer, redis: RedisClient,
                 stg_repository: StgRepository, batch_size: int, logger: Logger) -> None:
        self._logger = logger
        self._consumer = kafka_consumer
        self._producer = kafka_producer
        self._redis = redis
        self._stg_repository = stg_repository
        self._batch_size = batch_size

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")
        while True:
            kafka_msg = self._consumer.consume()
            if not kafka_msg:
                self._logger.info("No message")
                break
            try:
                payload = kafka_msg['payload']
                user_id = payload['user']['id']
                restaurant_id = payload['restaurant']['id']
                order_items = payload['order_items']
                self._stg_repository.order_events_insert(object_id=kafka_msg['object_id'],
                                                   object_type=kafka_msg['object_type'],
                                                   sent_dttm=kafka_msg['sent_dttm'], payload=json.dumps(payload))
                restaurant_data = self._redis.get(restaurant_id)
                output_message = {
                    "object_id": kafka_msg['object_id'],
                    "object_type": kafka_msg['object_type'],
                    "payload": {
                        "id": kafka_msg['object_id'],
                        "date": payload['date'],
                        "cost": payload['cost'],
                        "payment": payload['payment'],
                        "status": payload['final_status'],
                        "restaurant": {
                            "id": restaurant_id,
                            "name": restaurant_data['name']
                        },
                        "user": {
                            "id": user_id,
                            "name": self._redis.get(user_id)['name']
                        },
                        "products": []
                    }
                }

                for order in order_items:
                    for menu_position in restaurant_data['menu']:
                        if menu_position['_id'] == order['id']:
                            output_message['payload']['products'].append({
                                'id': order['id'],
                                'price': order['price'],
                                'quantity': order['quantity'],
                                'name': order['name'],
                                'category': menu_position['category']
                            })

                self._producer.product(output_message)

            except KeyError:
                continue
            except TypeError:
                continue

        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.utcnow()}: FINISH")
