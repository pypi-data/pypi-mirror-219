%define srcname gwdatafind-server
%define version 1.3.0
%define release 1

Name:      python-%{srcname}
Version:   %{version}
Release:   %{release}%{?dist}
Summary:   The server app for the GWDataFind service
License:   GPLv3+
Url:       https://git.ligo.org/gwdatafind/gwdatafind-server/
Source0:   %pypi_source
Packager:  Duncan Meacher <duncan.meacher@ligo.org>
Prefix:    %{_prefix}

BuildArch: noarch

# build dependencies
BuildRequires: python-srpm-macros
BuildRequires: python-rpm-macros
BuildRequires: python3-rpm-macros
BuildRequires: %__python3
BuildRequires: python%{python3_pkgversion}-setuptools
BuildRequires: python%{python3_pkgversion}-setuptools_scm
BuildRequires: python%{python3_pkgversion}-wheel
BuildRequires: systemd

# these are needed for setuptools to parse the version number
# out of gwdatafind_server/__init__.py, but only because setuptools
# is so old on rhel (< 46.4.0, https://github.com/pypa/setuptools/pull/1753)
%if 0%{?rhel} > 0 && 0%{?rhel} < 9
BuildRequires: python%{python3_pkgversion}-configobj
BuildRequires: python%{python3_pkgversion}-flask
BuildRequires: python%{python3_pkgversion}-ligo-segments
BuildRequires: python%{python3_pkgversion}-scitokens
# https://git.ligo.org/computing/packaging/rhel/python-configobj/-/issues/1
BuildRequires: python%{python3_pkgversion}-six
%endif

# -- src.rpm

%description
The GWDataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This is the source package for the
GWDataFind server.

# -- python3x-gwdatafind-server

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  Python %{python3_version} server app for the GWDataFind service
Requires: python%{python3_pkgversion}-configobj
Requires: python%{python3_pkgversion}-flask >= 1.0.0
Requires: python%{python3_pkgversion}-ligo-segments
Requires: python%{python3_pkgversion}-scitokens >= 1.7.0
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
%description -n python%{python3_pkgversion}-%{srcname}
The GWDataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the
Python %{python3_version} server app.

# -- gwdatafind-server

%package -n %{srcname}
Summary: GWDataFind Server Service
Requires: python%{python3_pkgversion}-gunicorn
Requires: python%{python3_pkgversion}-%{srcname} = %{version}-%{release}
%description -n %{srcname}
The GWDataFind service allows users to query for the location of
Gravitational-Wave Frame (GWF) files containing data from the current
gravitational-wave detectors. This package provides the HTTP app
configuration for a GWDataFind Service instance.

# -- build steps

%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
# app
%py3_install

# web server config examples
%__mkdir -pv %{buildroot}%{_datadir}/%{srcname}
%__install -m 644 -p -v config/gunicorn.conf %{buildroot}%{_datadir}/%{srcname}/
%__install -m 644 -p -v config/gunicorn.conf.py %{buildroot}%{_datadir}/%{srcname}/
%__install -m 644 -p -v config/wsgi.conf %{buildroot}%{_datadir}/%{srcname}/

# service config file
%__mkdir -pv %{buildroot}%{_sysconfdir}/
%__install -m 644 -p -v config/gwdatafind-server.ini %{buildroot}%{_sysconfdir}/%{srcname}.ini

# systemd
%__mkdir -pv %{buildroot}%{_unitdir}/
%__install -m 644 -p -v config/gwdatafind-server.service %{buildroot}%{_unitdir}/%{srcname}.service

%pre -n %{srcname}
getent group gwdatafind >/dev/null || groupadd -r gwdatafind
getent passwd gwdatafind >/dev/null || \
useradd \
    --system \
    --gid gwdatafind \
    --home-dir %{_sharedstatedir}/gwdatafind \
    --shell /sbin/nologin \
    --comment "Dedicated gwdatafind service account" \
    gwdatafind
exit 0

%post -n %{srcname}
%systemd_post %{srcname}.service

%preun -n %{srcname}
%systemd_preun %{srcname}.service

%postun -n %{srcname}
%systemd_postun_with_restart %{srcname}.service

%clean
rm -rf $RPM_BUILD_ROOT

%files -n python%{python3_pkgversion}-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/*

%files -n %{srcname}
%config(noreplace) %{_sysconfdir}/%{srcname}.ini
%doc README.md
%license LICENSE
%{_datadir}/%{srcname}/
%{_unitdir}/%{srcname}.service

# -- changelog

%changelog
* Fri Jul 13 2023 Duncan Meacher <duncan.meacher@ligo.org> 1.3.0-1
- Improved/cleaned up build and CI testing scripts
- Added OSDF URL support
* Fri May 05 2023 Duncan Meacher <duncan.meacher@ligo.org> 1.2.2-1
- Fixed bug in single file queries
- Fixed bug in search for fractional GPS times
* Fri Apr 07 2023 Duncan Meacher <duncan.meacher@ligo.org> 1.2.1-1
- Added comment handling in cache file
- Updated default SciToken issue and scope
- Added ability to search for fractional GPS times
* Thu Apr 21 2022 Duncan Meacher <duncan.meacher@ligo.org> 1.2.0-1
- Added full SciToken authentication support
- Updated README to point to documentation pages
- Improved error handling
- Updated CI tests and coverage
* Fri Mar 11 2022 Duncan Meacher <duncan.meacher@ligo.org> 1.1.0-1
- Added no-authentication method with virtual hosts
- Added API versioning
- general clean up of code
* Tue Jan 18 2022 Duncan Macleod <duncan.macleod@ligo.org> 1.0.1-1
- first packaging for RHEL
