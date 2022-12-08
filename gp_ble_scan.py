devices: Dict[str, BleakDevice] = {}
#Scan callback to also catch nonconnectable scan responses
def _scan_callback(device: BleakDevice, _: Any) -> None:
    #add to the dict if not unknown
    if device.name != "Unknown" and device.name is not None:
        devices[device.name] = device

#now deisover and add connectable adertisments
for device in await BleakScanner.discover(timeout=5, detection_callback=_scan_callback):
    if device.name != "Unknown" and device.name is not None:
        devices[device.name] = device