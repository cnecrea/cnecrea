---
name: home-assistant-integration
description: >
  Skill pentru crearea de integrări Home Assistant custom (custom_components) respectând
  standardele oficiale. Folosește acest skill ori de câte ori utilizatorul menționează
  Home Assistant, integrare HA, custom_component, HACS, config_flow, platforme HA
  (light, switch, sensor, button, binary_sensor, climate, cover, fan, number, select, etc.),
  DataUpdateCoordinator, coordinator, services.yaml, manifest.json, strings.json,
  sau orice alt concept legat de dezvoltarea unei integrări Home Assistant.
  De asemenea, folosește-l când utilizatorul vrea să implementeze entități HA,
  să creeze un brand, să adauge acțiuni/servicii custom, sau să structureze corect
  fișierele unei integrări. Activează-l inclusiv la întrebări despre best practices,
  debugging, sau conformitate cu Integration Quality Scale.
  ATENȚIE: Skill-ul este scris în limba română.
---

# Ghid Complet: Integrări Home Assistant

Acest skill te ghidează pas cu pas prin crearea unei integrări Home Assistant custom,
respectând standardele oficiale din documentația dezvoltatorilor:
https://developers.home-assistant.io/

Toate instrucțiunile se aplică pentru integrări de tip `custom_components` (instalabile
prin HACS sau manual), dar structura este identică cu cea a integrărilor din core.

---

## 1. Structura de Fișiere

O integrare completă arată astfel:

```
custom_components/domeniu_meu/
├── __init__.py          # Punctul de intrare — setup și unload
├── manifest.json        # Metadate: domeniu, nume, dependențe, versiune
├── config_flow.py       # Fluxul de configurare din UI
├── coordinator.py       # DataUpdateCoordinator — centralizează fetch-ul de date
├── const.py             # Constante: DOMAIN, chei de configurare, etc.
├── entity.py            # (opțional) Clasă de bază pentru entitățile integrării
├── light.py             # Platformă light
├── switch.py            # Platformă switch
├── sensor.py            # Platformă sensor
├── binary_sensor.py     # Platformă binary_sensor
├── button.py            # Platformă button
├── number.py            # Platformă number
├── select.py            # Platformă select
├── climate.py           # Platformă climate
├── cover.py             # Platformă cover
├── fan.py               # Platformă fan
├── services.yaml        # Descrierea acțiunilor custom (servicii)
├── strings.json         # Texte pentru traduceri (config flow, opțiuni, erori)
├── translations/
│   └── en.json          # Traduceri (copie din strings.json la minim)
│   └── ro.json          # (opțional) Traduceri în română
└── brand/
    ├── icon.png         # Pictogramă integrare (256×256, PNG)
    └── logo.png         # Logo integrare (256×256, PNG)
```

Nu toate fișierele sunt obligatorii. Minimul absolut: `__init__.py` + `manifest.json`.
Adaugi doar platformele pe care integrarea ta le suportă.

---

## 2. manifest.json

Fișierul `manifest.json` este cartea de identitate a integrării. Cheile obligatorii
și recomandarea oficială:

```json
{
  "domain": "domeniu_meu",
  "name": "Numele Integrării",
  "codeowners": ["@github_username"],
  "config_flow": true,
  "dependencies": [],
  "documentation": "https://github.com/user/repo",
  "integration_type": "hub",
  "iot_class": "local_polling",
  "requirements": ["biblioteca_pypi==1.0.0"],
  "version": "1.0.0"
}
```

### Explicații cheie:

- **domain**: Identificator unic, doar litere mici și underscore. NU se poate schimba.
- **config_flow**: Pune `true` dacă integrarea se configurează din UI (recomandat mereu).
- **integration_type**: Alege corect:
  - `"hub"` — gateway spre mai multe dispozitive (ex: Philips Hue bridge)
  - `"device"` — un singur dispozitiv per config entry
  - `"service"` — un singur serviciu per config entry (ex: API meteo)
  - `"entity"` — oferă doar entități helper (ex: template, input_boolean)
