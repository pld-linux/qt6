# Note on packaging .cmake files for plugins:
# Base Qt6${component}Config.cmake file includes all existing Qt6${component}_*Plugin.cmake
# files, which trigger check for presence of plugin module in filesystem.
# Thus, for plugins separated into subpackages, we package plugins .cmake file
# together with module, and the rest of .cmake files in appropriate -devel subpackage.
#
# Conditional build:
# -- build targets
%bcond_without	doc		# Documentation
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB platform support
%bcond_without	egl		# EGL (EGLFS, minimal EGL) platform support
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	kerberos5	# KRB5 GSSAPI Support
%bcond_without	kms		# KMS platform support
%bcond_without	libinput	# libinput support
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	statx		# build without statx()
%bcond_with	systemd		# logging to journald
%bcond_without	tslib		# tslib support
# -- databases
%bcond_without	freetds		# TDS (Sybase/MS SQL) plugin
%bcond_without	mysql		# MySQL plugin
%bcond_without	odbc		# unixODBC plugin
%bcond_without	pgsql		# PostgreSQL plugin
%bcond_without	sqlite3		# SQLite3 plugin
%bcond_without	ibase		# ibase (InterBase/Firebird) plugin
%bcond_with	db2		# DB2 support
%bcond_with	oci		# OCI (Oracle) support
# -- SIMD CPU instructions
%bcond_with	sse2		# use SSE2 instructions
%bcond_with	sse3		# use SSE3 instructions (since: Intel middle Pentium4, AMD Athlon64)
%bcond_with	ssse3		# use SSSE3 instructions (Intel since Core2, Via Nano)
%bcond_with	sse41		# use SSE4.1 instructions (Intel since middle Core2)
%bcond_with	sse42		# use SSE4.2 instructions (the same)
%bcond_with	avx		# use AVX instructions (Intel since Sandy Bridge, AMD since Bulldozer)
%bcond_with	avx2		# use AVX2 instructions (Intel since Haswell)

%ifnarch %{ix86} %{x8664} x32 sparc sparcv9 alpha ppc
%undefine	with_ibase
%endif
%ifarch	athlon
%define		with_3dnow	1
%endif
%ifarch athlon pentium3 pentium4 %{x8664} x32
%define		with_mmx	1
%endif
%ifarch pentium4 %{x8664} x32
%define		with_sse2	1
%endif
# QTBUG-36129
%ifnarch %{arm} aarch64
%define		with_red_reloc	1
%endif

%define		icu_abi		71
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

Summary:	Qt6 Library
Summary(pl.UTF-8):	Biblioteka Qt6
Name:		qt6
Version:	6.3.1
Release:	0.1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/6.3/%{version}/single/qt-everywhere-src-%{version}.tar.xz
# Source0-md5:	957a304773b281a4584f4c0254773456
Patch0:		system-cacerts.patch
Patch1:		ninja-program.patch
Patch2:		%{name}-gn.patch
URL:		https://www.qt.io/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	EGL-devel
%{?with_ibase:BuildRequires:	Firebird-devel}
%{?with_kms:BuildRequires:	Mesa-libgbm-devel}
BuildRequires:	OpenGL-devel
%{?with_kms:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	at-spi2-core-devel
# base dir requires 3.16, gn 3.19
BuildRequires:	cmake >= 3.19
%{?with_cups:BuildRequires:	cups-devel >= 1.4}
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	double-conversion-devel
BuildRequires:	fontconfig-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	freetype-devel >= 2.2.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.6}
BuildRequires:	harfbuzz-devel >= 1.6.0
%{?with_kerberos5:BuildRequires:	heimdal-devel}
%{?with_kms:BuildRequires:	libdrm-devel}
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
%{?with_libinput:BuildRequires:	libinput-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libxcb-devel >= 1.12
BuildRequires:	mtdev-devel
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	nodejs
BuildRequires:	openssl-devel >= 1.1.1
%{?with_oci:BuildRequires:	oracle-instantclient-devel}
BuildRequires:	pcre2-16-devel >= 10.20
BuildRequires:	pkgconfig
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	python3-html5lib
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	samurai
BuildRequires:	sed >= 4.0
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	tar >= 1:1.22
%{?with_tslib:BuildRequires:	tslib-devel}
BuildRequires:	udev-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	wayland-devel
BuildRequires:	xcb-util-image-devel >= 0.3.9
BuildRequires:	xcb-util-keysyms-devel >= 0.3.9
BuildRequires:	xcb-util-renderutil-devel >= 0.3.9
BuildRequires:	xcb-util-wm-devel >= 0.3.9
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel >= 0.6
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xorg-lib-libxkbcommon-x11-devel >= 0.5.0
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.0.8
BuildRequires:	zstd-devel >= 1.3
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		specflags	-fno-strict-aliasing
%define		filterout	-flto

%define		qt6dir		%{_libdir}/qt6

%description
Qt is a software toolkit for developing applications.

%description -l pl.UTF-8
Qt to programowy toolkit do tworzenia aplikacji.

%package -n Qt6Concurrent
Summary:	Qt6 Concurrent library
Summary(pl.UTF-8):	Biblioteka Qt6 Concurrent
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Concurrent
The Qt6 Concurrent library provides high-level APIs that make it
possible to write multi-threaded programs without using low-level
threading primitives.

%description -n Qt6Concurrent -l pl.UTF-8
Biblioteka Qt6 Concurrent udostępnia wysokopoziomowe API umożliwiające
pisanie wielowątkowych programów bez wykorzystywania niskopoziomowych
elementów związanych z wątkami.

%package -n Qt6Concurrent-devel
Summary:	Qt6 Concurrent library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Concurrent - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Concurrent = %{version}
Requires:	Qt6Core-devel = %{version}

%description -n Qt6Concurrent-devel
Header files for Qt6 Concurrent library.

%description -n Qt6Concurrent-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Concurrent.

%package -n Qt6Core
Summary:	Qt6 Core library
Summary(pl.UTF-8):	Biblioteka Qt6 Core
Group:		Libraries
Requires:	pcre2-16 >= 10.20
Requires:	zlib >= 1.0.8
Requires:	zstd >= 1.3

%description -n Qt6Core
Qt6 Core library provides core non-GUI functionality.

%description -n Qt6Core -l pl.UTF-8
Biblioteka Qt6 Core zawiera podstawową funkcjonalność nie związaną z
graficznym interfejsem użytkownika (GUI).

%package -n Qt6Core-devel
Summary:	Qt6 Core library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Core - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core = %{version}
Requires:	libicu-devel
Requires:	libstdc++-devel >= 6:4.7
Requires:	pcre2-16-devel >= 10.20
Requires:	qt6-build = %{version}
Requires:	qt6-qmake = %{version}
Requires:	zlib-devel >= 1.0.8

%description -n Qt6Core-devel
Header files for Qt6 Core library.

%description -n Qt6Core-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Core.

%package -n Qt6DBus
Summary:	Qt6 DBus library
Summary(pl.UTF-8):	Biblioteka Qt6 DBus
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	dbus-libs >= 1.2

%description -n Qt6DBus
The Qt6 D-Bus library is a Unix-only library that you can use to
perform Inter-Process Communication using the D-Bus protocol.

%description -n Qt6DBus -l pl.UTF-8
Biblioteka Qt6 D-Bus to wyłącznie uniksowa biblioteka pozwalająca na
komunikację międzyprocesową (IPC) przy użyciu protokołu D-Bus.

%package -n Qt6DBus-devel
Summary:	Qt6 DBus library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 DBus - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus = %{version}
Requires:	dbus-devel >= 1.2

%description -n Qt6DBus-devel
Header files for Qt6 DBus library.

%description -n Qt6DBus-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 DBus.

%package -n Qt6DeviceDiscoverySupport-devel
Summary:	Qt6 DeviceDiscoverySupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 DeviceDiscoverySupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6DeviceDiscoverySupport-devel
Qt6 DeviceDiscoverySupport library - development files.

%description -n Qt6DeviceDiscoverySupport-devel -l pl.UTF-8
Biblioteka Qt6 DeviceDiscoverySupport - pliki programistyczne.

%package -n Qt6EdidSupport-devel
Summary:	Qt6 EdidSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 EdidSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6EdidSupport-devel
Qt6 EdidSupport library - development files.

%description -n Qt6EdidSupport-devel -l pl.UTF-8
Biblioteka Qt6 EdidSupport - pliki programistyczne.

%package -n Qt6EglSupport-devel
Summary:	Qt6 EglSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 EglSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6EglSupport-devel
Qt6 EglSupport library - development files.

%description -n Qt6EglSupport-devel -l pl.UTF-8
Biblioteka Qt6 EglSupport - pliki programistyczne.

%package -n Qt6EventDispatcherSupport-devel
Summary:	Qt6 EventDispatcherSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 EventDispatcherSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}
Requires:	glib2-devel >= 2.0

%description -n Qt6EventDispatcherSupport-devel
Qt6 EventDispatcherSupport library - development files.

%description -n Qt6EventDispatcherSupport-devel -l pl.UTF-8
Biblioteka Qt6 EventDispatcherSupport - pliki programistyczne.

