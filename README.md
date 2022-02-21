# MagicMirror for HomeAssistant

![GitHub release (latest by date)](https://img.shields.io/github/v/release/sindrebroch/ha-magicmirror?style=flat-square)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/sindrebroch)

Requires [MMM-Remote-Control](https://github.com/Jopyth/MMM-Remote-Control) installed on your MagicMirror host, with an API-key configured.

## Installation

<details>
   <summary>HACS (Recommended)</summary>

1. Ensure that [HACS](https://hacs.xyz/) is installed.
2. Add this repository as a custom repository
3. Search for and install the "MagicMirror"-integration.
4. Restart Home Assistant.
5. Configure the `MagicMirror` integration.
</details>

<details>
   <summary>Manual</summary>

1. Download the `Source code (zip)` file from the
   [latest release](https://github.com/sindrebroch/ha-magicmirror/releases/latest).
2. Unpack the release and copy the `custom_components/ha-magicmirror` directory
   into the `custom_components` directory of your Home Assistant
   installation.
3. Restart Home Assistant.
4. Configure the `MagicMirror`-integration.
</details>


## Todo
- [ ] Add Button-entity to update [if possible]
- [ ] Handle installed_modules, and create a toggle to show/hide modules

## Features
### Binary sensor
- Update available

### Switch
- Toggle monitor

### Number
- Brightness

### Button
- Shutdown host
- Reboot host
- Restart magicmirror
- Refresh browser

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

## Debugging

If something is not working properly, logs might help with debugging. To turn on debug-logging add this to your `configuration.yaml`

```
logger:
  default: info
  logs:
    custom_components.magicmirror: debug
```

Have started work on diagnostics. This will be expanded on in the future as it is more clear what is needed to include to resolve issues.
To download diagnostics, go into your device and press DOWNLOAD DIAGNOSTICS.
This downloads a txt-file you can post in you issue. All sensitive data should be redacted here, so no need to worry, but you can inspect it if you want.
