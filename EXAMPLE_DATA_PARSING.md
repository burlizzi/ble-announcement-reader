# Guida al Parsing dei Dati BLE

## Formato dati del tuo dispositivo (Manufacturer ID: 1744)

Il tuo dispositivo invia i seguenti dati:

```
Hex: 012068ac5889a9c0a90100000000000000020300
Bytes: 01 20 68 ac 58 89 a9 c0 a9 01 00 00 00 00 00 00 00 02 03 00
```

### Struttura (ipotesi di parsing):

| Byte(i) | Descrizione | Valore esempio |
|---------|-------------|---------|
| 0 | Tipo dato | 01 |
| 1 | Lunghezza/Flag | 20 |
| 2-7 | MAC Address | 68 ac 58 89 a9 c0 |
| 8 | C0 (?) | c0 |
| 9 | A9 (?) | a9 |
| 10 | Battery/State | 01 |
| 11-17 | Reserved | 00 00 00 00 00 00 00 |
| 18 | Status byte | 02 |
| 19 | Valore 1 | 03 |
| 20 | Valore 2 | 00 |

## Come personalizzare il parsing

Modifica la funzione `_extract_value_from_manufacturer_data` in `sensor.py` per estrarre i valori specifici:

```python
def _extract_value_from_manufacturer_data(self, mfg_id: int, data: bytes) -> Optional[str]:
    if mfg_id == 1744:
        # Leggi byte specifici
        if len(data) >= 20:
            battery = data[10]
            status = data[18]
            value1 = data[19]
            value2 = data[20]
            
            self._extra_state_attributes["battery"] = battery
            self._extra_state_attributes["status"] = status
            
            return f"{value1}/{value2}"
    
    return None
```

## Test

Usa il seguente comando per testare il parsing:

```python
data = bytes.fromhex("012068ac5889a9c0a90100000000000000020300")
print(f"Byte 10 (battery): {data[10]:02x}")
print(f"Byte 18 (status): {data[18]:02x}")
print(f"Byte 19 (value1): {data[19]:02x}")
print(f"Byte 20 (value2): {data[20]:02x}")
```