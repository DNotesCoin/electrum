#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

with open('contrib/requirements/requirements.txt') as f:
    requirements = f.read().splitlines()

with open('contrib/requirements/requirements-hw.txt') as f:
    requirements_hw = f.read().splitlines()

version = imp.load_source('version', 'lib/version.py')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum DNotes requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    icons_dirname = 'pixmaps'
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        icons_dirname = 'icons'
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum-dnotes.desktop']),
        (os.path.join(usr_share, icons_dirname), ['icons/electrum-dnotes.png'])
    ]

setup(
    name="Electrum-DNotes",
    version=version.ELECTRUM_VERSION,
    install_requires=requirements,
    extras_require={
        'full': requirements_hw + ['pycryptodomex'],
    },
    packages=[
        'electrum_dnotes',
        'electrum_dnotes_gui',
        'electrum_dnotes_gui.qt',
        'electrum_dnotes_plugins',
        'electrum_dnotes_plugins.audio_modem',
        'electrum_dnotes_plugins.cosigner_pool',
        'electrum_dnotes_plugins.email_requests',
        'electrum_dnotes_plugins.greenaddress_instant',
        'electrum_dnotes_plugins.hw_wallet',
        'electrum_dnotes_plugins.keepkey',
        'electrum_dnotes_plugins.labels',
        'electrum_dnotes_plugins.ledger',
        'electrum_dnotes_plugins.trezor',
        'electrum_dnotes_plugins.digitalbitbox',
        'electrum_dnotes_plugins.trustedcoin',
        'electrum_dnotes_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum_dnotes': 'lib',
        'electrum_dnotes_gui': 'gui',
        'electrum_dnotes_plugins': 'plugins',
    },
    package_data={
        'electrum_dnotes': [
            'servers.json',
            'servers_testnet.json',
            'servers_regtest.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum-dnotes.mo',
        ]
    },
    scripts=['electrum-dnotes'],
    data_files=data_files,
    description="Lightweight DNotes Wallet",
    author="Thomas Voegtlin",
    author_email="thomasv@electrum.org",
    license="MIT Licence",
    url="https://electrum.org",
    long_description="""Lightweight DNotes Wallet"""
)
