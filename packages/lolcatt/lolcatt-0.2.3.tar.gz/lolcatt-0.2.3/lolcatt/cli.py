#!/usr/bin/env python3
from pathlib import Path

import click
import toml

from lolcatt import __version__
from lolcatt.app import LolCatt
from lolcatt.utils.utils import scan as do_scan
from lolcatt.utils.utils import write_initial_config


@click.command(
    'lolcatt',
    context_settings=dict(help_option_names=['-h', '--help']),
)
@click.version_option(__version__, '-v', '--version', prog_name='lolcatt')
@click.argument(
    'url_or_path',
    nargs=1,
    default=None,
    required=False,
)
@click.option(
    '-d',
    '--device',
    default='default',
    help='Device name or alias (defined in catt config) to cast to. '
    'Per default, uses the device noted as default in the `catt` config file. '
    'If no default is set, the first device found will be used.',
)
@click.option(
    '--scan',
    is_flag=True,
    default=False,
    help='Scan for Chromecast devices and exit, printing found devices.',
)
@click.option(
    '--config',
    default='~/.config/lolcatt/config.toml',
    type=click.Path(dir_okay=False),
    help='Path to catt config file. Defaults to ~/.config/lolcatt/config.toml -'
    'If the file does not exist, it will be created.',
)
def main(url_or_path, device, scan, config):
    """Cast media from a local file or URL to a Chromecast device."""
    config = Path(str(config)).expanduser()
    if not config.exists():
        config.parent.mkdir(parents=True, exist_ok=True)
        write_initial_config(config)

    config = toml.loads(config.read_text())

    if url_or_path is None and scan:
        do_scan()
        return

    lolcatt = LolCatt(device_name=device, config=config)
    if url_or_path is not None:
        lolcatt.caster.enqueue(url_or_path)
        lolcatt.caster.cast_next()
    lolcatt.run()


if __name__ == '__main__':
    main()
