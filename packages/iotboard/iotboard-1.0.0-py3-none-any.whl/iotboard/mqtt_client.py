import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker_address, broker_port):
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.client = mqtt.Client()

    def connect(self):
        self.client.connect(self.broker_address, self.broker_port)

    def disconnect(self):
        self.client.disconnect()

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def set_message_callback(self, callback):
        self.client.on_message = callback

    def start_loop(self):
        self.client.loop_forever()
