import paho.mqtt.client as mqtt
import socket
import keyboard
from .IEEEC37118 import Decode
import time


last_print_time = 0

def on_publish(client, userdata, result):  
    global last_print_time
    current_time = time.time()
    if current_time - last_print_time >= 60:
        print("Message published successfully. Message ID: {}".format(result))
        last_print_time = current_time

def get_client( client_id, user, password)->mqtt.Client:
    """
    Connects to an broker using WebSocket transport.

    Parameters:
    - client_id: The client identifier.
    - user: Username for authentication (if required).
    - password: Password for authentication (if required).

    Returns:
    - The connected MQTT client.

    """
    client = mqtt.Client(client_id, transport='websockets')
    client.on_publish = on_publish
    client.username_pw_set(user, password)
    client.tls_set()
    client.connect('io.sandi.c-ses.cl', 443, 60)
    client.loop_start()
    return client

def start_conection_sandi(client, topic, port_pmu):
    """
    Starts a UDP connection and receives data from clients.

    Parameters:
    - client: The MQTT client used to publish the received data.
    - topic: The topic to which the data will be published.
    - port_pmu: The UDP port for the connection.

    Returns:
    - No explicit return.

    """
    INICIO_CONFIG_FRAME = False
    data_frame = Decode()
    server_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = '0.0.0.0'
    server_port = port_pmu
    server = (server_address, server_port)
    server_udp.bind(server)
    print(f'To close the connection press Ctrl+c')
    while True:
        if keyboard.is_pressed('Ctrl+c'):
            break
        data, client_address = server_udp.recvfrom(1024)
        if data is not None:
            if data_frame.check_frame_data(data) == 0:
                if data_frame.phasor_type(data) == data_frame.TYPE_DATA:
                    if data_frame.num_pmu() != None:
                        post_message(client,topic+"/data", data_frame.data_frame(data))
                else:
                    if INICIO_CONFIG_FRAME==False:
                        print("Start decryption service - first configuration frame")
                        INICIO_CONFIG_FRAME = True
                    post_message(client, topic+"/config", data_frame.config_frame(data))


def post_message(client, topic, message):
    """
    Publishes a message to an MQTT broker.

    Parameters:
    - client: The MQTT client used to publish the message.
    - topic: The topic to which the message will be published.
    - message: The message to be published.

    Returns:
    - No explicit return.

    """
    client.publish(topic, message)
