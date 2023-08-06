<!--
SPDX-FileCopyrightText: 2022 Thomas Kramer

SPDX-License-Identifier: CC-BY-SA-4.0
-->

## Install on Debian

Install prerequisites:
```sh
sudo apt install python3-pyaudio python3-numpy python3-scipy python3-aiohttp python3-nacl
```

For the server only the following is necessary
```sh
sudo apt install python3-numpy python3-nacl
```

Optionally install `uvloop` for higher performance:
```sh
sudo apt install python3-uvloop
```

## Run the client

```sh
python3 picotalk-client.py -s my.server.com -r mySecretRoom
```

## Run the server
```sh
python3 picotalk-server.py # Use --uvloop to use uvloop.
```