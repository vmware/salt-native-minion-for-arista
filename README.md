# Salt Project Native Minions for Arista salt-native-minion-for-arista

## Overview

Salt Native Minion for Arista was originally developed on GitLab
Here are the instructions for GitLab, but in final releases, the Salt Native
Minion for Arista was built using a bash script.

Note:   The GitLab CI/CD relies on GO in it's backend for some tasks to be
        accomplished, for example: the uploading of build artifacts.

        At the time of writing 2022-11-09 the GO implementation and build number
        for SaltStack environment exceeds a 32-bit number, and hence CI/CD builds
        fail to upload any artifacts built. This limitation may not occur in
        other GitLab CI/CD environments.

## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.


## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://gitlab.com/saltstack/open/salt-native-minion-arista.git
git branch -M master
git push -uf origin master
```

## Integrate with your tools

- [ ] [Set up project integrations](https://gitlab.com/saltstack/open/salt-native-minion-arista/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Automatically merge when pipeline succeeds](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)

## Name

Salt support for Arista EOS 32-bit and 64-bit platforms

## Description

This project allows you to build support for Salt on Arista EOS 32-bit and 64-bit Intel-based routers.

Provided is a .gitlab-ci.yml file to utilise GitLab CI/CD or alternatively can use the test_bld_xxxx Bash scripts

The CI/CD file and Bash scripts generate a 32-bit and 64-bit Arista EOS SWIX package which can be installed and removed with Arista tools.

Documation on Salt 3005.1 for Arista EOS can be found here:

    https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/arista.html


## Installation

### Before installing the Arista native minion:

Check that your network device and firmware are supported. See Arista for more information.
Ensure that ports 4505 and 4506 are open on the applicable Arista switches or routers.
Salt uses ports 4505 and 4506 for outbound communication from the master to the minions. The Arista native minion uses a direct connection to the Arista switch or router and uses the Management Interface on the switch/router for communication. For that reason, ports 4505 and 4506 need to be open on the appropriate Management Interfaces.

Arista network devices run Arista EOS, which includes the Arista CLI. When connecting to an Arista network device, you start at the OS-level. Arista has a mode called Arista CLI privileged mode in which you can enter a Bash shell if needed. The command enable enters privileged mode. With this in mind, this guide assumes all commands are entered into the Arista CLI.

#### Install Salt on Arista

The Arista native minion package installs:

*   salt-minion service
*   salt-call service

Note: The salt-ssh and salt-proxy services are not installed with this package.

#### Minion SWIX package installation:

##### To install the SWIX package:

- Download, verify, and transfer the Arista installation files from (prior to community-support this was repo.saltproject.io). The Arista native minion package is a SWIX file.

Note: If installing on a virtual machine, consult the documentation for your hypervisor as the commands might differ slightly.

- Once the Arista native minion is available in the flash directory, enter privileged mode and copy the SWIX extension, replacing the placeholder text with the correct file name:

.. code-block::

    copy flash:arista-native-minion-filename.swix extension:

- View the extensions detail by running the following command:

.. code-block::

    show extensions detail

This command returns an output similar to the following example:

.. code-block::

            Name: salt-|arista-version|.64.swix
         Version: |arista-version|
         Release: 1
        Presence: available
          Status: not installed
          Vendor:
         Summary: Self contained Salt Minion binary
        Packages:
      Total size: 0 bytes
     Description:
     Self contained Python |arista-python-version| Salt Minion 64-bit binary

- Install the SWIX package, replacing the placeholder text with the correct file name:

.. code-block::

    extension arista-native-minion-filename.swix

- View the extensions detail again to verify that the status, package, and file size has changed:

.. code-block::

    show extensions detail

This command returns an output similar to the following example:

.. code-block::

            Name: salt-3005.1.64.swix
         Version: 3005.1
         Release: 1
        Presence: available
          Status: installed
          Vendor:
         Summary: Self contained Salt Minion binary
        Packages: salt-3005.1.x86_64.rpm 3005.1/1
      Total size: 222446843 bytes
     Description:
     Self contained Python |arista-python-version| Salt Minion 64-bit binary

- Run the following commands:

.. code-block::

    bash
    sudo su

- Edit the /etc/salt/minion file to update the minion configuration with your environment’s specific details, such as the master’s IP address, the minion ID, etc. For example, to set the minion name:

.. code-block::

    id: your-arista-minion-name

Edit the file to indicate the IP address of the master that is managing this minion. For example:

.. code-block::

    master: 192.0.2.1

- (Optional): If your router does not have the ability to use Reverse DNS lookup to obtain the Fully Qualified Domain Name (fqdn) for an IP Address, check the enable_fqdns_grains setting in the minion configuration file, /etc/salt/minion and ensure it is *False* instead. For example:

.. code-block::

    enable_fqdns_grains: False

Note: On a regular salt-minion this setting is defaulted to *True*, but for native minions the setting has been defaulted to *False*. This setting, if *True*, allows all IP addresses to be processed with underlying calls to socket.gethostbyaddr. These calls can take up to 5 seconds to be released after reaching socket.timeout. During that time, there is no fqdn for that IP address. Although calls to socket.gethostbyaddr are processed asynchronously, the calls still add 5 seconds every time grains are generated if an IP does not resolve.  Hence the reason to default the setting to False on native minions, some of which can be used on routers.

- Verify that Salt is running:

.. code-block:: bash

    ps -ef | grep salt

If the minion is installed correctly and is disabled, the output is similar to the following:

.. code-block:: bash

    * salt-minion.service - The Salt Minion
       Loaded: loaded (/usr/lib/systemd/system/salt-minion.service; disabled; vendor preset: disabled)
       Active: inactive (dead)
         Docs: man:salt-minion(1)
               file:///usr/share/doc/salt/html/contents.html
               https://docs.saltproject.io/en/latest/contents.html

- Start the Arista native minion as a daemon and check its status with the following command:

.. code-block:: bash

    sudo systemctl start salt-minion

The output should be similar to the following:

.. code-block::

       salt-minion.service - The Salt Minion
       Loaded: loaded (/usr/lib/systemd/system/salt-minion.service; disabled; vendor preset: disabled)
       Active: active (running) since Wed 2020-09-02 16:22:11 UTC; 4s ago
         Docs: man:salt-minion(1)
               file:///usr/share/doc/salt/html/contents.html
               https://docs.saltproject.io/en/latest/contents.html
     Main PID: 4259 (salt-minion)
       Memory: 81.7M (limit: 250.0M)
       CGroup: /system.slice/salt-minion.service
               |-4259 /bin/bash /usr/bin/salt-minion
               |-4267 /opt/saltstack/salt/run/run minion
               |-4268 /opt/saltstack/salt/run/run minion
               |-4273 /opt/saltstack/salt/run/run minion KeepAlive MultiMinionProcessManager MinionProcessManager
               |-4275 /opt/saltstack/salt/run/run minion KeepAlive MultiprocessingLoggingQueue

Note: Alternatively, you can check whether Salt is running with the command: ps -ef | grep salt.

- Once the Arista native minion has been started and is running, you can use the command salt-key to verify the master has received a request for the minion key.

- On the master, accept the minion’s key with the following command, replacing the placeholder test with the correct minion name:

.. code-block:: bash

    salt-key -y -a your-arista-minion-name

- After waiting a small period of time, verify the connectivity between the master and minion using simple commands. For example, try running the following commands:

.. code-block:: bash

    salt your-arista-minion-name test.versions
    salt your-arista-minion-name grains.items
    salt your-arista-minion-name cmd.run ‘ls -alrt /’

If the key is accepted and the binding process is complete, you might see an output similar to the following example:

.. code-block:: bash

     salt-master# salt arista-423 test.versions
     arista64-423:
         Salt Version:
                 Salt: 3005.1

         Dependency Versions:
                     cffi: 1.14.2
                 cherrypy: Not Installed
                 dateutil: Not Installed
                docker-py: Not Installed
                    gitdb: Not Installed
                gitpython: Not Installed
                   Jinja2: 2.11.2
                  libgit2: Not Installed
                 M2Crypto: 0.36.0
                     Mako: Not Installed
             msgpack-pure: Not Installed
           msgpack-python: 1.0.0
             mysql-python: Not Installed
                pycparser: 2.14
                 pycrypto: Not Installed
             pycryptodome: 3.9.8
                   pygit2: Not Installed
                   Python: |arista-python-version|
             python-gnupg: Not Installed
                   PyYAML: 5.3.1
                    PyZMQ: 19.0.2
                    smmap: Not Installed
                  timelib: Not Installed
                  Tornado: 4.5.3
                      ZMQ: 4.3.2

          System Versions:
                     dist: centos 7 Core
                   locale: utf-8
                  machine: x86_64
                  release: 4.9.122.Ar-15352225.4232F
                   system: Linux
                  version: CentOS Linux 7 Core

##### Enabling Arista eAPI access for the minion

The Arista native minion uses the pyeapi library to communicate with the Arista device. The pyeapi library is provided and installed by default with the Arista native minion. However, it is not installed by default with the standard Salt minion package.

Note: This document makes a distinction between a proxy minion connecting remotely to an Arista device and a standard minion making a remote connection. In general, the Arista native minion behaves more like the standard minion. The native minion has its own Salt keys, can be targeted with grains, and can report back.

###### To enable eAPI access:

- Turn on the Arista API using the following commands:

.. code-block::

    arista # config
    arista(config) # management API http-commands
    arista(config-mgmt-api-http-cmds) # protocol unix-socket
    arista(config-mgmt-api-http-cmds) # no shutdown
    arista(config-mgmt-api-http-cmds)
    arista(config-mgmt-api-http-cmds) # exit
    arista(config) # exit
    arista # write

- Open the minion configuration file at /etc/salt/minion and add the following section:

.. code-block::

    pyeapi:
      username: <name of admin or eAPI user>
      password: <password of admin or eAPI user>
      transport: socket
      enablepwd: <password for enable mode, optional>

- Restart the salt-minion service on the device with the following command:

.. code-block:: bash

    sudo systemctl restart salt-minion

- Connect the Arista native minion to its master and ensure its key has has been accepted, as explained in Minion SWIX package installation.

- Run the following command, replacing the placeholder text with the minion ID for the Arista native minion:

.. code-block:: bash

    salt arista-minion-ID test.ping

- If this command returns a value of *True*, you can execute eAPI commands in the shell. For example:

.. code-block:: bash

    salt-master# salt arista64-423 pyeapi.get_config
    arista64-423:
        - ! Command: show running-config
        - ! device: veos64-423 (vEOS, EOS-4.23.2F)
        - !
        - ! boot system flash:/vEOS-lab.swi
        - !
        - transceiver qsfp default-mode 4x10G
        - !
        - hostname veos64-423
        - ip name-server vrf default 8.8.8.8
        - !
        - spanning-tree mode mstp
        - !
        - no aaa root
        - !
        - username admin role network-admin secret sha512 $6$jm1wk44bKE2rRHfP$fc.OCS7/jqgNgHPymxo370c1XgoaS6V894tff02YIlgV2B.7kGczXpgpa0HDQs3tn.5eBcmIpwNiNszXqfSEf.
        - !
        - interface Ethernet1
        - !
        - interface Ethernet2
        - !
        - interface Ethernet3
        - !
        - interface Management1
        -    ip address 10.0.2.63/24
        - !
        - no ip routing
        - !
        - ip route 0.0.0.0/0 10.0.2.2
        - !
        - management api http-commands
        -    protocol unix-socket
        -    no shutdown
        - !
        - end

    salt-master#

For more documentation on the capabilities of pyeapi, see the Salt Arista pyeapi module documentation.


##### Configure the Napalm module

The napalm library is provided and installed by default with the Arista native minion. However, it is not installed by default with the standard Salt minion package.

To configure the native minion to use the napalm module:

- Open the minion configuration file at /etc/salt/minion and add the following section:

.. code-block::

    napalm:
      username: <name of admin or user>
      password: <password of admin or user>
      host: localhost
      driver: eos

- Restart the salt-minion service on the device with the following command:

.. code-block:: bash

    systemctl restart salt-minion

- Connect the Arista native minion to its master and ensure its key has has been accepted, as explained in Minion SWIX package installation.

- Run the following command to test that the module is configured correctly:

.. code-block:: bash

    salt veos-420 napalm.alive

This command should have an output similar to the following:

.. code-block:: bash

    veos-420:
       ----------
       comment:
       out:
          ----------
          is_alive:
              True

       result:
           True

See Salt Proxy Napalm module documentation for more information about this module.

#### Minion SWIX package removal

Removing the SWIX pack is similar to installation. The main difference is that the prefix no is prepended to certain commands.

Note: For more information, see the Arista documentation on extensions removal.

##### To remove the SWIX package:

- Run the following command:

.. code-block::

    show extensions detail

The output should be similar to the following example:

.. code-block::

            Name: salt-3005.1.64.swix
         Version: 3005.1
         Release: 1
        Presence: available
          Status: installed
          Vendor:
         Summary: Self contained Salt Minion binary
        Packages: salt-3005.1.x86_64.rpm 3005.1/1
      Total size: 222446843 bytes
     Description:
     Self contained Python 3005.1 Salt Minion 64-bit binary

- Remove the SWIX package by running the following command, replacing the placeholder file with the correct file name:

.. code-block::

    no extension arista-native-minion-filename.swix

- Delete the SWIX package by running the following command, replacing the placeholder file with the correct file name:

.. code-block::

    delete extension:arista-native-minion-filename.swix

- View the extensions detail again to verify that the status, package, and file size has changed by running the following command:

.. code-block::

    show extensions detail

This command returns an output similar to the following example:

.. code-block::

            Name: salt-3005.1.64.swix
         Version: 3005.1
         Release: 1
        Presence: available
          Status: not installed
          Vendor:
         Summary: Self contained Salt Minion binary
        Packages:
      Total size: 0 bytes
     Description:
     Self contained Python 3005.1 Salt Minion 64-bit binary


#### Post-installation

This reference section includes additional resources for porting the salt-minion service to Arista devices.

##### Starting and stopping the Arista native minion

After installation, you can disable (stop) and enable (start) the Arista native minion using the following commands:

.. code-block::

    systemctl stop salt-minion

To restart the Arista native minion, use the following command:

.. code-block::

    systemctl start salt-minion


## Creating a Tiamat-utilising rpm-based package

To create a rpm-based package for Arista which utilises Tiamat, the GitLab CI/CD pipeline used to do all the work, but as stated above, 32-bit limitations were encountered, hence the development of bash scripts to build 32-bit and 64-bit  SWIX packages.

### Building 32-bit Arista

Steps:

1. Utilize Centos 7 Alt-Arch 32-bit machine
2. Create tiamat build on 32-bit build machines using quickbuild_32
3. Move build product to Fedora Core 18 packaging machine
4. Create 32-bit rpm package (includes minion conf., systemd files, salt-call/salt-minion)
5. Move rpm package to base level Arista EOS 32-bit machine
6. Create SWIX package (including list of dependencies)
7. Run tests against multiple EOS versions

### Building 64-bit Arista

Steps:

1. Utilize Centos 7 machine
2. Create tiamat build on 64-bit build machines using quickbuild_64
3. Create 64-bit rpm package (includes minion conf., systemd files, salt-call/salt-minion)
4. Move rpm package to base level EOS 64-bit machine
5. Create SWIX package (including list of dependencies)
6. Run tests against multiple EOS versions

#### Dependencies and known issues

The Arista native minion is a self-contained binary that includes Salt 3005.1 with pyeapi and other Naplam dependencies that internally use Python 3.9.14 for 64-bit, and Python 3.7.16 for 32-bit. All Python 3 utf-8 considerations are handled internally leveraging Python PEP 538 and 540 and hence can function in locales which only support ‘C’ and POSIX without issue.

Note: The 64-bit Arista native minion uses Python 3.9.14, but the 32-bit Arista native minion uses Python 3.7.15 which is due to dependencies used with Python 3.9.14 which do not support 32-bit fully.

Since the Arista native minion is a self contained binary, there are no external dependencies to be considered.

Note: The deprecations are warnings of functionality that will be removed in Python 3.9. These deprecations do not affect current functionality and will be resolved in future versions of Salt.

The issue with the napalm grains also occurs on standard minions. It will be resolved in a future release of Salt.

## Support

Support can be found in various Salt communities, such as, Slack: https://saltstackcommunity.slack.com

## Contributing

Salt support on Arista is a community-run project and open to all contributions
The salt-native-minion-for-arista project team welcomes contributions from the
community. Before you start working with salt-native-minion-for-arista, please
read our [Developer Certificate of Origin](https://cla.vmware.com/dco).
All contributions to this repository must be signed as described on that page.
Your signature certifies that you wrote the patch or have the right to pass it
on as an open-source patch. For more detailed information,
refer to [CONTRIBUTING.md](CONTRIBUTING.md).

The regular Open Source methods of contributing to a project apply:

*   Fork the project
*   Make your modifications to your fork
*   Provide tests for your modifications
*   Submit Merge/Pull Request to the project
*   Adjust modifications as per Reviewers of Merge/Pull Request

## Additional reference

For reference, see:

* Arista EOS/Networking Tips https://aristaeos.blogspot.com/2019/03/install-arista-eos-swix-image.html
* Arista documentation on Extensions https://www.arista.com/en/qsg-book-search?searchword=eos%20section%206%207%20managing%20eos%20extensions&searchphrase=all&catid=Nzc
* Configuring VirtualBox (video) https://youtu.be/nbDF7hzBPM0
* Port forwarding (video) https://youtu.be/QEmHqHpeoZM
* Enable SSH (Arista Forums) https://aristanetworks.force.com/AristaCommunity/s/question/0D52I00007ERqMkSAL/enable-ssh


## Authors and acknowledgment

The initial work in porting Salt for the Arista platform was done by David Murphy damurphy@vmware.com

## License

Apache License 2.0

## Project status

The Salt native minion for Arista EOS is now a community project.  In the past, VMware through Salt Project supported and developed Salt for Arista EOS, but VMware has now turned over on-going development to the community.

The project is currently seeking volunteers to step in as a maintainer or owner, to allow the project to keep going.

