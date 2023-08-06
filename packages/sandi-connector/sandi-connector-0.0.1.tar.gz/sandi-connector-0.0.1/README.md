# SANDI_CONNECT

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/your-library.svg)](https://badge.fury.io/py/your-library)

## Description

Your Library is a Python library that allows you to connect to an MQTT broker using WebSockets easily and send messages.

To make this library work, you need to configure your PMU to send protocol frames over UDP.


## Installation

You can install sandi_connect using `pip`:

```bash 
pip install sandi_connect
```


## Usage

Here's a basic example of how to use Your Library to connect to an SANDI proyect and send messages:

```python
from sandi_connect import get_client ,start_conection_sandi

client = get_client('your_client_id_assigned', 'your_user_assigened','your_pass_assigned')
start_conection_sandi(client,"your_topic",<your_port>)
```
