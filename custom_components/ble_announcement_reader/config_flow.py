"""Config flow for BLE Announcement Reader."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from . import DOMAIN

class BLEAnnouncementReaderConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for BLE Announcement Reader."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
                vol.Required("device_addresses", default=""): str,
                vol.Optional("manufacturer_ids", default=""): str,
            }),
        )