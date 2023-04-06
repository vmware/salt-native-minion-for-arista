#!/usr/bin/bash

# Copyright 2019-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2

# shellcheck disable=SC2129,SC2016

pyenv_exist=$(which pyenv)
if [[ -z "$pyenv_exist" ]]; then
    sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
    ## mkdir .pyenv
    ## git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    curl https://pyenv.run | bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> "${HOME}/.bashrc"
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"'>> "${HOME}/.bashrc"
    echo 'eval "$(pyenv init -)"'>> "${HOME}/.bashrc"
    exec $SHELL -l
fi

curr_py3=$(python3 --version)
if [[ "Python 3.9.15" != "$curr_py3" ]]; then
    export PYTHON_CONFIGURE_OPTS="--enable-shared --enable-ipv6"
    export CONFIGURE_OPTS="--enable-shared --enable-ipv6"
    pyenv install 3.9.15
    pyenv global 3.9.15
    sudo rm -f /bin/python3
    sudo ln -s "${HOME}/.pyenv/versions/3.9.15/bin/python3" /bin/python3
    export LD_LIBRARY_PATH=~/.pyenv/versions/3.9.15/lib:$LD_LIBRARY_PATH
fi
