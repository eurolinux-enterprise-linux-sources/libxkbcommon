#global gitdate  20120917

Name:           libxkbcommon
Version:        0.7.1
Release:        3%{?gitdate:.%{gitdate}}%{?dist}
Summary:        X.Org X11 XKB parsing library
License:        MIT
URL:            http://www.x.org

%if 0%{?gitdate}
Source0:       %{name}-%{gitdate}.tar.bz2
%else
Source0:        http://xkbcommon.org/download/%{name}-%{version}.tar.xz
%endif
Source1:        make-git-snapshot.sh

# Bug 1623033 - CVE-2018-15864
Patch01:        0001-parser-Don-t-set-more-maps-when-we-don-t-have-any.patch
# Bug 1643488 - CVE-2018-15863
Patch02:        0002-xkbcomp-Don-t-crash-on-no-op-modmask-expressions.patch
# Bug 1623029 - CVE-2018-15862
Patch03:        0003-xkbcomp-Don-t-explode-on-invalid-virtual-modifiers.patch
# Bug 1643480 - CVE-2018-15861
Patch04:        0004-xkbcomp-Don-t-falsely-promise-from-ExprResolveLhs.patch
# Bug 1643153 - CVE-2018-15857
Patch05:        0005-xkbcomp-fix-pointer-value-for-FreeStmt.patch
# Bug 1643141 - CVE-2018-15856
Patch06:        0006-compose-fix-infinite-loop-in-parser-on-some-inputs.patch
# Bug 1643073 - CVE-2018-15855
Patch07:        0007-xkbcomp-fix-crash-when-parsing-an-xkb_geometry-secti.patch
# Bug 1642880 - CVE-2018-15854
Patch08:        0008-xkbcomp-fix-crashes-in-the-parser-when-geometry-toke.patch
# Bug 1642853 - CVE-2018-15853
Patch09:        0009-xkbcomp-fix-stack-overflow-when-evaluating-boolean-n.patch
# Bug 1643477 - CVE-2018-15859
Patch10:        0010-Fail-expression-lookup-on-invalid-atoms.patch

BuildRequires:  autoconf automake libtool
BuildRequires:  xorg-x11-util-macros byacc flex bison
BuildRequires:  xorg-x11-proto-devel libX11-devel
BuildRequires:  xkeyboard-config-devel
BuildRequires:  pkgconfig(xcb-xkb) >= 1.10

Requires:       xkeyboard-config

%description
%{name} is the X.Org library for compiling XKB maps into formats usable by
the X Server or other display servers.

%package devel
Summary:        X.Org X11 XKB parsing development package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
X.Org X11 XKB parsing development package

%package x11
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description x11
%{name}-x11 is the X.Org library for creating keymaps by querying the X
server.

%package x11-devel
Summary:        X.Org X11 XKB keymap creation library
Requires:       %{name}-x11%{?_isa} = %{version}-%{release}

%description x11-devel
X.Org X11 XKB keymap creation library development package

%prep
%setup -q -n %{name}-%{?gitdate:%{gitdate}}%{!?gitdate:%{version}}

autoreconf -v --install || exit 1
%patch01 -p1
%patch02 -p1
%patch03 -p1
%patch04 -p1
%patch05 -p1
%patch06 -p1
%patch07 -p1
%patch08 -p1
%patch09 -p1
%patch10 -p1

%build
%configure \
  --disable-silent-rules \
  --disable-static \
  --enable-x11 \
  --disable-docs

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

find $RPM_BUILD_ROOT -name '*.la' -exec rm -fv {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_libdir}/libxkbcommon.so.0.0.0
%{_libdir}/libxkbcommon.so.0

%files devel
%{_libdir}/libxkbcommon.so
%dir %{_includedir}/xkbcommon/
%{_includedir}/xkbcommon/xkbcommon.h
%{_includedir}/xkbcommon/xkbcommon-compat.h
%{_includedir}/xkbcommon/xkbcommon-compose.h
%{_includedir}/xkbcommon/xkbcommon-keysyms.h
%{_includedir}/xkbcommon/xkbcommon-names.h
%{_libdir}/pkgconfig/xkbcommon.pc

%post x11 -p /sbin/ldconfig
%postun x11 -p /sbin/ldconfig

%files x11
%{_libdir}/libxkbcommon-x11.so.0.0.0
%{_libdir}/libxkbcommon-x11.so.0

%files x11-devel
%{_libdir}/libxkbcommon-x11.so
%{_includedir}/xkbcommon/xkbcommon-x11.h
%{_libdir}/pkgconfig/xkbcommon-x11.pc

%changelog
* Wed Mar 06 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-3
- Actually apply the patch files

* Mon Feb 11 2019 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-2
- Fixes for
  CVE-2018-15864, CVE-2018-15863, CVE-2018-15862, CVE-2018-15861,
  CVE-2018-15859  CVE-2018-15857, CVE-2018-15856, CVE-2018-15855,
  CVE-2018-15854, CVE-2018-15853

* Thu Jan 19 2017 Peter Hutterer <peter.hutterer@redhat.com> 0.7.1-1
- xkbcommon 0.7.1

* Mon Nov 14 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.7.0-1
- xkbcommon 0.7.0

* Fri Jun 03 2016 Peter Hutterer <peter.hutterer@redhat.com> 0.6.1-1
- xkbcommon 0.6.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Dan Horák <dan[at]danny.cz> - 0.5.0-3
- always build the x11 subpackage

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Hans de Goede <hdegoede@redhat.com> - 0.5.0-1
- Update to 0.5.0 (#1154574)

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.3-2
- Require xkeyboard-config (#1145260)

* Wed Aug 20 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.3-1
- Update to 0.4.3

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-3
- make -x11 support conditional (f21+, #1000497)
- --disable-silent-rules

* Fri May 23 2014 Hans de Goede <hdegoede@redhat.com> - 0.4.2-2
- Bump release to 2 to avoid confusion with non official non scratch 0.4.2-1

* Thu May 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-1
- xkbcommon 0.4.2 (#1000497)
- own %%{_includedir}/xkbcommon/
- -x11: +ldconfig scriptlets
- -devel: don't include xkbcommon-x11.h
- run reautoconf in %%prep (instead of %%build)
- tighten subpkg deps via %%_isa
- .spec cleanup, remove deprecated stuff
- BR: pkgconfig(xcb-xkb) >= 1.10

* Wed Feb 05 2014 Peter Hutterer <peter.hutterer@redhat.com> 0.4.0-1
- xkbcommon 0.4.0
- Add new xkbcommon-x11 and xkbcommon-x11-devel subpackages

* Tue Aug 27 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.1-1
- xkbcommon 0.3.1

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 18 2013 Peter Hutterer <peter.hutterer@redhat.com> 0.3.0-1
- xkbcommon 0.3.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Adam Jackson <ajax@redhat.com> 0.2.0-1
- xkbcommon 0.2.0

* Mon Sep 17 2012 Thorsten Leemhuis <fedora@leemhuis.info> 0.1.0-8.20120917
- Today's git snapshot

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-7.20120306
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-6.20120306
- BuildRequire xkeyboard-config-devel to get the right XKB target path (#799717)

* Tue Mar 06 2012 Peter Hutterer <peter.hutterer@redhat.com> 0.1.0-5.20120306
- Today's git snapshot

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-4.20111109
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 09 2011 Adam Jackson <ajax@redhat.com> 0.1.0-3
- Today's git snap

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-2.20101110
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Nov 06 2010 Dave Airlie <airlied@redhat.com> 0.1.0-1.20101110
- inital import