%package -n Qt6FbSupport-devel
Summary:	Qt6 FbSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 FbSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6FbSupport-devel
Qt6 FbSupport library - development files.

%description -n Qt6FbSupport-devel -l pl.UTF-8
Biblioteka Qt6 FbSupport - pliki programistyczne.

%package -n Qt6FontDatabaseSupport-devel
Summary:	Qt6 FontDatabaseSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 FontDatabaseSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6FontDatabaseSupport-devel
Qt6 FontDatabaseSupport library - development files.

%description -n Qt6FontDatabaseSupport-devel -l pl.UTF-8
Biblioteka Qt6 FontDatabaseSupport - pliki programistyczne.

%package -n Qt6GlxSupport-devel
Summary:	Qt6 GlxSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 GlxSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6GlxSupport-devel
Qt6 GlxSupport library - development files.

%description -n Qt6GlxSupport-devel -l pl.UTF-8
Biblioteka Qt6 GlxSupport - pliki programistyczne.

%package -n Qt6Gui
Summary:	Qt6 Gui library
Summary(pl.UTF-8):	Biblioteka Qt6 Gui
Group:		Libraries
Requires:	Qt6Core = %{version}
# for ibus platforminputcontext plugin
Requires:	Qt6DBus = %{version}
# for compose platforminputcontext plugin
Requires:	xorg-lib-libxkbcommon >= 0.4.1
Suggests:	Qt6Gui-platform-xcb

%description -n Qt6Gui
The Qt6 GUI library provides the basic enablers for graphical
applications written with Qt 5.

%description -n Qt6Gui -l pl
Biblioteka Qt6 Gui udostępnia podstawową funkcjonalność dla
graficznych aplikacji napisanych z użyciem Qt 5.

%package -n Qt6Gui-generic-libinput
Summary:	Qt6 Gui generic input plugin for libinput
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt6 Gui z libinput
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-generic-libinput
Qt6 Gui generic input plugin to get mouse, keyboard and touch events
via libinput.

%description -n Qt6Gui-generic-libinput -l pl.UTF-8
Ogólna wtyczka wejścia Qt6 Gui do pobierania zdarzeń myszy, klawiatury
i dotykowych poprzez libinput.

%package -n Qt6Gui-generic-tslib
Summary:	Qt6 Gui generic input plugin for TSlib (touchscreen panel events)
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt6 Gui z TSlib (zdarzeń z paneli dotykowych)
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-generic-tslib
Qt6 Gui generic input plugin for TSlib (touchscreen panel events).

%description -n Qt6Gui-generic-tslib -l pl.UTF-8
Ogólna wtyczka wejścia Qt6 Gui z TSlib (zdarzeń z paneli dotykowych).

%package -n Qt6Gui-generic-tuiotouch
Summary:	Qt6 Gui generic input plugin for TuioTouch
Summary(pl.UTF-8):	Ogólna wtyczka wejścia Qt6 Gui z TuioTouch
Group:		Libraries
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6Gui-generic-tuiotouch
Qt6 Gui generic input plugin for TuioTouch.

%description -n Qt6Gui-generic-tuiotouch -l pl.UTF-8
Ogólna wtyczka wejścia Qt6 Gui z TuioTouch.

%package -n Qt6Gui-platform-directfb
Summary:	Qt6 Gui platform plugin for DirectFB
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui dla DirectFB
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platform-directfb
Qt6 Gui platform plugin for DirectFB.

%description -n Qt6Gui-platform-directfb -l pl.UTF-8
Wtyczka platformy Qt6 Gui dla DirectFB.

%package -n Qt6Gui-platform-egl
Summary:	Qt6 Gui platform plugin for minimal EGL
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui dla minimalnego EGL
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platform-egl
Qt6 Gui platform plugin for minimal EGL.

%description -n Qt6Gui-platform-egl -l pl.UTF-8
Wtyczki platformy Qt6 Gui dla minimalnego EGL.

%package -n Qt6Gui-platform-eglfs
Summary:	Qt6 Gui platform plugin and library for EglFs integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej EglFs
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platform-eglfs
Qt6 Gui platform plugin and library for EglFs integration layer.

%description -n Qt6Gui-platform-eglfs -l pl.UTF-8
Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej EglFs.

%package -n Qt6Gui-platform-eglfs-devel
Summary:	Development files for Qt6 EglFs integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt6 EglFs
Group:		Development/Libraries
Requires:	Qt6Gui-platform-eglfs = %{version}

%description -n Qt6Gui-platform-eglfs-devel
Development files for Qt6 EglFs integration layer.

%description -n Qt6Gui-platform-eglfs-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt6 EglFs.

%package -n Qt6Gui-platform-eglfs-kms
Summary:	Qt6 EglFs integration plugin for KMS
Summary(pl.UTF-8):	Wtyczka integracji Qt6 EglFs dla KMS
Group:		Libraries
Requires:	Qt6Gui-platform-eglfs = %{version}

%description -n Qt6Gui-platform-eglfs-kms
Qt6 EglFs integration plugin for KMS.

%description -n Qt6Gui-platform-eglfs-kms -l pl.UTF-8
Wtyczka integracji Qt6 EglFs dla KMS.

%package -n Qt6Gui-platform-eglfs-kms-devel
Summary:	Development files for Qt6 EglFs integration plugin for KMS
Summary(pl.UTF-8):	Pliki programistyczne dla wtyczki integracji Qt6 EglFs dla KMS
Group:		Libraries
Requires:	Qt6Gui-platform-eglfs = %{version}

%description -n Qt6Gui-platform-eglfs-kms-devel
Qt6 EglFs integration plugin for KMS - development files.

%description -n Qt6Gui-platform-eglfs-kms-devel -l pl.UTF-8
Wtyczka integracji Qt6 EglFs dla KMS - pliki programistyczne.

%package -n Qt6Gui-platform-eglfs-x11
Summary:	Qt6 EglFs integration plugin for X11
Summary(pl.UTF-8):	Wtyczka integracji Qt6 EglFs dla X11
Group:		Libraries
Requires:	Qt6Gui-platform-eglfs = %{version}

%description -n Qt6Gui-platform-eglfs-x11
Qt6 EglFs integration plugin for X11.

%description -n Qt6Gui-platform-eglfs-x11 -l pl.UTF-8
Wtyczka integracji Qt6 EglFs dla X11.

%package -n Qt6Gui-platform-linuxfb
Summary:	Qt6 Gui platform plugin for Linux FrameBuffer
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui dla linuksowego framebuffera
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platform-linuxfb
Qt6 Gui platform plugin for Linux FrameBuffer.

%description -n Qt6Gui-platform-linuxfb -l pl.UTF-8
Wtyczki platformy Qt6 Gui dla linuxksowego framebuffera.

%package -n Qt6Gui-platform-vnc
Summary:	Qt6 Gui platform plugin and library for VNC integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej VNC
Group:		Libraries
Requires:	Qt6DBus = %{version}
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platform-vnc
Qt6 Gui platform plugin and library for VNC integration layer.

%description -n Qt6Gui-platform-vnc -l pl.UTF-8
Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej VNC.

%package -n Qt6Gui-platform-vnc-devel
Summary:	Development files for Qt6 VNC integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt6 VNC
Group:		Development/Libraries

%description -n Qt6Gui-platform-vnc-devel
Development files for Qt6 VNC integration layer.

%description -n Qt6Gui-platform-vnc-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt6 VNC.

%package -n Qt6Gui-platform-xcb
Summary:	Qt6 Gui platform plugin and library for XcbQpa integration layer
Summary(pl.UTF-8):	Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej XcbQpa
Group:		Libraries
Requires:	Qt6DBus = %{version}
Requires:	Qt6Gui = %{version}
Requires:	libxcb >= 1.10
Requires:	xorg-lib-libxkbcommon-x11 >= 0.4.1

%description -n Qt6Gui-platform-xcb
Qt6 Gui platform plugin and library for XcbQpa integration layer.

%description -n Qt6Gui-platform-xcb -l pl.UTF-8
Wtyczka platformy Qt6 Gui oraz biblioteka warstwy integracyjnej
XcbQpa.

%package -n Qt6Gui-platform-xcb-devel
Summary:	Development files for Qt6 XcbQpa integration layer
Summary(pl.UTF-8):	Pliki programistyczne warstwy integracyjnej Qt6 XcbQpa
Group:		Development/Libraries
Requires:	Qt6Gui-platform-eglfs = %{version}

%description -n Qt6Gui-platform-xcb-devel
Development files for Qt6 XcbQpa integration layer.

%description -n Qt6Gui-platform-xcb-devel -l pl.UTF-8
Pliki programistyczne warstwy integracyjnej Qt6 XcbQpa.

%package -n Qt6Gui-platform-xcb-egl
Summary:	Qt6 XcbQpa integration plugin for EGL
Summary(pl.UTF-8):	Wtyczka integracji Qt6 XcbQpa dla EGL
Group:		Libraries
Requires:	Qt6Gui-platform-xcb = %{version}

