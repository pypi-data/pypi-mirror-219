#!/usr/bin/env python
"""Tests for `lolcatt` package."""
from lolcatt.app import LolCatt


def test_lolcat_start():
    """Simple smoke test for now."""
    lolcatt = LolCatt(device_name=None)
    lolcatt.run()