- **iot_class**: Descrie cum comunică integrarea:
  - `"local_polling"` — polling local
  - `"local_push"` — push local (device-ul trimite date)
  - `"cloud_polling"` — polling API cloud
  - `"cloud_push"` — push din cloud (webhook etc.)
  - `"calculated"` — valori calculate local
- **version**: Obligatoriu pentru custom_components. Folosește SemVer: `"1.0.0"`.
- **requirements**: Dependențe PyPI. NU pune pachete standard Python sau Home Assistant.

---

## 3. const.py — Constante

Centralizează toate constantele aici. Nu le împrăștia prin fișiere.

```python
"""Constante pentru integrarea domeniu_meu."""

DOMAIN = "domeniu_meu"

# Chei de configurare
CONF_HOST = "host"
CONF_PORT = "port"
CONF_API_KEY = "api_key"

# Valori implicite
DEFAULT_PORT = 8080
DEFAULT_SCAN_INTERVAL = 30

# Platforme suportate
PLATFORMS = ["light", "switch", "sensor", "button"]
```

---

## 4. __init__.py — Punctul de Intrare

Acest fișier orchestrează setup-ul integrării. Pattern-ul modern (2024+):

```python
"""Integrarea Domeniu Meu."""
from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, PLATFORMS
from .coordinator import MyCoordinator

_LOGGER = logging.getLogger(__name__)

# Tipul custom pentru ConfigEntry — pattern modern
type MyConfigEntry = ConfigEntry[MyCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
    """Configurează integrarea dintr-un config entry."""
    # Creează clientul API
    client = MyApiClient(
        host=entry.data["host"],
        api_key=entry.data["api_key"],
    )

    # Verifică conectivitatea
    try:
        await client.async_connect()
    except ConnectionError as err:
        raise ConfigEntryNotReady(
            f"Nu mă pot conecta la {entry.data['host']}"
        ) from err

    # Creează coordinatorul
    coordinator = MyCoordinator(hass, entry, client)

    # Primul fetch — dacă eșuează, integrarea nu se încarcă
    await coordinator.async_config_entry_first_refresh()

    # Stochează coordinatorul în runtime_data
    entry.runtime_data = coordinator

    # Încarcă platformele
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: MyConfigEntry) -> bool:
    """Descarcă integrarea."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
```

### Greșeli frecvente de evitat:

- NU folosi `hass.data[DOMAIN]` pentru stocare — folosește `entry.runtime_data` (pattern modern).
- NU folosi `async_forward_entry_setup` (singular, depreciat) — folosește
  `async_forward_entry_setups` (plural).
- Ridică `ConfigEntryNotReady` dacă dispozitivul nu răspunde — HA va reîncerca automat.

---

## 5. coordinator.py — DataUpdateCoordinator

Coordinatorul centralizează fetch-ul de date. Toate entitățile consumă date de la
coordinator în loc să facă fiecare propriul request.

```python
"""Coordinator pentru integrarea domeniu_meu."""
from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator care gestionează actualizarea datelor."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: MyApiClient,
    ) -> None:
        """Inițializează coordinatorul."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=30),
            # Dacă datele pot fi comparate cu __eq__, pune always_update=False
            # pentru a evita scrieri redundante în state machine
            always_update=True,
        )
        self.client = client

    async def _async_setup(self) -> None:
        """Pregătire inițială — apelat automat la async_config_entry_first_refresh."""
        # Aici poți face setup one-time: descoperire dispozitive, etc.
        self.devices = await self.client.get_devices()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch date de la API."""
        try:
            return await self.client.async_get_data()
        except AuthenticationError as err:
            # Oprește polling-ul și pornește reautentificarea
            raise ConfigEntryAuthFailed("Token expirat") from err
        except ConnectionError as err:
            raise UpdateFailed(
                f"Eroare comunicare cu API: {err}"
            ) from err
        except RateLimitError as err:
            # Dacă API-ul semnalizează backoff
            raise UpdateFailed(retry_after=60) from err
```

### Când NU ai nevoie de coordinator:

- Dacă dispozitivul trimite date prin push (websocket, MQTT), poți folosi
  coordinatorul fără `update_interval` și apelezi manual
  `coordinator.async_set_updated_data(new_data)`.
