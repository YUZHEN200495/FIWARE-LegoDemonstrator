# Digital Twin of SmartWorld by FIWARE [<img src="https://img.shields.io/badge/NGSI-LD-d6604d.svg" width="90"  align="left" />](https://www.etsi.org/deliver/etsi_gs/CIM/001_099/009/01.04.01_60/gs_cim009v010401p.pdf)[<img src="https://fiware.github.io/tutorials.IoT-Agent/img/fiware.png" align="left" width="162">](https://www.fiware.org/)<br/>

[![FIWARE IoT Agents](https://nexus.lab.fiware.org/repository/raw/public/badges/chapters/iot-agents.svg)](https://github.com/FIWARE/catalogue/blob/master/iot-agents/README.md)
[![License: MIT](https://img.shields.io/github/license/fiware/tutorials.Iot-Agent.svg)](https://opensource.org/licenses/MIT)
[![Support badge](https://img.shields.io/badge/tag-fiware-orange.svg?logo=stackoverflow)](https://stackoverflow.com/questions/tagged/fiware)
[![JSON LD](https://img.shields.io/badge/JSON--LD-1.1-f06f38.svg)](https://w3c.github.io/json-ld-syntax/)

---
## Smartworld by FIWARE

FIWARE's Smartworld is a Model of a Smart City using bricks, sensors, electronics and the FIWARE system. 

The Model was created to show the endless possibilities of the FIWARE technology in multiple fields, like digital governance, energy management, city management, mobility and construction.

---

## General setup

For the general setup of the digital twin of the SmartWorld by FIWARE have a look at the flowchart bellow. <br>
The base of the whole digital twin is the SmartWorld itself with all its microcontrollers, actuators and sensors. The information of the sensors is transferred from the microcontrollers via WiFi to the `mosquitto MQTT-Broker`. From there the `IoT-Agent` is reading this information, translating it into `NGSI-LD` and sending it to the `Orion-LD Context Broker`.<br>
The current data of the SmartWorld is available in real time and standartized in the context broker. The Digital Twin representation in the `Front-End` is getting its information from the `Context Broker` through a `proxy` to avoid CORS problems.<br> 
To record this real time data we use `QuantumLeap`, which watches the desired entities and stores them in a`Crate-DB` database. The dashboard-tool `Grafana` gets the information over time out of the database and show it in dashboards.

![Overview](overview.png)

---

## Start up the context broker

To run the context broker you need to have docker compose version 2 installed.

The commands to control the system are:

- ```./services create``` : pulls the docker images
- ```./services setup``` : downloads context data and saves it to be used later whitout internet, and starts the context broker
- ```./services start``` : starts the context broker without the need of internet
- ```./services simulate``` : starts the context broker along with the simulator (needs internet)
- ```./services stop``` : stops all the docker containers
- ```./services delete``` : deletes all volumes, resets the context broker to its initial state, without any data and configuration

---

## Grafana Setup
Here is a description on how to correctly setup grafana and import all the dashboards into it:

Open Grafana in a browser with ```http://localhost:3003/```.

Configure the data source: Go to ```Configuration``` -> ```Data Sources``` -> ```Add Data Source```. Select a ```PostgreSQL``` data source. Fill in the following:

|             |Content              |
|-------------|---------------------|
|Name:        |```CrateDB```           |
|Host:        |```crate-db``` |
|Database:    |```doc```    |
|User:        |```crate```    |
|Password:    |``` ```              |
|TLS/SSL Mode:|```disable```        |

4. Import dashboard: Go to ```Create``` -> ```Import``` -> ```Upload JSON file```.
For the digital twin select the JSON files of the folder ```Grafana-Dashboards/Grafana_Lego```.

---
# Expanding the SmartWorld
Here are a few insights on how to expand the SmartWorld and create new features to it:

## Changing the Containers
You can change the containers as much as you want. For example, now it is necessary to send a POST request through the `proxy`, so you change it to accept this kind if request. <br>
After changing the code the only thing you need to do is delete the old image:
```shell
docker image rm <IMAGE> 
```

## Adding new devices:
It is very easy to add new devices to the SmartWorld, just follow these simple steps:<br>

### 1. Provision Device
Modify the `import-data` file and add a `POST` request to generate your new device.
```shell
curl --location --request POST 'http://iot-agent:4041/iot/devices' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /' \
--header 'Content-Type: application/json' \
--data-raw '{
    "devices": [
        {
            "device_id": "MyType:MyDevice:1",
            "entity_name": "urn:ngsi-ld:MyType:MyDevice:1",
            "entity_type": "MyType",
            "protocol":"PDI-IoTA-JSON",
            "transport":"MQTT",
            "timezone": "Europe/Berlin",
            "attributes": [
                {
                    "object_id": "example",
                    "name": "example",
                    "type": "Number"
                }
            ],
            "commands":[
                {
                    "name":"setspeed",
                    "type":"command"
                }
                ],
            "static_attributes": [
                {
                    "name": "controlledAsset",
                    "type": "Relationship",
                    "value": "urn:ngsi-ld:Building:Basis"
                }
            ]
        }
    ]
}'
```
### 2 (Optional) Generate history data:
Modify the `import-data` file and add a `POST` request to subscribe `QuantumLeap` to changes in your device.
```shell
curl --location --request POST 'http://orion:1026/ngsi-ld/v1/subscriptions/' \
--header 'NGSILD-Tenant: openiot' \
--header 'Content-Type: application/json' \
--header 'Link: <http://context/ngsi-context.jsonld>; rel="http://www.w3.org/ns/json-ld#context"; type="application/ld+json"' \
--data-raw '{
  "description": "Notify me if example attribute of MyType devices has changed",
  "type": "Subscription",
  "entities": [{"type": "Device"}],
  "watchedAttributes": ["example"],
  "notification": {
    "attributes": ["example"],
    "format": "normalized",
    "endpoint": {
      "uri": "http://quantumleap:8668/v2/notify",
      "accept": "application/json",
      "receiverInfo" : [
        { 
          "key":"fiware-service",
          "value":"openiot"
        }
       ]
    }
  }
}'
```

### 3 (Optional) Add your device to the `fakegenerator`
If you want to test your configuration without building a physical device you can use the simulator to do this, just modify the `devices.json` file:
```json
{
    "device_id": "MyType:MyNewDevice:1",
    "attributes": [
        {
            "id": "example",
            "type": "Number",
            "range" : [0, 100], // starts between 0 and 100
            "bound" : [-30, 130] // will be kept between -30 and 130
        }
    ]
}
```

### 4 Connect your new Device
If everything was setup correctly you should now be able to simply connect your device to the MQTT Broker `mosquitto` by using the credentials. An example can be found in the `FIWARE-SmartTrain` repository.

---
## License

[MIT](LICENSE) © 2020 FIWARE Foundation e.V.