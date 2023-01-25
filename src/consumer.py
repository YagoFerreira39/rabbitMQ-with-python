import pika


def consumer_callback(channel, method, properties, body):
    print(body)


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = ""
        self.__port = ""
        self.__username = ""
        self.__password = ""
        self.__queue = ""
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()

        channel.queue_declare(
            queue=self.__queue,
            durable=True
        )

        channel.basic_consume(
            queue="data_queue",
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f'Listen RabbitMQ on Port 5672')

        self.__channel.start_consuming()