- Dacă ai o singură entitate cu un endpoint dedicat, poți implementa direct
  `async_update()` pe entitate — dar coordinatorul rămâne recomandat.

---

## 6. config_flow.py — Fluxul de Configurare

Config flow-ul permite utilizatorilor să configureze integrarea din UI.

```python
"""Config flow pentru integrarea domeniu_meu."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_API_KEY

from .const import DOMAIN

# Schema de date pentru formularul de configurare
DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Required(CONF_API_KEY): str,
    }
)


class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handler pentru config flow."""

    VERSION = 1
    # Mărește VERSION când modifici structura datelor stocate

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Pasul de configurare inițiat de utilizator."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Validare
            try:
                info = await self._test_connection(user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # noqa: BLE001
                errors["base"] = "unknown"
            else:
                # Previne duplicatele
                await self.async_set_unique_id(info["unique_id"])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=info["title"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=DATA_SCHEMA,
            errors=errors,
        )

    async def _test_connection(self, data: dict[str, Any]) -> dict[str, Any]:
        """Testează conexiunea cu dispozitivul/API-ul."""
        client = MyApiClient(host=data[CONF_HOST], api_key=data[CONF_API_KEY])
        device_info = await client.async_get_info()
        return {
            "title": device_info.name,
            "unique_id": device_info.serial,
        }
```

### Reguli importante:

- Setează mereu `unique_id` cu `async_set_unique_id()` — previne config entries duplicate.
- Apelează `_abort_if_unique_id_configured()` imediat după setarea unique_id.
- `VERSION` trebuie incrementat dacă schimbi structura datelor — implementează și
  o metodă de migrare.
- Erorile din `errors` dict trebuie mapate în `strings.json`.

---

## 7. strings.json și Traduceri

Fișierul `strings.json` definește textele afișate în UI:

```json
{
  "config": {
    "step": {
      "user": {
        "title": "Configurare Dispozitiv",
        "description": "Introdu datele de conectare.",
        "data": {
          "host": "Adresa IP sau hostname",
          "api_key": "Cheie API"
        },
        "data_description": {
          "host": "Exemplu: 192.168.1.100",
          "api_key": "Găsești cheia în setările dispozitivului"
        }
      }
    },
    "error": {
      "cannot_connect": "Nu mă pot conecta. Verifică adresa.",
      "invalid_auth": "Autentificare eșuată. Verifică cheia API.",
      "unknown": "Eroare neașteptată."
    },
    "abort": {
      "already_configured": "Dispozitivul este deja configurat."
    }
  }
}
```

Copiază conținutul identic în `translations/en.json`. Poți adăuga și `translations/ro.json`
pentru suport în limba română.

---

## 8. Platforme — Entități

Fiecare platformă (light, switch, sensor etc.) este un fișier Python separat.
Toate urmează același pattern de bază.

### 8.1. Pattern comun: async_setup_entry

Fiecare fișier de platformă trebuie să exporte funcția `async_setup_entry`:

```python
async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează entitățile din config entry."""
    coordinator = entry.runtime_data

    entities = [
        MyEntity(coordinator, device)
        for device in coordinator.data["devices"]
    ]
    async_add_entities(entities)
```

### 8.2. Clasă de bază CoordinatorEntity

Dacă folosești DataUpdateCoordinator (recomandat), entitățile trebuie să extindă
`CoordinatorEntity`. Aceasta setează automat `should_poll = False` și gestionează
update-urile.

```python
"""Entitate de bază pentru integrarea domeniu_meu."""
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import MyCoordinator


class MyBaseEntity(CoordinatorEntity[MyCoordinator]):
    """Clasă de bază pentru toate entitățile integrării."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: MyCoordinator, device_id: str) -> None:
        """Inițializează entitatea."""
        super().__init__(coordinator)
        self._device_id = device_id
        # unique_id obligatoriu pentru entity registry
        self._attr_unique_id = f"{DOMAIN}_{device_id}"

    @property
    def device_info(self) -> DeviceInfo:
        """Returnează informațiile despre dispozitiv."""
        return DeviceInfo(
            identifiers={(DOMAIN, self._device_id)},
            name=self.coordinator.data[self._device_id]["name"],
            manufacturer="Producătorul",
            model="Modelul",
            sw_version=self.coordinator.data[self._device_id].get("firmware"),
        )
```

