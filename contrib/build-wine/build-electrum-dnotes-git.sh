#!/bin/bash

NAME_ROOT=electrum-dnotes
PYTHON_VERSION=3.5.4

# These settings probably don't need any change
export WINEPREFIX=/opt/wine64
export PYTHONDONTWRITEBYTECODE=1
export PYTHONHASHSEED=22

PYHOME=c:/python$PYTHON_VERSION
PYTHON="wine $PYHOME/python.exe -OO -B"


# Let's begin!
cd `dirname $0`
set -e

mkdir -p tmp
cd tmp

for repo in electrum-dnotes; do
    if [ -d $repo ]; then
	cd $repo
	git pull
	git checkout master
	cd ..
    else
	URL=https://github.com/DNotesCoin/$repo.git
	git clone -b master $URL $repo
    fi
done

#pushd electrum-dnotes-locale
#for i in ./locale/*; do
#    dir=$i/LC_MESSAGES
#    mkdir -p $dir
#    msgfmt --output-file=$dir/electrum-dnotes.mo $i/electrum-dnotes.po || true
#done
#popd

pushd electrum-dnotes
if [ ! -z "$1" ]; then
    git checkout $1
fi

VERSION=`git describe --tags --dirty`
echo "Last commit: $VERSION"
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

rm -rf $WINEPREFIX/drive_c/electrum-dnotes
cp -r electrum-dnotes $WINEPREFIX/drive_c/electrum-dnotes
cp electrum-dnotes/LICENCE .
#cp -r electrum-dnotes-locale/locale $WINEPREFIX/drive_c/electrum-dnotes/lib/
cp ../../../gui/qt/icons_rc.py $WINEPREFIX/drive_c/electrum-dnotes/gui/qt/

# Install frozen dependencies
$PYTHON -m pip install -r ../../deterministic-build/requirements.txt

$PYTHON -m pip install -r ../../deterministic-build/requirements-hw.txt

pushd $WINEPREFIX/drive_c/electrum-dnotes
$PYTHON setup.py install
popd

cd ..

rm -rf dist/

# build standalone and portable versions
wine "C:/python$PYTHON_VERSION/scripts/pyinstaller.exe" --noconfirm --ascii --name $NAME_ROOT-$VERSION -w deterministic.spec

# set timestamps in dist, in order to make the installer reproducible
pushd dist
find -exec touch -d '2000-11-11T11:11:11+00:00' {} +
popd

# build NSIS installer
# $VERSION could be passed to the electrum-dnotes.nsi script, but this would require some rewriting in the script itself.
wine "$WINEPREFIX/drive_c/Program Files (x86)/NSIS/makensis.exe" /DPRODUCT_VERSION=$VERSION electrum-dnotes.nsi

cd dist
mv electrum-dnotes-setup.exe $NAME_ROOT-$VERSION-setup.exe
cd ..

echo "Done."
md5sum dist/electrum-dnotes*exe
