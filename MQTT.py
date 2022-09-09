'''
@@@ Author: Vincent
@@@ Date  : 8 Sep 2022
@@@ About : Send any mqtt message once for debugging
'''
import paho.mqtt.client as mqtt

class MQTTManager():
    '''
    server              <str>       : mqtt endpoint
    mqtt_port           <int>       : mqtt port number, default 1883
    connection_timeout  <int>       : mqtt connection timeout, default 60
    topics              <list>      : mqtt topics, refer to codebook topics_lib
    mqtt_client         <object>    : mqtt client
    '''
    def __init__(self,server,topics):
        self.server = server
        self.mqtt_port = 1883
        self.connection_timout = 60
        self.topics = topics
        self.mqtt_client = None
    
    def mqtt_client_setup(self):
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.connect(self.server,self.mqtt_port,self.connection_timout)
        print("[MQTT] Client <{}> is configured".format(self.server))
        
    def publish_mqtt_message(self,topic_index,mqtt_message):
        self.mqtt_client.publish(self.topics[topic_index], mqtt_message)
        #self.mqtt_client.loop_stop()
        #self.mqtt_client.disconnect()
        #print("[MQTT] Sent: Topic -> {} | Message -> {}".format(self.topics[topic_index],mqtt_message))