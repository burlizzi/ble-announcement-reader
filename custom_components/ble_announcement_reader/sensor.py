"""BLE Announcement Reader sensor platform."""
import logging
from typing import Any, Dict, Optional
from bleak import BleakScanner
from bleak.backends.device import BLEDevice
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

class BLEAnnouncementSensor(SensorEntity):
    """Represent a BLE announcement sensor."""
    
    def __init__(self, device_address: str, manufacturer_ids: list = None):
        """Initialize the sensor."""
        self._device_address = device_address
        self._manufacturer_ids = manufacturer_ids or []
        self._attr_name = f"BLE {device_address}"
        self._attr_unique_id = f"ble_sensor_{device_address}"
        self._attr_unit_of_measurement = None
        self._state = None
        self._extra_state_attributes: Dict[str, Any] = {}
        
    @property
    def state(self):
        """Return the current state."""
        return self._state
    
    @property
    def extra_state_attributes(self) -> Dict[str, Any]:
        """Return extra state attributes."""
        return self._extra_state_attributes
    
    async def async_update(self):
        """Update the sensor by scanning for BLE announcements."""
        try:
            scanner = BleakScanner()
            devices = await scanner.discover()
            
            for device in devices:
                if device.address.upper() == self._device_address.upper():
                    await self._parse_ble_announcement(device)
                    break
        except Exception as err:
            _LOGGER.error(f"Error scanning BLE devices: {err}")
    
    async def _parse_ble_announcement(self, device: BLEDevice):
        """Parse BLE announcement data."""
        self._extra_state_attributes = {
            "address": device.address,
            "name": device.name or "Unknown",
            "rssi": 0,
            "connectable": 1,
            "tx_power": None,
        }
        _LOGGER.debug(f"Parsed BLE announcement from {device.address}: {self._extra_state_attributes}")
    
        # Parse manufacturer data
        if hasattr(device, 'metadata') and device.metadata:
            metadata = device.metadata
            
            if hasattr(metadata, 'manufacturer_data') and metadata.manufacturer_data:
                self._extra_state_attributes["manufacturer_data"] = {}
                for mfg_id, data in metadata.manufacturer_data.items():
                    mfg_hex = data.hex() if isinstance(data, bytes) else data
                    self._extra_state_attributes["manufacturer_data"][str(mfg_id)] = mfg_hex
                    
                    # Estrai valore in base al produttore
                    self._state = self._extract_value_from_manufacturer_data(mfg_id, data)
            
            # Parse service data
            if hasattr(metadata, 'service_data') and metadata.service_data:
                self._extra_state_attributes["service_data"] = {
                    str(uuid): data.hex() if isinstance(data, bytes) else data
                    for uuid, data in metadata.service_data.items()
                }
            
            # Parse service UUIDs
            if hasattr(metadata, 'service_uuids') and metadata.service_uuids:
                self._extra_state_attributes["service_uuids"] = list(metadata.service_uuids)
        
        _LOGGER.debug(f"Parsed BLE announcement from {device.address}: {self._extra_state_attributes}")
    
    def _extract_value_from_manufacturer_data(self, mfg_id: int, data: bytes) -> Optional[str]:
        """Extract value from manufacturer data based on manufacturer ID.
        
        Questo è un esempio per il tuo dispositivo (1744 = 0x6D0):
        Formato: 01 20 68 ac 58 89 a9 c0 a9 01 00 00 00 00 00 00 00 02 03 00
        """
        if mfg_id == 0x6D0 or mfg_id == 0xffd0:  # Esempio per il tuo dispositivo
            try:
                hex_str = data.hex() if isinstance(data, bytes) else data
                _LOGGER.info(f"Manufacturer data (1744): {hex_str}")
                
                # Estrai i byte specifici in base alla struttura
                if len(data) >= 2:
                    value = f"0x{hex_str[:4]}"
                    return value
            except Exception as err:
                _LOGGER.error(f"Error parsing manufacturer data: {err}")
        
        return None

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up BLE sensors from a config entry."""
    device_addresses = entry.data.get("device_addresses", "").split(",")
    device_addresses = [addr.strip() for addr in device_addresses if addr.strip()]
    
    manufacturer_ids = entry.data.get("manufacturer_ids", "").split(",")
    manufacturer_ids = [int(id.strip()) for id in manufacturer_ids if id.strip().isdigit()]
    
    entities = [
        BLEAnnouncementSensor(address, manufacturer_ids)
        for address in device_addresses
    ]
    
    async_add_entities(entities, update_before_add=True)
