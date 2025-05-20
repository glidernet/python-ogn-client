# About this document
With version 2, the regex-based parser core has been replaced by a new Rust-based parser.
This document outlines the background and the resulting changes.

# Background
This parser, which was originally implemented entirely in native Python, has existed since 2016.
Over time, several issues have emerged:
1. Although the APRS format is extensively documented, compliance with the format is not enforced (e.g., it's possible to use illegal APRS callsigns like "D-1234" or invalid positions such as |lat| > 90 or |lon| > 180).
2. The APRS comment field, used by OGN for additional information (signal strength, software version, CPU load, etc.), is not standardized. In practice, new fields are added or changed sporadically—typically without prior discussion.
3. Similarly, new `dst_call`s are occasionally introduced, again usually without prior discussion. This means the parser must be retroactively adjusted to accommodate them.
4. To maximize performance, the original parser used (precompiled) regular expressions. Since the regex used depended on the `dst_call`, the number of regexes was substantial. Additionally, regex patterns are not very intuitive to read.
5. Even with regex optimization, the parser’s throughput was limited to around 100,000 beacons per minute on a Raspberry Pi. On thermally active days, this rate can be significantly exceeded, making improved performance desirable.

# Solution
To solve the above-mentioned problems, the parser was completely rewritten. For performance reasons, the Rust language was used:
[ogn-parser-rs](https://github.com/Meisterschueler/ogn-parser-rs).
Python bindings were created using [Maturin](https://github.com/PyO3/maturin) and [pythonize](https://github.com/davidhewitt/pythonize).
These bindings are compiled for all major architectures:

- Linux (x86_64, x86, aarch64, armv7, s390x, ppc64le)
- musllinux (x86_64, x86, aarch64, armv7)
- Windows (x64, x86)
- macOS (x86_64, aarch64)

They are published on PyPI and can be installed using `pip install ogn_parser`.
Within Rust, the parser is over 11x faster than the regex-based approach.
In Python, it is still 3.5x faster than the regex parser. To keep differences between the regex parser and the Rust parser minimal, some calculations (e.g., true timestamp calculation and computation of distance and bearing to the receiver) are still performed in Python.
This reduces the performance advantage to 2x. In the future, these calculations can also be moved to Rust to fully realize the potential 3.5x speedup.

# Consequences
Since all beacons are now parsed by a single parser that no longer considers `dst_call`, the results may differ from the previous parser.

## Fundamental differences
1. APRS comments from positions and statuses are split into words (separated by spaces). Unparsable parts of the comment are joined (with spaces) and assigned to the attribute user_comment.
2. The raw APRS comment is no longer returned.
3. The SSID in an APRS callsign must conform to APRS standards, i.e., it must be numeric.
4. Elements with an empty string ("") or None are not returned.

## Beacon-specific differences
The differences between the Rust parser and the old parser are analyzed using the example beacons stored at [ogn-aprs-protocol](https://github.com/glidernet/ogn-aprs-protocol).
For each example, a sample beacon is provided along with the differing parser results.
“dropped” and “added” refer to attributes that were only found by the Python or Rust parser, respectively.

### APRS
(The `dst_call` "APRS" is outdated and is therefore not considered.)

### OGNCAPT and OGNINRE
These messages are ignored

### FXCAPP
```
FXC201699>FXCAPP,qAS,FLYXC:/114100h3236.19S/01903.01Eg312/017/A=003474 !W05! id1E201699
dropped: []
added:
  - address: 201699
  - address_type: 2
  - stealth: False
  - aircraft_type: 7
  - no-tracking: False
```

### OGADSB
```
ICA34364F>OGADSB,qAS,LEMDadsb:/140827h4038.69N\00344.37W^235/248/A=010350 id2534364F +1792fpm  fnANE06BK
dropped: []
added:
  - climb_rate: 9.10336
  - address: 34364F
  - address_type: 1
  - stealth: False
  - aircraft_type: 9
  - no-tracking: False
  - user_comment: fnANE06BK
```

```
ICA4CA4EB>OGADSB,qAS,LEMDadsb:/142346h4034.03N\00315.64W^008/370/A=038000 id254CA4EB +000fpm  0.0rot fnRYR4057  regEI-DPG modelB738
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: 0.0
  - address: 4CA4EB
  - address_type: 1
  - stealth: False
  - aircraft_type: 9
  - no-tracking: False
  - user_comment: fnRYR4057 regEI-DPG modelB738
```

```
ICAA4FFC0>OGADSB,qAS,ADSBExch:/151612h4002.40N/10513.83W'000/001/A=005275 !W00! id05A4FFC0 +0fpm +0.0rot 0.0dB 0e +0.0kHz gps2x3
dropped: []
added:
  - climb_rate: 0.0
  - frequency_offset: 0.0
  - turn_rate: 0.0
  - signal_quality: 0.0
  - address: A4FFC0
  - error_count: 0
  - address_type: 1
  - stealth: False
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 2x3
```

### OGADSL
```
OGN631C45>OGADSL,qAS,OxfBarton:/104536h5145.96N/00111.47W'267/000/A=000312 !W25! id07631C45 -177fpm 22.8dB +2.5kHz gps63x63
dropped: []
added:
  - climb_rate: -0.8991600000000001
  - frequency_offset: 2.5
  - signal_quality: 22.799999237060547
  - address: 631C45
  - address_type: 3
  - stealth: False
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 63x63
```

### OGAIRM
```
AIRF00108>OGAIRM,qAS,Airmate:/151551h4326.16N\00637.42E^245/186/A=002555 !W18! idf00108 +198
dropped: []
added:
  - user_comment: idf00108 +198
```

### OGAPIK
```
FLRDDA396>OGAPIK,qAS,APIK:/113700h4520.00N/00510.00E'000/050/A=000472 !W37! id07DDA396 euiecdb86fffe00001b
dropped: []
added:
  - address: DDA396
  - address_type: 3
  - stealth: False
  - aircraft_type: 1
  - no-tracking: False
  - user_comment: euiecdb86fffe00001b
```

### OGEVARIO
```
OGN06A4D0>OGEVARIO,qAS,EVARIO:/054700h4223.23N/00902.69E'251/005/A=001130 !W34! id1F06A4D0 +000fpm +0rot gps8x3
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: 0.0
  - address: 06A4D0
  - address_type: 3
  - stealth: False
  - aircraft_type: 7
  - no-tracking: False
  - gps_quality: 8x3
```

### OGLT24
```
FLRDDE48A>OGLT24,qAS,LT24:/102606h4030.47N/00338.38W'000/018/A=002267 id25387 +000fpm GPS
dropped:
  - source: GPS
  - lt24_id: 25387
added:
  - user_comment: id25387 GPS
```

### OGNAVI
```
NAV042121>OGNAVI,qAS,NAVITER:/140648h4550.36N/01314.85E'090/152/A=001086 !W47! id0440042121 +000fpm +0.5rot
dropped:
  - do_not_track: False
added:
  - no-tracking: False
```

### OGNTRK
```
OGN8E20F0>OGNTRK,LEMD,OGNDELAY*,qAS,DLY2APRS:/114801h4030.23N/00341.96W'079/000/A=002450 !W44! id068E20F0 +000fpm +1.1rot 56.9dB 0e +3.1kHz gps3x5 31dly
dropped: []
added:
  - no-tracking: False
  - user_comment: 31dly
```

### OGNDVS
```
LEZS>OGNDVS,TCPIP*,qAC,GLIDERN2:>161501h 1:0 2.563s/1ms 74dB/+9kHz 090/5/6kt 51.6F 86.9% 0.0mm/h
dropped: []
added:
  - user_comment: 1:0 2.563s/1ms 74dB/+9kHz 090/5/6kt 51.6F 86.9% 0.0mm/h
```

### OGNEMO
```
CZBA2>OGNEMO,TCPIP*,qAC,NEMO:/094148h4326.64NI07951.12W&/A=000602 v2.00 nemobridge - Superlinxs 9dBi omni
dropped:
  - relay: TCPIP
added:
  - user_comment: v2.00 nemobridge - Superlinxs 9dBi omni
```

```
CZBA4>OGNEMO,TCPIP*,qAC,NEMO:/094148h4326.58NI07950.86W&/A=000602 v2.00 nemobridge - Omni 0dBi + 23dB AMP
dropped:
  - relay: TCPIP
added:
  - user_comment: v2.00 nemobridge - Omni 0dBi + AMP
  - signal_quality: 23.0
```

### OGNFNO
```
FNO0003F4>OGNFNO,qAS,Neurone:/171603h4338.04N/00510.74E'316/000/A=000623 !W28! id200003F4 +000fpm +0.0rot
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: 0.0
  - address: 0003F4
  - address_type: 0
  - stealth: False
  - aircraft_type: 8
  - no-tracking: False
```

### OGNFNT
```
FNT1103CE>OGNFNT,qAS,FNB1103CE:/183727h5057.94N/00801.00Eg355/002/A=001042 !W10! id1E1103CE +03fpm
dropped: []
added:
  - no-tracking: False
```

```
FNB1103CE>OGNFNT,TCPIP*,qAC,GLIDERN3:/183738h5057.95NI00801.00E&/A=001042
dropped:
  - relay: TCPIP
added: []
```

```
FNT1118C1>OGNFNT,qAS,BelaVista:/191919h3841.98N\00919.39Wn !W68! id3E1118C1 FNT71 26.3dB -12.4kHz
dropped: []
added:
  - frequency_offset: -12.399999618530273
  - signal_quality: 26.299999237060547
  - no-tracking: False
  - user_comment: !W68! FNT71
```

```
FNT1118C1>OGNFNT,qAS,BelaVista:>191924h Name="FlrmAIC" 26.0dB -12.1kHz
dropped:
  - frequency_offset: -12.1
  - fanet_name: FlrmAIC
  - signal_quality: 26.0
added:
  - user_comment: Name="FlrmAIC" 26.0dB -12.1kHz
```

```
FNT0828B8>OGNFNT,qAS,Huenenb2:/210414h4710.43N/00826.96E_152/001g002t057r000p000h48b10227 0.0dB
dropped: []
added:
  - beacon_type: fanet
  - signal_quality: 0.0
```

### OGNMTK
```
MTK39447C>OGNMTK,qAS,Microtrak:/170054h4909.81N/00218.71E'136/000/A=000209 !W15! id2339447C rssi-111 snr-5 sf10 gw1 abw0108000B36 gps16
dropped: []
added:
  - user_comment: rssi-111 snr-5 sf10 gw1 abw0108000B36 gps16
```

### OGNMYC
```
MYC78FF44>OGNMYC:>140735h Pilot=RichardHunt
dropped: []
added:
  - user_comment: Pilot=RichardHunt
```

```
MYC78FF44>OGNMYC:/140814h5205.34N/00207.12W'000/000/A=000095 id1B78FF44
dropped: []
added:
  - address: 78FF44
  - address_type: 3
  - stealth: False
  - aircraft_type: 6
  - no-tracking: False
```

### OGNSDR
```
LILH>OGNSDR,TCPIP*,qAC,GLIDERN2:/132201h4457.61NI00900.58E&/A=000423
dropped:
  - relay: TCPIP
added: []
```

```
SCVH>OGNSDR,TCPIP*,qAC,GLIDERN4:>153734h v0.2.8.RPI-GPU CPU:0.3 RAM:744.5/968.2MB NTP:3.6ms/+2.0ppm +68.2C 3/3Acfts[1h] Lat:1.6s RF:-8+67.8ppm/+10.33dB/+1.3dB@10km[30998]/+10.4dB@10km[3/5]
dropped: []
added:
  - rec_crystal_correction_fine: 67.80000305175781
  - good_senders: 3
  - latency: 1.600000023841858
  - rec_input_noise: 10.329999923706055
  - rec_crystal_correction: -8
  - senders_signal: 1.2999999523162842
  - good_senders_signal: 10.399999618530273
  - good_and_bad_senders: 5
  - senders_messages: 30998
```

### OGNSXR
```
K2B9>OGNSXR,TCPIP*,qAC,GLIDERN0:/000627h4353.05NI07215.22W&/A=000692
dropped:
  - relay: TCPIP
added: []
```

```
K2B9>OGNSXR,TCPIP*,qAC,GLIDERN0:>152545h vMB101-ESP32-OGNbase 3.7V 0/min 0/0Acfts[1h] 10sat time_synched 0_m_r_uptime
dropped: []
added:
  - senders_total: 0
  - senders_visible: 0
  - voltage: 3.700000047683716
  - user_comment: vMB101-ESP32-OGNbase 0/min 10sat time_synched 0_m_r_uptime
```

```
K2B9>OGNSXR,TCPIP*,qAC,GLIDERN0:>194557h vMB101-ESP32-OGNbase 3.8V 9sat time_synched 1155_m_r_sleep
dropped: []
added:
  - voltage: 3.799999952316284
  - user_comment: vMB101-ESP32-OGNbase 9sat time_synched 1155_m_r_sleep
```

```
K2B9>OGNSXR,TCPIP*,qAC,GLIDERN0:>195343h vMB101-ESP32-OGNbase time_not_synched 269_m_uptime
dropped: []
added:
  - user_comment: vMB101-ESP32-OGNbase time_not_synched 269_m_uptime
```

### OGNTRK
```
OGN3FC859>OGNTRK,qAS,LZHL:>093215h h00 v00 9sat/1 164m 1002.6hPa +20.2degC 0% 3.34V 14/-110.5dBm 1/min
dropped:
  - temperature: 20.2
  - hardware_version: 0
  - software_version: 0
  - pressure: 1002.6
  - relays: 1
  - humidity: 0
  - gps_altitude: 164
  - noise_level: -110.5
  - gps_quality: 1
  - gps_satellites: 9
  - transmitter_power: 14
added:
  - user_comment: h00 v00 9sat/1 164m 1002.6hPa +20.2degC 0% 14/-110.5dBm 1/min
```

```
OGN2FD00F>OGNTRK,qAS,LZHL:/093213h4848.78N/01708.32E'000/000/A=000538 !W12! id072FD00F -058fpm +0.0rot FL003.12 32.8dB 0e -0.8kHz gps3x5
dropped: []
added:
  - no-tracking: False
```

```
FLRDD9C70>OGNTRK,OGN2FD00F*,qAS,LZHL:/093021h4848.77N/01708.33E'000/000/A=000518 !W66! id06DD9C70 -019fpm +0.0rot 29.0dB 0e -0.8kHz gps2x3 s6.09 h03
dropped: []
added:
  - software_version: 6.090000152587891
  - no-tracking: False
  - hardware_version: 3
```

### OGNTTN
```
OGN60E6A0>OGNTTN,qAS,TTN2OGN:/181002h4030.24N/00341.95W'235/003/A=002343 !W27! id0760E6A0 +000fpm -12.4rot FL020.64 gps3x5 7.2dB
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: -37.19999885559082
  - flightlevel: 20.639999389648438
  - signal_quality: 7.199999809265137
  - address: 60E6A0
  - address_type: 3
  - stealth: False
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 3x5
```

```
OGN8E20F0>OGNTTN,RELAY*,qAS,TTN2OGN:/172403h4030.24N/00341.94W'182/002/A=002441 !W66! id078E20F0 -039fpm +8.4rot FL023.17 gps4x7 7.5dB
dropped: []
added:
  - climb_rate: -0.19812000000000002
  - turn_rate: 25.19999885559082
  - flightlevel: 23.170000076293945
  - signal_quality: 7.5
  - address: 8E20F0
  - stealth: False
  - address_type: 3
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 4x7
```

```
OGN60E6A0>OGNTTN,qAS,TTN2OGN:>172606h SN=OGN60E6A0 9.5dB
dropped: []
added:
  - user_comment: SN=OGN60E6A0 9.5dB
```

```
OGN60E6A0>OGNTTN,qAS,TTN2OGN:>173011h h02 v01 8sat/1/22dB 724m 932.3hPa +31.8degC +18.8% +4.28V 14/-99.5dBm 63/min 6.8dB
dropped: []
added:
  - voltage: 4.28000020980835
  - user_comment: h02 v01 8sat/1/22dB 724m 932.3hPa +31.8degC +18.8% 14/-99.5dBm 63/min 6.8dB
```

### OGNTTN3
```
OGNC3088C>OGTTN3,qAS,TTN3OGN:/180751h4030.23N/00341.98W'115/003/A=002218 !W61! id07C3088C +000fpm -7.2rot FL024.48 gps9x14 9.5dB
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: -21.59999942779541
  - flightlevel: 24.479999542236328
  - signal_quality: 9.5
  - address: C3088C
  - address_type: 3
  - stealth: False
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 9x14
```

```
OGN60E6A0>OGTTN3,qAS,TTN3OGN:>180757h Class=OPEN Base=LELT PilotID=12345 9.2dB
dropped: []
added:
  - user_comment: Class=OPEN Base=LELT PilotID=12345 9.2dB
```

```
OGNC30824>OGTTN3,RELAY*,qAS,TTN3OGN:/181005h4030.24N/00341.94W'218/000/A=002353 !W56! id07C30824 +000fpm +8.6rot FL024.45 gps3x5 8.2dB
dropped: []
added:
  - climb_rate: 0.0
  - turn_rate: 25.80000114440918
  - flightlevel: 24.450000762939453
  - signal_quality: 8.199999809265137
  - address: C30824
  - stealth: False
  - address_type: 3
  - aircraft_type: 1
  - no-tracking: False
  - gps_quality: 3x5
```

### OGNWMN
```
N0ABC7>OGNWMN,qAS,WMN:/134300h4923.60N/01535.54E'000/000/A=001624 id07N0ABC7A39971
dropped: []
added:
  - user_comment: id07N0ABC7A39971
```

### OGPAW
```
ICA404EC3>OGPAW,qAS,UKWOG:/104337h5211.24N\00032.65W^124/081/A=004026 !W62! id21404EC3 12.5dB +2.2kHz
dropped: []
added:
  - frequency_offset: 2.200000047683716
  - signal_quality: 12.5
  - address: 404EC3
  - address_type: 1
  - stealth: False
  - aircraft_type: 8
  - no-tracking: False
```

```
ICA404EC3>OGPAW,qAS,UKWOG:/104341h5211.18N\00032.53W^131/081/A=004010 !W85! id21404EC3 9.2dB +2.2kHz +10.0dBm
dropped: []
added:
  - frequency_offset: 2.200000047683716
  - signal_power: 10.0
  - signal_quality: 9.199999809265137
  - address: 404EC3
  - address_type: 1
  - stealth: False
  - aircraft_type: 8
  - no-tracking: False
```

### OGSKYL
```
FLRDDDD78>OGSKYL,qAS,SKYLINES:/134403h4225.90N/00144.83E'000/000/A=008438 id2816 +000fpm
dropped:
  - skylines_id: 2816
added:
  - user_comment: id2816
```

### OGSPID
```
FLRDDF944>OGSPID,qAS,SPIDER:/190930h3322.78S/07034.60W'000/000/A=002263 id300234010617040 +19dB LWE 3D
dropped:
  - signal_power: 19
  - spider_id: 300234010617040
  - spider_registration: LWE
  - gps_quality: 3D
added:
  - signal_quality: 19.0
  - user_comment: id300234010617040 LWE 3D
```

### OGSPOT
```
ICA3E7540>OGSPOT,qAS,SPOT:/161427h1448.35S/04610.86W'000/000/A=008677 id0-2860357 SPOT3 GOOD
dropped:
  - status: GOOD
  - model: SPOT3
  - spot_id: 0-2860357
added:
  - user_comment: id0-2860357 SPOT3 GOOD
```
