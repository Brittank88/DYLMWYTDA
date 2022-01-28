#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------#
# Created By  : Brittank88
# Created Date: 28/01/2022
# Version     : '1.0.0'
# -------------------------#
"""Python script to download all the SFX from https://gdcolon.com/🗿."""

from argparse import ArgumentParser
from json import loads
from requests import get
from pathlib import Path
from tqdm import tqdm

BLOCK_SIZE = 1024   # 1 Kibibyte = 1024 bytes
DOMAIN     = 'https://gdcolon.com'

def init_argparse() -> ArgumentParser:
    """Initialises and returns the argument parser."""

    parser = ArgumentParser(
        usage       = '%(prog)s [OPTION]',
        description = f'Downloads all SFX from {DOMAIN}/🗿.'
    )
    parser.add_argument(
        '-o', '--output'                 ,
        help    = 'The output directory.',
        default = './sfx'
    )
    parser.add_argument(
        '-s', '--soundlist'                                    ,
        help    = 'The JSON soundlist url (excluding domain!).',
        default = '/server/soundlist'
    )
    return parser

def main() -> None:
    """Main function to download SFX from Colon's server."""

    parser = init_argparse()
    args = parser.parse_args()

    for i, sfx_entry in enumerate(
        loads(get(f'{DOMAIN}/{args.soundlist}').text)
    ):
        filename = sfx_entry.get('filename', f'sfx_{i}.wav')
        filename_ext = filename.split('/')[-1]

        filepath = Path(args.output, filename_ext)
        filepath.parents[0].mkdir(parents = True, exist_ok = True)

        sfx_file = get(f'{DOMAIN}/{filename}', stream = True)
        progress_bar = tqdm(desc = filename_ext, unit = 'iB', unit_scale = True)
        
        for bytes in sfx_file.iter_content(BLOCK_SIZE):
            progress_bar.update(len(bytes))
            filepath.open('ab').write(bytes)

if __name__ == '__main__':
    main()