import json
import datetime
import uuid
import asyncio
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import ib_insync as ibi
import logging
from .producer import Producer

config ={
    'ib_client':'127.0.0.1',
    'ib_port': 7497,
    'ib_clientId': 11,
    'kafka_bootstrap_servers': 'localhost:9092'
}

class IBMarketProducer(Producer):
    """
    Market data stream handler
    """
    def __init__(self, config, tickers, logger=None):
        super().__init__(self, config['kafka_bootstrap_servers'])
        self.client = config['ib_client']
        self.port = config['ib_port']
        self.clientId = config['ib_clientId']
        self.logger = logger
        self.tickers = tickers

        self.subscriptions = []

        self.ib = ibi.IB().connect()

        self.producer = AIOKafkaProducer(
            bootstrap_servers=config['kafka_bootstrap_servers'])

    @property

    async def startProducer(self):
        self.producer = await self.producer.start()
        # self.producer = producer
        self.logger.info('Kafka producer started')

    async def streamMarketData(self, marketDataType):
        await self.producer.start()

        with await self.ib.connectAsync():
            contracts = [
                ibi.Stock(symbol, 'SMART', 'USD')
                for symbol in self.tickers]
            for contract in contracts:
                self.ib.reqMarketDataType(3)
                self.ib.reqMktData(contract)

            async for tickers in self.ib.pendingTickersEvent:
                for ticker in tickers:
                    # data = json.dumps(ticker.dict())
                    stock_dict = ticker.contract.dict()

                    data = {'name': ticker.contract.symbol,
                            'message_id': str(uuid.uuid4()),
                            'timestamp': str(datetime.datetime.utcnow()),
                            'symbol': ticker.contract.symbol,
                            'exchange': ticker.contract.exchange,
                            'currency': ticker.contract.currency,
                            # 'time': datetime.datetime(2023, 4, 24, 23, 0, 32, 864429, tzinfo=datetime.timezone.utc),
                            'time': str(ticker.time),
                            'bid': ticker.bid,
                            'bidSize': ticker.bidSize,
                            'ask': ticker.ask,
                            'askSize': ticker.askSize,
                            'last': ticker.last,
                            'lastSize': ticker.lastSize,
                            'prevBid': ticker.prevBid,
                            'prevBidSize': ticker.prevBidSize,
                            'prevAsk': ticker.prevAsk,
                            'prevAskSize': ticker.prevAskSize,
                            'prevLast': ticker.prevLast,
                            'prevLastSize': ticker.prevLastSize,
                            'volume': ticker.volume,
                            'open': ticker.open,
                            'high': ticker.high,
                            'low': ticker.low,
                            'close': ticker.close,
                            'vwap': ticker.vwap,
                            }

                    # print(ticker.dict())
                    print(json.dumps(data))
                    print(stock_dict)
                    print(datetime.datetime.now(), ticker.close)
                    msg_data = json.dumps(data).encode("ascii")
                    await self.producer.send('mktDataStream', msg_data)
                    # response = ProducerResponse(
                    #     name=msg.name, message_id=msg.message_id, topic=topicname
                    # )
                    # logger.info(response)
    def disconnectIb(self):
        self.ib.disconnect()
        self.logger.info('IB disconnected')

    def stop_producer(self):
        self.producer.stop()
        self.logger.info('Kafka producer stopped')

    def stop(self):
        self.disconnectIb()
        self.stop_producer()

def deserializer(serialized):
    return json.loads(serialized)

async def consume():
    # consumer will decompress messages automatically
    # in accordance to compression type specified in producer
    consumer = AIOKafkaConsumer(
        'mktDataStream',
        bootstrap_servers='localhost:9092',
        value_deserializer=deserializer)
    await consumer.start()
    data = await consumer.getmany(timeout_ms=10000)
    for tp, messages in data.items():
        for message in messages:
            print(type(message.value), message.value)
    await consumer.stop()

if __name__ == '__main__':
    test_stream = IBMarketProducer(config=config, tickers=['GOOG', 'AAPL'])
    test_stream.streamMarketData(marketDataType=3)
    asyncio.run(consume())

