# tuya-homeassistant

**THIS WILL ONLY WORK FOR SWITCHES AND BULBS**

This is a simple platform to control **SOME** switch devices and bulbs that use the Tuya cloud for control.

It uses the pytuya library (https://github.com/clach04/python-tuya) to directly control the devices. ATTENTION: The tuya_bulb.py DOES NOT use the pytuya version available via pip (which is installed automatically by HA if you use tuya.py). Plase use my fork of pytuya (https://github.com/samuscherer/python-tuya) until my changes are merged into the official pytuya version. Just replace the __init__.py file in "<home assistant config dir>/deps/lib/python3.6/site-packages/pytuya/" with the __init__.py file from my fork. If this directory doesn't exist just create it.

Most devices that use the Tuya cloud should work. If port 6668 is open then it will work.

switch id is if the switch device has multiple switches, the switch number.

See here for how to find localKey and devId: https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md

To use switches, copy tuya.py to "<home assistant config dir>/custom_components/switch" and add config below to configuration.yaml
The same goes for bulbs: Copy tuya_bulb.py to "<home assistant config dir>/custom_components/switch", rename it to tuya.py and add the config below.

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
    name: //switch name
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