%description -n Qt6Gui-platform-xcb-egl
Qt6 XcbQpa integration plugin for EGL.

%description -n Qt6Gui-platform-xcb-egl -l pl.UTF-8
Wtyczka integracji Qt6 XcbQpa dla EGL.

%package -n Qt6Gui-platform-xcb-glx
Summary:	Qt6 XcbQpa integration plugin for GLX
Summary(pl.UTF-8):	Wtyczka integracji Qt6 XcbQpa dla GLX
Group:		Libraries
Requires:	Qt6Gui-platform-xcb = %{version}

%description -n Qt6Gui-platform-xcb-glx
Qt6 XcbQpa integration plugin for GLX.

%description -n Qt6Gui-platform-xcb-glx -l pl.UTF-8
Wtyczka integracji Qt6 XcbQpa dla GLX.

%package -n Qt6Gui-platformtheme-gtk3
Summary:	Qt6 Gui platform theme plugin for GTK+ 3.x
Summary(pl.UTF-8):	Wtyczka motywów platform Qt6 Gui dla GTK+ 3.x
Group:		Libraries
Requires:	Qt6Gui = %{version}

%description -n Qt6Gui-platformtheme-gtk3
Qt6 Gui platform theme plugin for GTK+ 3.x.

%description -n Qt6Gui-platformtheme-gtk3 -l pl.UTF-8
Wtyczka motywów platform Qt6 Gui dla GTK+ 3.x.

%package -n Qt6Gui-platformtheme-xdgdesktopportal
Summary:	Qt6 Gui platform theme plugin for xdg-desktop-portal
Summary(pl.UTF-8):	Wtyczka motywów platform Qt6 Gui dla xdg-desktop-portal
Group:		Libraries
Requires:	Qt6Gui = %{version}
Requires:	harfbuzz >= 1.6.0

%description -n Qt6Gui-platformtheme-xdgdesktopportal
Qt6 Gui platform theme plugin for xdg-desktop-portal.

%description -n Qt6Gui-platformtheme-xdgdesktopportal -l pl.UTF-8
Wtyczka motywów platform Qt6 Gui dla xdg-desktop-portal.

%package -n Qt6Gui-devel
Summary:	Qt6 Gui library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Gui - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui = %{version}
Requires:	libpng-devel
Requires:	Vulkan-Loader-devel

%description -n Qt6Gui-devel
Header files for Qt6 Gui library.

%description -n Qt6Gui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Gui.

%package -n Qt6InputSupport-devel
Summary:	Qt6 InputSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 InputSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6InputSupport-devel
Qt6 InputSupport library - development files.

%description -n Qt6InputSupport-devel -l pl.UTF-8
Biblioteka Qt6 InputSupport - pliki programistyczne.

%package -n Qt6KmsSupport-devel
Summary:	Qt6 KmsSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 KmsSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6KmsSupport-devel
Qt6 KmsSupport library - development files.

%description -n Qt6KmsSupport-devel -l pl.UTF-8
Biblioteka Qt6 KmsSupport - pliki programistyczne.

%package -n Qt6Network
Summary:	Qt6 Network library
Summary(pl.UTF-8):	Biblioteka Qt6 Network
Group:		Libraries
Requires:	Qt6Core = %{version}
# for bearer plugins (qconnman, qnm):
Requires:	Qt6DBus = %{version}
%requires_ge_to openssl openssl-devel

%description -n Qt6Network
The Qt6 Network library provides classes to make network programming
easier and portable.

%description -n Qt6Network -l pl.UTF-8
Biblioteka Qt6 Network udostępnia klasy czyniące programowanie
sieciowe łatwiejszym i przenośnym.

%package -n Qt6Network-devel
Summary:	Qt6 Network library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Network - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network = %{version}
%requires_ge	openssl-devel

%description -n Qt6Network-devel
Header files for Qt6 Network library.

%description -n Qt6Network-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Network.

%package -n Qt6OpenGL
Summary:	Qt6 OpenGL library
Summary(pl.UTF-8):	Biblioteka Qt6 OpenGL
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6OpenGL
The Qt6 OpenGL library offers classes that make it easy to use OpenGL
in Qt 5 applications.

%description -n Qt6OpenGL -l pl.UTF-8
Biblioteka Qt6 OpenGL oferuje klasy ułatwiające wykorzystywanie
OpenGL-a w aplikacjach Qt 5.

%package -n Qt6OpenGL-devel
Summary:	Qt6 OpenGL library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 OpenGL - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6OpenGL = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6OpenGL-devel
Header files for Qt6 OpenGL library.

%description -n Qt6OpenGL-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 OpenGL.

%package -n Qt6OpenGLExtensions-devel
Summary:	Qt6 OpenGLExtensions library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 OpenGLExtensions - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}

%description -n Qt6OpenGLExtensions-devel
Qt6 OpenGLExtensions library (development files).

%description -n Qt6OpenGLExtensions-devel -l pl.UTF-8
Biblioteka Qt6 OpenGL Extensions - obsługa rozszerzeń OpenGL (pliki
programistyczne).

%package -n Qt6ServiceSupport-devel
Summary:	Qt6 ServiceSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 ServiceSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6ServiceSupport-devel
Qt6 ServiceSupport library - development files.

%description -n Qt6ServiceSupport-devel -l pl.UTF-8
Biblioteka Qt6 ServiceSupport - pliki programistyczne.

%package -n Qt6PlatformCompositorSupport-devel
Summary:	Qt6 PlatformCompositorSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 PlatformCompositorSupport - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	fontconfig-devel
Requires:	freetype-devel >= 2.2.0
Requires:	udev-devel
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel
Requires:	xorg-lib-libXrender-devel

%description -n Qt6PlatformCompositorSupport-devel
Qt6 PlatformCompositorSupport library (development files).

%description -n Qt6PlatformCompositorSupport-devel -l pl.UTF-8
Biblioteka Qt6 PlatformCompositorSupport - obsługa platformy (pliki
programistyczne).

%package -n Qt6PrintSupport
Summary:	Qt6 PrintSupport library
Summary(pl.UTF-8):	Biblioteka Qt6 PrintSupport
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}
%{?with_cups:Requires:	cups-lib >= 1.4}

%description -n Qt6PrintSupport
The Qt6 PrintSupport library provides classes to make printing easier
and portable.

%description -n Qt6PrintSupport -l pl.UTF-8
Biblioteka Qt6 PrintSupport udostępnia klasy czyniące drukowanie
łatwiejszym i bardziej przenośnym.

%package -n Qt6PrintSupport-devel
Summary:	Qt6 PrintSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 PrintSupport - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6PrintSupport-devel
Header files for Qt6 PrintSupport library.

%description -n Qt6PrintSupport-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 PrintSupport.

%package -n Qt6ThemeSupport-devel
Summary:	Qt6 ThemeSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 ThemeSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6ThemeSupport-devel
Qt6 ThemeSupport library - development files.

%description -n Qt6ThemeSupport-devel -l pl.UTF-8
Biblioteka Qt6 ThemeSupport - pliki programistyczne.

%package -n Qt6Sql
Summary:	Qt6 Sql library
Summary(pl.UTF-8):	Biblioteka Qt6 Sql
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Sql
The Qt6 Sql library provides a driver layer, SQL API layer, and a user
interface layer for SQL databases.

%description -n Qt6Sql -l pl.UTF-8
Biblioteka Qt6 Sql udostępnia warstwę sterowników, warstwę API SQL
oraz warstwę interfejsu użytkownika dla baz danych SQL.

%package -n Qt6Sql-devel
Summary:	Qt6 Sql library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Sql - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-devel
Header files for Qt6 Sql library.

%description -n Qt6Sql-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Sql.

%package -n Qt6Sql-sqldriver-db2
Summary:	Qt6 Sql driver for IBM DB2 database
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych IBM DB2
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-db2
Qt6 Sql driver for IBM DB2 database.

%description -n Qt6Sql-sqldriver-db2 -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych IBM DB2.

%package -n Qt6Sql-sqldriver-ibase
Summary:	Qt6 Sql driver for Firebird/InterBase database
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych Firebird/InterBase
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-ibase
Qt6 Sql driver for Firebird/InterBase database.

%description -n Qt6Sql-sqldriver-ibase -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych Firebird/InterBase.

%package -n Qt6Sql-sqldriver-sqlite3
Summary:	Qt6 Sql driver for SQLite 3.x database
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych SQLite 3.x
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-sqlite3
Qt6 Sql driver for SQLite 3.x database.

%description -n Qt6Sql-sqldriver-sqlite3 -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych SQLite 3.x.

%package -n Qt6Sql-sqldriver-mysql
Summary:	Qt6 Sql driver for MySQL database
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych MySQL
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-mysql
Qt6 Sql driver for MySQL database.

%description -n Qt6Sql-sqldriver-mysql -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych MySQL.

%package -n Qt6Sql-sqldriver-oci
Summary:	Qt6 Sql driver for Oracle database (using OCI interface)
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych Oracle (wykorzystujący interfejs OCI)
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-oci
Qt6 Sql driver for Oracle database (using OCI interface).

