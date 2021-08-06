# MagicMirror for HomeAssistant

WIP: This is just a skelton for now.

HomeAssistant-integration for MagicMirror.

Requires [MMM-Remote-Control](https://github.com/Jopyth/MMM-Remote-Control) installed on your MagicMirror host, with an API-key configured.

## Installation

### HACS (Recommended)

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "MagicMirror"-integration.
4. Restart Home Assistant.
5. Configure the `MagicMirror` integration.

### MANUAL INSTALLATION

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-magicmirror-remote/releases/latest).
2. Unpack the release and copy the `custom_components/ha-magicmirror` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `MagicMirror`-integration.

## Features
### System control
- SHUTDOWN
- REBOOT
- MONITORON
- MONITOROFF
- MONITORTOGGLE
- MONITORSTATUS

### MagicMirror control
- RESTART
- REFRESH
- UPDATE
- SAVE
- BRIGHTNESS

### MagicMirror Electron Browser window control
- MINIMIZE
- TOGGLEFULLSCREEN
- DEVTOOLS

### Module control
- HIDE
- SHOW
- TOGGLE
- FORCE
- MODULE_DATA

### Alerts and Notifications
- SHOW_ALERT
- HIDE_ALERT
- USER_PRESENCE
- NOTIFICATION
- DELAYED

