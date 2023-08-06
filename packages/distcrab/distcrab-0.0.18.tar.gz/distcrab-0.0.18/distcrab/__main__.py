#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
sys.dont_write_bytecode = True

from sys import stdout
from os import environ
from logging import getLogger, StreamHandler, DEBUG
from argparse import ArgumentParser, Action

logger = getLogger()
logger.setLevel(DEBUG)
handler = StreamHandler(stdout)
handler.setLevel(DEBUG)
logger.addHandler(handler)

class FirmwareAction(Action):
    def __init__(self, option_strings, abbr, *args, **kwargs):
        self.abbr = abbr
        super(FirmwareAction, self).__init__(option_strings=option_strings, *args, **kwargs)
    def __call__(self, parser, namespace, values, option_string=None):
        if values:
            setattr(namespace, self.dest, values)
        else:
            setattr(namespace, self.dest, self.abbr)

PARSER = ArgumentParser()
PARSER.add_argument('--firmware', action=FirmwareAction, default=environ.get('FIRMWARE', None), abbr='http://192.168.21.1:5080/APP/develop/develop/update/industry/preview/webui-cmake/firmware.bin')
PARSER.add_argument('--branch', type=str, default=environ.get('BRANCH', None))
PARSER.add_argument('--version', type=str, default=environ.get('VERSION', None))
PARSER.add_argument('--ip', type=str, default=environ.get('IP', '192.168.1.200'))
PARSER.add_argument('--password', type=str, default=environ.get('PASSWORD', 'elite2014'))
PARSER.add_argument('--download', action='store_true', default=environ.get('DOWNLOAD', False))

from .main import distcrab
for i in distcrab(**vars(PARSER.parse_args())):
    logger.debug(i.decode().strip())
