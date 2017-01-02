%global upstream_name requests-kerberos
%global module_name requests_kerberos

# Upstream doesn't support Python 3 yet, and there is no python3-kerberos.
%if 0 && 0%{?fedora}
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-%{upstream_name}
Version:        0.11.0
Release:        1%{?dist}
Summary:        A Kerberos authentication handler for python-requests
License:        MIT
URL:            https://github.com/requests/requests-kerberos
Source0:        https://github.com/requests/requests-kerberos/archive/v%{version}.tar.gz
# https://github.com/requests/requests-kerberos/issues/54
Patch2:         0002-avoid-handling-the-second-response-twice-fixes-54.patch
BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

Requires:       python-requests >= 1.1
Requires:       python-kerberos

%description
Requests is an HTTP library, written in Python, for human beings. This library 
adds optional Kerberos/GSSAPI authentication support and supports mutual 
authentication.

%if %{with python3}
%package -n python3-%{upstream_name}
Summary:        A Kerberos authentication handler for python-requests
Requires:       python3-requests >= 1.1
Requires:       python3-kerberos

%description -n python3-%{upstream_name}
Requests is an HTTP library, written in Python, for human beings. This library 
adds optional Kerberos/GSSAPI authentication support and supports mutual 
authentication.
%endif

%prep
%setup -q -n %{upstream_name}-%{version}
%patch2 -p1

%if %{with python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif

%build
%{__python} setup.py build

%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%install
%if %{with python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
popd
%endif

%{__python} setup.py install --skip-build --root %{buildroot}

%files
%doc README.rst LICENSE AUTHORS HISTORY.rst
%{python_sitelib}/%{module_name}
%{python_sitelib}/%{module_name}*.egg-info

%if %{with python3}
%files -n python3-%{upstream_name}
%doc README.rst LICENSE AUTHORS HISTORY.rst
%{python3_sitelib}/%{module_name}
%{python3_sitelib}/%{module_name}*.egg-info
%endif

%changelog
* Mon Jan 02 2017 Jajauma's Packages <jajauma@yandex.ru> - 0.11.0-1
- Update to latest upstream release
- Drop 0001-relax-version-in-kerberos-requirement.patch

* Thu Jun 11 2015 Dan Callaghan <dcallagh@redhat.com> - 0.7.0-2
- relaxed version in kerberos module requirement, to work with
  python-kerberos 1.1 (#1215565)
- fix double response handling with requests 1.1 (#1169296)

* Tue May 05 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.7.0-1
- Update to 0.7.0 (#1164464)

* Fri Nov 07 2014 Dan Callaghan <dcallagh@redhat.com> - 0.6-1
- fix for mutual authentication handling (RHBZ#1160545, CVE-2014-8650)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Dan Callaghan <dcallagh@redhat.com> - 0.5-1
- upstream bug fix release 0.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 03 2013 Dan Callaghan <dcallagh@redhat.com> - 0.3-1
- upstream bug fix release 0.3

* Mon May 27 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-2
- require requests >= 1.0

* Tue May 14 2013 Dan Callaghan <dcallagh@redhat.com> - 0.2-1
- initial version