### 8.3. Light Entity

```python
"""Platformă light pentru integrarea domeniu_meu."""
from __future__ import annotations

from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP_KELVIN,
    ATTR_HS_COLOR,
    ColorMode,
    LightEntity,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .entity import MyBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează entitățile light."""
    coordinator = entry.runtime_data
    async_add_entities(
        MyLight(coordinator, device_id)
        for device_id in coordinator.data
        if coordinator.data[device_id]["type"] == "light"
    )


class MyLight(MyBaseEntity, LightEntity):
    """Entitate light."""

    # Modurile de culoare suportate — OBLIGATORIU pentru integrări noi
    _attr_supported_color_modes = {ColorMode.HS, ColorMode.COLOR_TEMP}

    @callback
    def _handle_coordinator_update(self) -> None:
        """Actualizează starea din datele coordinatorului."""
        data = self.coordinator.data[self._device_id]
        self._attr_is_on = data["is_on"]
        self._attr_brightness = data.get("brightness")
        self._attr_hs_color = data.get("hs_color")
        self._attr_color_temp_kelvin = data.get("color_temp_kelvin")

        # Setează color_mode curent pe baza stării
        if data.get("color_temp_kelvin") is not None:
            self._attr_color_mode = ColorMode.COLOR_TEMP
        elif data.get("hs_color") is not None:
            self._attr_color_mode = ColorMode.HS
        else:
            self._attr_color_mode = ColorMode.UNKNOWN

        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Aprinde lumina."""
        params: dict[str, Any] = {}

        if ATTR_BRIGHTNESS in kwargs:
            params["brightness"] = kwargs[ATTR_BRIGHTNESS]
        if ATTR_HS_COLOR in kwargs:
            params["hs_color"] = kwargs[ATTR_HS_COLOR]
        if ATTR_COLOR_TEMP_KELVIN in kwargs:
            params["color_temp_kelvin"] = kwargs[ATTR_COLOR_TEMP_KELVIN]

        await self.coordinator.client.async_set_light(
            self._device_id, on=True, **params
        )
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stinge lumina."""
        await self.coordinator.client.async_set_light(
            self._device_id, on=False
        )
        await self.coordinator.async_request_refresh()
```

### Reguli light critice:

- Implementează MEREU `color_mode` și `supported_color_modes` — sunt obligatorii.
- `ColorMode` posibile: `ONOFF`, `BRIGHTNESS`, `COLOR_TEMP`, `HS`, `XY`, `RGB`,
  `RGBW`, `RGBWW`, `WHITE`.
- În `async_turn_on` primești UN SINGUR atribut de culoare (HA face conversia automată).
- Folosește `value_to_brightness` din `homeassistant.util.color` dacă trebuie să scalezi.

### 8.4. Switch Entity

```python
"""Platformă switch pentru integrarea domeniu_meu."""
from __future__ import annotations

from typing import Any

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .entity import MyBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează entitățile switch."""
    coordinator = entry.runtime_data
    async_add_entities(
        MySwitch(coordinator, device_id)
        for device_id in coordinator.data
        if coordinator.data[device_id]["type"] == "switch"
    )


class MySwitch(MyBaseEntity, SwitchEntity):
    """Entitate switch."""

    _attr_device_class = SwitchDeviceClass.SWITCH

    @callback
    def _handle_coordinator_update(self) -> None:
        """Actualizează starea."""
        self._attr_is_on = self.coordinator.data[self._device_id]["is_on"]
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Pornește switch-ul."""
        await self.coordinator.client.async_set_switch(self._device_id, True)
        self._attr_is_on = True
        self.async_write_ha_state()
        # SAU: await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Oprește switch-ul."""
        await self.coordinator.client.async_set_switch(self._device_id, False)
        self._attr_is_on = False
        self.async_write_ha_state()
```

### Diferența dintre switch și light:

