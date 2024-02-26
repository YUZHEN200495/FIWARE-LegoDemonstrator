# SmartWorld's FakeGenerator by FIWARE[<img src="https://fiware.github.io/tutorials.IoT-Agent/img/fiware.png" align="left" width="162">](https://www.fiware.org/)<br/>

[![FIWARE IoT Agents](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/iot-agents.svg)](https://github.com/FIWARE/catalogue/blob/master/iot-agents/README.md)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.Iot-Agent.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/tag-fiware-orange.svg?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/fiware)

# Overview
This simple python project generates "simulated" data and sends it to the `Context Broker` using `MQTT`. The idea is to test the system with data that seems real without dealing with real devices. <br>
Bellow you will find information on how to simulate new devices and configure them:

```json
{
        "device_id": "Id_of_the_device",
        "attributes": [
            // Integer Attribute
            {
                "id": "integer_name",
                "type": "Number",
                "range":[0, 20], // Start between 0 and 20
                "bound":[0, 100] // Will stay between 0 and 100
            },
            // Float Attribute
            {
                "id": "float_name",
                "type": "Number",
                "range":[0.0,0.4], // Start between 0.0 and 0.4
                "bound": null // Is not bounded by anything
            },
            // String Attribute
            {
                "id": "string_name",
                "type": "Text",
                "range":["option1", "option2", "option3"]
            }
        ]
    }
```
