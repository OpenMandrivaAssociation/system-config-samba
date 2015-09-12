%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(0)")}
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print get_python_version()")}

%bcond_with require_docs

Summary:	Samba server configuration tool
Name:		system-config-samba
Version:	1.2.92
Release:	13
URL:		http://fedorahosted.org/%{name}
License:	GPLv2+
Group:		System/Configuration/Networking
BuildArch:	noarch
Source0:	http://fedorahosted.org/released/%{name}/%{name}-%{version}.tar.bz2
Source1:	config.tar.gz
Patch0:		mdv_make.patch
Patch1:		mdv_dbus.patch
Patch2:		mdv_desktop.patch
BuildRequires:	python
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
BuildRequires:	gettext
BuildRequires:	intltool
# Until version 1.2.67, system-config-samba contained online documentation.
# From version 1.2.68 on, online documentation is split off into its own
# package system-config-samba-docs. The following ensures that updating from
# earlier versions gives you both the main package and documentation.
Requires:	system-config-samba-docs
Requires:	python-dbus
Requires:	pygtk2.0
Requires:	pygtk2.0-libglade
Requires:	python
Requires:	python-slip >= 0.2.6
Requires:	python-slip-dbus >= 0.2.9
Requires:	samba
Requires:	samba-common
Requires:	hicolor-icon-theme

%description
system-config-samba is a graphical user interface for creating, 
modifying, and deleting samba shares.

%prep
%setup -q -a 1
%patch0 -p0
%patch1 -p0
%patch2 -p0
#delete fedora config
rm -f config/org.fedoraproject.*

%build
make %{?_smp_mflags}

%install
make DESTDIR=%buildroot POLKIT0_SUPPORTED=0 install

%find_lang %name

# for consolehelper config
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_bindir}
ln -sf %{_sysconfdir}/pam.d/mandriva-simple-auth %{buildroot}%{_sysconfdir}/pam.d/system-config-samba
ln -sf %{_bindir}/consolehelper %{buildroot}%{_bindir}/system-config-samba

#fix desktop back for using /usr/bin dir

sed -i s/sbin/bin/ %{buildroot}%{_datadir}/applications/system-config-samba.desktop


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc COPYING
%{_bindir}/system-config-samba
%{_sbindir}/system-config-samba
%{_datadir}/system-config-samba
%{_datadir}/applications/system-config-samba.desktop
%{_datadir}/icons/hicolor/*/apps/system-config-samba.png
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/pam.d/*
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/polkit-1/actions/org.freedesktop.config.samba.policy
%{python_sitelib}/scsamba
%{python_sitelib}/scsamba-%{version}-py%{python_version}.egg-info
%{python_sitelib}/scsamba.dbus-%{version}-py%{python_version}.egg-info