- **Switch** = on/off pur (priză, releu, func. software). Device classes: `SWITCH`,
  `OUTLET`, `NONE`.
- **Light** = sursă de lumină cu posibile atribute (brightness, color).
- Dacă dispozitivul controlează o lumină, folosește MEREU `light`, chiar dacă e
  doar on/off — setează `supported_color_modes = {ColorMode.ONOFF}`.

### 8.5. Button Entity

Button-ul este o entitate „stateless" — nu are stare on/off, doar execută o acțiune
când e apăsat.

```python
"""Platformă button pentru integrarea domeniu_meu."""
from __future__ import annotations

from homeassistant.components.button import ButtonDeviceClass, ButtonEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .entity import MyBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează entitățile button."""
    coordinator = entry.runtime_data
    async_add_entities([
        MyRestartButton(coordinator, device_id)
        for device_id in coordinator.data
    ])


class MyRestartButton(MyBaseEntity, ButtonEntity):
    """Buton de restart dispozitiv."""

    _attr_device_class = ButtonDeviceClass.RESTART
    _attr_translation_key = "restart_device"

    def __init__(self, coordinator, device_id: str) -> None:
        """Inițializează."""
        super().__init__(coordinator, device_id)
        self._attr_unique_id = f"{device_id}_restart"

    async def async_press(self) -> None:
        """Acțiunea executată la apăsare."""
        await self.coordinator.client.async_restart(self._device_id)
```

### Când folosești button vs switch:

- **Button** = acțiune fără stare, foc-și-uită (restart, sincronizare, identify).
- **Switch** = ceva ce rămâne pornit sau oprit.

### 8.6. Sensor Entity

```python
"""Platformă sensor pentru integrarea domeniu_meu."""
from __future__ import annotations

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import MyConfigEntry
from .entity import MyBaseEntity


async def async_setup_entry(
    hass: HomeAssistant,
    entry: MyConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Configurează entitățile sensor."""
    coordinator = entry.runtime_data
    async_add_entities(
        MyTemperatureSensor(coordinator, device_id)
        for device_id in coordinator.data
        if "temperature" in coordinator.data[device_id]
    )


class MyTemperatureSensor(MyBaseEntity, SensorEntity):
    """Sensor de temperatură."""

    _attr_device_class = SensorDeviceClass.TEMPERATURE
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
    _attr_suggested_display_precision = 1

    def __init__(self, coordinator, device_id: str) -> None:
        """Inițializează."""
        super().__init__(coordinator, device_id)
        self._attr_unique_id = f"{device_id}_temperature"

    @callback
    def _handle_coordinator_update(self) -> None:
        """Actualizează valoarea."""
        self._attr_native_value = self.coordinator.data[self._device_id]["temperature"]
        self.async_write_ha_state()
```

### Reguli sensor critice:

- Setează MEREU `device_class` dacă există unul potrivit — afectează unitatea,
  iconul și afișarea.
- Setează `state_class` pentru statistici pe termen lung:
  - `MEASUREMENT` — valoare instantanee (temperatură, umiditate)
  - `TOTAL` — valoare cumulativă cu resetări (contor energie zilnic)
  - `TOTAL_INCREASING` — valoare strict crescătoare (contor total energie)
- Folosește `native_unit_of_measurement` + `native_value` — HA face conversia.

### 8.7. Binary Sensor

```python
"""Platformă binary_sensor."""
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)


class MyDoorSensor(MyBaseEntity, BinarySensorEntity):
    """Senzor binar de ușă."""

    _attr_device_class = BinarySensorDeviceClass.DOOR

    @callback
    def _handle_coordinator_update(self) -> None:
        self._attr_is_on = self.coordinator.data[self._device_id]["door_open"]
        self.async_write_ha_state()
```

### 8.8. Entity Descriptions (pentru entități multiple similare)

Când ai multe entități de același tip (ex: 10 senzori diferiți), folosește
`EntityDescription` pentru a le defini declarativ:

