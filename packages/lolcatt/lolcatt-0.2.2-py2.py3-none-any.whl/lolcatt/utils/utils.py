#!/usr/bin/env python3
from pathlib import Path

from catt.api import discover
from catt.cli import get_config_as_dict


def marquee(s: str, max_len: int, step_size: int) -> str:
    """
    Yields a string that is max_len characters long, and shifts the string by step_size each time.

    :param s: The string to be shifted
    :param max_len: The maximum length of the string
    :param step_size: The number of characters to shift the string by
    :return: A string that is max_len characters long and appropriately shifted
    """
    while True:
        if len(s) < max_len:
            yield s
        else:
            s = f'{s[step_size:]}{s[:step_size]}'
            yield s[:max_len]


def scan():
    """Scans the network for Chromecast devices and prints the results."""
    print('Scanning for Chromecast devices...')

    # Invert aliases dict
    aliases = get_config_as_dict().get('aliases', {})
    devices_to_aliases = {v: k for k, v in aliases.items()}

    discovered = discover()
    deduped = []
    found_ips = set()
    max_name_len = 11  # len('Device name')
    max_alias_len = 5  # len('Alias')
    for device in discovered:
        if device.ip_addr not in found_ips:
            found_ips.add(device.ip_addr)
            max_name_len = max(max_name_len, len(device.name))
            max_alias_len = max(max_alias_len, len(devices_to_aliases.get(device.name, '')))
            deduped.append((device.name, devices_to_aliases.get(device.name, ''), device.ip_addr))

    deduped = [
        (
            '"' + x + '"' + ' ' * (max_name_len - len(x)),
            ('"' + y + '"' if len(y) else '') + ' ' * (max_alias_len - len(y)),
            z,
        )
        for x, y, z in deduped
    ]
    deduped = sorted(deduped, key=lambda x: x[1])

    print('Found {} device(s):'.format(len(found_ips)))
    print(f'Device name{" " * (max_name_len - 11)}\tAlias{" " * (max_alias_len - 5) }\tDevice IP')
    print('=' * (max_name_len + max_alias_len + 22))
    for name, alias, ip in deduped:
        print(f'{name}\t{alias}\t{ip}')


def write_initial_config(p: Path):
    p.write_text(
        "[options]\n"
        "fancy_icons = true  # Whether to use fancy icons\n"
        "#youtube_cookies_file = \"~/.config/lolcatt/cookies.txt\"  # Path to a cookies.txt file for YouTube\n"
        "youtube_mark_watched = true # Whether to mark YouTube videos as watched (only if we have cookies)"
    )
