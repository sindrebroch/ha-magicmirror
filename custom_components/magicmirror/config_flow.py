"""Config flow for MagicMirror integration."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from .magicmirror import MagicMirror
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN as MAGICMIRROR_DOMAIN

from homeassistant.const import (CONF_HOST, CONF_NAME)

_LOGGER = logging.getLogger(__name__)

class MagicMirrorFlowHandler(config_entries.ConfigFlow, domain=MAGICMIRROR_DOMAIN):
    """Config flow for MagicMirror."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle a flow initialized by the user."""

        if user_input is not None:

            name = user_input[CONF_NAME]
            host = user_input[CONF_HOST]

            #if await self._async_existing_devices(area.name):
            #    return self.async_abort(reason="already_configured")

            session = async_get_clientsession(self.hass)
            magicmirror = MagicMirror(session=session)

            errors: dict[str, Any] = {}

            try:
                await magicmirror.fetch()
            except aiohttp.ClientError as error:
                errors["base"] = "cannot_connect"
                _LOGGER.warning("error=%s. errors=%s", error, errors)

            if errors:
                return self.async_show_form(
                    step_id="user", data_schema=SCHEMA, errors=errors
                )

            #unique_id: str = magicmirror
            unique_id: str = "unique_id"
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
