# -*- mode: python -*-

from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs

import sys
import os

PACKAGE='Electrum-DNotes'
PYPKG='electrum_dnotes'
MAIN_SCRIPT='electrum-dnotes'
ICONS_FILE='electrum-dnotes.icns'

for i, x in enumerate(sys.argv):
    if x == '--name':
        VERSION = sys.argv[i+1]
        break
else:
    raise Exception('no version')

electrum_dnotes = os.path.abspath(".") + "/"
block_cipher = None

# see https://github.com/pyinstaller/pyinstaller/issues/2005
hiddenimports = []
hiddenimports += collect_submodules('trezorlib')
hiddenimports += collect_submodules('btchip')
hiddenimports += collect_submodules('keepkeylib')
hiddenimports += collect_submodules('websocket')

datas = [
    (electrum_dnotes+'lib/currencies.json', PYPKG),
    (electrum_dnotes+'lib/servers.json', PYPKG),
    (electrum_dnotes+'lib/checkpoints.json', PYPKG),
    (electrum_dnotes+'lib/servers_testnet.json', PYPKG),
    (electrum_dnotes+'lib/checkpoints_testnet.json', PYPKG),
    (electrum_dnotes+'lib/wordlist/english.txt', PYPKG + '/wordlist'),
    #(electrum_dnotes+'lib/locale', PYPKG + '/locale'),
    (electrum_dnotes+'plugins', PYPKG + '_plugins'),
]
datas += collect_data_files('trezorlib')
datas += collect_data_files('btchip')
datas += collect_data_files('keepkeylib')

# Add libusb so Trezor will work
binaries = [(electrum_dnotes + "contrib/build-osx/libusb-1.0.dylib", ".")]

# Workaround for "Retro Look":
binaries += [b for b in collect_dynamic_libs('PyQt5') if 'macstyle' in b[0]]

# We don't put these files in to actually include them in the script but to make the Analysis method scan them for imports
a = Analysis([electrum_dnotes+MAIN_SCRIPT,
              electrum_dnotes+'gui/qt/main_window.py',
              electrum_dnotes+'gui/text.py',
              electrum_dnotes+'lib/util.py',
              electrum_dnotes+'lib/wallet.py',
              electrum_dnotes+'lib/simple_config.py',
              electrum_dnotes+'lib/bitcoin.py',
              electrum_dnotes+'lib/dnssec.py',
              electrum_dnotes+'lib/commands.py',
              electrum_dnotes+'plugins/cosigner_pool/qt.py',
              electrum_dnotes+'plugins/email_requests/qt.py',
              electrum_dnotes+'plugins/trezor/client.py',
              electrum_dnotes+'plugins/trezor/qt.py',
              electrum_dnotes+'plugins/keepkey/qt.py',
              electrum_dnotes+'plugins/ledger/qt.py',
              ],
             binaries=binaries,
             datas=datas,
             hiddenimports=hiddenimports,
             hookspath=[])

# http://stackoverflow.com/questions/19055089/pyinstaller-onefile-warning-pyconfig-h-when-importing-scipy-or-scipy-signal
for d in a.datas:
    if 'pyconfig' in d[0]:
        a.datas.remove(d)
        break

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          name=PACKAGE,
          debug=False,
          strip=False,
          upx=True,
          icon=electrum_dnotes+ICONS_FILE,
          console=False)

app = BUNDLE(exe,
             version = VERSION,
             name=PACKAGE + '.app',
             icon=electrum_dnotes+ICONS_FILE,
             bundle_identifier=None,
             info_plist={
                'NSHighResolutionCapable': 'True',
                'NSSupportsAutomaticGraphicsSwitching': 'True'
             }
)
