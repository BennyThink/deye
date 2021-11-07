#!/usr/local/bin/python3
# coding: utf-8

# deye - mqtt.py
# 11/6/21 17:46
#

__author__ = "Benny <benny.think@gmail.com>"

import base64
import logging

from paho.mqtt import client as mqtt_client

from config import apply_log_formatter

apply_log_formatter()



class Device:
    def online(self):
        pass

    def offline(self):
        pass


class DYD_E12A3(Device):
    def __init__(self, loginname, clientid, endpoint, password, mqtthost, product_id, device_id, **kwargs):
        self._online_code = base64.b64decode("CAIDQDwAAAAAAA==")
        self._offline_code = base64.b64decode("CAICQDwAAAAAAA==")
        self._client_id = clientid
        self._loginname = loginname
        self._password = password
        self._mqtthost = mqtthost
        self.topic = f"{endpoint}/{product_id}/{device_id}/command/hex"
        self.server = self.__connect_mqtt()

    def __connect_mqtt(self):
        def on_connect(kwargs):
            rc = kwargs.get('rc')
            if rc == 0:
                logging.debug("Connected to MQTT Broker!")
            else:
                logging.critical("Failed to connect, return code %d\n", rc)

        # Set Connecting Client ID
        client = mqtt_client.Client(self._client_id)
        client.on_connect = on_connect
        client.username_pw_set(username=self._loginname, password=self._password)
        client.connect(self._mqtthost)
        return client

    def __publish(self, msg):
        result = self.server.publish(self.topic, msg)
        status = result[0]
        if status == 0:
            logging.debug(f"Send `%s` to topic `%s`", msg, self.topic)
        else:
            logging.error(f"Failed to send message to topic %s", self.topic)

    def online(self):
        self.__publish(self._online_code)

    def offline(self):
        self.__publish(self._offline_code)

    def __str__(self):
        return f"""{self.server}
        broker:{self._mqtthost}
        client_id:{self._client_id}
        username:{self._loginname}
        password:{self._password}
        topic:{self.topic}
        """


if __name__ == '__main__':
    dev = DYD_E12A3("loginname", "clientid", "endpoint", "password", "broker-cn.emqx.io", "product_id", "device_id")
    dev.online()
    dev.offline()
