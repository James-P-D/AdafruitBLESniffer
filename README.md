# AdafruitBLESniffer
Bluetooth sniffer for the Adafruit Bluefruit device in Python

![Screenshot](https://github.com/James-P-D/AdafruitBLESniffer/blob/main/screenshot.gif)

## Introduction

After purchasing the [Bluefruit device from Adafruit](https://www.adafruit.com/product/2267), I decided to create a very small program for logging BLE traffic.

![Adafruit Bluefruit](https://github.com/James-P-D/AdafruitBLESniffer/blob/main/Buefruit.jpg)

## Running

The Adafruit Bluefruit device communicates over a COM port on Windows, so we need to install `pyserial`:

```
pip install pyserial
```

Also note the program uses the SnifferAPI library from Adafruit:

[https://github.com/adafruit/Adafruit_BLESniffer_Python/tree/master/SnifferAPI](https://github.com/adafruit/Adafruit_BLESniffer_Python/tree/master/SnifferAPI)

Use the `-h` parameter to see the usage for the script:

```
c:\AdafruitBLESniffer>python main.py -h
usage: main.py [-h] [-l] -c COM port [-n [follow name]]

Process some integers.

options:
  -h, --help        show this help message and exit
  -l                List known BLE devices
  -c COM port       COM port for Adafruit Bluefruit device
  -n [follow name]  BLE device name to follow
```

We can use `-c` to specify the COM port our BlueFruit device is plugged into, and `-l` to list all known BLE devices:

```
c:\AdafruitBLESniffer>python main.py -c COM16 -l
80:e1:26:6d:30:48:00 "Control H0lwh1n"
5b:4b:63:1d:a5:a2:01
36:86:be:54:a4:18:01
40:37:ec:fc:c8:cf:01
ec:81:93:2a:e4:94:00 ""
79:f9:f9:39:87:4d:01
38:6f:f9:9d:9d:54:01
86:a9:3e:33:8e:1a:00
3b:99:60:86:d9:bc:01
04:b9:e3:12:60:8d:00
44:87:bd:28:9d:85:01
78:bd:bc:40:c2:57:00
4f:b9:9a:8b:c8:2c:01
47:50:c5:bb:1f:a4:01
00:a0:50:d7:19:05:00 "AL1905<Dimplex>"
d0:d2:b0:a0:ed:f3:00
41:55:bf:4d:4a:26:01
82:77:16:b9:5b:db:00 "Redmi Watch 2 Lite 5BDB"
c4:67:5a:0c:5e:25:01
5e:36:79:53:79:c8:01
cb:53:fd:81:5f:9a:01
d2:9a:8c:dd:c2:8f:01
e1:b1:e5:79:40:e1:01
e6:0e:8e:31:57:f0:01
20:44:41:76:51:3c:00 "P243 SkyQ LC103"
ee:78:5e:44:ef:1d:01
00:a0:50:c1:29:55:00 "AL2955<Dimplex>"
ed:35:d3:e8:cd:73:01
46:94:8d:04:39:51:01
52:db:3f:b5:61:fb:01
```

We can then either get all packets for a particular device, for example my [Flipper Zero](https://flipperzero.one/) which is called `H0lwh1n` by using the `-n` parameter:

```
c:\AdafruitBLESniffer>python main.py -c COM16 -n "Control H0lwh1n"
name: "Control H0lwh1n"
addr: 80:e1:26:6d:30:48:00
06 34 01 58 88 06 0a 01 26 4a 00 00 b9 76 01 00 | .4.X....&J..¹v..
d6 be 89 8e 00 21 48 30 6d 26 e1 80 02 01 06 10 | Ö¾...!H0m&á.....
09 43 6f 6e 74 72 6f 6c 20 48 30 6c 77 68 31 6e | .Control H0lwh1n
03 02 12 18 02 0a 00 63 2b 03                   | .......c+.

[...]
```

Note that packets matching the `-n` parameter will appear in blue, malformed packets will appear in red, and all other valid packets will appear in green.

Finally we can omit the `-n` parameter altogether to see all packets:

```
c:\AdafruitBLESniffer>python main.py -c COM16
```