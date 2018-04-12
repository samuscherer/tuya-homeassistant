"""
Simple platform to control Tuya based bulbs.

"""
import voluptuous as vol
from homeassistant.components.light import (Light, ATTR_HS_COLOR, ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, SUPPORT_COLOR, PLATFORM_SCHEMA, SUPPORT_COLOR_TEMP, ATTR_COLOR_TEMP)
from homeassistant.const import (CONF_NAME, CONF_HOST, CONF_ID)
import homeassistant.helpers.config_validation as cv
import homeassistant.util.color as color_util

#REQUIREMENTS = ['pytuya==0.1']

CONF_DEVICE_ID = 'device_id'
CONF_LOCAL_KEY = 'local_key'

DEFAULT_ID = '1'
DEFAULT_BRIGHTNESS_SCALE = 255
DEFAULT_WHITE_VALUE_SCALE = 255


PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_DEVICE_ID): cv.string,
    vol.Required(CONF_LOCAL_KEY): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up of the Tuya bulb."""
    import pytuya

    add_devices([TuyaDevice(
        pytuya.BulbDevice(
            config.get(CONF_DEVICE_ID),
            config.get(CONF_HOST),
            config.get(CONF_LOCAL_KEY),
        ),
        config.get(CONF_NAME),
    )])


class TuyaDevice(Light):
    """Representation of a Tuya bulb."""

    def __init__(self, device, name):
        """Initialize the Tuya bulb."""
        self._device = device
        self._name = name
        self._state = False
        self._brightness = 255
        self._hs_color = (0, 0)
        self._brightness = 0
        self._rgbcolor = [0,0,0]
        self._supported_features = 0
        self._supported_features |= (SUPPORT_COLOR)
        self._supported_features |= (SUPPORT_BRIGHTNESS)
        self._supported_features |= (SUPPORT_COLOR_TEMP)
        self._white_value_scale = 255
        self._white_value = 0
        self._color_mode = False
        self._color_temp = 100

    @property
    def name(self):
        """Get name of Tuya bulb."""
        return self._name

    @property
    def is_on(self):
        """Check if Tuya bulb is on."""
        return self._state

    @property
    def brightness(self):
        return self._brightness

    @property
    def hs_color(self):
        return self._hs_color

    @property
    def supported_features(self):
        return self._supported_features

    def turn_on(self, **kwargs):
        """Turn Tuya bulb on."""
        if not self._state:
            self._device.set_status(True)

        if ATTR_HS_COLOR in kwargs:
            hs_color = kwargs.get(ATTR_HS_COLOR)
            print("\n\n\n\n" + str(hs_color) + "\n\n\n\n")
            brightness = kwargs.get(ATTR_BRIGHTNESS, self._brightness if self._brightness else 255)
            rgb = color_util.color_hsv_to_RGB(hs_color[0], hs_color[1], brightness/255*100)
            try:
                if rgb[0] < 240 or rgb[1] < 240 or rgb[2] < 240:
                    self._device.set_colour(rgb[0],rgb[1],rgb[2])
                    self._color_mode = True
                    self._hs_color = hs_color
                    self._brightness = brightness
                    self._rgbcolor = [rgb[0],rgb[1],rgb[2]]
                else:
                    self._device.set_white(brightness, self._color_temp)
                    self._color_mode = False                    
                    self._hs_color = hs_color
                    self._rgbcolor = [rgb[0],rgb[1],rgb[2]]

            except ConnectionError as e:
                pass

        if ATTR_BRIGHTNESS in kwargs:
            brightness = kwargs.get(ATTR_BRIGHTNESS)
            if self._color_mode:
                rgb = color_util.color_hsv_to_RGB(self._hs_color[0], self._hs_color[1], brightness/255*100)
                try:
                    self._device.set_colour(rgb[0],rgb[1],rgb[2])
                    self._brightness = brightness
                    self._rgbcolor = [rgb[0],rgb[1],rgb[2]]
                except ConnectionError as e:
                    pass
            else:
                try:
                    self._device.set_white(brightness, self._color_temp)
                    self._brightness = brightness
                except ConnectionError as e:
                    pass

        if ATTR_COLOR_TEMP in kwargs:
            color_temp = kwargs.get(ATTR_COLOR_TEMP)
            try:
                self._device.set_white(self._brightness, int((color_temp/500)*255))
                self._color_mode = False
                self._color_temp = color_temp
            except ConnectionError as e:
                pass

    def turn_off(self, **kwargs):
        """Turn Tuya bulb off."""
        self._device.set_status(False)
        self._state = False
    
    def update(self):
        """Get state of Tuya bulb."""
        success = False
        for i in range(3):
            if success is False:
                try:
                    status = self._device.status()
                    self._state = status['dps']['1']
                    success = True
                except ConnectionError:
                    if i+1 == 3:
                        success = False
                        raise ConnectionError("Failed to update status.")