%description -n Qt6Sql-sqldriver-oci -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych Oracle (wykorzystujący interfejs
OCI).

%package -n Qt6Sql-sqldriver-odbc
Summary:	Qt6 Sql driver for ODBC databases
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla baz danych ODBC
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-odbc
Qt6 Sql driver for ODBC databases.

%description -n Qt6Sql-sqldriver-odbc -l pl.UTF-8
Sterownik Qt6 Sql dla baz danych ODBC.

%package -n Qt6Sql-sqldriver-pgsql
Summary:	Qt6 Sql driver for PostgreSQL database
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych PostgreSQL
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-pgsql
Qt6 Sql driver for PostgreSQL database.

%description -n Qt6Sql-sqldriver-pgsql -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych PostgreSQL.

%package -n Qt6Sql-sqldriver-tds
Summary:	Qt6 Sql driver for Sybase/MS SQL database (using TDS interface)
Summary(pl.UTF-8):	Sterownik Qt6 Sql dla bazy danych Sybase/MS SQL (wykorzystujący interfejs TDS)
Group:		Libraries
Requires:	Qt6Sql = %{version}

%description -n Qt6Sql-sqldriver-tds
Qt6 Sql driver for Sybase/MS SQL database (using TDS interface).

%description -n Qt6Sql-sqldriver-tds -l pl.UTF-8
Sterownik Qt6 Sql dla bazy danych Sybase/MS SQL (wykorzystujący
interfejs TDS).

%package -n Qt6Test
Summary:	Qt6 Test library
Summary(pl.UTF-8):	Biblioteka Qt6 Test
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Test
The Qt6 Test library provides classes for unit testing Qt 5
applications and libraries.

%description -n Qt6Test -l pl.UTF-8
Biblioteka Qt6 Test udostępnia klasy do testów jednostkowych aplikacji
oraz bibliotek Qt 5.

%package -n Qt6Test-devel
Summary:	Qt6 Test library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Test - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Test = %{version}

%description -n Qt6Test-devel
Header files for Qt6 Test library.

%description -n Qt6Test-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Test.

%package -n Qt6VulkanSupport-devel
Summary:	Qt6 VulkanSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 VulkanSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6VulkanSupport-devel
Qt6 VulkanSupport library - development files.

%description -n Qt6VulkanSupport-devel -l pl.UTF-8
Biblioteka Qt6 VulkanSupport - pliki programistyczne.

%package -n Qt6Widgets
Summary:	Qt6 Widgets library
Summary(pl.UTF-8):	Biblioteka Qt6 Widgets
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}

%description -n Qt6Widgets
The Qt6 Widgets library extends Qt 5 GUI with C++ widget
functionality.

%description -n Qt6Widgets -l pl.UTF-8
Biblioteka Qt6 Widgets rozszerza graficzny interfejs Qt 5 o
funkcjonalność widgetów C++.

%package -n Qt6Widgets-devel
Summary:	Qt6 Widgets library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Widgets - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	xorg-lib-libX11-devel
Requires:	xorg-lib-libXext-devel

%description -n Qt6Widgets-devel
Header files for Qt6 Widgets library.

%description -n Qt6Widgets-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Widgets.

%package -n Qt6XkbCommonSupport-devel
Summary:	Qt6 XkbCommonSupport library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 XkbCommonSupport - pliki programistyczne
Group:		Development/Libraries
# for (subset of) Qt6Core headers
Requires:	Qt6Core-devel = %{version}

%description -n Qt6XkbCommonSupport-devel
Qt6 XkbCommonSupport library - development files.

%description -n Qt6XkbCommonSupport-devel -l pl.UTF-8
Biblioteka Qt6 XkbCommonSupport - pliki programistyczne.

%package -n Qt6Xml
Summary:	Qt6 Xml library
Summary(pl.UTF-8):	Biblioteka Qt6 Xml
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Xml
The Qt6 Xml library provides C++ implementations of the SAX and DOM
standards for XML.

%description -n Qt6Xml -l pl.UTF-8
Biblioteka Qt6 Xml udostępnia implementację w C++ standardów SAX oraz
DOM dla formatu XML.

%package -n Qt6Xml-devel
Summary:	Qt6 Xml library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Xml - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Xml = %{version}

%description -n Qt6Xml-devel
Header files for Qt6 Xml library.

%description -n Qt6Xml-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Xml.

%package -n qt6-doc-common
Summary:	Common part of Qt6 documentation
Summary(pl.UTF-8):	Część wspólna dokumentacji do Qt6
Group:		Documentation
BuildArch:	noarch

%description -n qt6-doc-common
Common part of Qt6 documentation, global for all components.

%description -n qt6-doc-common -l pl.UTF-8
Część wspólna dokumentacji do Qt6 ("global", dla wszystkich
elementów).

%package doc
Summary:	Qt6 application framework base components documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja podstawowych komponentów szkieletu aplikacji Qt6 w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description doc
Qt6 application framework base components documentation in HTML
format.

%description doc -l pl.UTF-8
Dokumentacja podstawowych komponentów szkieletu aplikacji Qt6 w
formacie HTML.

%package doc-qch
Summary:	Qt6 application framework base components documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja podstawowych komponentów szkieletu aplikacji Qt6 w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description doc-qch
Qt6 application framework base components documentation in QCH format.

%description doc-qch -l pl.UTF-8
Dokumentacja podstawowych komponentów szkieletu aplikacji Qt6 w
formacie QCH.

%package examples
Summary:	Examples for Qt6 application framework base components
Summary(pl.UTF-8):	Przykłady do podstawowych komponentów szkieletu aplikacji Qt6
Group:		X11/Development/Libraries
BuildArch:	noarch

%description examples
Examples for Qt6 application framework base components.

%description examples -l pl.UTF-8
Przykłady do podstawowych komponentów szkieletu aplikacji Qt6.

%package -n qt6-build
Summary:	Qt6 build tools
Summary(pl.UTF-8):	Narzędzia do budowania dla Qt6
Group:		Development/Tools

%description -n qt6-build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) etc.

%description -n qt6-build -l pl.UTF-8
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów użytkownika (uic) i podobne
narzędzia.

%package -n qt6-qmake
Summary:	Qt6 makefile generator
Summary(pl.UTF-8):	Generator plików makefile dla aplikacji Qt6
Group:		Development/Tools

%description -n qt6-qmake
Qt6 makefile generator.

%description -n qt6-qmake -l pl.UTF-8
Generator plików makefile dla aplikacji Qt6.

%prep
%setup -q -n qt-everywhere-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%{__sed} -i -e 's,usr/X11R6/,usr/,g' qtbase/mkspecs/linux-g++-64/qmake.conf

# change QMAKE FLAGS to build
%{__sed} -i -e '
	s|^\(QMAKE_CC *\)=.*gcc|\1= %{__cc}|;
	s|^\(QMAKE_CXX *\)=.*g++|\1= %{__cxx}|;
	' qtbase/mkspecs/common/g++-base.conf
%{__sed} -i -e '
	s|^\(QMAKE_CFLAGS_RELEASE_WITH_DEBUGINFO *\)+=.*|\1+= %{rpmcppflags} %{rpmcflags} -g|;
	s|^\(QMAKE_CXXFLAGS_RELEASE_WITH_DEBUGINFO *\)+=.*|\1+= %{rpmcppflags} %{rpmcxxflags} -g|;
	s|^\(QMAKE_CFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcflags}|;
	s|^\(QMAKE_CXXFLAGS_RELEASE *\)+=.*|\1+= %{rpmcppflags} %{rpmcxxflags}|;
	s|^\(QMAKE_CFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_CXXFLAGS_DEBUG *\)+=.*|\1+= %{debugcflags}|;
	s|^\(QMAKE_LFLAGS *\)+=.*|\1+= %{rpmldflags}|;
	' qtbase/mkspecs/common/gcc-base.conf

# define QMAKE_STRIP to true, so we get useful -debuginfo pkgs
%{__sed} -i -e '
	s|^\(QMAKE_STRIP *\)=.*|\1= :|;
	s|^\(QMAKE_STRIPFLAGS_LIB *\)+=.*|\1+= :|;
	' qtbase/mkspecs/common/linux.conf

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
	qtbase/mkspecs/features/uikit/devices.py
	qtbase/util/testrunner/qt-testrunner.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
	qtbase/libexec/syncqt.pl

%if %(echo %{cxx_version} | cut -d. -f1) < 9
# available since gcc 9
%{__sed} -i -e '/-Wdeprecated-copy/d' \
	qtwebengine/src/3rdparty/chromium/third_party/{angle,dawn/src/common,pdfium,skia/gn/skia}/BUILD.gn \
	qtwebengine/src/3rdparty/chromium/third_party/swiftshader/CMakeLists.txt
%endif

