# tuya-homeassistant

**THIS WILL ONLY WORK FOR SWITCHES AND BULBS**

This is a simple platform to control **SOME** switch devices and bulbs that use the Tuya cloud for control.

It uses the pytuya library (https://github.com/clach04/python-tuya) to directly control the devices.
Most devices that use the Tuya cloud should work. If port 6668 is open then it will work.

switch id is if the switch device has multiple switches, the switch number.

See here for how to find localKey and devId: https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md

To use switches, copy tuya.py to "<home assistant config dir>/custom_components/switch" and add config below to configuration.yaml

The same goes for bulbs: Copy tuya.py to "<home assistant config dir>/custom_components/light" and add the config below to configuration.yaml.

Config Fields:
```
switch:
  - platform: tuya
    name: //switch name
    host: //ip of device
    local_key: //localKey
    device_id: //devId
    id: //switch id. Remove line if only one switch
```
```
light:
  - platform: tuya
    name: //name
    host: //ip of device
    local_key: //localKey
    device_id: //devId
```

Example:
```
switch:
  - platform: tuya
    name: Switch
    host: xxx.xxx.xxx.xxx
    local_key: xxxxxxxxxxxxxxxx
    device_id: xxxxxxxxxxxxxxxxxxxx
    id: 3
```
