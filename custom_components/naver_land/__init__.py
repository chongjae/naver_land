import logging
from datetime import timedelta
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.components import persistent_notification

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_USERNAME
from homeassistant.core import (
    HomeAssistant,
    ServiceResponse,
    ServiceCall,
    SupportsResponse,
)
from .naver_land import NaverLandApi
from .const import DOMAIN, AREA, TYPE

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(minutes=60)

async def async_setup(hass, config):
    """Set up the integration."""
    hass.data[DOMAIN] = {}
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up the integration from a config entry."""
    apt_id = entry.data[CONF_USERNAME]
    area = entry.data[AREA]
    trade_type = entry.data[TYPE]
    naver_land_api = NaverLandApi(apt_id, area, trade_type)

    hass.data[DOMAIN][entry.entry_id] = naver_land_api

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )

    return True
