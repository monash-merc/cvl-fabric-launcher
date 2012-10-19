# Don't try fancy stuff like debuginfo, which is useless on binary-only
# packages. Don't strip binary too
# Be sure buildpolicy set to do nothing
%define        __spec_install_post %{nil}
%define          debug_package %{nil}
%define        __os_install_post %{_dbpath}/brp-compress

Summary: MASSIVE/CVL Launcher
Name: massive-launcher
Version: 0.3.1
Release: 1
License: GPL+
Group: Development/Tools
SOURCE0 : %{name}-%{version}.tar.gz
URL: https://www.massive.org.au/userguide/cluster-instructions/massive-launcher

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

provides: libc.so.6(GLIBC_PRIVATE)

# http://www.mail-archive.com/fedora-devel-list@redhat.com/msg13200.html
%global __prelink_undo_cmd %{nil}


%description
%{summary}

%prep
%setup -q

%build
# Empty section.

%install
rm -rf %{buildroot}
mkdir -p  %{buildroot}

# in builddir
cp -a * %{buildroot}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
# %config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
#%{_bindir}/*
/opt/*

%changelog
* Fri Oct 19 2012 boo
- boo
