# MagicMirror for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-magicmirror?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sindrebroch)

Requires [Jopyth/MMM-Remote-Control](https://github.com/Jopyth/MMM-Remote-Control) installed on your MagicMirror host, with an API-key configured.

## Installation

<details>
   <summary>HACS</summary>

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "MagicMirror"-integration.
4. Restart Home Assistant.
5. Configure the `MagicMirror` integration.
</details>

## Features
### Light
- Toggle monitor on/off
- Change brightness

### Switch
- Show / hide modules (See [Note](https://github.com/sindrebroch/ha-magicmirror#note))

### Button
- Shutdown host
- Reboot host
- Restart magicmirror
- Refresh browser

### Update
- MagicMirror update
- Module update (supports installing new version)

### Notify
```
service: notify.magicmirror
data:
  title: Title      # optional
  message: Message  # required
  data:
    timer: 5000     # default, optional
    dropdown: False # default, optional
```

## Note
Module controls are using an ID from the API which is generated from MagicMirror config.js. This means that if you change the order of your config.js, the modules might become out of sync. This **_should_** be fixed by reloading the integration, to have new devices generated. The old ones needs to be deleted. 
