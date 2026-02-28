# Dreame Mower A1 Pro

[![HACS](https://img.shields.io/badge/HACS-Custom-orange?style=flat-square)](https://hacs.xyz/)
[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-support-yellow?style=flat-square&logo=buy-me-a-coffee)](https://buymeacoffee.com/nicolasglg)

**Control your Dreame A1 Pro robotic lawn mower directly from Home Assistant.**

Start, stop, and dock your mower, monitor battery and charging status, and more — all from your HA dashboard.

## What you get

| Entity | Type | What it does |
|--------|------|--------------|
| A1 Pro | Lawn Mower | Start, stop, return to dock |
| Battery Level | Sensor | Current battery percentage |
| State | Sensor | What the mower is doing (mowing, charging, idle, error) |
| Charging Status | Sensor | Charging or not |
| Firmware Version | Sensor | Installed firmware |
| Do Not Disturb | Switch | Enable/disable DnD mode |

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant
2. Click the 3 dots menu > **Custom repositories**
3. Add `nicolasglg/dreame-mower-a1-pro` as **Integration**
4. Search for and install **Dreame Mower A1 Pro**
5. Restart Home Assistant
6. Go to **Settings** > **Integrations** > **Add Integration** > **Dreame Mower**

### Manual

Copy the `custom_components/dreame_mower` folder to your Home Assistant `custom_components/` directory and restart.

## Configuration

Use the same Dreame / Xiaomi account credentials as the Dreamehome app.

## Roadmap

Features being worked on for future releases:

- [ ] Mowing zone map display
- [ ] Mowing history and statistics
- [ ] Schedule management from HA
- [ ] Custom mowing zones
- [ ] Mowing progress tracking

Suggestions? [Open an issue](https://github.com/nicolasglg/dreame-mower-a1-pro/issues).

## Credits

This integration is a fork of [dreame-mower](https://github.com/bhuebschen/dreame-mower) by [@bhuebschen](https://github.com/bhuebschen), itself based on [dreame-vacuum](https://github.com/Tasshack/dreame-vacuum) by [@Tasshack](https://github.com/Tasshack). It has been reworked to fix cloud connectivity issues, error code mapping, and entity availability specific to the Dreame A1 Pro outdoor mower.
