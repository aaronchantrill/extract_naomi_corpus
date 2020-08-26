#!/usr/bin/env python3

# -*- coding: utf-8 -*-
import argparse
import json
import logging
import os
import pkg_resources
import re
import socket
import sqlite3
import webbrowser
import wsgiref.simple_server
from datetime import datetime
from jiwer import wer
from naomi import paths
from naomi import profile
from naomi import pluginstore
from socketserver import ThreadingMixIn
from threading import Thread
from urllib.parse import unquote

# Set Debug to True to see debugging information
# or use the --debug flag on the command line
Debug = False
_logger = logging.getLogger(__name__)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Naomi Corpus Extractor')
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Show debug messages'
    )
    parser.add_argument(dest='filename', help="File to save the corpus to")
    p_args = parser.parse_args()
    if p_args.debug:
        Debug = True
        print("Setting logging level to DEBUG")
        logging.basicConfig(
            level=logging.DEBUG
        )
    wakewords = profile.get(['keyword'])
    if not isinstance(wakewords, list):
        wakewords = [wakewords]
    print(wakewords)
    if(os.path.isfile(p_args.filename)):
        print("File {} exists, exiting".format(p_args.filename))
    else:
        with(open(p_args.filename,'w')) as f:
            # Load the STT_Trainer plugins
            plugin_directories = [
                paths.config('plugins'),
                pkg_resources.resource_filename(__name__, os.path.join('plugins'))
            ]
            plugins = pluginstore.PluginStore(plugin_directories)
            plugins.detect_plugins()
            for info in plugins.get_plugins_by_category("speechhandler"):
                try:
                    plugin = info.plugin_class(
                        info,
                        profile.get_profile()
                    )
                    if(hasattr(plugin, "intents")):
                        intents = plugin.intents()
                        for intent in intents:
                            print(intent)
                            for template in intents[intent]['locale']['en-US']['templates']:
                                for wakeword in wakewords:
                                    f.write("{} {}\n".format(wakeword.lower(), re.sub('\{(.*?)\}', '', template).lower()))
                                    f.write("{} {}\n".format(re.sub('\{(.*?)\}', '', template).lower(), wakeword.lower()))
                except Exception as e:
                    print(
                        "Plugin '{}' skipped! (Reason: {})".format(
                            info.name,
                            e.message if hasattr(e, 'message') else 'Unknown'
                        )
                    )
                    _logger.warn(
                        "Plugin '{}' skipped! (Reason: {})".format(
                            info.name,
                            e.message if hasattr(e, 'message') else 'Unknown'
                        ),
                        exc_info=True
                    )
