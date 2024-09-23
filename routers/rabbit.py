from fastapi import APIRouter
import pika


rabbit_router = APIRouter()


@rabbit_router.get("/")
async def get_rabbit():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello2')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()
    return {"message": "Hello Rabbit"}
