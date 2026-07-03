%global commitdate 20260226
%global commit 4712347f2da0b7d4a5fbdb0d81d071c1704b3f20
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           bpftune
Version:        0.4.%{commitdate}.git.%{shortcommit}
Release:        3%{?dist}
Summary:        BPF/tracing tools for auto-tuning Linux

License:        GPL-2.0-only WITH Linux-syscall-note
URL:            https://github.com/oracle/bpftune
Source0:        %{url}/archive/%{commit}/%{name}-%{commit}.tar.gz

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libbpf-devel >= 0.6
BuildRequires:  libcap-devel
BuildRequires:  bpftool >= 4.18
BuildRequires:  libnl3-devel
BuildRequires:  clang >= 11
BuildRequires:  clang-libs >= 11
BuildRequires:  llvm >= 11
BuildRequires:  llvm-libs >= 11
BuildRequires:  python3-docutils
BuildRequires:  systemd-rpm-macros

%description
Service consisting of daemon (bpftune) and plugins which
support auto-tuning of Linux via BPF observability.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libbpf-devel >= 0.6
Requires:       libcap-devel
Requires:       bpftool
Requires:       libnl3-devel

%description devel
The %{name}-devel package contains libraries and header files for
developing BPF shared object tuners that use %{name}.

%prep
%autosetup -n %{name}-%{commit}

%build
%make_build

%install
%make_install
rm -f %{buildroot}%{_sysconfdir}/init.d/%{name}
rm -f %{buildroot}%{_sysconfdir}/ld.so.conf.d/libbpftune.conf
sed -i 's|/usr/sbin/bpftune|%{_sbindir}/bpftune|g' %{buildroot}%{_unitdir}/%{name}.service
soname=$(basename %{buildroot}%{_libdir}/libbpftune.so.0.4.*)
ln -sf "$soname" %{buildroot}%{_libdir}/libbpftune.so

%post
%systemd_post bpftune.service

%preun
%systemd_preun bpftune.service

%postun
%systemd_postun_with_restart bpftune.service

%files
%license LICENSE.txt
%doc README.md
%config(noreplace) %{_sysconfdir}/conf.d/bpftune
%{_sbindir}/bpftune
%{_unitdir}/bpftune.service
%{_libdir}/libbpftune.so.0.4.*
%{_libdir}/bpftune/
%{_mandir}/man8/bpftune.8*
%{_mandir}/man8/bpftune-ip-frag.8*
%{_mandir}/man8/bpftune-neigh.8*
%{_mandir}/man8/bpftune-net-buffer.8*
%{_mandir}/man8/bpftune-netns.8*
%{_mandir}/man8/bpftune-sysctl.8*
%{_mandir}/man8/bpftune-tcp-buffer.8*
%{_mandir}/man8/bpftune-tcp-conn.8*
%{_mandir}/man8/bpftune-udp-buffer.8*
%dir %{_localstatedir}/lib/pcp/pmdas/bpftune
%{_localstatedir}/lib/pcp/pmdas/bpftune/*

%files devel
%license LICENSE.txt
%{_libdir}/libbpftune.so
%{_includedir}/bpftune/

%changelog
* Fri Jul 03 2026 ElXreno <elxreno@gmail.com> - 0.4.20260226.git.4712347-3
- Follow Fedora packaging guidelines: SPDX license tag, drop obsolete
  ldconfig scriptlets and useless ld.so.conf.d file, drop redundant
  explicit library Requires, make devel .so a proper symlink

* Fri Jul 03 2026 ElXreno <elxreno@gmail.com> - 0.4.20260226.git.4712347-2
- Drop openrc init script (bogus /sbin/openrc-run dependency on Fedora)
- Fix systemd unit ExecStart path for sbin-merged Fedora
