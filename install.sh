#!/bin/sh

DIR=$(dirname ${0})

echo -n "Installing Anarchy Online chat .."

python ${DIR}/setup.py build >/dev/null && echo -n ".." &&
python ${DIR}/setup.py install >/dev/null && echo -n ".." &&
python ${DIR}/setup.py clean >/dev/null && echo -n ".." &&

rm -rf ${DIR}/build >/dev/null && echo " Done!" &&

exit 0 || exit 1