%build
#TODO optflags
# We're using samurai instead of ninja because teh later
# cannot be told what command line flags to use globally
mkdir -p build
cd build
%cmake ../ \
	-GNinja \
	-DCMAKE_MAKE_PROGRAM:FILEPATH=/usr/bin/samu \
	-DNinja_EXECUTABLE:FILEPATH=/usr/bin/samu \
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DINSTALL_ARCHDATADIR=%{qt6dir} \
	-DINSTALL_BINDIR=%{qt6dir}/bin \
	-DINSTALL_LIBDIR=%{_libdir} \
	-DINSTALL_LIBEXECDIR=%{qt6dir}/libexec \
	-DINSTALL_DATADIR=%{_datadir}/qt6 \
	-DINSTALL_DOCDIR=%{_docdir}/qt6-doc \
	-DINSTALL_INCLUDEDIR=%{_includedir}/qt6 \
	-DINSTALL_EXAMPLESDIR=%{_examplesdir}/qt6 \
	-DINSTALL_MKSPECSDIR=%{qt6dir}/mkspecs \
	-DINSTALL_PLUGINSDIR=%{qt6dir}/plugins \
	-DINSTALL_QMLDIR=%{qt6dir}/qml \
	-DINSTALL_SYSCONFDIR=%{_sysconfdir}/qt6 \
	-DINSTALL_TRANSLATIONSDIR=%{_datadir}/qt6/translations \
	-DBUILD_SHARED_LIBS=ON \
	%{?with_oci:-DOracle_INCLUDE_DIR=%{_includedir}/oracle/client} \
	-DQT_DISABLE_RPATH=TRUE \
	-DQT_BUILD_EXAMPLES=ON \
	-DQT_FEATURE_relocatable=OFF \
	-DQT_FEATURE_rpath=OFF \
	-DQT_FEATURE_separate_debug_info=OFF \
	%{cmake_on_off red_reloc QT_FEATURE_reduce_relocations} \
	%{cmake_on_off pch BUILD_WITH_PCH} \
	-DQT_FEATURE_use_gold_linker=ON \
	-DQT_FEATURE_enable_new_dtags=ON \
	-DQT_FEATURE_dbus_linked=ON \
	-DQT_FEATURE_openssl_linked=ON \
	-DQT_FEATURE_accessibility=ON \
	-DQT_FEATURE_fontconfig=ON \
	-DQT_FEATURE_glib=ON \
	-DQT_FEATURE_icu=ON \
	-DQT_FEATURE_xcb=ON \
	-DQT_FEATURE_xcb_sm=ON \
	-DQT_FEATURE_xkbcommon=ON \
	-DQT_FEATURE_system_doubleconversion=ON \
	-DQT_FEATURE_system_freetype=ON \
	-DQT_FEATURE_system_harfbuzz=ON \
	-DQT_FEATURE_system_jpeg=ON \
	-DQT_FEATURE_system_libjpeg=ON \
	-DQT_FEATURE_system_png=ON \
	-DQT_FEATURE_system_libpng=ON \
	-DQT_FEATURE_system_pcre2=ON \
	-DQT_FEATURE_system_sqlite=ON \
	-DQT_FEATURE_system_zlib=ON \
	%{cmake_on_off sse2 QT_FEATURE_sse2} \
	%{cmake_on_off sse3 QT_FEATURE_sse3} \
	%{cmake_on_off ssse3 QT_FEATURE_ssse3} \
	%{cmake_on_off sse41 QT_FEATURE_sse4_1} \
	%{cmake_on_off sse42 QT_FEATURE_sse4_2} \
	%{cmake_on_off avx QT_FEATURE_avx} \
	%{cmake_on_off avx2 QT_FEATURE_avx2} \
	%{cmake_on_off cups QT_FEATURE_cups} \
	%{cmake_on_off systemd QT_FEATURE_journald} \
	%{cmake_on_off db2 QT_FEATURE_sql_db2} \
	%{cmake_on_off ibase QT_FEATURE_sql_ibase} \
	%{cmake_on_off mysql QT_FEATURE_sql_mysql} \
	%{cmake_on_off oci QT_FEATURE_sql_oci} \
	%{cmake_on_off odbc QT_FEATURE_sql_odbc} \
	%{cmake_on_off pgsql QT_FEATURE_sql_psql} \
	%{cmake_on_off sqlite3 QT_FEATURE_sql_sqlite} \
	%{cmake_on_off tds QT_FEATURE_sql_tds} \
	%{cmake_on_off directfb QT_FEATURE_directfb} \
	%{cmake_on_off gtk QT_FEATURE_gtk3} \
	%{cmake_on_off egl QT_FEATURE_eglfs} \
	%{cmake_on_off statx QT_FEATURE_statx} \
	%{cmake_on_off kms QT_FEATURE_kms} \
	%{cmake_on_off libinput QT_FEATURE_libinput} \
	%{cmake_on_off tslib QT_FEATURE_tslib}

## pass OPTFLAGS to build qmake itself with optimization
#export OPTFLAGS="%{rpmcflags}"
#export PATH=$PWD/bin:$PATH
#
#./configure \
#%if %{with mysql}
#	-I/usr/include/mysql \
#%endif
#%if %{with pgsql}
#	-I/usr/include/postgresql/server \
#%endif

# Make sure arg-less sub-invocations will follow our parallel build setting
export CMAKE_BUILD_PARALLEL_LEVEL="%__jobs"
export SAMUFLAGS="%{_smp_mflags}"
%{__cmake} --build . --verbose %{_smp_mflags}

%if %{with doc}
export QT_PLUGIN_PATH="$(pwd)/qtbase/lib64/qt6/plugins"
%{__cmake} --build . --target docs --verbose %{_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/qt6,%{_bindir},%{_pkgconfigdir},%{qt6dir}/libexec}

# for QtSolutions (qtlockedfile, qtsingleapplication, etc)
#install -d $RPM_BUILD_ROOT%{_includedir}/qt6/QtSolutions

DESTDIR=$RPM_BUILD_ROOT %{__cmake} --install build/

%if %{with doc}
DESTDIR=$RPM_BUILD_ROOT %{__cmake} --build build/ --target install_docs
%endif

# external plugins loaded from qtbase libs
install -d $RPM_BUILD_ROOT%{qt6dir}/plugins/iconengines

# kill unnecessary -L%{_libdir} from *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.prl \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# symlinks in system bin dir
cd $RPM_BUILD_ROOT%{_bindir}
ln -sf ../%{_lib}/qt6/bin/moc moc-qt6
ln -sf ../%{_lib}/qt6/bin/qmake qmake-qt6
ln -sf ../%{_lib}/qt6/bin/uic uic-qt6
ln -sf ../%{_lib}/qt6/bin/rcc rcc-qt6
ln -sf ../%{_lib}/qt6/bin/qdbuscpp2xml qdbuscpp2xml-qt6
ln -sf ../%{_lib}/qt6/bin/qdbusxml2cpp qdbusxml2cpp-qt6
ln -sf ../%{_lib}/qt6/bin/qdoc qdoc-qt6
ln -sf ../%{_lib}/qt6/bin/qlalr qlalr-qt6
cd -

# Prepare some files list
ifecho() {
	r="$RPM_BUILD_ROOT$2"
	if [ -d "$r" ]; then
		echo "%%dir $2" >> $1.files
	elif [ -x "$r" ] ; then
		echo "%%attr(755,root,root) $2" >> $1.files
	elif [ -f "$r" ]; then
		echo "$2" >> $1.files
	else
		echo "Error generation $1 files list!"
		echo "$r: no such file or directory!"
		return 1
	fi
}
ifecho_tree() {
	ifecho $1 $2
	for f in `find $RPM_BUILD_ROOT$2 -printf "%%P "`; do
		ifecho $1 $2/$f
	done
}