```python
from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, PERCENTAGE


@dataclass(frozen=True, kw_only=True)
class MySensorDescription(SensorEntityDescription):
    """Descriere extinsă pentru senzorii mei."""
    value_fn: Callable[[dict], float | None]


SENSOR_DESCRIPTIONS: tuple[MySensorDescription, ...] = (
    MySensorDescription(
        key="temperature",
        translation_key="temperature",
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        value_fn=lambda data: data.get("temperature"),
    ),
    MySensorDescription(
        key="humidity",
        translation_key="humidity",
        device_class=SensorDeviceClass.HUMIDITY,
        state_class=SensorStateClass.MEASUREMENT,
        native_unit_of_measurement=PERCENTAGE,
        value_fn=lambda data: data.get("humidity"),
    ),
)
```

---

## 9. services.yaml — Acțiuni Custom

Dacă integrarea expune acțiuni (servicii) proprii, le descrii în `services.yaml`:

```yaml
# services.yaml
set_mode:
  target:
    entity:
      domain: light
      integration: domeniu_meu
  fields:
    mode:
      required: true
      example: "party"
      selector:
        select:
          options:
            - "normal"
            - "party"
            - "sleep"
            - "movie"

sync_devices:
  # Acțiune fără target — se aplică la nivel de config entry
  fields:
    config_entry_id:
      required: true
      selector:
        config_entry:
          integration: domeniu_meu
```

### Înregistrarea acțiunilor în __init__.py:

```python
from homeassistant.helpers import config_validation as cv
import voluptuous as vol


async def async_setup_entry(hass, entry):
    # ... setup normal ...

    # Înregistrează acțiune la nivel de entitate
    platform = entity_platform.async_get_current_platform()
    platform.async_register_entity_service(
        "set_mode",
        {vol.Required("mode"): cv.string},
        "async_set_mode",  # numele metodei de pe entitate
    )

    # SAU acțiune la nivel de integrare (nu entitate)
    async def handle_sync_devices(call):
        """Gestionează apelul de sincronizare."""
        # Logica ta aici
        await coordinator.client.async_sync()
        await coordinator.async_request_refresh()

    hass.services.async_register(
        DOMAIN, "sync_devices", handle_sync_devices
    )
```

### Niveluri de targetare a acțiunilor:

- **Entity level** — acțiunea operează pe o entitate specifică. Folosește
  `entity_platform.async_register_entity_service()`.
- **Device level** — acțiunea operează pe un dispozitiv. Folosește `device_id` ca field.
- **Config entry level** — acțiunea operează pe instanța integrării. Folosește
  `config_entry_id` ca field.

Principiul: targetează lucrul pe care acțiunea chiar operează.

---

## 10. Brand

Pentru HACS și afișarea în UI, creează directorul `brand/`:

```
brand/
├── icon.png    # 256×256, PNG, fundal transparent, pictogramă simplă
└── logo.png    # 256×256, PNG, logo-ul complet
```

Pentru integrări core, brand-urile se trimit în repository-ul separat
`home-assistant/brands`. Pentru custom_components, le incluzi direct în
directorul integrării.

---

## 11. Options Flow (Opțiuni Post-Configurare)

Permite utilizatorilor să modifice opțiuni după instalare fără a reconfigura:

```python
# În config_flow.py, adaugă pe clasa ConfigFlow:

class MyConfigFlow(ConfigFlow, domain=DOMAIN):
    # ... pasul user ...

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Returnează handler-ul de options flow."""
        return MyOptionsFlow()


class MyOptionsFlow(OptionsFlowWithReload):
    """Handler options flow — cu reload automat la schimbare."""

    async def async_step_init(self, user_input=None):
        """Pasul inițial al options flow."""
        if user_input is not None:
            return self.async_create_entry(data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "scan_interval",
                        default=self.config_entry.options.get(
                            "scan_interval", 30
                        ),
                    ): vol.All(int, vol.Range(min=10, max=3600)),
                }
            ),
        )
```

Dacă integrarea trebuie reîncărcată după schimbarea opțiunilor, extinde
`OptionsFlowWithReload` în loc de `OptionsFlow` — face reload automat.

---

## 12. Diagnostics

Permite utilizatorilor să descarce date de diagnosticare utile la debug:

