cpyvpn
======

cpyvpn is pure python implementation of the Checkpoint VPN client.

# Features
* SSL Network eXtender based.
* 'Legacy' and new login mode with realm select and Multi Factor authorization.
* Certificate-based login, certificate enrollment and renewal.
* Mobile Access Portal authorization and Native Applications support.
* Intermediary CAs certificates fetch when gateway certificate does not contain full trust chain.
* Privileged and root-less VNA (Virtual Network Adapter) modes of operation.

# Description of the executables

cpyvpn contains three scripts: cp_client, cp_server and cpga.pyz.

* **cp_client** is similar to the snx utility from CheckPoint: it establishes
VPN between client host and private network behind gateway.

* **cpga.pyz** performs Mobile Access Portal (MAP) authorization to get session cookie,
used during MAP SNX tunnel setup.

**Note 1**: Separate cpga.pyz is not currently available. Refer to the cpga.pyz build instructions to make one if needed.
cpga script is still installed alongside cp_client.

**Note 2**: Test server script and data files are no longer included in the release wheel. Download the source distribution to run the test server.

All scripts support a number of different options. Invoke them with -h
flag to see full help.

Cached CA certs is stored in the cache.pem, located in:
* ~/.cache/cpyvpn - on Unux and the likes
* ~/Library/Caches/cpyvpn - on Mac OS X
* C:\Users\<username>\AppData\Local\cpyvpn\cpyvpn\Cache

# Installation
Dependencies for the current version of the scripts is Python 3.7+ and:
- TUN/TAP device driver for NM or vpnc-script (see below) modes
- UTUN device driver on macOS (available starting from 10.6.8 version) with vpnc-script
- NetworkManager (NM) for cp_server and cp_client in default mode (without -s or -S)

Main package wheel is self-contained and all scripts can be run from
the directory containing the wheel like this:

``env PYTHONPATH=cpyvpn-<version>-py3-none-any.whl python -m cpyvpn.client std.server.org``

``env PYTHONPATH=cpyvpn-<version>-py3-none-any.whl python -m cpyvpn.ma ma.server.org``

Or from the source folder:

``python -m cpyvpn.client std.server.org``

``python -m cpyvpn.srv.server localhost:4433``

A regular ``pip install`` is supported as well. In latter case script names
are **cp_client** and **cpga**.

cpga.pyz - a self-contained version of cpyvpn.ma -  does not require
installation also and intended to be used as a standalone program: ``cpga.pyz ma.server.org`` or
be invoked from e.g. [openconnect](https://gitlab.com/openconnect/openconnect.git):


# VNA modes
## Network Manager (linux)
By default cp_client and cp_server rely on the NM to do tun device configuration
and to run without root privileges. Please note, that the user running cp_client/cp_server must be in plugdev group
and be logged in locally (not ssh!) for the NM to allow required network setup.

## vpnc script (linux/macOS)
Download current version from [here](https://gitlab.com/openconnect/vpnc-scripts.git), use with `-s` command line switch. Requires superuser privileges to initialize and configure VNA device.

## vpn proxy (linux/macOS)
cp_client can use [ocproxy](https://github.com/cernekee/ocproxy) or [tunsocks](https://github.com/russdill/tunsocks), originally written for the openconnect. Such configuration works entirely in the user mode.

## vpnns (linux)
Part of ocproxy package to use with 'hard-to-proxy' protocols and applications. Refer to the ocproxy documentation for more info. Works in the user mode just like aforementioned proxy programs.

# More usage examples

* Standard (TRAC) login with user name and password using default VNA:

    `cp_client -m l -u testuser vpn.example.org`

* TRAC login with realm and predefined user name:

    `cp_client --realm vpn -u testuser vpn.example.org`

* TRAC login with the predefined user name, run in the background after user authication, redirect output to cp.log and save background process pid to the cp.pid file:

    `cp_client --daemon --logfile=./cp.log --pidfile=./cp.pid -u testuser vpn.example.org`
* TRAC login with predefined user name and password from external program:

    `cp_client -u user --passwd-script 'kwallet-query kdewallet' vpn.example.org`

* TRAC login with certificate as a first factor:

    `cp_client -c cert.pem vpn.example.org`

* MAP login:

    `cp_client https://vpn.example.org/sslpvn/`

* MAP login with certificate:

    `cp_client  -c cert.pem https://vpn.example.org/sslpvn/`

* MAP login with cookies from browser:

    `echo 'CPCVPN_SESSION_ID=...; CPCVPN_BASE_HOST=...'| cp_client --cookies-on-stdin ... https://vpn.example.org/sslpvn/Portal/Main`

    Session cookie can be extracted using browser extension [Export Cookies](https://addons.mozilla.org/ru/firefox/addon/export-cookies-txt/), [cookie-editor](https://cookie-editor.cgagnier.ca/), [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/bgaddhkoddajcdgocldbbfleckgcbcid), etc. Builtin browser development tools can to of use here also.

* MAP logout from browser session:

    `echo 'CPCVPN_SESSION_ID=...; CPCVPN_BASE_HOST=...'| cpga --so --cookies-on-stdin https://vpn.example.org/sslpvn/Portal/Main`

* User mode proxy with ssh and rdp forwarding:

    `cp_client -S 'ocproxy -L 2222:<host_ip1>:22 -L 3389:<host_ip2>:3389' vpn.example.org`

    After successful login you may run commands like: `ssh -p2222 localhost` or `xfreerdp /v:localhost`

* vpnc-based VNA configuration(with sudo or root shell):

    `sudo cp_client -s '<vpnc_script_filename>' -u testuser vpn.example.org`

* Certificate enrollment:

    `cp_client --enroll -c ./cert.p12 vpn.example.org`

    After successfull certificate fetch cp_client will try to convert from p12 to pem using openssl. If conversion fails for some reason user should do it manually.

* Certificate renewal:

    `cp_client --rc new_cert.p12 -c ./cert.p12 vpn.example.org`

    Conversion notes applies here likewise.

# Performance
Python incurs extra overhead and the maximum bitrate will be 2-3 times lower than the bitrate achievable with the native client or openconnect. However it will only be noticable when the link speed is >100MB/s.

# Known Issues
* Early R81 gateway versions were 'enhanced' in a way affecting user experience. One of the enhancements (or a bug) prevents multiple tunnel initializations from the same Web Portal session. Any client doing second connection attempt just hangs.
In this case either logout manually after each cp_client run, use cpga logout or add --force_logout to perform automatic signout after tunnel shutdown to workaround this issue.

* Internal DNS will need additional setup with the vpnc script. Interface priority/ordering must be adjusted manually. E.g. 'interface_order="snx* lo* en*"' in resolvconf.conf file for resolvconf tool.

# Source installation
Download sources using git or as an archive (and unzip if necessary).

Run a command in the source directory:

`python -m pip install [-e] .` (Preferred way)

or

`python setup.py install|develop`

Add --user flag if needed.

# Build cpga.pyz from source
Run in the top source folder:
`python setup.py build_cpga`

The path to the generated file will be: `dist/cpga.pyz`

# License
Copyright &copy; 2020-2022 Nikolay A. Krylov
All rights reserved.

The cpyvpn is a free software package, distributed under GPLv3 license. See the file LICENSE for more details.
