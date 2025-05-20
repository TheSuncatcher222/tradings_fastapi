import asyncio
import json

import aio_pika

from app.src.config.config import settings
from app.src.utils.logger_json import (
    Logger,
    LoggerJsonRabbitMQ,
)

logger: Logger = LoggerJsonRabbitMQ


async def event_callback(data: any):
    logger.info(
        msg='Received data from rabbitmq',
        extra=data,
    )


class EventTypes:

    CALLBACK = 'callback'


class QueuesNames:

    APP_TRADINGS = "app_tradings"

    @classmethod
    def all(cls):
        return (cls.APP_TRADINGS,)


class RabbitMQApp:

    def __init__(self):
        self.__connection: aio_pika.abc.AbstractConnection = None
        self.__channel: aio_pika.abc.AbstractChannel = None
        self.__consume_queues_names: list[str] = (QueuesNames.APP_TRADINGS,)
        self.__EVENT_HANDLERS = {"callback": event_callback}

    async def perform_connect(self):
        self.__connection: aio_pika.abc.AbstractConnection = await aio_pika.connect(
            host=settings.RABBITMQ_HOST,
            port=settings.RABBITMQ_PORT,
            login=settings.RABBITMQ_USER,
            password=settings.RABBITMQ_PASSWORD,
            virtualhost=settings.RABBITMQ_VHOST,
        )
        self.__channel: aio_pika.abc.AbstractChannel = await self.__connection.channel()
        await self.__ensure_queues()

    async def perform_close(self):
        await self.__channel.close()
        await self.__connection.close()

    async def send_message(self, data: dict, queues: list[str]):
        await self.__validate_outcome_message(data=data)
        for queue_name in queues:
            await self.__channel.default_exchange.publish(
                message=aio_pika.Message(body=json.dumps(data).encode()),
                routing_key=queue_name,
            )

    async def start_consuming(self):
        for queue_name in self.__consume_queues_names:
            queue: aio_pika.abc.AbstractQueue = await self.__channel.declare_queue(queue_name, durable=True)
            await queue.consume(self.__handle_message)

    async def __ensure_queues(self):
        for queue_name in QueuesNames.all():
            await self.__channel.declare_queue(queue_name, durable=True)

    async def __handle_message(self, message: aio_pika.IncomingMessage):
        try:
            async with message.process(ignore_processed=True):
                logger.info(msg=f'Processing message from RabbitMQ id={message.message_id}')
                data: dict = json.loads(message.body)
                event_type: str = data.get('event_type')
                handler: callable = self.__EVENT_HANDLERS.get(event_type)
                if handler:
                    await handler(data)
                else:
                    raise ValueError(f'Unhandled event: {event_type} ({message.exchange})')
        except Exception as e:
            logger.warning(
                msg=f'Failed to process message: {e}',
                extra={
                    "message_id": message.message_id,
                    "headers": message.headers,
                    "timestamp": message.timestamp,
                    "delivery_tag": message.delivery_tag,
                    "routing_key": message.routing_key,
                    "exchange": message.exchange,
                    "body": data,
                },
            )
            await message.reject(requeue=True)

    async def __validate_outcome_message(self, data: dict):
        event_type: str = data.get("event_type")
        if event_type not in self.__EVENT_HANDLERS.keys():
            raise ValueError(f"Invalid event type: {event_type}")


rabbitmq: RabbitMQApp = RabbitMQApp()


async def main():
    import signal

    loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
    shutdown_event: asyncio.Event = asyncio.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, lambda: shutdown_event.set())
    
    try:
        await rabbitmq.perform_connect()
        await rabbitmq.start_consuming()
        await shutdown_event.wait()
    except Exception as e:
        logger.critical(msg=f"Error during RabbitMQ startup: {e}")

    await rabbitmq.perform_close()


if __name__ == "__main__":
    asyncio.run(main())
