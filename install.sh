#!/bin/sh

DIR=$(dirname ${0})

echo -n "Installing ..."

python ${DIR}/setup.py bdist_egg >/dev/null &&
python ${DIR}/setup.py clean >/dev/null &&

easy_install -f ${DIR} aochat

rm -rf ${DIR}/build >/dev/null &&
rm -rf ${DIR}/dist >/dev/null &&

echo " Done!" &&

exit 0 || exit 1
