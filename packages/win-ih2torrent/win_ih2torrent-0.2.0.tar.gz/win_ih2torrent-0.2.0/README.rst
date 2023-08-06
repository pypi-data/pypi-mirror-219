win-ih2torrent
==========

`win-ih2torrent` creates a trackerless torrent file from an infohash or a
magnet URI. It uses BitTorrent [DHT][1] and the [metadata protocol][2]
to find peers for the torrent and obtain its metadata.

`For windows devices only. It is a drop in replacement for ih2torrent`

In order to get the dependencies inside a virtualenv, run `make`. You
need Python 3.5 or higher to run ih2torrent.

You can use pip to install ih2torrent: `pip3 install win-ih2torrent`

Please note this is a fork of @elektito/ih2torrent and made so just for the convenience of myself and others

[1]: http://www.bittorrent.org/beps/bep_0005.html
[2]: http://www.bittorrent.org/beps/bep_0009.html
