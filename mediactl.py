#!/usr/bin/env python3

# The following are basic functions for controlling available media players on the system, using dbus.
# Intended for use with only one media player running, tho works with multiple just without separate controls.
# If dbus error, try setting include-system-site-packages = true in virtual environment's pyvenv.cfg file.
# by Nik Stromberg - nikorasu85@gmail.com - MIT 2022 - copilot

from dbus import SessionBus, Interface

bus = SessionBus()

def _playerlist() -> list:
    return [service for service in bus.list_names() if service.startswith('org.mpris.MediaPlayer2.')]

def playpause() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            player.PlayPause(dbus_interface='org.mpris.MediaPlayer2.Player')
        except:
            worked -= 1
    return True if worked else False

def next() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            player.Next(dbus_interface='org.mpris.MediaPlayer2.Player')
        except:
            worked -= 1
    return True if worked else False

def prev() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            player.Previous(dbus_interface='org.mpris.MediaPlayer2.Player')
        except:
            worked -= 1
    return True if worked else False

def stop() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            player.Stop(dbus_interface='org.mpris.MediaPlayer2.Player')
        except:
            worked -= 1
    return True if worked else False

def volumeup() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            properties = Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
            volume = properties.Get('org.mpris.MediaPlayer2.Player', 'Volume')
            properties.Set('org.mpris.MediaPlayer2.Player', 'Volume', volume+0.2)
        except:
            worked -= 1
    return True if worked else False

def volumedown() -> bool:
    players = _playerlist()
    worked = len(players)
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            properties = Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
            volume = properties.Get('org.mpris.MediaPlayer2.Player', 'Volume')
            properties.Set('org.mpris.MediaPlayer2.Player', 'Volume', volume-0.2)
        except:
            worked -= 1
    return True if worked else False

def getstatus() -> list:
    players = _playerlist()
    details = []
    for player in players:
        try:
            player = bus.get_object(player, '/org/mpris/MediaPlayer2')
            properties = Interface(player, dbus_interface='org.freedesktop.DBus.Properties')
            metadata = properties.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            Title = metadata['xesam:title'] if 'xesam:title' in metadata else 'Unknown'
            Artist = metadata['xesam:artist'][0] if 'xesam:artist' in metadata else 'Unknown'
            PlayStatus = properties.Get('org.mpris.MediaPlayer2.Player', 'PlaybackStatus')
            details.append({'title': str(Title), 'artist': str(Artist), 'status': str(PlayStatus)})
        except:
            pass
    return details

#if __name__ == '__main__':  # if I decide to make this a standalone terminal media controller later.