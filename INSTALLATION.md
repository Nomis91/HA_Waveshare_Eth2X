# Installation Guide - Waveshare RS485-to-ETH Home Assistant Integration

## Prerequisites

Before installing this integration, ensure you have:

- **Home Assistant**: Version 2023.12.0 or newer (install from https://www.home-assistant.io)
- **Waveshare RS485-to-ETH Device**: 
  - Model: RS485 to Ethernet converter
  - Default TCP port: 8234
  - Network connectivity verified
- **Solar Inverter**: Connected to the RS485 gateway
- **Network**: Home Assistant must be able to reach the gateway via network

## Step 1: Verify Network Connectivity

Before installation, test connectivity to your Waveshare device:

### From Linux/macOS:
```bash
# Test TCP connection to gateway
nc -zv <gateway_ip> 8234
# Expected output: Connection successful
```

### From Windows (PowerShell):
```powershell
# Test TCP connection to gateway
Test-NetConnection -ComputerName <gateway_ip> -Port 8234
# Expected: TcpTestSucceeded should be True
```

## Step 2: Install the Integration

### Option A: Automatic Installation (HACS)
If using HACS (Home Assistant Community Store):

1. Open Home Assistant
2. Go to **HACS → Integrations**
3. Click **+ Create Integration**
4. Search for "Waveshare RS485-to-ETH"
5. Click **Install**
6. Restart Home Assistant

### Option B: Manual Installation

1. Download the integration files to your computer
2. Connect to your Home Assistant system (via SSH or file browser)
3. Navigate to: `custom_components/` folder
4. Create folder: `waveshare_rs485toeth/`
5. Copy all integration files to this folder
6. Directory structure should be:
   ```
   ~/.homeassistant/custom_components/waveshare_rs485toeth/
   ├── __init__.py
   ├── config_flow.py
   ├── const.py
   ├── manifest.json
   ├── strings.json
   ├── core/
   ├── coordinators/
   ├── devices/
   ├── errors/
   ├── health/
   └── platforms/
   ```
7. Restart Home Assistant

## Step 3: Enable the Integration

After installation:

1. Open Home Assistant web interface
2. Go to **Settings → Devices & Services → Integrations**
3. Click the **+ Create Integration** button
4. Search for "Waveshare RS485-to-ETH Gateway"
5. Click to select the integration
6. Follow the 3-step configuration wizard (see Configuration Guide below)

## Step 4: Verify Installation

Once configured:

1. Check **Settings → Devices & Services** for a new device entry
2. Click the device to see created entities
3. Look for sensors like:
   - `sensor.waveshare_rs485toeth_*_solar_pv1_power`
   - `binary_sensor.waveshare_rs485toeth_*_connection_status`
   - `sensor.waveshare_rs485toeth_*_response_time`
4. Entities should update regularly (default: every 30 seconds)

## Waveshare Device Setup

### Network Configuration

1. **Physical Setup**:
   - Connect RS485 device to solar inverter via RS485 A/B cables
   - Connect Waveshare to network (Ethernet)
   - Ensure proper RS485 line termination (120Ω resistor at each end)

2. **Find Device IP**:
   - Access your router web interface
   - Look for "Waveshare" or unknown DHCP clients
   - Or use network scanning tools:
     ```bash
     nmap -p 8234 192.168.1.0/24
     ```

3. **Set Static IP** (recommended):
   - Access Waveshare web interface (http://<gateway_ip>)
   - Configure static IP to prevent connection issues
   - Note the IP address for Home Assistant configuration

### RS485 Wiring

Proper RS485 termination is critical:

```
     Terminal 1         Terminal 2
     (Waveshare)      (Inverter or far end)
        ┌─────────────────────┐
   A ──┤├─────────────────────┤├── A
        │ RS485 Cable (twisted)│
   B ──┤├─────────────────────┤├── B
        │                     │
   GND─┤├─────────────────────┤├─ GND
        │                     │
        │  120Ω Terminator    │
        │  (if at far end)    │
        └─────────────────────┘
```

**Important**: Install 120Ω termination resistors:
- Between A and B at Waveshare device
- Between A and B at furthest inverter or end of line
- Do NOT add termination in the middle of the line

## Troubleshooting Installation

### Integration Not Appearing
- Verify integration files are in correct location
- Check file permissions (should be readable)
- Restart Home Assistant completely (not just reload)
- Check Home Assistant logs for errors:
  - **Settings → System → Logs**

### Connection Test Fails
- Verify gateway IP address is correct
- Check network connectivity:
  ```bash
  ping <gateway_ip>
  ```
- Verify port 8234 is open:
  ```bash
  telnet <gateway_ip> 8234
  ```
- Check Waveshare device is powered on
- Review Waveshare device logs if available

### Device Discovery Fails
- Ensure at least one inverter is connected and powered on
- Verify RS485 wiring is correct
- Check Modbus slave IDs are in valid range (typically 1-10)
- Try manual device configuration if auto-discovery fails

### Entities Not Creating
- Check integration debug logs
- Verify device type was correctly detected
- Ensure device is in "healthy" state (not offline)
- Try reloading the integration

## Next Steps

1. **Configuration**: See [CONFIGURATION.md](CONFIGURATION.md) for detailed setup options
2. **Supported Devices**: See [SUPPORTED_DEVICES.md](SUPPORTED_DEVICES.md) for compatibility information
3. **Troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues

## Support

If you encounter issues:

1. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) first
2. Enable debug logging to collect detailed diagnostic information
3. Review Home Assistant system logs
4. Check Waveshare device status (power, network connectivity)
5. Verify physical RS485 connections and termination

## Rollback

To remove the integration:

1. Go to **Settings → Devices & Services → Integrations**
2. Find "Waveshare RS485-to-ETH Gateway"
3. Click the three-dot menu
4. Select **Delete**
5. Confirm deletion

To uninstall completely:
1. Delete `~/.homeassistant/custom_components/waveshare_rs485toeth/` folder
2. Restart Home Assistant
