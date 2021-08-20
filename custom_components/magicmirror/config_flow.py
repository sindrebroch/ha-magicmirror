"""Config flow for MagicMirror integration."""

from __future__ import annotations

from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_API_KEY, CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN as MAGICMIRROR_DOMAIN, LOGGER
from .magicmirror import MagicMirror
from .models import MagicMirrorResponse

SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_PORT, default="8080"): str,
        vol.Required(CONF_API_KEY): str,
    }
)


class MagicMirrorFlowHandler(config_entries.ConfigFlow, domain=MAGICMIRROR_DOMAIN):
    """Config flow for MagicMirror."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            api_key = user_input[CONF_API_KEY]

            if await self._async_existing_devices(host):
                return self.async_abort(reason="already_configured")

            session = async_get_clientsession(self.hass)
            magicmirror = MagicMirror(host, port, api_key, session=session)

            errors: dict[str, Any] = {}

            try:
                t: MagicMirrorResponse = await magicmirror.api_test()

                if not t.success:
                    errors["base"] = "cannot_connect"

            except aiohttp.ClientError as error:
                errors["base"] = "cannot_connect"
                LOGGER.warning("error=%s. errors=%s", error, errors)

            if errors:
                return self.async_show_form(
                    step_id="user", data_schema=SCHEMA, errors=errors
                )

            unique_id: str = host
            await self.async_set_unique_id(unique_id)
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=unique_id.title(),
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=SCHEMA,
            errors={},
        )

    async def _async_existing_devices(self, host: str) -> bool:
        """Find existing devices."""

        existing_devices = [
            f"{entry.data.get(CONF_HOST)}" for entry in self._async_current_entries()
        ]

        return host in existing_devices
