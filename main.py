#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#--------------------------#
# Created By  : Brittank88
# Created Date: 28/01/2022
# Version     : '2.0.0'
# -------------------------#
"""Python script to download all the SFX from https://gdcolon.com/🗿."""

from argparse import ArgumentParser
from json import loads
from xmlrpc.client import Boolean
from requests import get
from pathlib import Path
from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map
from loguru import logger
from os import cpu_count
from threading import get_native_id
from colorama import Fore, Back, Style

BLOCK_SIZE = 1024   # 1 Kibibyte = 1024 bytes
DOMAIN     = 'https://gdcolon.com'
BLOCKING_COEFFICIENT = 0.5

def init_argparse() -> ArgumentParser:
    """Initialises and returns the argument parser."""

    parser = ArgumentParser(
        usage       = '%(prog)s [OPTION]',
        description = f'Downloads all SFX from {DOMAIN}/🗿.'
    )
    parser.add_argument(
        '-o', '--output'                 ,
        help    = 'The output directory for downloaded SFX.',
        default = './sfx'                                   ,
        type    = str
    )
    parser.add_argument(
        '-s', '--soundlist'                                    ,
        help    = 'The JSON soundlist url (excluding domain!).',
        default = '/server/soundlist'                          ,
        type    = str
    )
    parser.add_argument(
        '-t', '--threads'                                  ,
        help    = 'The number of threads to use.'          ,
        default = cpu_count() // (1 - BLOCKING_COEFFICIENT),
        type    = int
    )
    return parser

def main() -> None:
    """Main function to download SFX from Colon's server."""

    parser = init_argparse()
    args   = parser.parse_args()

    logger.remove()
    logger.add(lambda msg: tqdm.write(msg, end = ''))

    def _download(sound: dict) -> None:
        """Underlying function that ownloads a sound from the server."""

        try:
            filename     = sound.get('filename')
            filename_ext = filename.split('/')[-1]

            logger_prefix = f'{Fore.BLACK}{Back.WHITE}[Thread | {"%05d" % get_native_id()}]{Style.RESET_ALL}'
            tqdm.write(f'{logger_prefix}{Fore.LIGHTBLUE_EX}{Style.DIM} Downloading \'{filename_ext}\'...{Style.RESET_ALL}')

            with Path(args.output, filename_ext) as filepath:
                filepath.parents[0].mkdir(parents = True, exist_ok = True)
                filepath.open('wb').write(get(f'{DOMAIN}/{filename}').content)

            tqdm.write(f'{logger_prefix}{Fore.LIGHTGREEN_EX}{Style.BRIGHT} Downloaded \'{filename_ext}\'!{Style.RESET_ALL}')

        except Exception as _:
            tqdm.write(f'{logger_prefix}{Fore.LIGHTYELLOW_EX} Download failed for \'{filename_ext}\'!{Style.RESET_ALL}')

    thread_map(_download, loads(get(f'{DOMAIN}{args.soundlist}').text), max_workers = args.threads)

if __name__ == '__main__':
    main()