echo "%defattr(644,root,root,755)" > examples.files
ifecho_tree examples %{_examplesdir}/qt6/corelib
ifecho_tree examples %{_examplesdir}/qt6/dbus
ifecho_tree examples %{_examplesdir}/qt6/gui
ifecho_tree examples %{_examplesdir}/qt6/network
ifecho_tree examples %{_examplesdir}/qt6/opengl
ifecho_tree examples %{_examplesdir}/qt6/qpa
ifecho_tree examples %{_examplesdir}/qt6/qtconcurrent
ifecho_tree examples %{_examplesdir}/qt6/qtestlib
ifecho_tree examples %{_examplesdir}/qt6/sql
ifecho_tree examples %{_examplesdir}/qt6/vulkan
ifecho_tree examples %{_examplesdir}/qt6/widgets
ifecho_tree examples %{_examplesdir}/qt6/xml

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_localedir}/*/LC_MESSAGES layout
find_qt6_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt6/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtbase.lang
%if %{with doc}
find_qt6_qm qt >> qtbase.lang
find_qt6_qm qtbase >> qtbase.lang
%endif

install -d $RPM_BUILD_ROOT%{qt6dir}/plugins/styles

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt6Concurrent -p /sbin/ldconfig
%postun	-n Qt6Concurrent -p /sbin/ldconfig

%post	-n Qt6Core -p /sbin/ldconfig
%postun	-n Qt6Core -p /sbin/ldconfig

%post	-n Qt6DBus -p /sbin/ldconfig
%postun	-n Qt6DBus -p /sbin/ldconfig

%post	-n Qt6Gui -p /sbin/ldconfig
%postun	-n Qt6Gui -p /sbin/ldconfig

%post	-n Qt6Gui-platform-eglfs -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-eglfs -p /sbin/ldconfig

%post	-n Qt6Gui-platform-eglfs-kms -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-eglfs-kms -p /sbin/ldconfig

%post	-n Qt6Gui-platform-xcb -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-xcb -p /sbin/ldconfig

%post	-n Qt6Network -p /sbin/ldconfig
%postun	-n Qt6Network -p /sbin/ldconfig

%post	-n Qt6OpenGL -p /sbin/ldconfig
%postun	-n Qt6OpenGL -p /sbin/ldconfig

%post	-n Qt6PrintSupport -p /sbin/ldconfig
%postun	-n Qt6PrintSupport -p /sbin/ldconfig

%post	-n Qt6Sql -p /sbin/ldconfig
%postun	-n Qt6Sql -p /sbin/ldconfig

%post	-n Qt6Test -p /sbin/ldconfig
%postun	-n Qt6Test -p /sbin/ldconfig

%post	-n Qt6Widgets -p /sbin/ldconfig
%postun	-n Qt6Widgets -p /sbin/ldconfig

%post	-n Qt6Xml -p /sbin/ldconfig
%postun	-n Qt6Xml -p /sbin/ldconfig

%files -n Qt6Concurrent
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Concurrent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Concurrent.so.5

%files -n Qt6Concurrent-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Concurrent.so
%{_libdir}/libQt6Concurrent.prl
%{_includedir}/qt6/QtConcurrent
%{_pkgconfigdir}/Qt6Concurrent.pc
%{_libdir}/cmake/Qt6Concurrent
%{qt6dir}/mkspecs/modules/qt_lib_concurrent.pri
%{qt6dir}/mkspecs/modules/qt_lib_concurrent_private.pri

%files -n Qt6Core -f qtbase.lang
%defattr(644,root,root,755)
%doc dist/{README,changes-*}
%attr(755,root,root) %{_libdir}/libQt6Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Core.so.5
%dir %{_sysconfdir}/qt6
%dir %{qt6dir}
%dir %{qt6dir}/bin
%dir %{qt6dir}/libexec
%dir %{qt6dir}/mkspecs
%dir %{qt6dir}/mkspecs/modules
%dir %{qt6dir}/plugins
%dir %{_datadir}/qt6
%dir %{_datadir}/qt6/translations

%files -n Qt6Core-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core.so
%{_libdir}/libQt6Core.prl
%dir %{_libdir}/metatypes
%{_libdir}/metatypes/qt6core_metatypes.json
%dir %{_includedir}/qt6
%dir %{_includedir}/qt6/QtSolutions
%{_includedir}/qt6/QtCore
%{_pkgconfigdir}/Qt6Core.pc
%{_libdir}/cmake/Qt6
%{_libdir}/cmake/Qt6Core
%{qt6dir}/mkspecs/modules/qt_lib_core.pri
%{qt6dir}/mkspecs/modules/qt_lib_core_private.pri
%attr(755,root,root) %{qt6dir}/bin/tracegen

%files -n Qt6DBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DBus.so.5

%files -n Qt6DBus-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DBus.so
%{_libdir}/libQt6DBus.prl
%{_includedir}/qt6/QtDBus
%{_pkgconfigdir}/Qt6DBus.pc
%{_libdir}/cmake/Qt6DBus
%{qt6dir}/mkspecs/modules/qt_lib_dbus.pri
%{qt6dir}/mkspecs/modules/qt_lib_dbus_private.pri

%files -n Qt6DeviceDiscoverySupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtDeviceDiscoverySupport
%{_libdir}/libQt6DeviceDiscoverySupport.a
%{_libdir}/libQt6DeviceDiscoverySupport.prl
%{_libdir}/cmake/Qt6DeviceDiscoverySupport
%{qt6dir}/mkspecs/modules/qt_lib_devicediscovery_support_private.pri

%files -n Qt6EdidSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtEdidSupport
%{_libdir}/libQt6EdidSupport.a
%{_libdir}/libQt6EdidSupport.prl
%{_libdir}/cmake/Qt6EdidSupport
%{qt6dir}/mkspecs/modules/qt_lib_edid_support_private.pri

%files -n Qt6EglSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtEglSupport
%{_libdir}/libQt6EglSupport.a
%{_libdir}/libQt6EglSupport.prl
%{_libdir}/cmake/Qt6EglSupport
%{qt6dir}/mkspecs/modules/qt_lib_egl_support_private.pri

%files -n Qt6EventDispatcherSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtEventDispatcherSupport
%{_libdir}/libQt6EventDispatcherSupport.a
%{_libdir}/libQt6EventDispatcherSupport.prl
%{_libdir}/cmake/Qt6EventDispatcherSupport
%{qt6dir}/mkspecs/modules/qt_lib_eventdispatcher_support_private.pri

%files -n Qt6FbSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtFbSupport
%{_libdir}/libQt6FbSupport.a
%{_libdir}/libQt6FbSupport.prl
%{_libdir}/cmake/Qt6FbSupport
%{qt6dir}/mkspecs/modules/qt_lib_fb_support_private.pri

%files -n Qt6FontDatabaseSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtFontDatabaseSupport
%{_libdir}/libQt6FontDatabaseSupport.a
%{_libdir}/libQt6FontDatabaseSupport.prl
%{_libdir}/cmake/Qt6FontDatabaseSupport
%{qt6dir}/mkspecs/modules/qt_lib_fontdatabase_support_private.pri

%files -n Qt6GlxSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtGlxSupport
%{_libdir}/libQt6GlxSupport.a
%{_libdir}/libQt6GlxSupport.prl
%{_libdir}/cmake/Qt6GlxSupport
%{qt6dir}/mkspecs/modules/qt_lib_glx_support_private.pri

%files -n Qt6Gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Gui.so.5
# loaded from src/gui/kernel/qgenericpluginfactory.cpp
%dir %{qt6dir}/plugins/generic
# R: udev-libs (by all qevdev* plugins)
%attr(755,root,root) %{qt6dir}/plugins/generic/libqevdevkeyboardplugin.so
%attr(755,root,root) %{qt6dir}/plugins/generic/libqevdevmouseplugin.so
%attr(755,root,root) %{qt6dir}/plugins/generic/libqevdevtabletplugin.so
%attr(755,root,root) %{qt6dir}/plugins/generic/libqevdevtouchplugin.so
# loaded from src/gui/image/qicon.cpp
%dir %{qt6dir}/plugins/iconengines
# loaded from src/gui/image/qimage{reader,writer}.cpp
%dir %{qt6dir}/plugins/imageformats
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqgif.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqico.so
# R: libjpeg
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqjpeg.so
# loaded from src/gui/kernel/qplatforminputcontextfactory.cpp
%dir %{qt6dir}/plugins/platforminputcontexts
# R: libxkbcommon
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libcomposeplatforminputcontextplugin.so
# R: Qt6DBus
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libibusplatforminputcontextplugin.so
# loaded from src/gui/kernel/qplatformintegrationfactory.cpp
%dir %{qt6dir}/plugins/platforms
# R: fontconfig freetype
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqminimal.so
# R: OpenGL freetype libX11 libXrender
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqoffscreen.so
# loaded from src/gui/kernel/qplatformthemefactory.cpp
%dir %{qt6dir}/plugins/platformthemes
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt6Gui

%if %{with libinput}
%files -n Qt6Gui-generic-libinput
%defattr(644,root,root,755)
# R: libinput libxkbcommon udev
%attr(755,root,root) %{qt6dir}/plugins/generic/libqlibinputplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QLibInputPlugin.cmake
%endif

%if %{with tslib}
%files -n Qt6Gui-generic-tslib
%defattr(644,root,root,755)
# R: tslib
%attr(755,root,root) %{qt6dir}/plugins/generic/libqtslibplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QTsLibPlugin.cmake
%endif

%files -n Qt6Gui-generic-tuiotouch
%defattr(644,root,root,755)
# R: Qt6Network
%attr(755,root,root) %{qt6dir}/plugins/generic/libqtuiotouchplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QTuioTouchPlugin.cmake

%if %{with directfb}
%files -n Qt6Gui-platform-directfb
%defattr(644,root,root,755)
# R: DirectFB fontconfig freetype
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqdirectfb.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QDirectFbIntegrationPlugin.cmake
%endif

%if %{with egl}
%files -n Qt6Gui-platform-egl
%defattr(644,root,root,755)
# R: egl fontconfig freetype
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqminimalegl.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QMinimalEglIntegrationPlugin.cmake
%endif

%files -n Qt6Gui-platform-eglfs
%defattr(644,root,root,755)
# R: Qt6Gui Qt6Core EGL GL ts fontconfig freetype glib2 udev mtdev
%attr(755,root,root) %{_libdir}/libQt6EglFSDeviceIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6EglFSDeviceIntegration.so.5
# R: egl fontconfig freetype (for two following)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqeglfs.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEglFSIntegrationPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEglFSEmulatorIntegrationPlugin.cmake
# loaded from src/plugins/platforms/eglfs/qeglfsdeviceintegration.cpp
%dir %{qt6dir}/plugins/egldeviceintegrations
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-emu-integration.so

%files -n Qt6Gui-platform-eglfs-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtEglFSDeviceIntegration
%attr(755,root,root) %{_libdir}/libQt6EglFSDeviceIntegration.so
%{_libdir}/cmake/Qt6EglFSDeviceIntegration
%{_libdir}/libQt6EglFSDeviceIntegration.prl
%{qt6dir}/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri

%if %{with kms}
%files -n Qt6Gui-platform-eglfs-kms
%defattr(644,root,root,755)
# R: gl egl libdrm libgbm udev
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6EglFsKmsSupport.so.5
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-kms-integration.so
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so

%files -n Qt6Gui-platform-eglfs-kms-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsSupport.so
%{_libdir}/libQt6EglFsKmsSupport.prl
%{_libdir}/cmake/Qt6EglFsKmsSupport
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEglFSKmsEglDeviceIntegrationPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEglFSKmsGbmIntegrationPlugin.cmake
%{qt6dir}/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri
%endif

%files -n Qt6Gui-platform-eglfs-x11
%defattr(644,root,root,755)
# R: libX11 libxcb
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-x11-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEglFSX11IntegrationPlugin.cmake

%files -n Qt6Gui-platform-linuxfb
%defattr(644,root,root,755)
# R: fontconfig freetype libinput tslib udev-libs
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqlinuxfb.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QLinuxFbIntegrationPlugin.cmake

%files -n Qt6Gui-platform-vnc
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqvnc.so

%files -n Qt6Gui-platform-vnc-devel
%defattr(644,root,root,755)
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QVncIntegrationPlugin.cmake

%files -n Qt6Gui-platform-xcb
%defattr(644,root,root,755)
# R: Qt6DBus xorg* xcb* libxkbcommon-x11 fontconfig freetype
%attr(755,root,root) %{_libdir}/libQt6XcbQpa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6XcbQpa.so.5
# R: Qt6DBus xcb-* xorg*
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqxcb.so
# loaded from src/plugins/platforms/xcb/gl_integrations/qxcbglintegrationfactory.cpp
%dir %{qt6dir}/plugins/xcbglintegrations
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QXcbIntegrationPlugin.cmake

%files -n Qt6Gui-platform-xcb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6XcbQpa.so
%{_libdir}/libQt6XcbQpa.prl
%{_libdir}/cmake/Qt6XcbQpa
%{qt6dir}/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri

%files -n Qt6Gui-platform-xcb-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-egl-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QXcbEglIntegrationPlugin.cmake

%files -n Qt6Gui-platform-xcb-glx
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-glx-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QXcbGlxIntegrationPlugin.cmake

%if %{with gtk}
%files -n Qt6Gui-platformtheme-gtk3
%defattr(644,root,root,755)
# R: gtk+3
%attr(755,root,root) %{qt6dir}/plugins/platformthemes/libqgtk3.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QGtk3ThemePlugin.cmake
%endif

%files -n Qt6Gui-platformtheme-xdgdesktopportal
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platformthemes/libqxdgdesktopportal.so
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QXdgDesktopPortalThemePlugin.cmake

%files -n Qt6Gui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/bin/qvkgen
%attr(755,root,root) %{_libdir}/libQt6Gui.so
%{_libdir}/libQt6Gui.prl
%{_libdir}/metatypes/qt6gui_metatypes.json
%{_includedir}/qt6/QtGui
%{_includedir}/qt6/QtPlatformHeaders
%{_pkgconfigdir}/Qt6Gui.pc
%{_libdir}/cmake/Qt6Gui/Qt6GuiConfig*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEvdevKeyboardPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEvdevMousePlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEvdevTabletPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QEvdevTouchScreenPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QGifPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QICOPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QJpegPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QComposePlatformInputContextPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QIbusPlatformInputContextPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QMinimalIntegrationPlugin.cmake
%{_libdir}/cmake/Qt6Gui/Qt6Gui_QOffscreenIntegrationPlugin.cmake
%{qt6dir}/mkspecs/modules/qt_lib_gui.pri
%{qt6dir}/mkspecs/modules/qt_lib_gui_private.pri

%files -n Qt6InputSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtInputSupport
%{_libdir}/libQt6InputSupport.a
%{_libdir}/libQt6InputSupport.prl
%{_libdir}/cmake/Qt6InputSupport
%{qt6dir}/mkspecs/modules/qt_lib_input_support_private.pri

%files -n Qt6KmsSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtKmsSupport
%{_libdir}/libQt6KmsSupport.a
%{_libdir}/libQt6KmsSupport.prl
%{_libdir}/cmake/Qt6KmsSupport
%{qt6dir}/mkspecs/modules/qt_lib_kms_support_private.pri

%files -n Qt6Network
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Network.so.5
# loaded from src/network/bearer/qnetworkconfigmanager_p.cpp
%dir %{qt6dir}/plugins/bearer
# R: Qt6DBus
%attr(755,root,root) %{qt6dir}/plugins/bearer/libqconnmanbearer.so
%attr(755,root,root) %{qt6dir}/plugins/bearer/libqgenericbearer.so
# R: Qt6DBus
%attr(755,root,root) %{qt6dir}/plugins/bearer/libqnmbearer.so

%files -n Qt6Network-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so
%{_libdir}/libQt6Network.prl
%{_includedir}/qt6/QtNetwork
%{_pkgconfigdir}/Qt6Network.pc
%dir %{_libdir}/cmake/Qt6Network
%{_libdir}/cmake/Qt6Network/Qt6NetworkConfig*.cmake
%{_libdir}/cmake/Qt6Network/Qt6Network_QConnmanEnginePlugin.cmake
%{_libdir}/cmake/Qt6Network/Qt6Network_QGenericEnginePlugin.cmake
%{_libdir}/cmake/Qt6Network/Qt6Network_QNetworkManagerEnginePlugin.cmake
%{qt6dir}/mkspecs/modules/qt_lib_network.pri
%{qt6dir}/mkspecs/modules/qt_lib_network_private.pri

%files -n Qt6OpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6OpenGL.so.5

%files -n Qt6OpenGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpenGL.so
%{_libdir}/libQt6OpenGL.prl
%{_includedir}/qt6/QtOpenGL
%{_pkgconfigdir}/Qt6OpenGL.pc
%{_libdir}/cmake/Qt6OpenGL
%{qt6dir}/mkspecs/modules/qt_lib_opengl.pri
%{qt6dir}/mkspecs/modules/qt_lib_opengl_private.pri

%files -n Qt6OpenGLExtensions-devel
%defattr(644,root,root,755)
# static-only
%{_libdir}/libQt6OpenGLExtensions.a
%{_libdir}/libQt6OpenGLExtensions.prl
%{_includedir}/qt6/QtOpenGLExtensions
%{_pkgconfigdir}/Qt6OpenGLExtensions.pc
%{_libdir}/cmake/Qt6OpenGLExtensions
%{qt6dir}/mkspecs/modules/qt_lib_openglextensions.pri
%{qt6dir}/mkspecs/modules/qt_lib_openglextensions_private.pri

%files -n Qt6PlatformCompositorSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtPlatformCompositorSupport
%{_libdir}/libQt6PlatformCompositorSupport.a
%{_libdir}/libQt6PlatformCompositorSupport.prl
%{_libdir}/cmake/Qt6PlatformCompositorSupport
%{qt6dir}/mkspecs/modules/qt_lib_platformcompositor_support_private.pri

%files -n Qt6PrintSupport
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6PrintSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PrintSupport.so.5
# loaded from src/printsupport/kernel/qplatformprintplugin.cpp
%dir %{qt6dir}/plugins/printsupport
%if %{with cups}
%attr(755,root,root) %{qt6dir}/plugins/printsupport/libcupsprintersupport.so
%endif

%files -n Qt6PrintSupport-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6PrintSupport.so
%{_libdir}/libQt6PrintSupport.prl
%{_includedir}/qt6/QtPrintSupport
%{_pkgconfigdir}/Qt6PrintSupport.pc
%dir %{_libdir}/cmake/Qt6PrintSupport
%{_libdir}/cmake/Qt6PrintSupport/Qt6PrintSupportConfig*.cmake
%if %{with cups}
%{_libdir}/cmake/Qt6PrintSupport/Qt6PrintSupport_QCupsPrinterSupportPlugin.cmake
%endif
%{qt6dir}/mkspecs/modules/qt_lib_printsupport.pri
%{qt6dir}/mkspecs/modules/qt_lib_printsupport_private.pri

%files -n Qt6ServiceSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtServiceSupport
%{_libdir}/libQt6ServiceSupport.a
%{_libdir}/libQt6ServiceSupport.prl
%{_libdir}/cmake/Qt6ServiceSupport
%{qt6dir}/mkspecs/modules/qt_lib_service_support_private.pri

%files -n Qt6Sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Sql.so.5
# loaded from src/sql/kernel/qsqldatabase.cpp
%dir %{qt6dir}/plugins/sqldrivers
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt6Sql

%if %{with db2}
%files -n Qt6Sql-sqldriver-db2
%defattr(644,root,root,755)
# R: (proprietary) DB2 libs
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqldb2.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QDB2DriverPlugin.cmake
%endif

%if %{with ibase}
%files -n Qt6Sql-sqldriver-ibase
%defattr(644,root,root,755)
# R: Firebird-lib
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlibase.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QIBaseDriverPlugin.cmake
%endif

%if %{with sqlite3}
%files -n Qt6Sql-sqldriver-sqlite3
%defattr(644,root,root,755)
# R: sqlite3
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlite.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QSQLiteDriverPlugin.cmake
%endif

%if %{with mysql}
%files -n Qt6Sql-sqldriver-mysql
%defattr(644,root,root,755)
# R: mysql-libs
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlmysql.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QMYSQLDriverPlugin.cmake
%endif

%if %{with oci}
%files -n Qt6Sql-sqldriver-oci
%defattr(644,root,root,755)
# R: (proprietary) Oracle libs
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqloci.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QOCIDriverPlugin.cmake
%endif

%if %{with odbc}
%files -n Qt6Sql-sqldriver-odbc
%defattr(644,root,root,755)
# R: unixODBC
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlodbc.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QODBCDriverPlugin.cmake
%endif

%if %{with pgsql}
%files -n Qt6Sql-sqldriver-pgsql
%defattr(644,root,root,755)
# R: postgresql-libs
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlpsql.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QPSQLDriverPlugin.cmake
%endif

%if %{with freetds}
%files -n Qt6Sql-sqldriver-tds
%defattr(644,root,root,755)
# R: freetds
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqltds.so
%{_libdir}/cmake/Qt6Sql/Qt6Sql_QTDSDriverPlugin.cmake
%endif

%files -n Qt6Sql-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sql.so
%{_libdir}/libQt6Sql.prl
%{_includedir}/qt6/QtSql
%{_pkgconfigdir}/Qt6Sql.pc
%{_libdir}/cmake/Qt6Sql/Qt6SqlConfig*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_sql.pri
%{qt6dir}/mkspecs/modules/qt_lib_sql_private.pri

%files -n Qt6Test
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Test.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Test.so.5

%files -n Qt6Test-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Test.so
%{_libdir}/libQt6Test.prl
%{_includedir}/qt6/QtTest
%{_pkgconfigdir}/Qt6Test.pc
%{_libdir}/cmake/Qt6Test
%{qt6dir}/mkspecs/modules/qt_lib_testlib.pri
%{qt6dir}/mkspecs/modules/qt_lib_testlib_private.pri

%files -n Qt6ThemeSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtThemeSupport
%{_libdir}/libQt6ThemeSupport.a
%{_libdir}/libQt6ThemeSupport.prl
%{_libdir}/cmake/Qt6ThemeSupport
%{qt6dir}/mkspecs/modules/qt_lib_theme_support_private.pri

%files -n Qt6VulkanSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtVulkanSupport
%{_libdir}/libQt6VulkanSupport.a
%{_libdir}/libQt6VulkanSupport.prl
%{_libdir}/cmake/Qt6VulkanSupport
%{qt6dir}/mkspecs/modules/qt_lib_vulkan_support_private.pri

%files -n Qt6Widgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Widgets.so.5
%dir %{qt6dir}/plugins/styles

%files -n Qt6Widgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so
%{_libdir}/libQt6Widgets.prl
%{_libdir}/metatypes/qt6widgets_metatypes.json
%{_includedir}/qt6/QtWidgets
%{_pkgconfigdir}/Qt6Widgets.pc
%dir %{_libdir}/cmake/Qt6Widgets
%{_libdir}/cmake/Qt6Widgets/Qt6WidgetsConfig*.cmake
%{_libdir}/cmake/Qt6Widgets/Qt6WidgetsMacros.cmake
%{qt6dir}/mkspecs/modules/qt_lib_widgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_widgets_private.pri

%files -n Qt6XkbCommonSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtXkbCommonSupport
%{_libdir}/libQt6XkbCommonSupport.a
%{_libdir}/libQt6XkbCommonSupport.prl
%{_libdir}/cmake/Qt6XkbCommonSupport
%{qt6dir}/mkspecs/modules/qt_lib_xkbcommon_support_private.pri

%files -n Qt6Xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Xml.so.5

%files -n Qt6Xml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Xml.so
%{_libdir}/libQt6Xml.prl
%{_includedir}/qt6/QtXml
%{_pkgconfigdir}/Qt6Xml.pc
%{_libdir}/cmake/Qt6Xml
%{qt6dir}/mkspecs/modules/qt_lib_xml.pri
%{qt6dir}/mkspecs/modules/qt_lib_xml_private.pri

%files -n qt6-doc-common
%defattr(644,root,root,755)
%dir %{_docdir}/qt6-doc
%{_docdir}/qt6-doc/config
%{_docdir}/qt6-doc/global

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qmake
%{_docdir}/qt6-doc/qtconcurrent
%{_docdir}/qt6-doc/qtcore
%{_docdir}/qt6-doc/qtdbus
%{_docdir}/qt6-doc/qtgui
%{_docdir}/qt6-doc/qtnetwork
%{_docdir}/qt6-doc/qtopengl
%{_docdir}/qt6-doc/qtplatformheaders
%{_docdir}/qt6-doc/qtprintsupport
%{_docdir}/qt6-doc/qtsql
%{_docdir}/qt6-doc/qttestlib
%{_docdir}/qt6-doc/qtwidgets
%{_docdir}/qt6-doc/qtxml

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qmake.qch
%{_docdir}/qt6-doc/qtconcurrent.qch
%{_docdir}/qt6-doc/qtcore.qch
%{_docdir}/qt6-doc/qtdbus.qch
%{_docdir}/qt6-doc/qtgui.qch
%{_docdir}/qt6-doc/qtnetwork.qch
%{_docdir}/qt6-doc/qtopengl.qch
%{_docdir}/qt6-doc/qtplatformheaders.qch
%{_docdir}/qt6-doc/qtprintsupport.qch
%{_docdir}/qt6-doc/qtsql.qch
%{_docdir}/qt6-doc/qttestlib.qch
%{_docdir}/qt6-doc/qtwidgets.qch
%{_docdir}/qt6-doc/qtxml.qch
%endif

%files examples -f examples.files
%defattr(644,root,root,755)
%dir %{_examplesdir}/qt6
%doc %{_examplesdir}/qt6/README
%{_examplesdir}/qt6/examples.pro

%files -n qt6-build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/moc-qt6
%attr(755,root,root) %{_bindir}/qdbuscpp2xml-qt6
%attr(755,root,root) %{_bindir}/qdbusxml2cpp-qt6
%attr(755,root,root) %{_bindir}/qdoc-qt6
%attr(755,root,root) %{_bindir}/qlalr-qt6
%attr(755,root,root) %{_bindir}/rcc-qt6
%attr(755,root,root) %{_bindir}/uic-qt6
%attr(755,root,root) %{qt6dir}/bin/fixqt4headers.pl
%attr(755,root,root) %{qt6dir}/bin/moc
%attr(755,root,root) %{qt6dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt6dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt6dir}/bin/qlalr
%attr(755,root,root) %{qt6dir}/bin/rcc
%attr(755,root,root) %{qt6dir}/bin/syncqt.pl
%attr(755,root,root) %{qt6dir}/bin/uic

%files -n qt6-qmake
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmake-qt6
%attr(755,root,root) %{qt6dir}/bin/qmake
%{qt6dir}/mkspecs/aix-*
%{qt6dir}/mkspecs/android-*
%{qt6dir}/mkspecs/common
%{qt6dir}/mkspecs/dummy
%{qt6dir}/mkspecs/cygwin-*
%{qt6dir}/mkspecs/darwin-*
%{qt6dir}/mkspecs/devices
%{qt6dir}/mkspecs/features
%{qt6dir}/mkspecs/freebsd-*
%{qt6dir}/mkspecs/haiku-*
%{qt6dir}/mkspecs/hpuxi-*
%{qt6dir}/mkspecs/hurd-*
%{qt6dir}/mkspecs/integrity-armv7*
%{qt6dir}/mkspecs/integrity-armv8*
%{qt6dir}/mkspecs/integrity-x86
%{qt6dir}/mkspecs/linux-*
%{qt6dir}/mkspecs/lynxos-*
%{qt6dir}/mkspecs/macx-*
%{qt6dir}/mkspecs/netbsd-*
%{qt6dir}/mkspecs/openbsd-*
%{qt6dir}/mkspecs/qnx-*
%{qt6dir}/mkspecs/solaris-*
%{qt6dir}/mkspecs/unsupported
%{qt6dir}/mkspecs/wasm-emscripten
%{qt6dir}/mkspecs/win32-*
%{qt6dir}/mkspecs/winrt-*
%{qt6dir}/mkspecs/*.pri
