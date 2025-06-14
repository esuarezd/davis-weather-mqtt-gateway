import paho.mqtt.client as mqtt

def sanitize_topic(name: str) -> str:
    return name.strip().lower().replace(" ", "_").replace(".", "").replace("/", "_")

def publish_data(data: dict, mqtt_config: dict):
    client = mqtt.Client()
    client.connect(mqtt_config["host"], mqtt_config["port"], 60)

    for key, value in data.items():
        topic = f"{mqtt_config['topic_prefix']}/{sanitize_topic(key)}"
        client.publish(topic, str(value), retain=True)

    client.disconnect()


