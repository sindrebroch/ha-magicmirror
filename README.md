# MagicMirror for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-magicmirror?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sindrebroch)

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
   [latest release](https://github.com/sindrebroch/ha-magicmirror/releases/latest).
2. Unpack the release and copy the `custom_components/ha-magicmirror` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `MagicMirror`-integration.

## TODO
- [ ] Handle installed_modules, and create a toggle to show/hide modules
- [ ] Add notify-service for notification and alert
- [ ] Add Button-entity to update (if possible)
- [ ] Remove binary_sensor for monitor state (not needed with switch entity)
- [ ] Remove monitor on/off/toggle-services (not needed with switch entity)

## Features
### Binary sensor
- Monitor state
- Update available

### Switch
- Monitor on/off

### Button
- reboot
- restart
- shutdown
- refresh

### Services
- monitor on
- monitor off
- monitor toggle
- brightness
- notification
- alert
