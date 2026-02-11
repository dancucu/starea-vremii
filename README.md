# Starea Vremii (Home Assistant)

[![GitHub release (pre-release)](https://img.shields.io/github/v/release/dancucu/starea-vremii?include_prereleases)](https://github.com/dancucu/starea-vremii/releases)

Custom integration that fetches weather data from Meteoromania and exposes a sensor for a selected county or station.

## Install

1. Copy `custom_components/starea_vremii` into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Add the integration from **Settings > Devices & Services** and choose the mode (county or station).

## Lovelace card example

```yaml
type: sensor
entity: sensor.starea_vremii_alba
name: Vremea Alba

# Station mode example
# entity: sensor.starea_vremii_statie_cluj_napoca
```

Or show more details:

```yaml
type: entities
title: Vremea Alba
entities:
  - entity: sensor.starea_vremii_alba
  - type: attribute
    attribute: station
    entity: sensor.starea_vremii_alba
    name: Statie
  - type: attribute
    attribute: updated
    entity: sensor.starea_vremii_alba
    name: Actualizat
  - type: attribute
    attribute: humidity
    entity: sensor.starea_vremii_alba
    name: Umezeala
  - type: attribute
    attribute: wind
    entity: sensor.starea_vremii_alba
    name: Vant
  - type: attribute
    attribute: pressure
    entity: sensor.starea_vremii_alba
    name: Presiune
  - type: attribute
    attribute: phenomenon
    entity: sensor.starea_vremii_alba
    name: Fenomen
```
