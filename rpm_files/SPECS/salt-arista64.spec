# Copyright 2019-2022 VMware, Inc.
# SPDX-License-Identifier: Apache-2

# Turn off the brp-python-bytecompile automagic
%global _python_bytecompile_extra 0

# Turn off the brp-python-bytecompile script
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

%global srcname salt
%global oldname salt-bin-arista


Name:       %{srcname}
Version:    VERSION_TO_BE_REPLACED
Release:    RELEASE_TO_BE_REPLACED
Group:      System Environment/Daemons
Summary:    Self contained Salt Minion binary
License:    ASL 2.0

Source0: run
Source1: minion
Source2: salt-common.logrotate
Source3: salt-minion.service
Source4: salt-call
Source5: salt-minion
Source6: %{oldname}


BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%if 0%{?systemd_preun:1}
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

## ensure BUILD directory exists in conjunction with SPECS and SOURCES
## for Arista, that is, mkdir -p BUILD

%description
Self contained Python 3.9 Salt Minion 64-bit binary

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%install
rm -fR %{buildroot}

mkdir -p %{buildroot}/opt/saltstack/salt
cp -ra %{SOURCE0} %{buildroot}/opt/saltstack/salt

# Add some directories
install -d -m 0755 %{buildroot}%{_var}/log/salt
touch %{buildroot}%{_var}/log/salt/minion
install -d -m 0755 %{buildroot}%{_var}/cache/salt
## install -d -m 0755 %{buildroot}/etc/salt
## install -d -m 0755 %{buildroot}/etc/salt/minion.d
## install -d -m 0755 %{buildroot}/etc/salt/pki
## install -d -m 0755 %{buildroot}/etc/salt/pki/minion
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/minion.d
install -d -m 0755 %{buildroot}%{_sysconfdir}/salt/pki
install -d -m 0700 %{buildroot}%{_sysconfdir}/salt/pki/minion
install -d -m 0755 %{buildroot}%{_bindir}

# Add helper scripts
install -m 0755 %{SOURCE4} %{buildroot}%{_bindir}/salt-call
install -m 0755 %{SOURCE5} %{buildroot}%{_bindir}/salt-minion

# fake out old name salt-bin-arista to allow for backwards
# compatibilty for the first few releases
mkdir -p %{buildroot}%{_bindir}/%{oldname}
install -m 0755 %{SOURCE6} %{buildroot}%{_bindir}/%{oldname}/%{oldname}

# Add the config files
install -p -m 0640 %{SOURCE1} %{buildroot}%{_sysconfdir}/salt/minion

# Logrotate
mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d/
install -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/salt

# Add the Systemd unit files
mkdir -p %{buildroot}%{_unitdir}
install -p -m 0644 %{SOURCE3} %{buildroot}%{_unitdir}/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_var}/cache/salt
%{_var}/log/salt
%{_unitdir}/salt-minion.service
%config(noreplace) %{_sysconfdir}/logrotate.d/salt
/opt/saltstack/salt/run
%{_bindir}/salt-call
%{_bindir}/salt-minion
%{_bindir}/%{oldname}/%{oldname}
%config(noreplace) %{_sysconfdir}/salt/
%config(noreplace) %{_sysconfdir}/salt/minion
%config(noreplace) %{_sysconfdir}/salt/minion.d
%config(noreplace) %{_sysconfdir}/salt/pki/minion

%preun
%if 0%{?systemd_preun:1}
  %systemd_preun salt-minion.service
%else
  if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable salt-minion.service > /dev/null 2>&1 || :
    /bin/systemctl stop salt-minion.service > /dev/null 2>&1 || :
  fi
%endif

%post
%if 0%{?systemd_post:1}
  if [ $1 -gt 1 ] ; then
    /usr/bin/systemctl try-restart salt-minion.service >/dev/null 2>&1 || :
  else
    %systemd_post salt-minion.service
  fi
%else
  /bin/systemctl daemon-reload &>/dev/null || :
%endif

%postun
%if 0%{?systemd_post:1}
  %systemd_postun_with_restart salt-minion.service
%else
  /bin/systemctl daemon-reload &>/dev/null
  [ $1 -gt 0 ] && /bin/systemctl try-restart salt-minion.service &>/dev/null || :
%endif

%changelog
* DATE_TO_BE_REPLACED SaltStack Packaging Team <packaging@saltstack.com> - %{version}-%{release}
- Update for Arista 64-bit native minion for point release Salt %{version}

* Tue Aug 18 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3001.1
- Update for Arista 64-bit native minion for point release Salt 3001.1

* Wed Apr 08 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3000.1
- Update for point release Salt 3000.1, includes setproctitle

* Mon Mar 23 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3000-4
- Rebuilt salt-bin using Python 3.7.6

* Thu Mar 12 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3000-3
- fixes for systemd functionality

* Tue Mar 10 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3000-2
- onedir based rpm for delivering Salt Minion binary to Arista 32-bit platforms

* Thu Feb 20 2020 SaltStack Packaging Team <packaging@saltstack.com> - 3000-1
- Initial rpm for delivering Salt Minion binary to Arista 32-bit platforms
