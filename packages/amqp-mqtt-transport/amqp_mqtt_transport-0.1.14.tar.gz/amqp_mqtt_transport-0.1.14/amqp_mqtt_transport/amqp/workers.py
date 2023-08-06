import aio_pika
import abc
import asyncio
import logging
import signal
from typing import List, Dict, Awaitable
from amqp_mqtt_transport.amqp import BindingsParams, ConnectionParams, AMQPController, AMQPConsumer

__all__ = ['Workforce', 'Worker']
logger = logging.getLogger(__name__)

class Worker(abc.ABC):
    """Abstract worker class that should be inherited when creating custom workers,
    override methods setup_queue to setup queue and on_message for actions on recieving message
    """
    
    @abc.abstractmethod
    async def setup_worker(self, channel: aio_pika.abc.AbstractChannel):
        """ Abstract method used to setup queue and exchange for it and bind them\n
         Channel that can be recived beforehand from connection_controller.\n
         Before method exit, call self._setup_queue()"""
        ...
        
    async def _setup_queue(self, channel: aio_pika.abc.AbstractChannel, binding_params: BindingsParams):

        self._consumer = AMQPConsumer(channel)
        self._consumer.set_up_binding_params(binding_params)
        await self._consumer.create_queue()
        await self._consumer.subscribe(self.on_message)

    @abc.abstractmethod
    async def on_message(self, message: aio_pika.IncomingMessage):
        """Handler for messages recieved from amqp

        Args:
            message (aio_pika.IncomingMessage): Amqp message, should be acknoledged or not acknoledged before method return
        """
        ...
    

class Workforce():

    def __init__(self, amqp_connection_params : ConnectionParams) -> None:
        self._amqp_controller = AMQPController(amqp_connection_params)
        self._workers : List[Worker] = []
        self._supervisor : Dict[Worker, Awaitable] = {}
   
    def add_worker(self, worker : Worker):
        self._workers.append(worker)
    
    async def _rally_workers(self, channel):
        for worker in self._workers:
            await worker.setup_worker(channel)

    async def start(self):
        """Entry point for class to start its work"""
        await self._amqp_controller.connect()
        channel = await self._amqp_controller.get_channel()
        await channel.set_qos(prefetch_count=10)
        await self._rally_workers(channel)
