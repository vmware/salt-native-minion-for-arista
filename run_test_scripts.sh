#!/usr/bin/bash -x
# Copyright 2019-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2

CICD_SALT_VERSION_ADJ=$1
CICD_SALT_RELEASE=$2
/usr/bin/CliShell -c "show extensions" -e -p 15
/usr/bin/CliShell -c "$(echo -e enable\\nshow version)"
/usr/bin/CliShell -c "show management api http-commands" -e -p 15
/usr/bin/CliShell -c "$(echo -e enable\\nconfigure\\nmanagement api http-commands\\nprotocol unix-socket\\nno shutdown\\nend\\nwri)"
/usr/bin/CliShell -c "show management api http-commands" -e -p 15
/usr/bin/CliShell -c "dir flash:" -e -p 15
/usr/bin/CliShell -c "copy flash:salt-${CICD_SALT_VERSION_ADJ}-${CICD_SALT_RELEASE}.64.swix extension:" -e -p 15
/usr/bin/CliShell -c "extension salt-${CICD_SALT_VERSION_ADJ}-${CICD_SALT_RELEASE}.64.swix" -e -p 15
/usr/bin/CliShell -c "show extensions" -e -p 15
