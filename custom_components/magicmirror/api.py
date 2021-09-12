"""MagicMirror library."""

from typing import Any, Optional

import aiohttp

from homeassistant.const import HTTP_FORBIDDEN, HTTP_OK

from .const import LOGGER
from .models import MagicMirrorResponse


# Mirror control
API_TEST = "api/test"
API_MONITOR = "api/monitor"
API_MONITOR_ON = f"{API_MONITOR}/on"
API_MONITOR_OFF = f"{API_MONITOR}/off"
API_MONITOR_STATUS = f"{API_MONITOR}/status"
API_MONITOR_TOGGLE = f"{API_MONITOR}/toggle"

API_SHUTDOWN = "api/shutdown"
API_REBOOT = "api/reboot"
API_RESTART = "api/restart"
API_MINIMIZE = "api/minimize"
API_TOGGLEFULLSCREEN = "api/togglefullscreen"
API_DEVTOOLS = "api/devtools"
API_REFRESH = "api/refresh"
API_BRIGHTNESS = "api/brightness"

# Module control
API_MODULE = "api/module"
API_MODULES = "api/modules"
API_MODULE_INSTALLED = f"{API_MODULE}/installed"
API_MODULE_AVAILABLE = f"{API_MODULE}/available"
API_UPDATE_MODULE = "api/update"
API_INSTALL_MODULE = "api/install"
API_UPDATE_AVAILBALE = "/api/mmUpdateAvailable"  #

# API
API_CONFIG = "api/config"

SWAGGER = "/api/docs/#/"


class MagicMirrorApiClient:
    """Main class for handling connection with."""

    def __init__(
        self,
        host: str,
        port: str,
        api_key: str,
        session: Optional[aiohttp.client.ClientSession] = None,
    ) -> None:
        """Initialize connection with MagicMirror."""

        self.host = host
        self.port = port
        self.api_key = api_key
        self._session = session

        self.base_url = f"http://{self.host}:{self.port}"
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

    async def handle_request(self, response) -> Any:
        """Handle request."""

        LOGGER.debug("pre handle_request=%s", response)

        async with response as resp:

            if resp.status == HTTP_FORBIDDEN:
                raise Exception(f"Forbidden {resp}")  # Probably need API-key

            if resp.status != HTTP_OK:
                raise Exception(f"Response not HTTP_OK {resp}")

            data = await resp.json()

        LOGGER.debug("post handle_request=%s", data)

        return data

    async def get(self, path: str) -> Any:
        """Get request."""

        LOGGER.debug("GET path=%s", path)

        assert self._session is not None

        get = await self._session.get(
            url=f"{self.base_url}/{path}",
            headers=self.headers,
        )

        LOGGER.debug("Response=%s", get)

        return await self.handle_request(get)

    async def post(self, path: str, data: Optional[str] = None) -> Any:
        """Post request."""

        LOGGER.debug("POST path=%s. data=%s", path, data)

        assert self._session is not None

        post = (
            await self._session.post(
                url=f"{self.base_url}/{path}",
                headers=self.headers,
                data=data,
            ),
        )

        LOGGER.debug("Response=%s", post)

        return await self.handle_request(post)

    async def api_test(self) -> MagicMirrorResponse:
        """Test api."""
        return MagicMirrorResponse.from_dict(await self.get(API_TEST))

    async def monitor_status(self) -> MagicMirrorResponse:
        """Get monitor status."""
        return MagicMirrorResponse.from_dict(await self.get(API_MONITOR_STATUS))

    async def monitor_on(self) -> Any:
        """Turn on monitor."""
        return MagicMirrorResponse.from_dict(await self.get(API_MONITOR_ON))

    async def monitor_off(self) -> Any:
        """Turn off monitor."""
        return MagicMirrorResponse.from_dict(await self.get(API_MONITOR_OFF))

    async def monitor_toggle(self) -> Any:
        """Toggle monitor."""
        return MagicMirrorResponse.from_dict(await self.get(API_MONITOR_TOGGLE))

    async def shutdown(self) -> Any:
        """Shutdown."""
        return await self.get(API_SHUTDOWN)

    async def reboot(self) -> Any:
        """Reboot."""
        return await self.get(API_REBOOT)

    async def restart(self) -> Any:
        """Restart."""
        return await self.get(API_RESTART)

    async def minimize(self) -> Any:
        """Minimize."""
        return await self.get(API_MINIMIZE)

    async def toggle_fullscreen(self) -> Any:
        """Toggle fullscreen."""
        return await self.get(API_TOGGLEFULLSCREEN)

    async def devtools(self) -> Any:
        """Devtools."""
        return await self.get(API_DEVTOOLS)

    async def refresh(self) -> Any:
        """Refresh."""
        return await self.get(API_REFRESH)

    async def brightness(self, brightness: str) -> Any:
        """Brightness."""
        return await self.get(f"{API_BRIGHTNESS}/{brightness}")

    async def module(self, moduleName: str) -> Any:
        """Endpoint for module."""
        return await self.get(f"{API_MODULE}/{moduleName}")

    async def module_action(self, moduleName: str, action) -> Any:
        """Endpoint for module action."""
        return await self.get(f"{API_MODULE}/{moduleName}/{action}")

    async def module_update(self, moduleName: str) -> Any:
        """Endpoint for module update."""
        return await self.get(f"{API_UPDATE_MODULE}/{moduleName}")

    async def modules(self) -> Any:
        """Endpoint for modules."""
        return await self.get(API_MODULES)

    async def module_installed(self) -> Any:
        """Endpoint for module installed."""
        return await self.get(API_MODULE_INSTALLED)

    async def module_available(self) -> Any:
        """Endpoint for module available."""
        return await self.get(API_MODULE_AVAILABLE)

    async def module_install(self, data) -> Any:
        """Endpoint for module install."""
        return await self.post(API_INSTALL_MODULE, data=data)

    async def config(self) -> Any:
        """Config."""
        return await self.get(API_CONFIG)

    async def alert(
        self,
        title: str,
        message: str,
        timer: str,
        dropdown: bool = False,
    ) -> Any:
        """Notification screen."""

        type = "&type=notification" if dropdown else ""
        return await self.get(
            f"{API_MODULE}/alert/showalert?title={title}&message={message}&timer={timer}{type}"
        )