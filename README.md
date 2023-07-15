# Lumiax MPPT BT solar regulator - unofficial repository

## Description
This repo was made for reverse engineering of Lumiax MPPT BT solar regulator. It comes with various brand names:
- Volt Polska
- Lumiax
- others, which I don't know yet...

It looks like one of these:

![alt text](https://raw.githubusercontent.com/majki09/lumiax_solar_bt/main/docs/volt_polska.jpg "VOLT Polska variant")

### What we can do
- read current parameters (Voltage, Current, Wattage for PV and LOAD; Battery SoC (%), temperature),
- toggle OUTPUT (send appropriate command from command table),
- send values to domoticz (soon).

⚠️All scripts here was made by manual reverse engineering of it's Android app communication. There was no any official resources, hence information provided here may be incomplete and comes with **no warranty**.

# Need list
## Hardware
- any PC with USB and python3 (this was tested on Raspberry 3)
- preffered USB Bluetooth dongle with Low-Energy (LE) support.

## Software
- python3
- [pygatt](https://github.com/peplin/pygatt)

# Installation
1. Clone this repo.
2. Get your regulator's BT MAC

` sudo hcitool lescan `

3. Get your adapter designator

` sudo hcitool dev `

Make sure you will be using USB BT dongle.

# Usage
1. Run the script
   
` python3 ./lumiax_bt.py hci1 04:7F:0E:12:34:56 fe043030002bab15 `

where:
- `hci1` - your adapter's designator,
- `04:7F:0E:12:34:56` - your Lumiax's BT MAC,
- `fe043030002bab15` - GET STATUS command (see command table).

you should get something like:

```
pi@rasp:~ $ python3 ./lumiax_bt.py hci1 04:7F:0E:12:34:56 fe043030002bab15
adapter started
connected
subscribed
Data: 0104560001000004b00003000d00000ce40c8000
message_length=86
Data detected. Next data will be concated
Data: 0700000000000000000000000000000000000000
Data: 0000000000001a04a6002b01ff00000000000000
Data: 0000000da20010022e0000000100010000000200
Data: 0200000032000000004ecf
Full data fetched. Concat finished.
batt SoC =26
PV V=34.9
PV A=0.16
PV W=   5.58
PV TOTAL=       0.01    kWh
BATT V=11.9
BATT A=0.43
BATT temp=32.0
LOAD V=0.0
LOAD A=0.0
LOAD W= 0.0
LOAD TOTAL=     0.02    kWh
Script finished
adapter stopped
```

# Rev-eng
## Command table
| Command | Description |
|---------|-------------|
| `fe043030002bab15` | get status |
| `fe0500000000d9c5` | disable OUTPUT |
| `fe050000ff009835` | enable OUTPUT |
| `fe039017000a4cc6` | get time/date |
| `fe043061003d7b0a` | get PV history |
| `fe0430aa0078cb07` | ? |
| `fe043130003d2b27` | get LOAD history |
| `fe039021001aad04` | ? |
| `fe038ff0001dbb2b` | ? |
| `fe03902b003c0cdc` | ? |

# Issues
## Raspberry Pi issues
When you randomly getting problems with built-in BT adapter of your RPi and getting this error:

` Can't init device hci0: Device or resource busy (16)`

you may need to use another USB BT adapter.

# Links
- https://github.com/Freeyourgadget/Gadgetbridge/wiki/BT-Protocol-Reverse-Engineering
- https://stackoverflow.com/questions/15657007/bluetooth-low-energy-listening-for-notifications-indications-in-linux
- https://www.instructables.com/Reverse-Engineering-Smart-Bluetooth-Low-Energy-Dev/
- https://reverse-engineering-ble-devices.readthedocs.io/en/latest/protocol_reveng/00_protocol_reveng.html
