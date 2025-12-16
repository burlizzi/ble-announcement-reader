# BLE Announcement Reader

Un'integrazione Home Assistant per leggere e analizzare i dati dei BLE announcement.

## Funzionalità

- Scansione BLE in background
- Parsing dei dati manufacturer
- Parsing dei dati service
- Estrazione valori in base alla struttura dei dati
- Sensore con attributi estesi

## Installazione

1. Clona il repository nella cartella `custom_components` di Home Assistant:
   ```bash
   git clone https://github.com/burlizzi/ble-announcement-reader.git \
   ~/.homeassistant/custom_components/ble_announcement_reader
   ```

2. Riavvia Home Assistant

3. Aggiungi l'integrazione tramite UI o YAML

## Configurazione

### Via Config Flow (UI)
- Vai a Settings > Devices & Services
- Clicca "Create Integration"
- Seleziona "BLE Announcement Reader"
- Inserisci gli indirizzi MAC dei dispositivi (separati da virgola)
- Inserisci i manufacturer IDs da monitorare (opzionale)

### Esempio di configurazione YAML
```yaml
ble_announcement_reader:
  name: "BLE Sensor"
  device_addresses: "A9:89:58:AC:68:20,XX:XX:XX:XX:XX:XX"
  manufacturer_ids: "1744,2652"
```

## Formato dati supportati

L'integrazione supporta il seguente formato di BLE announcement:

```json
{
  "name": "A9:89:58:AC:68:20",
  "address": "A9:89:58:AC:68:20",
  "rssi": -72,
  "manufacturer_data": {
    "1744": "012068ac5889a9c0a90100000000000000020300"
  },
  "service_data": {},
  "service_uuids": ["0000ffd0-0000-1000-8000-00805f9b34fb"],
  "source": "A4:E8:8D:08:20:99",
  "connectable": true,
  "time": 1765915105.1249456,
  "tx_power": null
}
```

## Attributi del sensore

Ogni sensore fornisce i seguenti attributi:

- `address`: Indirizzo MAC del dispositivo
- `name`: Nome del dispositivo
- `rssi`: Signal strength (-dBm)
- `manufacturer_data`: Dati manufacturer in formato hex
- `service_data`: Dati service in formato hex
- `service_uuids`: Lista di UUID del servizio
- `connectable`: Se il dispositivo è connettibile
- `tx_power`: Potenza trasmissione (se disponibile)

## Personalizzazione

Per aggiungere il parsing di nuovi manufacturer ID, modifica il metodo `_extract_value_from_manufacturer_data` in `sensor.py`:

```python
def _extract_value_from_manufacturer_data(self, mfg_id: int, data: bytes) -> Optional[str]:
    if mfg_id == 0xYOUR_ID:
        # Implementa la logica di parsing
        pass
```

## License

MIT

## Author

@burlizzi