```python
# diagnostics.py
"""Diagnostics pentru integrarea domeniu_meu."""
from __future__ import annotations
from typing import Any
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ConfigEntry
) -> dict[str, Any]:
    """Returnează diagnosticele integrării."""
    coordinator = entry.runtime_data
    return {
        "config_entry_data": dict(entry.data),  # HA redactează automat cheile sensibile
        "coordinator_data": coordinator.data,
    }
```

---

## 13. Checklist Finală

Înainte de a publica integrarea, verifică:

1. **manifest.json** are `version`, `domain`, `config_flow: true`, `iot_class` corecte.
2. **unique_id** setat pe TOATE entitățile — fără unique_id, entitatea nu apare în
   entity registry.
3. **device_info** setat pe entități — fără el, entitățile nu apar grupate sub
   un dispozitiv.
4. **has_entity_name = True** pe entități — pattern-ul modern de denumire.
5. **CoordinatorEntity** folosit ca bază, nu Entity direct.
6. **should_poll = False** asigurat (CoordinatorEntity face asta automat).
7. **strings.json** conține TOATE erorile și textele referite în config flow.
8. **translations/en.json** există și e identic cu strings.json.
9. **Niciun import blocat** — tot ce face I/O trebuie să fie `async` sau rulat
   cu `hass.async_add_executor_job()`.
10. **ConfigEntryNotReady** ridicat dacă dispozitivul nu răspunde la setup.
11. **async_unload_entry** implementat corect — curăță listeners, închide conexiuni.
12. **Teste** — cel puțin teste pentru config flow (obligatoriu pentru core).

---

## 14. Referințe Oficiale

Consultă mereu documentația oficială actualizată:

- Ghid general: https://developers.home-assistant.io/docs/creating_component_index/
- Structura fișierelor: https://developers.home-assistant.io/docs/creating_integration_file_structure/
- Manifest: https://developers.home-assistant.io/docs/creating_integration_manifest/
- Config Flow: https://developers.home-assistant.io/docs/config_entries_config_flow_handler/
- Options Flow: https://developers.home-assistant.io/docs/config_entries_options_flow_handler/
- Fetching Data / Coordinator: https://developers.home-assistant.io/docs/integration_fetching_data/
- Entități (generic): https://developers.home-assistant.io/docs/core/entity/
- Light: https://developers.home-assistant.io/docs/core/entity/light/
- Switch: https://developers.home-assistant.io/docs/core/entity/switch/
- Button: https://developers.home-assistant.io/docs/core/entity/button/
- Sensor: https://developers.home-assistant.io/docs/core/entity/sensor/
- Services / Acțiuni: https://developers.home-assistant.io/docs/dev_101_services/
- Quality Scale: https://developers.home-assistant.io/docs/core/integration-quality-scale/
- Exemple: https://github.com/home-assistant/example-custom-config/

---

## 15. Greșeli Frecvente și Antipattern-uri

Aceste greșeli revin obsesiv în integrările custom. Evită-le:

- **Nu folosi `hass.data` pentru stocare** — folosește `entry.runtime_data`.
  `hass.data` e un pattern vechi care duce la memory leaks la unload.
- **Nu hardcoda `entity_id`** — folosește `unique_id` + entity registry.
- **Nu folosi `async_forward_entry_setup`** (singular) — e depreciat. Folosește
  `async_forward_entry_setups` (plural, acceptă lista de platforme).
- **Nu pune logică blocantă în event loop** — orice I/O (request HTTP, citire fișier)
  trebuie `async` sau wrapped cu `hass.async_add_executor_job()`.
- **Nu ignora `async_unload_entry`** — fără el, integrarea nu se poate descărca
  corect, iar reîncărcarea din UI va eșua.
- **Nu omite `_attr_has_entity_name = True`** — fără el, numele entității va include
  redundant numele dispozitivului.
- **Nu crea entități fără `unique_id`** — fără el, utilizatorul nu poate personaliza
  entitatea, nu poate dezactiva entitatea, și entitatea nu supraviețuiește restart-ului.
- **Nu folosi `supported_features` pentru color modes** — pattern-ul vechi cu
  flags a fost depreciat. Folosește `supported_color_modes` și `color_mode`.
