import json
import datetime
import uuid
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import ib_insync as ibi
import logging

class Producer(AIOKafkaProducer):
    """
    Base producer class

    """

    def __init__(self, cluster_config=None,*args, **kwargs):
        super(Producer, self,).__init__(*args, **kwargs)
        self.cluster_config = cluster_config

    def send_messages(self, topic, *msg):
        try:
            super(Producer, self).send_messages(topic, *msg)

        # except (YelpKafkaError, KafkaError):
        except:
            pass
