#!/usr/bin/env python3
from pathlib import Path

from catt.api import discover


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

    discovered = discover()
    deduped = []
    found_ips = set()
    max_name_len = 11  # len('Device name')
    for device in discovered:
        if device.ip_addr not in found_ips:
            found_ips.add(device.ip_addr)
            max_name_len = max(max_name_len, len(device.name))
            deduped.append((device.name, device.ip_addr))

    deduped = [('"' + x + '"' + ' ' * (max_name_len - len(x)), y) for x, y in deduped]
    deduped = sorted(deduped, key=lambda x: x[1])

    print('Found {} device(s):'.format(len(found_ips)))
    print(f'Device name{" " * (max_name_len - 11)}\tDevice IP')
    print('=' * (max_name_len + 19))
    for name, ip in deduped:
        print(f'{name}\t{ip}')


def write_initial_config(p: Path):
    p.write_text(
        "[options]\n"
        "fancy_icons = true  # Whether to use fancy icons\n"
        "#youtube_cookies_file = \"~/.config/lolcatt/cookies.txt\"  # Path to a cookies.txt file for YouTube"
    )
