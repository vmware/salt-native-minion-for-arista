#!/usr/bin/bash

# Copyright 2019-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2

# shellcheck disable=SC2016

PYVERSION="3.9.15"
PYTHON_OPTS="--enable-optimizations --enable-shared --enable-ipv6"

if [[ $(python3 --version) != "Python ${PYVERSION}" ]] ; then
    oldpwd=$(pwd)
    rm -fR dev_python3.9
    mkdir dev_python3.9
    cd dev_python3.9 || exit
    wget "https://www.python.org/ftp/python/${PYVERSION}/Python-${PYVERSION}.tgz"
    tar -xvf "Python-${PYVERSION}.tgz"
    cd "Python-${PYVERSION}" || exit
    ./configure "${PYTHON_OPTS}" 2>&1 | tee "${HOME}/mypython_${PYVERSION}.log"
    make -j "$(nproc)" 2>&1 | tee -a "${HOME}/mypython_${PYVERSION}.log"
    sudo make altinstall 2>&1 | tee -a "${HOME}/mypython_${PYVERSION}.log"
    cd /usr/bin/ || exit
    sudo ln -f -s /usr/local/bin/python3.9 python3
    sudo ln -f -s /usr/local/bin/python3.9 python3.9
    sudo ln -f -s /usr/local/bin/python3.9-config python3-config
    sudo ln -f -s /usr/local/bin/pip3.9 pip3
    sudo ldconfig /usr/local/lib
    echo "remember to do the following:"
    echo 'export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH'
    echo 'export PATH=/usr/local/bin:$PATH'
    cd "${oldpwd}" || exit
fi
