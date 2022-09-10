# Note on packaging .cmake files for plugins:
# Base Qt6${component}Config.cmake file includes all existing Qt6${component}_*Plugin.cmake
# files, which trigger check for presence of plugin module in filesystem.
# Thus, for plugins separated into subpackages, we package plugins .cmake file
# together with module, and the rest of .cmake files in appropriate -devel subpackage.
#
# TODO:
#
#   /usr/lib64/cmake/Qt6BundledOpenwnn/Qt6BundledOpenwnnDependencies.cmake
#   /usr/lib64/cmake/Qt6BundledPinyin/Qt6BundledPinyinDependencies.cmake
#   /usr/lib64/cmake/Qt6BundledTcime/Qt6BundledTcimeDependencies.cmake
#   /usr/lib64/cmake/Qt6Bundled_Clip2Tri/Qt6Bundled_Clip2TriDependencies.cmake
#
#   /usr/lib64/cmake/Qt6HostInfo/Qt6HostInfoConfig.cmake
#   /usr/lib64/objects-PLD/QmlCompilerPrivate_resources_1/.rcc/qrc_builtins.cpp.o
#   /usr/lib64/qt6/bin/instancer
#   /usr/lib64/qt6/bin/materialeditor
#   /usr/lib64/qt6/bin/qt-configure-module
#   /usr/lib64/qt6/bin/shadergen
#   /usr/lib64/qt6/bin/shapegen
#   /usr/lib64/qt6/libexec/gn
#   /usr/lib64/qt6/mkspecs/modules/README
#   /usr/lib64/qt6/mkspecs/qtdoc_dummy_file.txt
# android:
#   /usr/lib64/qt6/libexec/android_emulator_launcher.sh
#   /usr/lib64/qt6/plugins/networkinformation/libqglib.so
#   /usr/lib64/qt6/plugins/networkinformation/libqnetworkmanager.so
#
# Conditional build:
# -- build targets
%bcond_without	doc		# Documentation
%bcond_without	webengine	# Qt WebEngine
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB platform support
%bcond_without	egl		# EGL (EGLFS, minimal EGL) platform support
%bcond_with	fbx		# Autodesk FBX SDK support (proprietary)
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
%ifarch %{ix86} x32
%undefine	with_webengine
%endif

%define		icu_abi		71
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

Summary:	Qt6 Library
Summary(pl.UTF-8):	Biblioteka Qt6
Name:		qt6
Version:	6.3.1
Release:	2
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/6.3/%{version}/single/qt-everywhere-src-%{version}.tar.xz
# Source0-md5:	957a304773b281a4584f4c0254773456
Patch0:		system-cacerts.patch
Patch1:		ninja-program.patch
Patch2:		%{name}-gn.patch
Patch3:		no-implicit-sse2.patch
Patch4:		x32.patch
URL:		https://www.qt.io/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	EGL-devel
%{?with_ibase:BuildRequires:	Firebird-devel}
%{?with_kms:BuildRequires:	Mesa-libgbm-devel}
BuildRequires:	OpenGL-devel
%{?with_kms:BuildRequires:	OpenGLESv2-devel}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	alsa-lib-devel
BuildRequires:	assimp-devel >= 5
BuildRequires:	at-spi2-core-devel
BuildRequires:	bluez-libs-devel
# qdoc
BuildRequires:	clang-devel
# base dir requires 3.16, gn 3.19
BuildRequires:	cmake >= 3.19
%{?with_cups:BuildRequires:	cups-devel >= 1.4}
BuildRequires:	dbus-devel >= 1.2
BuildRequires:	double-conversion-devel
%{?with_fbx:BuildRequires:	fbxsdk-devel}
BuildRequires:	ffmpeg-devel
BuildRequires:	fontconfig-devel
%{?with_freetds:BuildRequires:	freetds-devel}
BuildRequires:	freetype-devel >= 2.2.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 2.0.0
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.6}
BuildRequires:	harfbuzz-devel >= 1.6.0
BuildRequires:	harfbuzz-subset-devel
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	lcms2-devel
%{?with_kms:BuildRequires:	libdrm-devel}
BuildRequires:	libevent-devel
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
%{?with_libinput:BuildRequires:	libinput-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel >= 2:1.0.8
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libvpx-devel
BuildRequires:	libwebp-devel
BuildRequires:	libxcb-devel >= 1.12
BuildRequires:	libxml2-devel
BuildRequires:	minizip-devel
BuildRequires:	mtdev-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_webengine:BuildRequires:	nodejs}
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	opus-devel
%{?with_oci:BuildRequires:	oracle-instantclient-devel}
BuildRequires:	pciutils-devel
BuildRequires:	pcre2-16-devel >= 10.20
BuildRequires:	pkgconfig
BuildRequires:	poppler-cpp-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	pulseaudio-devel
BuildRequires:	python3-html5lib
BuildRequires:	re2-devel
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.752
BuildRequires:	samurai
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
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

%define		filterout	-flto

%define		qt6dir		%{_libdir}/qt6

%description
Qt is a software toolkit for developing applications.

%description -l pl.UTF-8
Qt to programowy toolkit do tworzenia aplikacji.

%package -n qt6-qttools
Summary:	Development tools for Qt 6
Summary(pl.UTF-8):	Narzędzia programistyczne dla Qt 6
Group:		X11/Libraries
# pixeltool: Core, Gui, Widgets
# qtdiag: Core Gui Network Widgets
# qtpaths: Core
# qtplugininfo: Core
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}

%description -n qt6-qttools
Qt is a cross-platform application and UI framework. Using Qt, you can
write web-enabled applications once and deploy them across desktop,
mobile and embedded systems without rewriting the source code.

This package contains additional tools for building Qt applications.

%description -n qt6-qttools -l pl.UTF-8
Qt to wieloplatformowy szkielet aplikacji i interfejsów użytkownika.
Przy użyciu Qt można pisać aplikacje powiązane z WWW i wdrażać je w
systemach biurkowych, przenośnych i wbudowanych bez przepisywania kodu
źródłowego.

Ten pakiet zawiera dodatkowe narzędzia do budowania aplikacji Qt.

%package -n qt6-assistant
Summary:	Qt documentation browser
Summary(pl.UTF-8):	Przeglądarka dokumentacji Qt
Group:		X11/Development/Tools
# assistant: Core, Gui, Help, Network, PrintSupport, Sql, Widgets
# qdistancefieldgenerator: Core Gui Quick Widgets
# qdoc: Core, clang-libs
# qhelpgenerator: Core, Gui, Help Sql; sqldriver-sqlite3 to work
# qtattributionsscanner: Core
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Help = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Sql = %{version}
Requires:	Qt6Sql-sqldriver-sqlite3 = %{version}
Requires:	Qt6Widgets = %{version}

%description -n qt6-assistant
Qt Assistant is a tool for browsing on-line documentation with
indexing, bookmarks and full-text search.

%description -n qt6-assistant -l pl.UTF-8
Qt Assistant to narzędzie do przeglądania dokumentacji z możliwością
indeksowania, dodawania zakładek i pełnotekstowego wyszukiwania.

%package -n qt6-designer
Summary:	IDE used for GUI designing with Qt 6 library
Summary(pl.UTF-8):	IDE służące do projektowania GUI przy użyciu biblioteki Qt 6
Group:		X11/Applications
Requires:	Qt6Core = %{version}
Requires:	Qt6Designer = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	Qt6Xml = %{version}

%description -n qt6-designer
An advanced tool used for GUI designing with Qt 6 library.

%description -n qt6-designer -l pl.UTF-8
Zaawansowane narzędzie służące do projektowania interfejsu graficznego
przy użyciu biblioteki Qt 6.

%package -n qt6-linguist
Summary:	Translation helper for Qt 6
Summary(pl.UTF-8):	Aplikacja ułatwiająca tłumaczenie aplikacji opartych na Qt 6
Group:		X11/Development/Tools
# lconvert,lprodump,lrelease*,lupdate*: Core
# linguist: Core, Gui, PrintSupport, Widgets
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	Qt6Xml = %{version}

%description -n qt6-linguist
Translation helper for Qt 6.

%description -n qt6-linguist -l pl.UTF-8
Aplikacja ułatwiająca tłumaczenie aplikacji opartych na Qt 6.

%package -n qt6-qdbus
Summary:	Qt6 DBus tools
Summary(pl.UTF-8):	Narzędzia Qt6 do magistrali DBus
Group:		X11/Applications
# qdbus: Core, DBus, Xml
# qdbusviewer: Core, DBus, Gui, Widgets, Xml
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	Qt6Xml = %{version}

%description -n qt6-qdbus
This package contains the qdbus and qdbusviewer tools.

%description -n qt6-qdbus -l pl.UTF-8
Ten pakiet zawiera narzędzia qdbus i qdbusviewer.

%package -n qt6-qtdeclarative
Summary:	The Qt6 Declarative libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Declarative
Group:		X11/Libraries
# qml: Core Gui Qml Widgets
# qmlcachegen: Core
# qmleasing: Core Gui Qml Quick Widgets
# qmlformat: Core
# qmlimportscanner: Core
# qmllint: Core
# qmlmin: Core
# qmlplugindump: Core Gui Qml Widgets
# qmlpreview: Core Network
# qmlprofiler: Core Network
# qmlscene: Core Gui Qml Quick Widgets
# qmltestrunner: Core QuickTest
# qmltyperegistrar: Core
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Widgets = %{version}

%description -n qt6-qtdeclarative
This package contains Qt6 Declarative tools.

%description -n qt6-qtdeclarative -l pl.UTF-8
Ten pakiet zawiera narzeędzia Qt6 Declarative.

%package -n qt6-qttools-doc
Summary:	Qt6 Tools documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do narzędzi Qt6 w formacie HTML
Group:		X11/Development/Libraries
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n qt6-qttools-doc
Qt6 Tools documentation in HTML format.

%description -n qt6-qttools-doc -l pl.UTF-8
Dokumentacja do narzędzi Qt6 w formacie HTML.

%package -n qt6-qttools-doc-qch
Summary:	Qt6 Tools documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do narzędzi Qt6 w formacie QCH
Group:		X11/Development/Libraries
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n qt6-qttools-doc-qch
Qt6 Tools documentation in QCH format.

%description -n qt6-qttools-doc-qch -l pl.UTF-8
Dokumentacja do narzędzi Qt6 w formacie QCH.

%package -n Qt63D
Summary:	The Qt6 3D libraries
Summary(pl.UTF-8):	Biblioteki Qt6 3D
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	assimp >= 5

%description -n Qt63D
Qt6 3D libraries.

%description -n Qt63D -l pl.UTF-8
Biblioteki Qt6 3D.
%package -n Qt63D-devel
Summary:	Qt6 3D - development files
Summary(pl.UTF-8):	Biblioteki Qt6 3D - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt63D = %{version}
Requires:	Qt6Concurrent-devel = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Qml-devel = %{version}

%description -n Qt63D-devel
Qt6 3D - development files.

%description -n Qt63D-devel -l pl.UTF-8
Biblioteki Qt6 3D - pliki programistyczne.

%package -n Qt63D-doc
Summary:	Qt6 3D documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 3D w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt63D-doc
Qt6 3D documentation in HTML format.

%description -n Qt63D-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 3D w formacie HTML.

%package -n Qt63D-doc-qch
Summary:	Qt6 3D documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 3D w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt63D-doc-qch
Qt6 3D documentation in QCH format.

%description -n Qt63D-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 3D w formacie QCH.

%package -n Qt6Bluetooth
Summary:	Qt6 Bluetooth library
Summary(pl.UTF-8):	Biblioteka Qt6 Bluetooth
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6Bluetooth
Qt6 Bluetooth library provides classes that enable basic Bluetooth
operations like scanning for devices and connecting them.

%description -n Qt6Bluetooth -l pl.UTF-8
Biblioteka Qt6 Bluetooth dostarcza klasy umożliwiające podstawowe
operacje Bluetooth, takie jak wyszukiwanie urządzeń i łączenie z nimi.

%package -n Qt6Bluetooth-devel
Summary:	The Qt6 Bluetooth - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Bluetooth - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Bluetooth = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus-devel = %{version}

%description -n Qt6Bluetooth-devel
The Qt6 Bluetooth - development files.

%description -n Qt6Bluetooth-devel -l pl.UTF-8
Biblioteka Qt6 Bluetooth - pliki programistyczne.

%package -n Qt6Bluetooth-doc
Summary:	Qt6 Bluetooth documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Bluetooth w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Bluetooth-doc
Qt6 Bluetooth documentation in HTML format.

%description -n Qt6Bluetooth-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Bluetooth w formacie HTML.

%package -n Qt6Bluetooth-doc-qch
Summary:	Qt6 Bluetooth documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Bluetooth w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Bluetooth-doc-qch
Qt6 Bluetooth documentation in QCH format.

%description -n Qt6Bluetooth-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Bluetooth w formacie QCH.

%package -n Qt6Bodymovin
Summary:	The Qt6 Bodymovin library
Summary(pl.UTF-8):	Biblioteka Qt6 Bodymovin
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Bodymovin
Qt6 Bodymovin library.

%description -n Qt6Bodymovin -l pl.UTF-8
Biblioteka Qt6 Bodymovin.

%package -n Qt6Bodymovin-devel
Summary:	Qt6 Bodymovin - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Bodymovin - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Bodymovin = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}

%description -n Qt6Bodymovin-devel
Qt6 Bodymovin - development files.

%description -n Qt6Bodymovin-devel -l pl.UTF-8
Biblioteka Qt6 Bodymovin - pliki programistyczne.

%package -n Qt6Bodymovin-doc
Summary:	Qt6 Lottie (Bodymovin) documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Lottie (Bodymovin) w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Bodymovin-doc
Qt6 Lottie (Bodymovin) documentation in HTML format.

%description -n Qt6Bodymovin-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Lottie (Bodymovin) w formacie HTML.

%package -n Qt6Bodymovin-doc-qch
Summary:	Qt6 Lottie (Bodymovin) documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Lottie (Bodymovin) w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Bodymovin-doc-qch
Qt6 Lottie (Bodymovin) documentation in QCH format.

%description -n Qt6Bodymovin-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Lottie (Bodymovin) w formacie QCH.

%package -n Qt6Charts
Summary:	The Qt6 Charts library
Summary(pl.UTF-8):	Biblioteka Qt6 Charts
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}
# for qml module
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Charts
Qt Charts module provides a set of easy to use chart components. It
uses the Qt Graphics View Framework, therefore charts can be easily
integrated to modern user interfaces.

%description -n Qt6Charts -l pl.UTF-8
Biblioteka Qt6 Charts udostępnia łatwe w użyciu komponenty do
tworzenia wykresów. Wykorzystuje szkielet Qt Graphics View, dzięki
czemu wykresy mogą być łatwo integrowane z nowoczesnymi interfejsami
użytkownika.

%package -n Qt6Charts-devel
Summary:	Qt6 Charts library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Charts - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Charts = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6Charts-devel
Qt6 Charts library - development files.

%description -n Qt6Charts-devel -l pl.UTF-8
Biblioteka Qt6 Charts - pliki programistyczne.

%package -n Qt6Charts-doc
Summary:	Qt6 Charts documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Charts w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Charts-doc
Qt6 Charts documentation in HTML format.

%description -n Qt6Charts-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Charts w formacie HTML.

%package -n Qt6Charts-doc-qch
Summary:	Qt6 Charts documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Charts w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Charts-doc-qch
Qt6 Charts documentation in QCH format.

%description -n Qt6Charts-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Charts w formacie QCH.

%package -n Qt6Coap
Summary:	The Qt6 Coap library
Summary(pl.UTF-8):	Biblioteka Qt6 Coap
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6Coap
Qt Coap module contains a library that supports the CoAP protocol.
CoAP is a protocol for IoT devices and machine to machine
communication.

%description -n Qt6Coap -l pl.UTF-8
Moduł Qt Coap zawiera bibliotekę obsługującą protokół CoAP. Jest to
protokół dla urządzeń IoT oraz do komunikacji między maszynami.

%package -n Qt6Coap-devel
Summary:	Qt6 Coap library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Coap - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Coap = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}

%description -n Qt6Coap-devel
Qt6 Coap library - development files.

%description -n Qt6Coap-devel -l pl.UTF-8
Biblioteka Qt6 Coap - pliki programistyczne.

%package -n Qt6Coap-doc
Summary:	Qt6 Coap documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Coap w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Coap-doc
Qt6 Coap documentation in HTML format.

%description -n Qt6Coap-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Coap w formacie HTML.

%package -n Qt6Coap-doc-qch
Summary:	Qt6 Coap documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Coap w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Coap-doc-qch
Qt6 Coap documentation in QCH format.

%description -n Qt6Coap-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Coap w formacie QCH.

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
Requires:	qt6-qttools = %{version}
Requires:	zlib-devel >= 1.0.8

%description -n Qt6Core-devel
Header files for Qt6 Core library.

%description -n Qt6Core-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Core.

%package -n Qt6DataVisualization
Summary:	The Qt6 DataVisualization library
Summary(pl.UTF-8):	Biblioteka Qt6 DataVisualization
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6DataVisualization
Qt6 DataVisualization library.

%description -n Qt6DataVisualization -l pl.UTF-8
Biblioteka Qt6 DataVisualization.

%package -n Qt6DataVisualization-devel
Summary:	Qt6 DataVisualization - development files
Summary(pl.UTF-8):	Biblioteka Qt6 DataVisualization - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DataVisualization = %{version}
Requires:	Qt6Gui-devel = %{version}

%description -n Qt6DataVisualization-devel
Qt6 DataVisualization - development files.

%description -n Qt6DataVisualization-devel -l pl.UTF-8
Biblioteka Qt6 DataVisualization - pliki programistyczne.

%package -n Qt6DataVisualization-doc
Summary:	Qt6 DataVisualization documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 DataVisualization w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6DataVisualization-doc
Qt6 DataVisualization documentation in HTML format.

%description -n Qt6DataVisualization-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 DataVisualization w formacie HTML.

%package -n Qt6DataVisualization-doc-qch
Summary:	Qt6 DataVisualization documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 DataVisualization w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6DataVisualization-doc-qch
Qt6 DataVisualization documentation in QCH format.

%description -n Qt6DataVisualization-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 DataVisualization w formacie QCH.

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

%package -n Qt6Designer
Summary:	Qt6 Designer libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Designer
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	Qt6Xml = %{version}

%description -n Qt6Designer
The Qt6 Designer libraries provide classes to create your own custom
widget plugins for Qt Designer and classes to access Qt Designer
components.

%description -n Qt6Designer -l pl.UTF-8
Biblioteki Qt6 Designer dostarczają klasy do tworzenia wtyczek Qt
Designera do obsługi własnych widgetów oraz klasy pozwalające na
dostęp do komponentów Qt Designera.

%package -n Qt6Designer-devel
Summary:	Qt6 Designer libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Designer - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core = %{version}
Requires:	Qt6Designer = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}
Requires:	Qt6Xml = %{version}

%description -n Qt6Designer-devel
Header files for Qt6 Designer libraries.

%description -n Qt6Designer-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek Qt6 Designer.

%package -n Qt6Designer-plugin-qquickwidget
Summary:	QQuickWidget (Quick2) plugin for Qt6 Designer
Summary(pl.UTF-8):	Wtyczka QQuickWidget (Quick2) dla Qt6 Designera
Group:		X11/Libraries
Requires:	Qt6Designer = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Designer-plugin-qquickwidget
QQuickWidget (Quick2) plugin for Qt6 Designer.

%description -n Qt6Designer-plugin-qquickwidget -l pl.UTF-8
Wtyczka QQuickWidget (Quick2) dla Qt6 Designera.

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
applications written with Qt 6.

%description -n Qt6Gui -l pl
Biblioteka Qt6 Gui udostępnia podstawową funkcjonalność dla
graficznych aplikacji napisanych z użyciem Qt 6.

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
Requires:	Vulkan-Loader-devel
Requires:	libpng-devel

%description -n Qt6Gui-devel
Header files for Qt6 Gui library.

%description -n Qt6Gui-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Gui.

%package -n Qt6Help
Summary:	Qt6 Help library
Summary(pl.UTF-8):	Biblioteka Qt6 Help
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Sql = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Help
Qt6 Help library provides classes for integrating online documentation
in applications.

%description -n Qt6Help -l pl.UTF-8
Biblioteka Qt6 Help dostarcza klasy służące do integracji dokumentacji
online w aplikacjach.

%package -n Qt6Help-devel
Summary:	Qt6 Help library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Help - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Help = %{version}
Requires:	Qt6Sql-devel = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6Help-devel
Header files for Qt6 Help library.

%description -n Qt6Help-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Help.

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

%package -n Qt6JsonRpc
Summary:	Qt6 JsonRpc library
Summary(pl.UTF-8):	Biblioteka Qt6 JsonRpc
Group:		X11/Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6JsonRpc
Qt6 LanguageServer library provides an implementation of the JSON-RPC
protocol.

%package -n Qt6JsonRpc-devel
Summary:	Qt6 JsonRpc library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 JsonRpc - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6JsonRpc-devel = %{version}

%description -n Qt6JsonRpc-devel
Qt6 JsonRpc library - development files.

%description -n Qt6JsonRpc-devel -l pl.UTF-8
Biblioteka Qt6 JsonRpc - pliki programistyczne.

%package -n Qt6LanguageServer
Summary:	Qt6 LanguageServer library
Summary(pl.UTF-8):	Biblioteka Qt6 LanguageServer
Group:		X11/Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6LanguageServer
Qt6 LanguageServer library provides an implementation of the Language
Server Protocol.

%package -n Qt6LanguageServer-devel
Summary:	Qt6 LanguageServer library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 LanguageServer - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6LanguageServer-devel = %{version}

%description -n Qt6LanguageServer-devel
Qt6 LanguageServer library - development files.

%description -n Qt6LanguageServer-devel -l pl.UTF-8
Biblioteka Qt6 LanguageServer - pliki programistyczne.

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

%package -n Qt6Mqtt
Summary:	The Qt6 Mqtt library
Summary(pl.UTF-8):	Biblioteka Qt6 Mqtt
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6Mqtt
Qt Mqtt module contains a library that supports the MQTT protocol.
MQTT is a machine-to-machine (M2M) protocol utilizing the
publish-and-subscribe paradigm. Its purpose is to provide a channel
with minimal communication overhead.

%description -n Qt6Mqtt -l pl.UTF-8
Moduł Qt Mqtt zawiera bibliotekę obsługującą protokół MQTT. Jest to
protokół międzymaszynowy (M2M), korzystający z paradygmatu publikacji
i subskrypcji. Celem jest zapewnienie kanału z minimalnym narzutem na
komunikację.

%package -n Qt6Mqtt-devel
Summary:	Qt6 Mqtt library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Mqtt - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Mqtt = %{version}
Requires:	Qt6Network-devel = %{version}

%description -n Qt6Mqtt-devel
Qt6 Mqtt library - development files.

%description -n Qt6Mqtt-devel -l pl.UTF-8
Biblioteka Qt6 Mqtt - pliki programistyczne.

%package -n Qt6Mqtt-doc
Summary:	Qt6 Mqtt documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Mqtt w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Mqtt-doc
Qt6 Mqtt documentation in HTML format.

%description -n Qt6Mqtt-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Mqtt w formacie HTML.

%package -n Qt6Mqtt-doc-qch
Summary:	Qt6 Mqtt documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Mqtt w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Mqtt-doc-qch
Qt6 Mqtt documentation in QCH format.

%description -n Qt6Mqtt-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Mqtt w formacie QCH.

%package -n Qt6Multimedia
Summary:	The Qt6 Multimedia libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Multimedia
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	alsa-lib >= 1.0.10
Requires:	pulseaudio-libs >= 0.9.11

%description -n Qt6Multimedia
Qt6 Multimedia libraries provide audio, video, radio and camera
functionality.

%description -n Qt6Multimedia -l pl.UTF-8
Biblioteki Qt6 Multimedia dostarczają funkcjonalność związaną z
dźwiękiem, obrazem, radiem i kamerą.

%package -n Qt6Multimedia-devel
Summary:	Qt6 Multimedia libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Multimedia - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Multimedia = %{version}
Requires:	Qt6Network-devel = %{version}

%description -n Qt6Multimedia-devel
Qt6 Multimedia libraries - development files.

%description -n Qt6Multimedia-devel -l pl.UTF-8
Biblioteki Qt6 Multimedia - pliki programistyczne.

%package -n Qt6Multimedia-doc
Summary:	Qt6 Multimedia documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Multimedia w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Multimedia-doc
Qt6 Multimedia documentation in HTML format.

%description -n Qt6Multimedia-doc -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Multimedia w formacie HTML.

%package -n Qt6Multimedia-doc-qch
Summary:	Qt6 Multimedia documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Multimedia w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Multimedia-doc-qch
Qt6 Multimedia documentation in QCH format.

%description -n Qt6Multimedia-doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Multimedia w formacie QCH.

%package -n Qt6MultimediaQuick
Summary:	Qt6 Multimedia Quick library and modules
Summary(pl.UTF-8):	Biblioteka i moduły Qt6 Multimedia Quick
Group:		X11/Libraries
Requires:	Qt6Multimedia = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	pulseaudio-devel >= 0.9.11

%description -n Qt6MultimediaQuick
Qt6 Multimedia Quick library and modules.

%description -n Qt6MultimediaQuick -l pl.UTF-8
Biblioteka i moduły Qt6 Multimedia Quick.

%package -n Qt6MultimediaQuick-devel
Summary:	Qt6 Multimedia Quick library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Multimedia Quick - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Multimedia-devel = %{version}
Requires:	Qt6MultimediaQuick = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick-devel = %{version}

%description -n Qt6MultimediaQuick-devel
Qt6 Multimedia Quick library - development files.

%description -n Qt6MultimediaQuick-devel -l pl.UTF-8
Biblioteka Qt6 Multimedia Quick - pliki programistyczne.

%package -n Qt6MultimediaWidgets
Summary:	Qt6 Multimedia Widgets library
Summary(pl.UTF-8):	Biblioteka Qt6 Multimedia Widgets
Group:		X11/Libraries
Requires:	Qt6Multimedia = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6MultimediaWidgets
Qt6 Multimedia Widgets library provides widgets classes for Qt6
Multimedia.

%description -n Qt6MultimediaWidgets -l pl.UTF-8
Biblioteka Qt6 Multimedia Widgets dostarcza klasy widgetów dla
biblioteki Qt6 Multimedia.

%package -n Qt6MultimediaWidgets-devel
Summary:	Qt6 Multimedia Widgets library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Multimedia Widgets - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Multimedia-devel = %{version}
Requires:	Qt6MultimediaWidgets = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6MultimediaWidgets-devel
Qt6 Multimedia Widgets library - development files.

%description -n Qt6MultimediaWidgets-devel -l pl.UTF-8
Biblioteka Qt6 Multimedia Widgets - pliki programistyczne.

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
%requires_ge openssl-devel

%description -n Qt6Network-devel
Header files for Qt6 Network library.

%description -n Qt6Network-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki Qt6 Network.

%package -n Qt6NetworkAuth
Summary:	The Qt6 Network Auth library
Summary(pl.UTF-8):	Biblioteka Qt6 Network Auth
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6NetworkAuth
Qt6 Network Auth library provides classes for network authentication.

%description -n Qt6NetworkAuth -l pl.UTF-8
Biblioteka Qt6 Network Auth dostarcza klasy do uwierzytelniania w
sieci.

%package -n Qt6NetworkAuth-devel
Summary:	Qt6 Network Auth library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Network Auth - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6NetworkAuth = %{version}

%description -n Qt6NetworkAuth-devel
Qt6 Network Auth library - development files.

%description -n Qt6NetworkAuth-devel -l pl.UTF-8
Biblioteka Qt6 NetworkAuth - pliki programistyczne.

%package -n Qt6NetworkAuth-doc
Summary:	Qt6 Network Auth documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Network Auth w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6NetworkAuth-doc
Qt6 Network Auth documentation in HTML format.

%description -n Qt6NetworkAuth-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Netwok Auth w formacie HTML.

%package -n Qt6NetworkAuth-doc-qch
Summary:	Qt6 Network Auth documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Network Auth w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6NetworkAuth-doc-qch
Qt6 Network Auth documentation in QCH format.

%description -n Qt6NetworkAuth-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Network Auth w formacie QCH.

%package -n Qt6Nfc
Summary:	Qt6 Nfc library
Summary(pl.UTF-8):	Biblioteka Qt6 Nfc
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}

%description -n Qt6Nfc
Qt6 Nfc library provides classes to access NFC Forum Tags.

%description -n Qt6Nfc -l pl.UTF-8
Biblioteka Qt6 Nfc dostarcza klasy służace do dostępu do urządzeń NFC
Forum.

%package -n Qt6Nfc-devel
Summary:	The Qt6 Nfc - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Nfc - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus-devel = %{version}
Requires:	Qt6Nfc = %{version}

%description -n Qt6Nfc-devel
The Qt6 Nfc - development files.

%description -n Qt6Nfc-devel -l pl.UTF-8
Biblioteka Qt6 Nfc - pliki programistyczne.

%package -n Qt6Nfc-doc
Summary:	Qt6 Nfc documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Nfc w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Nfc-doc
Qt6 Nfc documentation in HTML format.

%description -n Qt6Nfc-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Nfc w formacie HTML.

%package -n Qt6Nfc-doc-qch
Summary:	Qt6 Nfc documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Nfc w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Nfc-doc-qch
Qt6 Nfc documentation in QCH format.

%description -n Qt6Nfc-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Nfc w formacie QCH.

%package -n Qt6OpcUa
Summary:	The Qt6 OpcUa library
Summary(pl.UTF-8):	Biblioteka Qt6 OpcUa
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6OpcUa
Qt OpcUa module implements OPC UA connectivity through a Qt API.

%description -n Qt6OpcUa -l pl.UTF-8
Moduł Qt OpcUa implementuje łączność OPC UA poprzez API Qt.

%package -n Qt6OpcUa-devel
Summary:	Qt6 OpcUa library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 OpcUa - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6OpcUa = %{version}

%description -n Qt6OpcUa-devel
Qt6 OpcUa library - development files.

%description -n Qt6OpcUa-devel -l pl.UTF-8
Biblioteka Qt6 OpcUa - pliki programistyczne.

%package -n Qt6OpcUa-doc
Summary:	Qt6 OpcUa documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 OpcUa w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6OpcUa-doc
Qt6 OpcUa documentation in HTML format.

%description -n Qt6OpcUa-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 OpcUa w formacie HTML.

%package -n Qt6OpcUa-doc-qch
Summary:	Qt6 OpcUa documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 OpcUa w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6OpcUa-doc-qch
Qt6 OpcUa documentation in QCH format.

%description -n Qt6OpcUa-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 OpcUa w formacie QCH.

%package -n Qt6OpenGL
Summary:	Qt6 OpenGL library
Summary(pl.UTF-8):	Biblioteka Qt6 OpenGL
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6OpenGL
The Qt6 OpenGL library offers classes that make it easy to use OpenGL
in Qt 6 applications.

%description -n Qt6OpenGL -l pl.UTF-8
Biblioteka Qt6 OpenGL oferuje klasy ułatwiające wykorzystywanie
OpenGL-a w aplikacjach Qt 6.

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

%package -n Qt6Pdf
Summary:	The Qt6 Pdf library
Summary(pl.UTF-8):	Biblioteka Qt6 Pdf
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Pdf
Qt6 Pdf module contains classes and functions for rendering PDF
documents.

%description -n Qt6Pdf -l pl.UTF-8
Moduł Qt6 Pdf zawiera klasy i funkcje do renderowania dokumentów PDF.

%package -n Qt6Pdf-devel
Summary:	Qt6 Pdf library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Pdf - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Pdf = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6Pdf-devel
Qt6 Pdf library - development files.

%description -n Qt6Pdf-devel -l pl.UTF-8
Biblioteka Qt6 Pdf - pliki programistyczne.

%package -n Qt6Pdf-doc
Summary:	Qt6 Pdf documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Pdf w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Pdf-doc
Qt6 Pdf documentation in HTML format.

%description -n Qt6Pdf-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Pdf w formacie HTML.

%package -n Qt6Pdf-doc-qch
Summary:	Qt6 Pdf documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Pdf w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Pdf-doc-qch
Qt6 Pdf documentation in QCH format.

%description -n Qt6Pdf-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Pdf w formacie QCH.

%package -n Qt6Designer-plugin-qwebengineview
Summary:	QWebEngineView plugin for Qt6 Designer
Summary(pl.UTF-8):	Wtyczka QWebEngineView dla Qt6 Designera
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Designer = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6WebEngine = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Designer-plugin-qwebengineview
QWebEngineView plugin for Qt6 Designer.

%description -n Qt6Designer-plugin-qwebengineview -l pl.UTF-8
Wtyczka QWebEngineView dla Qt6 Designera.

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

%package -n Qt6Qt5Compat
Summary:	Qt6 Qt5Compat libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Qt5Compat
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Qt5Compat
Qt6 Qt5Compat libraries.

%package -n Qt6Qt5Compat-devel
Summary:	Qt6 Qt5Compat libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Qt5Compat - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}

%description -n Qt6Qt5Compat-devel
Qt6 Qt5Compat libraries - development files.

%description -n Qt6Qt5Compat-devel -l pl.UTF-8
Biblioteki Qt6 Qt5Compat - pliki programistyczne.

%package -n Qt6Qt5Compat-doc
Summary:	Qt6 Qt5Compat documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Qt5Compat w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Qt5Compat-doc
Qt6 Qt5Compat documentation in HTML format.

%description -n Qt6Qt5Compat-doc -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Qt5Compat w formacie HTML.

%package -n Qt6Qt5Compat-doc-qch
Summary:	Qt6 Qt5Compat documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Qt5Compat w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Qt5Compat-doc-qch
Qt6 Qt5Compat documentation in QCH format.

%description -n Qt6Qt5Compat-doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Qt5Compat w formacie QCH.

%package -n Qt6Qml
Summary:	Qt6 Qml libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Qml
Group:		Libraries
# Qt6Qml: Core Network
# Qt6QmlModels: Core Qml
# Qt6QmlWorkerScript: Core Network Qml
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6Qml
The Qt6 QML module provides a framework for developing applications
and libraries with the QML language. It defines and implements the
language and engine infrastructure, and provides an API to enable
application developers to extend the QML language with custom types
and integrate QML code with JavaScript and C++. The Qt6 QML module
provides both a QML API and a C++ API.

%description -n Qt6Qml -l pl.UTF-8
Moduł Qt6 Qml dostarcza szkielet do tworzenia aplikacji i bibliotek
przy użyciu języka QML. Moduł definiuje i implementuje język oraz
silnik, a także udostąpnia API pozwalające programistom rozszerzać
język QML o własne typy oraz integrować kod w języku QML z
JavaScriptem i C++. Moduł Qt6 QML udostępnia API zarówno dla języka
QML, jak i C++.

%package -n Qt6Qml-devel
Summary:	Qt6 Qml libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Qml - pliki programistyczne
Group:		Development/Libraries
# Qt6Qml: Core Network
# Qt6QmlModels: Core Network Qml
# Qt6QmlWorkerScript: Core Network Qml
# Qt6PacketProtocol.a: Core
# Qt6QmlDebug.a: Core Network PacketProtocol Qml
# Qt6QmlDevTools.a: Core
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6Qml-devel
Qt6 Qml libraries - development files.

%description -n Qt6Qml-devel -l pl.UTF-8
Biblioteki Qt6 Qml - pliki programistyczne.

%package -n Qt6Qml-doc
Summary:	Qt6 Declarative documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Declarative w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Qml-doc
Qt6 Declarative documentation in HTML format.

%description -n Qt6Qml-doc -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Declarative w formacie HTML.

%package -n Qt6Qml-doc-qch
Summary:	Qt6 Declarative documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Declarative w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Qml-doc-qch
Qt6 Declarative documentation in QCH format.

%description -n Qt6Qml-doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Declarative w formacie QCH.

%package -n Qt6Quick
Summary:	Qt6 Quick libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Quick
Group:		X11/Libraries
# Qt6Quick: Core Gui Network Qml QmlModels
# Qt6QuickParticles: Core Gui Qml Quick GL
# Qt6QuickShapes: Core Gui Qml Quick
# Qt6QuickTest: Core Gui Qml Quick Test Widgets
# Qt6QuickWidgets: Core Gui Qml Quick Widgets
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Test = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Quick
The Qt6 Quick module is the standard library for writing QML
applications. While the Qt6 QML module provides the QML engine and
language infrastructure, the Qt6 Quick module provides all the basic
types necessary for creating user interfaces with QML. It provides a
visual canvas and includes types for creating and animating visual
components, receiving user input, creating data models and views and
delayed object instantiation.

The Qt6 Quick module provides both a QML API which supplies QML types
for creating user interfaces with the QML language, and a C++ API for
extending QML applications with C++ code.

%description -n Qt6Quick -l pl.UTF-8
Moduł Qt6 Quick to biblioteka standardowa do pisania aplikacji QML.
Sam moduł Qt6 QML dostarcza silnik i infrastrukturę języka, natomiast
moduł Qt6 Quick udostępnia wszystkie podstawowe typy niezbędne do
tworzenia interfejsu użytkownika przy użyciu języka QML. Udostępnia
graficzne "płótno", zawiera typy do tworzenia i animowania komponentów
graficznych, odczytu wejścia od użytkownika, tworzenia modeli i
widoków danych oraz opóźnionych instancji obiektów.

Moduł Qt6 Quick dostarcza API zarówno dla języka QML, zapewniające
typy QML do tworzenia interfejsów użytkownika w języku QML, jak i dla
języka C++ do rozszerzania aplikacji QML przy użyciu kodu w C++.

%package -n Qt6Quick-devel
Summary:	Qt6 Qml libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Qml - pliki programistyczne
Group:		X11/Development/Libraries
# Qt6Quick: Core Gui Network Qml QmlModels
# Qt6QuickParticles: Core Gui Network Qml QmlModels Quick
# Qt6QuickShapes: Core Gui Network Qml QmlModels Quick
# Qt6QuickTest: Core Gui Test Widgets
# Qt6QuickWidgets: Core Gui Network Qml QmlModels Quick Test Widgets
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Widgets-devel = %{version}
Requires:	qt6-qtdeclarative = %{version}

%description -n Qt6Quick-devel
Qt6 Qml libraries - development files.

%description -n Qt6Quick-devel -l pl.UTF-8
Biblioteki Qt6 Qml - pliki programistyczne.

%package -n Qt6Quick-doc
Summary:	Qt6 Declarative documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Declarative w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick-doc
Qt6 Declarative documentation in HTML format.

%description -n Qt6Quick-doc -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Declarative w formacie HTML.

%package -n Qt6Quick-doc-qch
Summary:	Qt6 Declarative documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Declarative w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick-doc-qch
Qt6 Declarative documentation in QCH format.

%description -n Qt6Quick-doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Declarative w formacie QCH.

%package -n Qt6Quick3D
Summary:	The Qt6 Quick3D library
Summary(pl.UTF-8):	Biblioteka Qt6 Quick3D
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	assimp >= 5.0.0

%description -n Qt6Quick3D
Qt6 Quick3D libraries.

%description -n Qt6Quick3D -l pl.UTF-8
Biblioteki Qt6 Quick3D.

%package -n Qt6Quick3D-devel
Summary:	Qt6 Quick3D - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Quick3D - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Quick3D = %{version}

%description -n Qt6Quick3D-devel
Qt6 Quick3D - development files.

%description -n Qt6Quick3D-devel -l pl.UTF-8
Biblioteka Qt6 Quick3D - pliki programistyczne.

%package -n Qt6Quick3D-doc
Summary:	Qt6 Quick3D documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Quick3D w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick3D-doc
Qt6 Quick3D documentation in HTML format.

%description -n Qt6Quick3D-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Quick3D w formacie HTML.

%package -n Qt6Quick3D-doc-qch
Summary:	Qt6 Quick3D documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Quick3D w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick3D-doc-qch
Qt6 Quick3D documentation in QCH format.

%description -n Qt6Quick3D-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Quick3D w formacie QCH.

%package -n Qt6Quick-Timeline
Summary:	The Qt6 Quick Timeline module
Summary(pl.UTF-8):	Moduł Qt6 Quick Timeline
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Quick-Timeline
Qt6 Quick Timeline module.

%description -n Qt6Quick-Timeline -l pl.UTF-8
Moduł Qt6 Quick Timeline.

%package -n Qt6Quick-Timeline-doc
Summary:	Qt6 Quick Timeline module documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do modułu Qt6 Quick Timeline w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick-Timeline-doc
Qt6 Quick Timeline module documentation in HTML format.

%description -n Qt6Quick-Timeline-doc -l pl.UTF-8
Dokumentacja do modułu Qt6 Quick Timeline w formacie HTML.

%package -n Qt6Quick-Timeline-doc-qch
Summary:	Qt6 Quick Timeline module documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do modułu Qt6 Quick Timeline w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Quick-Timeline-doc-qch
Qt6 Quick Timeline module documentation in QCH format.

%description -n Qt6Quick-Timeline-doc-qch -l pl.UTF-8
Dokumentacja do modułu Qt6 Quick Timeline w formacie QCH.

%package -n Qt6RemoteObjects
Summary:	The Qt6 RemoteObjects library
Summary(pl.UTF-8):	Biblioteka Qt6 RemoteObjects
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6RemoteObjects
Qt6 RemoteObjects library.

%description -n Qt6RemoteObjects -l pl.UTF-8
Biblioteka Qt6 RemoteObjects.

%package -n Qt6RemoteObjects-devel
Summary:	Qt6 RemoteObjects - development files
Summary(pl.UTF-8):	Biblioteka Qt6 RemoteObjects - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6RemoteObjects = %{version}

%description -n Qt6RemoteObjects-devel
Qt6 RemoteObjects - development files.

%description -n Qt6RemoteObjects-devel -l pl.UTF-8
Biblioteka Qt6 RemoteObjects - pliki programistyczne.

%package -n Qt6RemoteObjects-doc
Summary:	Qt6 RemoteObjects documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 RemoteObjects w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6RemoteObjects-doc
Qt6 RemoteObjects documentation in HTML format.

%description -n Qt6RemoteObjects-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 RemoteObjects w formacie HTML.

%package -n Qt6RemoteObjects-doc-qch
Summary:	Qt6 RemoteObjects documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 RemoteObjects w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6RemoteObjects-doc-qch
Qt6 RemoteObjects documentation in QCH format.

%description -n Qt6RemoteObjects-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 RemoteObjects w formacie QCH.

%package -n Qt6Scxml
Summary:	The Qt6 Scxml library
Summary(pl.UTF-8):	Biblioteka Qt6 Scxml
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6Scxml
Qt6 Scxml library.

%description -n Qt6Scxml -l pl.UTF-8
Biblioteka Qt6 Scxml.

%package -n Qt6Scxml-devel
Summary:	Qt6 Scxml - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Scxml - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Scxml = %{version}

%description -n Qt6Scxml-devel
Qt6 Scxml - development files.

%description -n Qt6Scxml-devel -l pl.UTF-8
Biblioteka Qt6 Scxml - pliki programistyczne.

%package -n Qt6Scxml-doc
Summary:	Qt6 Scxml documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Scxml w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Scxml-doc
Qt6 Scxml documentation in HTML format.

%description -n Qt6Scxml-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Scxml w formacie HTML.

%package -n Qt6Scxml-doc-qch
Summary:	Qt6 Scxml documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Scxml w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Scxml-doc-qch
Qt6 Scxml documentation in QCH format.

%description -n Qt6Scxml-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Scxml w formacie QCH.

%package -n Qt6Sensors
Summary:	The Qt6 Sensors library
Summary(pl.UTF-8):	Biblioteka Qt6 Sensors
Group:		Libraries
Requires:	Qt6Bluetooth = %{version}
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6Sensors
Qt6 Sensors library provides classes for reading sensor data.

%description -n Qt6Sensors -l pl.UTF-8
Biblioteka Qt6 Sensors dostarcza klasy do odczytu danych z czujników.

%package -n Qt6Sensors-devel
Summary:	Qt6 Sensors library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Sensors - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Sensors = %{version}

%description -n Qt6Sensors-devel
Qt6 Sensors library - development files.

%description -n Qt6Sensors-devel -l pl.UTF-8
Biblioteka Qt6 Sensors - pliki programistyczne.

%package -n Qt6Sensors-doc
Summary:	Qt6 Sensors documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Sensors w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Sensors-doc
Qt6 Sensors documentation in HTML format.

%description -n Qt6Sensors-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Sensors w formacie HTML.

%package -n Qt6Sensors-doc-qch
Summary:	Qt6 Sensors documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Sensors w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Sensors-doc-qch
Qt6 Sensors documentation in QCH format.

%description -n Qt6Sensors-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Sensors w formacie QCH.

%package -n Qt6SerialBus
Summary:	The Qt6 SerialBus library
Summary(pl.UTF-8):	Biblioteka Qt6 SerialBus
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}

%description -n Qt6SerialBus
Qt6 SerialBus library.

%description -n Qt6SerialBus -l pl.UTF-8
Biblioteka Qt6 SerialBus.

%package -n Qt6SerialBus-devel
Summary:	Qt6 SerialBus - development files
Summary(pl.UTF-8):	Biblioteka Qt6 SerialBus - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6SerialBus = %{version}

%description -n Qt6SerialBus-devel
Qt6 SerialBus - development files.

%description -n Qt6SerialBus-devel -l pl.UTF-8
Biblioteka Qt6 SerialBus - pliki programistyczne.

%package -n Qt6SerialBus-doc
Summary:	Qt6 SerialBus documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 SerialBus w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6SerialBus-doc
Qt6 SerialBus documentation in HTML format.

%description -n Qt6SerialBus-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 SerialBus w formacie HTML.

%package -n Qt6SerialBus-doc-qch
Summary:	Qt6 SerialBus documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 SerialBus w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6SerialBus-doc-qch
Qt6 SerialBus documentation in QCH format.

%description -n Qt6SerialBus-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 SerialBus w formacie QCH.

%package -n Qt6SerialPort
Summary:	The Qt6 SerialPort library
Summary(pl.UTF-8):	Biblioteka Qt6 SerialPort
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6SerialPort
Qt6 SerialPort library provides classes that enable access to a serial
port.

%description -n Qt6SerialPort -l pl.UTF-8
Biblioteka Qt6 SerialPort udostępnia klasy pozwalające na dostęp do
portu szeregowego.

%package -n Qt6SerialPort-devel
Summary:	Qt6 SerialPort library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 SerialPort - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6SerialPort = %{version}
Requires:	udev-devel

%description -n Qt6SerialPort-devel
Qt6 SerialPort library - development files.

%description -n Qt6SerialPort-devel -l pl.UTF-8
Biblioteka Qt6 SerialPort - pliki programistyczne.

%package -n Qt6SerialPort-doc
Summary:	Qt6 SerialPort documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 SerialPort w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6SerialPort-doc
Qt6 SerialPort documentation in HTML format.

%description -n Qt6SerialPort-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 SerialPort w formacie HTML.

%package -n Qt6SerialPort-doc-qch
Summary:	Qt6 SerialPort documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 SerialPort w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6SerialPort-doc-qch
Qt6 SerialPort documentation in QCH format.

%description -n Qt6SerialPort-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 SerialPort w formacie QCH.

%package -n qt6-shadertools
Summary:	The Qt6 ShaderTools library comman line tools
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6ShaderTools = %{version}

%description -n qt6-shadertools
The Qt6 ShaderTools library comman line tools.

%package -n Qt6ShaderTools
Summary:	The Qt6 ShaderTools library
Summary(pl.UTF-8):	Biblioteka Qt6 ShaderTools
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6ShaderTools
The Qt Shader Tools module builds on the SPIR-V Open Source Ecosystem
as described at the Khronos SPIR-V web site https://www.khronos.org/spir/

%package -n Qt6ShaderTools-devel
Summary:	Qt6 ShaderTools library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 ShaderTools - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6ShaderTools = %{version}

%description -n Qt6ShaderTools-devel
Qt6 ShaderTools library - development files.

%description -n Qt6ShaderTools-devel -l pl.UTF-8
Biblioteka Qt6 ShaderTools - pliki programistyczne.

%package -n Qt6ShaderTools-doc
Summary:	Qt6 ShaderTools documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 ShaderTools w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6ShaderTools-doc
Qt6 ShaderTools documentation in HTML format.

%description -n Qt6ShaderTools-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 ShaderTools w formacie HTML.

%package -n Qt6ShaderTools-doc-qch
Summary:	Qt6 ShaderTools documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 ShaderTools w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6ShaderTools-doc-qch
Qt6 ShaderTools documentation in QCH format.

%description -n Qt6ShaderTools-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 ShaderTools w formacie QCH.

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

%package -n Qt6Svg
Summary:	The Qt6 Svg library
Summary(pl.UTF-8):	Biblioteka Qt6 Svg
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Svg
Qt6 Svg library provides functionality for handling SVG images.

%description -n Qt6Svg -l pl.UTF-8
Biblioteka Qt6 Svg udostępnia obsługę obrazów SVG.

%package -n Qt6Svg-devel
Summary:	Qt6 Svg library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Svg - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Svg = %{version}
Requires:	Qt6Widgets-devel = %{version}
Requires:	zlib-devel

%description -n Qt6Svg-devel
Qt6 Svg library - development files.

%description -n Qt6Svg-devel -l pl.UTF-8
Biblioteka Qt6 Svg - pliki programistyczne.

%package -n Qt6Svg-doc
Summary:	Qt6 Svg documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Svg w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Svg-doc
Qt6 Svg documentation in HTML format.

%description -n Qt6Svg-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Svg w formacie HTML.

%package -n Qt6Svg-doc-qch
Summary:	Qt6 Svg documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Svg w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Svg-doc-qch
Qt6 Svg documentation in QCH format.

%description -n Qt6Svg-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Svg w formacie QCH.

%package -n Qt6Test
Summary:	Qt6 Test library
Summary(pl.UTF-8):	Biblioteka Qt6 Test
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Test
The Qt6 Test library provides classes for unit testing Qt 6
applications and libraries.

%description -n Qt6Test -l pl.UTF-8
Biblioteka Qt6 Test udostępnia klasy do testów jednostkowych aplikacji
oraz bibliotek Qt 6.

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

%package -n Qt6UiTools
Summary:	Qt6 Ui Tools library
Summary(pl.UTF-8):	Biblioteka Qt6 Ui Tools
Group:		X11/Development/Libraries
Requires:	OpenGL
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6UiTools
Qt6 Ui Tools library provides classes to handle forms created with Qt
Designer.

%description -n Qt6UiTools -l pl.UTF-8
Biblioteka Qt6 Ui Tools dostarcza klasy do obsługi formularzy
utworzonych przy użyciu Qt Designera.

%package -n Qt6UiTools-devel
Summary:	Qt6 Ui Tools library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Ui Tools - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6UiTools = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6UiTools-devel
Header files and static Qt6 Ui Tools library.

Qt6 Ui Tools library provides classes to handle forms created with Qt
Designer.

%description -n Qt6UiTools-devel -l pl.UTF-8
Pliki nagłówkowe i statyczna biblioteka Qt6 Ui Tools.

Biblioteka Qt6 Ui Tools dostarcza klasy do obsługi formularzy
utworzonych przy użyciu Qt Designera.

%package -n Qt6VirtualKeyboard
Summary:	The Qt6 VirtualKeyboard library
Summary(pl.UTF-8):	Biblioteka Qt6 VirtualKeyboard
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6VirtualKeyboard
Qt6 VirtualKeyboard library.

%description -n Qt6VirtualKeyboard -l pl.UTF-8
Biblioteka Qt6 VirtualKeyboard.

%package -n Qt6VirtualKeyboard-devel
Summary:	Qt6 VirtualKeyboard - development files
Summary(pl.UTF-8):	Biblioteka Qt6 VirtualKeyboard - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick-devel = %{version}
Requires:	Qt6VirtualKeyboard = %{version}

%description -n Qt6VirtualKeyboard-devel
Qt6 VirtualKeyboard - development files.

%description -n Qt6VirtualKeyboard-devel -l pl.UTF-8
Biblioteka Qt6 VirtualKeyboard - pliki programistyczne.

%package -n Qt6VirtualKeyboard-doc
Summary:	Qt6 VirtualKeyboard documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 VirtualKeyboard w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6VirtualKeyboard-doc
Qt6 VirtualKeyboard documentation in HTML format.

%description -n Qt6VirtualKeyboard-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 VirtualKeyboard w formacie HTML.

%package -n Qt6VirtualKeyboard-doc-qch
Summary:	Qt6 VirtualKeyboard documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 VirtualKeyboard w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6VirtualKeyboard-doc-qch
Qt6 VirtualKeyboard documentation in QCH format.

%description -n Qt6VirtualKeyboard-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 VirtualKeyboard w formacie QCH.

%package -n Qt6WaylandCompositor
Summary:	The Qt6 WaylandCompositor library
Summary(pl.UTF-8):	Biblioteka Qt6 WaylandCompositor
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	wayland >= 1.4.0
Requires:	xorg-lib-libxkbcommon >= 0.2.0

%description -n Qt6WaylandCompositor
Qt6 WaylandCompositor library enables the creation of Wayland
compositors using Qt and QtQuick.

%description -n Qt6WaylandCompositor -l pl.UTF-8
Biblioteka Qt6 WaylandCompositor pozwala na tworzenie kompozytorów
Wayland przy użyciu bibliotek Qt i QtQuick.

%package -n Qt6WaylandCompositor-devel
Summary:	Qt6 WaylandCompositor library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WaylandCompositor - pliki programistyczne
Group:		Development/Libraries
Requires:	OpenGL-devel
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick-devel = %{version}
Requires:	Qt6WaylandCompositor = %{version}
Requires:	wayland-devel >= 1.4.0
Requires:	xorg-lib-libxkbcommon-devel >= 0.2.0

%description -n Qt6WaylandCompositor-devel
Qt6 WaylandCompositor library - development files.

%description -n Qt6WaylandCompositor-devel -l pl.UTF-8
Biblioteka Qt6 WaylandCompositor - pliki programistyczne.

%package -n Qt6WaylandCompositor-doc
Summary:	Qt6 Wayland documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Wayland w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WaylandCompositor-doc
Qt6 Wayland documentation in HTML format.

%description -n Qt6WaylandCompositor-doc -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Wayland w formacie HTML.

%package -n Qt6WaylandCompositor-doc-qch
Summary:	Qt6 Wayland documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do bibliotek Qt6 Wayland w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WaylandCompositor-doc-qch
Qt6 Wayland documentation in QCH format.

%description -n Qt6WaylandCompositor-doc-qch -l pl.UTF-8
Dokumentacja do bibliotek Qt6 Wayland w formacie QCH.

%package -n Qt6WaylandClient
Summary:	The Qt6 WaylandClient library
Summary(pl.UTF-8):	Biblioteka Qt6 WaylandClient
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}
Requires:	Qt6Gui = %{version}
Requires:	wayland >= 1.4.0
Requires:	xorg-lib-libxkbcommon >= 0.2.0

%description -n Qt6WaylandClient
Qt6 WaylandClient library enables Qt applications to be run as Wayland
clients.

%description -n Qt6WaylandClient -l pl.UTF-8
Biblioteka Qt6 WaylandClient pozwala na uruchamianie aplikacji Qt jako
klientów Wayland.

%package -n Qt6WaylandClient-devel
Summary:	Qt6 WaylandClient library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WaylandClient - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6PlatformCompositorSupport-devel = %{version}
Requires:	Qt6WaylandClient = %{version}
Requires:	wayland-devel >= 1.4.0
Requires:	xorg-lib-libxkbcommon-devel >= 0.2.0

%description -n Qt6WaylandClient-devel
Qt6 WaylandClient library - development files.

%description -n Qt6WaylandClient-devel -l pl.UTF-8
Biblioteka Qt6 WaylandClient - pliki programistyczne.

%package -n Qt6WebChannel
Summary:	The Qt6 WebChannel library
Summary(pl.UTF-8):	Biblioteka Qt6 WebChannel
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6WebChannel
Qt6 WebChannel library provides seamless integration of C++ and QML
applications with HTML/JavaScript clients.

%description -n Qt6WebChannel -l pl.UTF-8
Biblioteka Qt6 WebChannel udostępnia integrację aplikacji C++ i QML z
klientami w HTML-u/JavaScripcie.

%package -n Qt6WebChannel-devel
Summary:	Qt6 WebChannel library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WebChannel - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6WebChannel = %{version}

%description -n Qt6WebChannel-devel
Qt6 WebChannel library - development files.

%description -n Qt6WebChannel-devel -l pl.UTF-8
Biblioteka Qt6 WebChannel - pliki programistyczne.

%package -n Qt6WebChannel-doc
Summary:	Qt6 WebChannel documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebChannel w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebChannel-doc
Qt6 WebChannel documentation in HTML format.

%description -n Qt6WebChannel-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebChannel w formacie HTML.

%package -n Qt6WebChannel-doc-qch
Summary:	Qt6 WebChannel documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebChannel w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebChannel-doc-qch
Qt6 WebChannel documentation in QCH format.

%description -n Qt6WebChannel-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebChannel w formacie QCH.

%package -n Qt6WebEngine
Summary:	The Qt6 WebEngine library
Summary(pl.UTF-8):	Biblioteka Qt6 WebEngine
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6WebChannel = %{version}
Requires:	alsa-lib >= 1.0.10
Requires:	freetype >= 1:2.4.2
Requires:	harfbuzz >= 3.0.0
Requires:	harfbuzz-subset >= 3.0.0
Requires:	libicu >= 65
Requires:	libpng >= 2:1.6.0
Requires:	libvpx >= 1.8.0
Requires:	nss >= 3.26
Requires:	opus >= 1.3.1
Requires:	pulseaudio-libs >= 0.9.10

%description -n Qt6WebEngine
Qt6 WebEngine library provides seamless integration of C++ and QML
applications with HTML/JavaScript clients.

%description -n Qt6WebEngine -l pl.UTF-8
Biblioteka Qt6 WebEngine udostępnia integrację aplikacji C++ i QML z
klientami w HTML-u/JavaScripcie.

%package -n Qt6WebEngine-devel
Summary:	Qt6 WebEngine library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WebEngine - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6PrintSupport-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick-devel = %{version}
Requires:	Qt6WebChannel-devel = %{version}
Requires:	Qt6WebEngine = %{version}
Requires:	Qt6Widgets-devel = %{version}

%description -n Qt6WebEngine-devel
Qt6 WebEngine library - development files.

%description -n Qt6WebEngine-devel -l pl.UTF-8
Biblioteka Qt6 WebEngine - pliki programistyczne.

%package -n Qt6WebEngine-doc
Summary:	Qt6 WebEngine documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebEngine w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebEngine-doc
Qt6 WebEngine documentation in HTML format.

%description -n Qt6WebEngine-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebEngine w formacie HTML.

%package -n Qt6WebEngine-doc-qch
Summary:	Qt6 WebEngine documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebEngine w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebEngine-doc-qch
Qt6 WebEngine documentation in QCH format.

%description -n Qt6WebEngine-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebEngine w formacie QCH.

%package -n Qt6WebSockets
Summary:	The Qt6 WebSockets library
Summary(pl.UTF-8):	Biblioteka Qt6 WebSockets
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
# for qml module
Requires:	Qt6Qml = %{version}

%description -n Qt6WebSockets
Qt6 WebSockets library provides WebSockets communication classes.

%description -n Qt6WebSockets -l pl.UTF-8
Biblioteka Qt6 WebSockets dostarcza klasy do komunikacji przez
WebSockets.

%package -n Qt6WebSockets-devel
Summary:	Qt6 WebSockets library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WebSockets - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6WebSockets = %{version}

%description -n Qt6WebSockets-devel
Qt6 WebSockets library - development files.

%description -n Qt6WebSockets-devel -l pl.UTF-8
Biblioteka Qt6 WebSockets - pliki programistyczne.

%package -n Qt6WebSockets-doc
Summary:	Qt6 WebSockets documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebSockets w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebSockets-doc
Qt6 WebSockets documentation in HTML format.

%description -n Qt6WebSockets-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebSockets w formacie HTML.

%package -n Qt6WebSockets-doc-qch
Summary:	Qt6 WebSockets documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebSockets w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebSockets-doc-qch
Qt6 WebSockets documentation in QCH format.

%description -n Qt6WebSockets-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebSockets w formacie QCH.

%package -n Qt6WebView
Summary:	The Qt6 WebView library
Summary(pl.UTF-8):	Biblioteka Qt6 WebView
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6WebView
Qt6 WebView library.

%description -n Qt6WebView -l pl.UTF-8
Biblioteka Qt6 WebView.

%package -n Qt6WebView-devel
Summary:	Qt6 WebView - development files
Summary(pl.UTF-8):	Biblioteka Qt6 WebView - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6WebView = %{version}

%description -n Qt6WebView-devel
Qt6 WebView - development files.

%description -n Qt6WebView-devel -l pl.UTF-8
Biblioteka Qt6 WebView - pliki programistyczne.

%package -n Qt6WebView-plugin-webengine
Summary:	Qt6 WebView library WebEngine plugin
Summary(pl.UTF-8):	Wtyczka WebEngine do biblioteki Qt6 WebView
Group:		X11/Libraries
Requires:	Qt6WebEngine = %{version}
Requires:	Qt6WebView = %{version}

%description -n Qt6WebView-plugin-webengine
Qt6 WebView library WebEngine plugin.

%description -n Qt6WebView-plugin-webengine -l pl.UTF-8
Wtyczka WebEngine do biblioteki Qt6 WebView.

%package -n Qt6WebView-doc
Summary:	Qt6 WebView documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebView w formacie HTML
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebView-doc
Qt6 WebView documentation in HTML format.

%description -n Qt6WebView-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebView w formacie HTML.

%package -n Qt6WebView-doc-qch
Summary:	Qt6 WebView documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 WebView w formacie QCH
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6WebView-doc-qch
Qt6 WebView documentation in QCH format.

%description -n Qt6WebView-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 WebView w formacie QCH.

%package -n Qt6Widgets
Summary:	Qt6 Widgets library
Summary(pl.UTF-8):	Biblioteka Qt6 Widgets
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}

%description -n Qt6Widgets
The Qt6 Widgets library extends Qt 6 GUI with C++ widget
functionality.

%description -n Qt6Widgets -l pl.UTF-8
Biblioteka Qt6 Widgets rozszerza graficzny interfejs Qt 6 o
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
Provides:	qt6-qmake = %{version}-%{release}

%description -n qt6-build
This package includes the Qt resource compiler (rcc), meta objects
compiler (moc), user interface compiler (uic) etc.

%description -n qt6-build -l pl.UTF-8
Ten pakiet zawiera kompilator zasobów Qt (rcc), kompilator
metaobiektów (moc), kompilator interfejsów użytkownika (uic) i podobne
narzędzia.

%prep
%setup -q -n qt-everywhere-src-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
	qtbase/mkspecs/features/uikit/devices.py \
	qtbase/util/testrunner/qt-testrunner.py

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+perl(\s|$),#!%{__perl}\1,' \
	qtbase/libexec/syncqt.pl

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+node(\s|$),#!/usr/bin/node\1,' \
	qtwebchannel/examples/webchannel/qwclient/qwclient.js

%if %(echo %{cxx_version} | cut -d. -f1) < 9
# available since gcc 9
%{__sed} -i -e '/-Wdeprecated-copy/d' \
	qtwebengine/src/3rdparty/chromium/third_party/{angle,dawn/src/common,pdfium,skia/gn/skia}/BUILD.gn \
	qtwebengine/src/3rdparty/chromium/third_party/swiftshader/CMakeLists.txt
%endif

%build
# We're using samurai instead of ninja because teh later
# cannot be told what command line flags to use globally
mkdir -p build
cd build
%cmake ../ \
	-GNinja \
	%{cmake_on_off webengine BUILD_qtwebengine} \
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
	-DQT_BUILD_EXAMPLES=OFF \
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
	-DQT_FEATURE_webengine_proprietary_codecs=ON \
	-DQT_FEATURE_webengine_system_alsa=ON \
	-DQT_FEATURE_webengine_system_ffmpeg=ON \
	-DQT_FEATURE_webengine_system_freetype=ON \
	-DQT_FEATURE_webengine_system_glib=ON \
	-DQT_FEATURE_webengine_system_harfbuzz=ON \
	-DQT_FEATURE_webengine_system_icu=ON \
	-DQT_FEATURE_webengine_system_lcms2=ON \
	-DQT_FEATURE_webengine_system_libevent=ON \
	-DQT_FEATURE_webengine_system_libjpeg=ON \
	-DQT_FEATURE_webengine_system_libpci=ON \
	-DQT_FEATURE_webengine_system_libpng=ON \
	-DQT_FEATURE_webengine_system_libvpx=ON \
	-DQT_FEATURE_webengine_system_libwebp=ON \
	-DQT_FEATURE_webengine_system_libxml=ON \
	-DQT_FEATURE_webengine_system_minizip=ON \
	-DQT_FEATURE_webengine_system_opus=ON \
	-DQT_FEATURE_webengine_system_poppler=ON \
	-DQT_FEATURE_webengine_system_pulseaudio=ON \
	-DQT_FEATURE_webengine_system_re2=ON \
	-DQT_FEATURE_webengine_system_snappy=ON \
	-DQT_FEATURE_webengine_system_zlib=ON \
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
	%{cmake_on_off freetds QT_FEATURE_sql_tds} \
	%{cmake_on_off directfb QT_FEATURE_directfb} \
	%{cmake_on_off gtk QT_FEATURE_gtk3} \
	%{cmake_on_off egl QT_FEATURE_eglfs} \
	%{cmake_on_off statx QT_FEATURE_statx} \
	%{cmake_on_off kms QT_FEATURE_kms} \
	%{cmake_on_off libinput QT_FEATURE_libinput} \
	%{cmake_on_off tslib QT_FEATURE_tslib}

# Make sure arg-less sub-invocations will follow our parallel build setting
export CMAKE_BUILD_PARALLEL_LEVEL="%__jobs"
export SAMUFLAGS="%{_smp_mflags}"
export VERBOSE=1
export CFLAGS="%{rpmcflags}"
export CXXFLAGS="%{rpmcxxflags}"
export LDFLAGS="%{rpmldflags}"

%{__cmake} --build . --verbose %{_smp_mflags}

%if %{with doc}
export QT_PLUGIN_PATH="$(pwd)/qtbase/%{_lib}/qt6/plugins"
%{__cmake} --build . --target docs --verbose %{_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/qt6,%{_bindir},%{_pkgconfigdir},%{qt6dir}/libexec}

# for QtSolutions (qtlockedfile, qtsingleapplication, etc)
install -d $RPM_BUILD_ROOT%{_includedir}/qt6/QtSolutions

DESTDIR=$RPM_BUILD_ROOT %{__cmake} --install build/

%if %{with doc}
DESTDIR=$RPM_BUILD_ROOT %{__cmake} --build build/ --target install_docs

# win32 only
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/qt6-doc/activeqt*
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/qt6-doc/qtdoc/activeqt*
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/qt6-doc/qtdoc/qt-activex*
%endif

# external plugins loaded from qtbase libs
install -d $RPM_BUILD_ROOT%{qt6dir}/plugins/{iconengines,webview}

# kill unnecessary -L%{_libdir} from *.prl, *.pc
%{__sed} -i -e "s,-L%{_libdir} \?,,g" \
	$RPM_BUILD_ROOT%{_libdir}/*.prl \
	$RPM_BUILD_ROOT%{_pkgconfigdir}/*.pc

# symlinks in system bin dir
cd $RPM_BUILD_ROOT%{_bindir}
for prog in \
assistant \
designer \
lconvert \
linguist \
lrelease \
lupdate \
pixeltool \
qdbus \
qdbuscpp2xml \
qdbusviewer \
qdbusxml2cpp \
qdistancefieldgenerator \
qdoc \
qmake \
qml \
qmleasing \
qmlformat \
qmllint \
qmlplugindump \
qmlpreview \
qmlprofiler \
qmlscene \
qmltestrunner \
qmltime \
qt-cmake \
qtdiag \
qtpaths \
qsb \
qtplugininfo ; do
	ln -sf ../%{_lib}/qt6/bin/${prog} ${prog}-qt6
done
for prog in \
lprodump \
lrelease-pro \
lupdate-pro \
moc \
qhelpgenerator \
qlalr \
qmlcachegen \
qmlimportscanner \
qmltyperegistrar \
rcc \
uic \
; do
	ln -sf ../%{_lib}/qt6/libexec/${prog} ${prog}-qt6
done
cd -

install -d $RPM_BUILD_ROOT%{_examplesdir}/qt6
for dir in qt* ; do
  [ -d $dir/examples ] || continue
  mkdir -p $RPM_BUILD_ROOT%{_examplesdir}/qt6/$dir
  cp -a $dir/examples/* $RPM_BUILD_ROOT%{_examplesdir}/qt6/$dir/
done

# find_lang --with-qm supports only PLD qt3/qt4 specific %{_localedir}/*/LC_MESSAGES layout
find_qt6_qm()
{
	name="$1"
	find $RPM_BUILD_ROOT%{_datadir}/qt6/translations -name "${name}_*.qm" | \
		sed -e "s:^$RPM_BUILD_ROOT::" \
		    -e 's:\(.*/'$name'_\)\([a-z][a-z][a-z]\?\)\(_[A-Z][A-Z]\)\?\(\.qm\)$:%lang(\2\3) \1\2\3\4:'
}

echo '%defattr(644,root,root,755)' > qtbase.lang
echo '%defattr(644,root,root,755)' > assistant.lang
echo '%defattr(644,root,root,755)' > designer.lang
echo '%defattr(644,root,root,755)' > linguist.lang
echo '%defattr(644,root,root,755)' > qt_help.lang
echo '%defattr(644,root,root,755)' > qtconnectivity.lang
echo '%defattr(644,root,root,755)' > qtdeclarative.lang
echo '%defattr(644,root,root,755)' > qtmultimedia.lang
echo '%defattr(644,root,root,755)' > qtserialport.lang
echo '%defattr(644,root,root,755)' > qtwebengine.lang
echo '%defattr(644,root,root,755)' > qtwebsockets.lang
%if %{with doc}
find_qt6_qm qt >> qtbase.lang
find_qt6_qm qtbase >> qtbase.lang
find_qt6_qm qtlocation >> qtbase.lang
find_qt6_qm assistant >> assistant.lang
find_qt6_qm designer >> designer.lang
find_qt6_qm linguist >> linguist.lang
find_qt6_qm qt_help >> qt_help.lang
find_qt6_qm qtconnectivity >> qtconnectivity.lang
find_qt6_qm qtdeclarative >> qtdeclarative.lang
find_qt6_qm qtmultimedia >> qtmultimedia.lang
find_qt6_qm qtserialport >> qtserialport.lang
find_qt6_qm qtwebengine >> qtwebengine.lang
find_qt6_qm qtwebsockets >> qtwebsockets.lang
%endif

install -d $RPM_BUILD_ROOT%{qt6dir}/plugins/styles

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n Qt63D -p /sbin/ldconfig
%postun	-n Qt63D -p /sbin/ldconfig

%post	-n Qt6Bluetooth -p /sbin/ldconfig
%postun	-n Qt6Bluetooth -p /sbin/ldconfig

%post	-n Qt6Bodymovin -p /sbin/ldconfig
%postun	-n Qt6Bodymovin -p /sbin/ldconfig

%post	-n Qt6Charts -p /sbin/ldconfig
%postun	-n Qt6Charts -p /sbin/ldconfig

%post	-n Qt6Coap -p /sbin/ldconfig
%postun	-n Qt6Coap -p /sbin/ldconfig

%post	-n Qt6Concurrent -p /sbin/ldconfig
%postun	-n Qt6Concurrent -p /sbin/ldconfig

%post	-n Qt6Core -p /sbin/ldconfig
%postun	-n Qt6Core -p /sbin/ldconfig

%post	-n Qt6DataVisualization -p /sbin/ldconfig
%postun	-n Qt6DataVisualization -p /sbin/ldconfig

%post	-n Qt6DBus -p /sbin/ldconfig
%postun	-n Qt6DBus -p /sbin/ldconfig

%post	-n Qt6Designer -p /sbin/ldconfig
%postun	-n Qt6Designer -p /sbin/ldconfig

%post	-n Qt6Gui -p /sbin/ldconfig
%postun	-n Qt6Gui -p /sbin/ldconfig

%post	-n Qt6Gui-platform-eglfs -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-eglfs -p /sbin/ldconfig

%post	-n Qt6Gui-platform-eglfs-kms -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-eglfs-kms -p /sbin/ldconfig

%post	-n Qt6Gui-platform-xcb -p /sbin/ldconfig
%postun	-n Qt6Gui-platform-xcb -p /sbin/ldconfig

%post	-n Qt6Help -p /sbin/ldconfig
%postun	-n Qt6Help -p /sbin/ldconfig

%post	-n Qt6JsonRpc -p /sbin/ldconfig
%postun	-n Qt6JsonRpc -p /sbin/ldconfig

%post	-n Qt6LanguageServer -p /sbin/ldconfig
%postun	-n Qt6LanguageServer -p /sbin/ldconfig

%post	-n Qt6Mqtt -p /sbin/ldconfig
%postun	-n Qt6Mqtt -p /sbin/ldconfig

%post	-n Qt6Multimedia -p /sbin/ldconfig
%postun	-n Qt6Multimedia -p /sbin/ldconfig

%post	-n Qt6MultimediaQuick -p /sbin/ldconfig
%postun	-n Qt6MultimediaQuick -p /sbin/ldconfig

%post	-n Qt6MultimediaWidgets -p /sbin/ldconfig
%postun	-n Qt6MultimediaWidgets -p /sbin/ldconfig

%post	-n Qt6Network -p /sbin/ldconfig
%postun	-n Qt6Network -p /sbin/ldconfig

%post	-n Qt6NetworkAuth -p /sbin/ldconfig
%postun	-n Qt6NetworkAuth -p /sbin/ldconfig

%post	-n Qt6Nfc -p /sbin/ldconfig
%postun	-n Qt6Nfc -p /sbin/ldconfig

%post	-n Qt6OpcUa -p /sbin/ldconfig
%postun	-n Qt6OpcUa -p /sbin/ldconfig

%post	-n Qt6OpenGL -p /sbin/ldconfig
%postun	-n Qt6OpenGL -p /sbin/ldconfig

%post	-n Qt6Pdf -p /sbin/ldconfig
%postun	-n Qt6Pdf -p /sbin/ldconfig

%post	-n Qt6PrintSupport -p /sbin/ldconfig
%postun	-n Qt6PrintSupport -p /sbin/ldconfig

%post	-n Qt6Qt5Compat -p /sbin/ldconfig
%postun	-n Qt6Qt5Compat -p /sbin/ldconfig

%post	-n Qt6Qml -p /sbin/ldconfig
%postun	-n Qt6Qml -p /sbin/ldconfig

%post	-n Qt6Quick -p /sbin/ldconfig
%postun	-n Qt6Quick -p /sbin/ldconfig

%post	-n Qt6Quick3D -p /sbin/ldconfig
%postun	-n Qt6Quick3D -p /sbin/ldconfig

%post	-n Qt6RemoteObjects -p /sbin/ldconfig
%postun	-n Qt6RemoteObjects -p /sbin/ldconfig

%post	-n Qt6Scxml -p /sbin/ldconfig
%postun	-n Qt6Scxml -p /sbin/ldconfig

%post	-n Qt6Sensors -p /sbin/ldconfig
%postun	-n Qt6Sensors -p /sbin/ldconfig

%post	-n Qt6SerialBus -p /sbin/ldconfig
%postun	-n Qt6SerialBus -p /sbin/ldconfig

%post	-n Qt6SerialPort -p /sbin/ldconfig
%postun	-n Qt6SerialPort -p /sbin/ldconfig

%post	-n Qt6ShaderTools -p /sbin/ldconfig
%postun	-n Qt6ShaderTools -p /sbin/ldconfig

%post	-n Qt6Sql -p /sbin/ldconfig
%postun	-n Qt6Sql -p /sbin/ldconfig

%post	-n Qt6Svg -p /sbin/ldconfig
%postun	-n Qt6Svg -p /sbin/ldconfig

%post	-n Qt6Test -p /sbin/ldconfig
%postun	-n Qt6Test -p /sbin/ldconfig

%post	-n Qt6VirtualKeyboard -p /sbin/ldconfig
%postun	-n Qt6VirtualKeyboard -p /sbin/ldconfig

%post	-n Qt6WaylandCompositor -p /sbin/ldconfig
%postun	-n Qt6WaylandCompositor -p /sbin/ldconfig

%post	-n Qt6WaylandClient -p /sbin/ldconfig
%postun	-n Qt6WaylandClient -p /sbin/ldconfig

%post	-n Qt6WebChannel -p /sbin/ldconfig
%postun	-n Qt6WebChannel -p /sbin/ldconfig

%post	-n Qt6WebEngine -p /sbin/ldconfig
%postun	-n Qt6WebEngine -p /sbin/ldconfig

%post	-n Qt6WebSockets -p /sbin/ldconfig
%postun	-n Qt6WebSockets -p /sbin/ldconfig

%post	-n Qt6WebView -p /sbin/ldconfig
%postun	-n Qt6WebView -p /sbin/ldconfig

%post	-n Qt6Widgets -p /sbin/ldconfig
%postun	-n Qt6Widgets -p /sbin/ldconfig

%post	-n Qt6Xml -p /sbin/ldconfig
%postun	-n Qt6Xml -p /sbin/ldconfig

%files -n qt6-qttools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/pixeltool-qt6
%attr(755,root,root) %{_bindir}/qtdiag-qt6
%attr(755,root,root) %{_bindir}/qtpaths-qt6
%attr(755,root,root) %{_bindir}/qtplugininfo-qt6
%attr(755,root,root) %{qt6dir}/bin/androiddeployqt
%attr(755,root,root) %{qt6dir}/bin/androidtestrunner
%attr(755,root,root) %{qt6dir}/bin/pixeltool
%attr(755,root,root) %{qt6dir}/bin/qtdiag
%attr(755,root,root) %{qt6dir}/bin/qtdiag6
%attr(755,root,root) %{qt6dir}/bin/qtpaths
%attr(755,root,root) %{qt6dir}/bin/qtpaths6
%attr(755,root,root) %{qt6dir}/bin/qtplugininfo
# devel?
%{_includedir}/qt6/QtTools
%{_libdir}/cmake/Qt6Tools
%{_libdir}/cmake/Qt6ToolsTools
%{qt6dir}/mkspecs/modules/qt_lib_tools_private.pri
%dir %{_datadir}/qt6/modules
%{_datadir}/qt6/modules/Tools.json

%files -n qt6-assistant -f assistant.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/assistant-qt6
%attr(755,root,root) %{_bindir}/qdistancefieldgenerator-qt6
%attr(755,root,root) %{_bindir}/qhelpgenerator-qt6
%attr(755,root,root) %{qt6dir}/bin/assistant
%attr(755,root,root) %{qt6dir}/bin/qdistancefieldgenerator
%attr(755,root,root) %{qt6dir}/bin/qdoc
%attr(755,root,root) %{qt6dir}/libexec/qhelpgenerator
%attr(755,root,root) %{qt6dir}/libexec/qtattributionsscanner

%files -n qt6-designer -f designer.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/designer-qt6
%attr(755,root,root) %{qt6dir}/bin/designer

%files -n qt6-linguist -f linguist.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/lconvert-qt6
%attr(755,root,root) %{_bindir}/linguist-qt6
%attr(755,root,root) %{_bindir}/lprodump-qt6
%attr(755,root,root) %{_bindir}/lrelease-pro-qt6
%attr(755,root,root) %{_bindir}/lrelease-qt6
%attr(755,root,root) %{_bindir}/lupdate-pro-qt6
%attr(755,root,root) %{_bindir}/lupdate-qt6
%attr(755,root,root) %{qt6dir}/bin/lconvert
%attr(755,root,root) %{qt6dir}/bin/linguist
%attr(755,root,root) %{qt6dir}/bin/lrelease
%attr(755,root,root) %{qt6dir}/bin/lupdate
%attr(755,root,root) %{qt6dir}/libexec/lprodump
%attr(755,root,root) %{qt6dir}/libexec/lrelease-pro
%attr(755,root,root) %{qt6dir}/libexec/lupdate-pro
# devel?
%{_datadir}/qt6/phrasebooks
%{_libdir}/cmake/Qt6Linguist
%{_libdir}/cmake/Qt6LinguistTools
%{_pkgconfigdir}/Qt6Linguist.pc
%{_datadir}/qt6/modules/Linguist.json
%{qt6dir}/mkspecs/modules/qt_lib_linguist.pri
%{qt6dir}/mkspecs/modules/qt_lib_linguist_private.pri

%files -n qt6-qdbus
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qdbus-qt6
%attr(755,root,root) %{_bindir}/qdbusviewer-qt6
%attr(755,root,root) %{qt6dir}/bin/qdbus
%attr(755,root,root) %{qt6dir}/bin/qdbusviewer

%if %{with doc}
%files -n qt6-qttools-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qdoc
%{_docdir}/qt6-doc/qtassistant
%{_docdir}/qt6-doc/qtdesigner
%{_docdir}/qt6-doc/qtdistancefieldgenerator
%{_docdir}/qt6-doc/qthelp
%{_docdir}/qt6-doc/qtlinguist
%{_docdir}/qt6-doc/qtuitools

%files -n qt6-qttools-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qdoc.qch
%{_docdir}/qt6-doc/qtassistant.qch
%{_docdir}/qt6-doc/qtdesigner.qch
%{_docdir}/qt6-doc/qtdistancefieldgenerator.qch
%{_docdir}/qt6-doc/qthelp.qch
%{_docdir}/qt6-doc/qtlinguist.qch
%{_docdir}/qt6-doc/qtuitools.qch
%endif

%files -n qt6-qtdeclarative
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qmlcachegen-qt6
%attr(755,root,root) %{_bindir}/qmleasing-qt6
%attr(755,root,root) %{_bindir}/qmlformat-qt6
%attr(755,root,root) %{_bindir}/qmlimportscanner-qt6
%attr(755,root,root) %{_bindir}/qmllint-qt6
%attr(755,root,root) %{_bindir}/qmlplugindump-qt6
%attr(755,root,root) %{_bindir}/qmlpreview-qt6
%attr(755,root,root) %{_bindir}/qmlprofiler-qt6
%attr(755,root,root) %{_bindir}/qml-qt6
%attr(755,root,root) %{_bindir}/qmlscene-qt6
%attr(755,root,root) %{_bindir}/qmltestrunner-qt6
%attr(755,root,root) %{_bindir}/qmltime-qt6
%attr(755,root,root) %{_bindir}/qmltyperegistrar-qt6
%attr(755,root,root) %{qt6dir}/bin/qml
%attr(755,root,root) %{qt6dir}/bin/qmleasing
%attr(755,root,root) %{qt6dir}/bin/qmlformat
%attr(755,root,root) %{qt6dir}/bin/qmllint
%attr(755,root,root) %{qt6dir}/bin/qmlplugindump
%attr(755,root,root) %{qt6dir}/bin/qmlpreview
%attr(755,root,root) %{qt6dir}/bin/qmlprofiler
%attr(755,root,root) %{qt6dir}/bin/qmlscene
%attr(755,root,root) %{qt6dir}/bin/qmltestrunner
%attr(755,root,root) %{qt6dir}/bin/qmltime
%attr(755,root,root) %{qt6dir}/libexec/qmlcachegen
%attr(755,root,root) %{qt6dir}/libexec/qmlimportscanner
%attr(755,root,root) %{qt6dir}/libexec/qmltyperegistrar

%files -n Qt63D
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt63DAnimation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DAnimation.so.6
%attr(755,root,root) %{_libdir}/libQt63DCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DCore.so.6
%attr(755,root,root) %{_libdir}/libQt63DExtras.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DExtras.so.6
%attr(755,root,root) %{_libdir}/libQt63DInput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DInput.so.6
%attr(755,root,root) %{_libdir}/libQt63DLogic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DLogic.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuick.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuickAnimation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickAnimation.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuickExtras.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickExtras.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuickInput.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickInput.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuickRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickRender.so.6
%attr(755,root,root) %{_libdir}/libQt63DQuickScene2D.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickScene2D.so.6
%attr(755,root,root) %{_libdir}/libQt63DRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DRender.so.6
# - loaded from src/render/geometry/qmesh.cpp
%dir %{qt6dir}/plugins/geometryloaders
%attr(755,root,root) %{_libdir}/qt6/plugins/geometryloaders/libdefaultgeometryloader.so
%attr(755,root,root) %{_libdir}/qt6/plugins/geometryloaders/libgltfgeometryloader.so
# - loaded from src/render/qrendererpluginfactory.cpp
%dir %{qt6dir}/plugins/renderers
%attr(755,root,root) %{qt6dir}/plugins/renderers/libopenglrenderer.so
%attr(755,root,root) %{qt6dir}/plugins/renderers/librhirenderer.so
# - loaded from src/render/frontend/qrenderpluginfactory.cpp
%dir %{qt6dir}/plugins/renderplugins
%attr(755,root,root) %{_libdir}/qt6/plugins/renderplugins/libscene2d.so
# - loaded from src/render/io/qsceneimportfactory.cpp
%dir %{qt6dir}/plugins/sceneparsers
%attr(755,root,root) %{_libdir}/qt6/plugins/sceneparsers/libassimpsceneimport.so
%attr(755,root,root) %{_libdir}/qt6/plugins/sceneparsers/libgltfsceneexport.so
%attr(755,root,root) %{_libdir}/qt6/plugins/sceneparsers/libgltfsceneimport.so
%dir %{qt6dir}/qml/Qt3D
%dir %{qt6dir}/qml/Qt3D/Animation
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Animation/libquick3danimationplugin.so
%{qt6dir}/qml/Qt3D/Animation/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Animation/qmldir
%dir %{qt6dir}/qml/Qt3D/Core
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Core/libquick3dcoreplugin.so
%{qt6dir}/qml/Qt3D/Core/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Core/qmldir
%dir %{qt6dir}/qml/Qt3D/Extras
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Extras/libquick3dextrasplugin.so
%{qt6dir}/qml/Qt3D/Extras/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Extras/qmldir
%dir %{qt6dir}/qml/Qt3D/Input
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Input/libquick3dinputplugin.so
%{qt6dir}/qml/Qt3D/Input/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Input/qmldir
%dir %{qt6dir}/qml/Qt3D/Logic
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Logic/libquick3dlogicplugin.so
%{qt6dir}/qml/Qt3D/Logic/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Logic/qmldir
%dir %{qt6dir}/qml/Qt3D/Render
%attr(755,root,root) %{qt6dir}/qml/Qt3D/Render/libquick3drenderplugin.so
%{qt6dir}/qml/Qt3D/Render/plugins.qmltypes
%{qt6dir}/qml/Qt3D/Render/qmldir
%dir %{qt6dir}/qml/QtQuick/Scene2D
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Scene2D/libqtquickscene2dplugin.so
%{qt6dir}/qml/QtQuick/Scene2D/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Scene2D/qmldir
%dir %{qt6dir}/qml/QtQuick/Scene3D
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Scene3D/libqtquickscene3dplugin.so
%{qt6dir}/qml/QtQuick/Scene3D/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Scene3D/qmldir

%files -n Qt63D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt63DAnimation.so
%attr(755,root,root) %{_libdir}/libQt63DCore.so
%attr(755,root,root) %{_libdir}/libQt63DExtras.so
%attr(755,root,root) %{_libdir}/libQt63DInput.so
%attr(755,root,root) %{_libdir}/libQt63DLogic.so
%attr(755,root,root) %{_libdir}/libQt63DQuickAnimation.so
%attr(755,root,root) %{_libdir}/libQt63DQuickExtras.so
%attr(755,root,root) %{_libdir}/libQt63DQuickInput.so
%attr(755,root,root) %{_libdir}/libQt63DQuickRender.so
%attr(755,root,root) %{_libdir}/libQt63DQuickScene2D.so
%attr(755,root,root) %{_libdir}/libQt63DQuick.so
%attr(755,root,root) %{_libdir}/libQt63DRender.so
%{_libdir}/libQt63DAnimation.prl
%{_libdir}/libQt63DCore.prl
%{_libdir}/libQt63DExtras.prl
%{_libdir}/libQt63DInput.prl
%{_libdir}/libQt63DLogic.prl
%{_libdir}/libQt63DQuickAnimation.prl
%{_libdir}/libQt63DQuickExtras.prl
%{_libdir}/libQt63DQuickInput.prl
%{_libdir}/libQt63DQuick.prl
%{_libdir}/libQt63DQuickRender.prl
%{_libdir}/libQt63DQuickScene2D.prl
%{_libdir}/libQt63DRender.prl
%{_includedir}/qt6/Qt3DAnimation
%{_includedir}/qt6/Qt3DCore
%{_includedir}/qt6/Qt3DExtras
%{_includedir}/qt6/Qt3DInput
%{_includedir}/qt6/Qt3DLogic
%{_includedir}/qt6/Qt3DQuick
%{_includedir}/qt6/Qt3DQuickAnimation
%{_includedir}/qt6/Qt3DQuickExtras
%{_includedir}/qt6/Qt3DQuickInput
%{_includedir}/qt6/Qt3DQuickRender
%{_includedir}/qt6/Qt3DQuickScene2D
%{_includedir}/qt6/Qt3DRender
%{_pkgconfigdir}/Qt63DAnimation.pc
%{_pkgconfigdir}/Qt63DCore.pc
%{_pkgconfigdir}/Qt63DExtras.pc
%{_pkgconfigdir}/Qt63DInput.pc
%{_pkgconfigdir}/Qt63DLogic.pc
%{_pkgconfigdir}/Qt63DQuickAnimation.pc
%{_pkgconfigdir}/Qt63DQuickExtras.pc
%{_pkgconfigdir}/Qt63DQuickInput.pc
%{_pkgconfigdir}/Qt63DQuick.pc
%{_pkgconfigdir}/Qt63DQuickRender.pc
%{_pkgconfigdir}/Qt63DQuickScene2D.pc
%{_pkgconfigdir}/Qt63DRender.pc
%{_libdir}/cmake/Qt63DAnimation
%{_libdir}/cmake/Qt63DCore
%{_libdir}/cmake/Qt63DExtras
%{_libdir}/cmake/Qt63DInput
%{_libdir}/cmake/Qt63DLogic
%{_libdir}/cmake/Qt63DQuick
%{_libdir}/cmake/Qt63DQuickAnimation
%{_libdir}/cmake/Qt63DQuickExtras
%{_libdir}/cmake/Qt63DQuickInput
%{_libdir}/cmake/Qt63DQuickRender
%{_libdir}/cmake/Qt63DQuickScene2D
%{_libdir}/cmake/Qt63DRender

%{qt6dir}/mkspecs/modules/qt_lib_3danimation.pri
%{qt6dir}/mkspecs/modules/qt_lib_3danimation_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dcore.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dcore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dextras.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dextras_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dinput.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dinput_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dlogic.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dlogic_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickanimation.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickanimation_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickextras.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickextras_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickinput.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickinput_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickrender.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickrender_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickscene2d.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickscene2d_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3drender.pri
%{qt6dir}/mkspecs/modules/qt_lib_3drender_private.pri

%{_datadir}/qt6/modules/3DAnimation.json
%{_datadir}/qt6/modules/3DCore.json
%{_datadir}/qt6/modules/3DExtras.json
%{_datadir}/qt6/modules/3DInput.json
%{_datadir}/qt6/modules/3DLogic.json
%{_datadir}/qt6/modules/3DQuick.json
%{_datadir}/qt6/modules/3DQuickAnimation.json
%{_datadir}/qt6/modules/3DQuickExtras.json
%{_datadir}/qt6/modules/3DQuickInput.json
%{_datadir}/qt6/modules/3DQuickRender.json
%{_datadir}/qt6/modules/3DQuickScene2D.json
%{_datadir}/qt6/modules/3DRender.json

%{_libdir}/metatypes/qt63danimation_pld_metatypes.json
%{_libdir}/metatypes/qt63dcore_pld_metatypes.json
%{_libdir}/metatypes/qt63dextras_pld_metatypes.json
%{_libdir}/metatypes/qt63dinput_pld_metatypes.json
%{_libdir}/metatypes/qt63dlogic_pld_metatypes.json
%{_libdir}/metatypes/qt63dquick_pld_metatypes.json
%{_libdir}/metatypes/qt63dquickanimation_pld_metatypes.json
%{_libdir}/metatypes/qt63dquickextras_pld_metatypes.json
%{_libdir}/metatypes/qt63dquickinput_pld_metatypes.json
%{_libdir}/metatypes/qt63dquickrender_pld_metatypes.json
%{_libdir}/metatypes/qt63dquickscene2d_pld_metatypes.json
%{_libdir}/metatypes/qt63drender_pld_metatypes.json

%if %{with doc}
%files -n Qt63D-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qt3d

%files -n Qt63D-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qt3d.qch
%endif

%files -n Qt6Bluetooth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Bluetooth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Bluetooth.so.6
%attr(755,root,root) %{qt6dir}/libexec/sdpscanner

%files -n Qt6Bluetooth-devel -f qtconnectivity.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Bluetooth.so
%{_libdir}/libQt6Bluetooth.prl
%{_includedir}/qt6/QtBluetooth
%{_pkgconfigdir}/Qt6Bluetooth.pc
%{_libdir}/cmake/Qt6Bluetooth
%{qt6dir}/mkspecs/modules/qt_lib_bluetooth.pri
%{qt6dir}/mkspecs/modules/qt_lib_bluetooth_private.pri
%{_datadir}/qt6/modules/Bluetooth.json
%{_libdir}/metatypes/qt6bluetooth_pld_metatypes.json

%if %{with doc}
%files -n Qt6Bluetooth-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtbluetooth
%{_docdir}/qt6-doc/qtnfc

%files -n Qt6Bluetooth-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtbluetooth.qch
%{_docdir}/qt6-doc/qtnfc.qch
%endif

%files -n Qt6Bodymovin
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Bodymovin.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Bodymovin.so.6
%dir %{qt6dir}/qml/Qt/labs/lottieqt
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/lottieqt/liblottieqtplugin.so
%{qt6dir}/qml/Qt/labs/lottieqt/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/lottieqt/qmldir

%files -n Qt6Bodymovin-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Bodymovin.so
%{_libdir}/libQt6Bodymovin.prl
%{_includedir}/qt6/QtBodymovin
%{_libdir}/cmake/Qt6BodymovinPrivate
%{qt6dir}/mkspecs/modules/qt_lib_bodymovin_private.pri
%{_datadir}/qt6/modules/BodymovinPrivate.json
%{_libdir}/metatypes/qt6bodymovinprivate_pld_metatypes.json

%if %{with doc}
%files -n Qt6Bodymovin-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtlottieanimation

%files -n Qt6Bodymovin-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtlottieanimation.qch
%endif

%files -n Qt6Charts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Charts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Charts.so.6
%attr(755,root,root) %{_libdir}/libQt6ChartsQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ChartsQml.so.6
%dir %{qt6dir}/qml/QtCharts
%{qt6dir}/qml/QtCharts/designer
%attr(755,root,root) %{qt6dir}/qml/QtCharts/libqtchartsqml2plugin.so
%{qt6dir}/qml/QtCharts/plugins.qmltypes
%{qt6dir}/qml/QtCharts/qmldir

%files -n Qt6Charts-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Charts.so
%attr(755,root,root) %{_libdir}/libQt6ChartsQml.so
%{_libdir}/libQt6Charts.prl
%{_libdir}/libQt6ChartsQml.prl
%{_includedir}/qt6/QtCharts
%{_includedir}/qt6/QtChartsQml
%{_pkgconfigdir}/Qt6Charts.pc
%{_pkgconfigdir}/Qt6ChartsQml.pc
%{_libdir}/cmake/Qt6Charts
%{_libdir}/cmake/Qt6ChartsQml
%{qt6dir}/mkspecs/modules/qt_lib_charts.pri
%{qt6dir}/mkspecs/modules/qt_lib_charts_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_chartsqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_chartsqml_private.pri
%{_datadir}/qt6/modules/Charts.json
%{_datadir}/qt6/modules/ChartsQml.json
%{_libdir}/metatypes/qt6charts_pld_metatypes.json
%{_libdir}/metatypes/qt6chartsqml_pld_metatypes.json

%if %{with doc}
%files -n Qt6Charts-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcharts

%files -n Qt6Charts-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcharts.qch
%endif

%files -n Qt6Coap
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Coap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Coap.so.6

%files -n Qt6Coap-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Coap.so
%{_libdir}/libQt6Coap.prl
%{_includedir}/qt6/QtCoap
%{_pkgconfigdir}/Qt6Coap.pc
%{_libdir}/cmake/Qt6Coap
%{qt6dir}/mkspecs/modules/qt_lib_coap.pri
%{qt6dir}/mkspecs/modules/qt_lib_coap_private.pri
%{_datadir}/qt6/modules/Coap.json
%{_libdir}/metatypes/qt6coap_pld_metatypes.json

%if %{with doc}
%files -n Qt6Coap-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcoap

%files -n Qt6Coap-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcoap.qch
%endif

%files -n Qt6Concurrent
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Concurrent.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Concurrent.so.6

%files -n Qt6Concurrent-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Concurrent.so
%{_libdir}/libQt6Concurrent.prl
%{_includedir}/qt6/QtConcurrent
%{_pkgconfigdir}/Qt6Concurrent.pc
%{_libdir}/cmake/Qt6Concurrent
%{qt6dir}/mkspecs/modules/qt_lib_concurrent.pri
%{qt6dir}/mkspecs/modules/qt_lib_concurrent_private.pri
%{_datadir}/qt6/modules/Concurrent.json
%{_libdir}/metatypes/qt6concurrent_pld_metatypes.json

%files -n Qt6Core -f qtbase.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Core.so.6
%dir %{_sysconfdir}/qt6
%dir %{qt6dir}
%dir %{qt6dir}/bin
%dir %{qt6dir}/libexec
%dir %{qt6dir}/mkspecs
%dir %{qt6dir}/mkspecs/modules
%dir %{qt6dir}/plugins
%dir %{_datadir}/qt6
%dir %{_datadir}/qt6/translations
%dir %{qt6dir}/qml/QtCore
%attr(755,root,root) %{qt6dir}/qml/QtCore/libqtqmlcoreplugin.so
%{qt6dir}/qml/QtCore/plugins.qmltypes
%{qt6dir}/qml/QtCore/qmldir
%dir %{qt6dir}/plugins/tls
%attr(755,root,root) %{qt6dir}/plugins/tls/libqcertonlybackend.so
%attr(755,root,root) %{qt6dir}/plugins/tls/libqopensslbackend.so
%dir %{qt6dir}/plugins/platforms
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqvkkhrdisplay.so

%files -n Qt6Core-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core.so
%{_libdir}/libQt6Core.prl
%dir %{_libdir}/metatypes
%{_libdir}/metatypes/qt6core_pld_metatypes.json
%dir %{_includedir}/qt6
%dir %{_includedir}/qt6/QtSolutions
%{_includedir}/qt6/QtCore
%{_pkgconfigdir}/Qt6Core.pc
%{_pkgconfigdir}/Qt6Platform.pc
%{_libdir}/cmake/Qt6
%{_libdir}/cmake/Qt6Core
%{_libdir}/cmake/Qt6CoreTools
%dir %{_libdir}/cmake/Qt6BuildInternals
%{_libdir}/cmake/Qt6BuildInternals/*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_core.pri
%{qt6dir}/mkspecs/modules/qt_lib_core_private.pri
%attr(755,root,root) %{qt6dir}/libexec/tracegen
%{_datadir}/qt6/modules/Core.json

%files -n Qt6DataVisualization
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DataVisualization.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DataVisualization.so.6
%attr(755,root,root) %{_libdir}/libQt6DataVisualizationQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DataVisualizationQml.so.6
%dir %{qt6dir}/qml/QtDataVisualization
%attr(755,root,root) %{qt6dir}/qml/QtDataVisualization/libdatavisualizationqmlplugin.so
%{qt6dir}/qml/QtDataVisualization/plugins.qmltypes
%{qt6dir}/qml/QtDataVisualization/qmldir
%{qt6dir}/qml/QtDataVisualization/designer

%files -n Qt6DataVisualization-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DataVisualization.so
%attr(755,root,root) %{_libdir}/libQt6DataVisualizationQml.so
%{_libdir}/libQt6DataVisualization.prl
%{_libdir}/libQt6DataVisualizationQml.prl
%{_includedir}/qt6/QtDataVisualization
%{_includedir}/qt6/QtDataVisualizationQml
%{_pkgconfigdir}/Qt6DataVisualization.pc
%{_pkgconfigdir}/Qt6DataVisualizationQml.pc
%{_libdir}/cmake/Qt6DataVisualization
%{_libdir}/cmake/Qt6DataVisualizationQml
%{qt6dir}/mkspecs/modules/qt_lib_datavisualization.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualization_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualizationqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualizationqml_private.pri
%{_datadir}/qt6/modules/DataVisualization.json
%{_datadir}/qt6/modules/DataVisualizationQml.json
%{_libdir}/metatypes/qt6datavisualization_pld_metatypes.json
%{_libdir}/metatypes/qt6datavisualizationqml_pld_metatypes.json

%if %{with doc}
%files -n Qt6DataVisualization-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtdatavis3d

%files -n Qt6DataVisualization-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtdatavis3d.qch
%endif

%files -n Qt6DBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DBus.so.6

%files -n Qt6DBus-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6DBus.so
%{_libdir}/libQt6DBus.prl
%{_includedir}/qt6/QtDBus
%{_pkgconfigdir}/Qt6DBus.pc
%{_libdir}/cmake/Qt6DBus
%{_libdir}/cmake/Qt6DBusTools
%{qt6dir}/mkspecs/modules/qt_lib_dbus.pri
%{qt6dir}/mkspecs/modules/qt_lib_dbus_private.pri
%{_datadir}/qt6/modules/DBus.json
%{_libdir}/metatypes/qt6dbus_pld_metatypes.json

%files -n Qt6Designer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Designer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Designer.so.6
%attr(755,root,root) %{_libdir}/libQt6DesignerComponents.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DesignerComponents.so.6
%dir %{qt6dir}/plugins/designer

%files -n Qt6Designer-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Designer.so
%attr(755,root,root) %{_libdir}/libQt6DesignerComponents.so
%{_libdir}/libQt6Designer.prl
%{_libdir}/libQt6DesignerComponents.prl
%{_includedir}/qt6/QtDesigner
%{_includedir}/qt6/QtDesignerComponents
%{_pkgconfigdir}/Qt6Designer.pc
%dir %{_libdir}/cmake/Qt6Designer
%{_libdir}/cmake/Qt6Designer/Qt6Designer*.cmake
%{_libdir}/cmake/Qt6DesignerComponentsPrivate
%{qt6dir}/mkspecs/modules/qt_lib_designer.pri
%{qt6dir}/mkspecs/modules/qt_lib_designer_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_designercomponents_private.pri
%{_datadir}/qt6/modules/Designer.json
%{_datadir}/qt6/modules/DesignerComponentsPrivate.json
%{_libdir}/metatypes/qt6designercomponentsprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6designer_pld_metatypes.json

%files -n Qt6Designer-plugin-qquickwidget
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/designer/libqquickwidget.so
%{_libdir}/cmake/Qt6Designer/Qt6QQuickWidgetPlugin*.cmake

%files -n Qt6DeviceDiscoverySupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtDeviceDiscoverySupport
%{_libdir}/libQt6DeviceDiscoverySupport.a
%{_libdir}/libQt6DeviceDiscoverySupport.prl
%{_libdir}/cmake/Qt6DeviceDiscoverySupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_devicediscovery_support_private.pri
%{_datadir}/qt6/modules/DeviceDiscoverySupportPrivate.json
%{_libdir}/metatypes/qt6devicediscoverysupportprivate_pld_metatypes.json

%files -n Qt6FbSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtFbSupport
%{_libdir}/libQt6FbSupport.a
%{_libdir}/libQt6FbSupport.prl
%{_libdir}/cmake/Qt6FbSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_fb_support_private.pri
%{_datadir}/qt6/modules/FbSupportPrivate.json
%{_libdir}/metatypes/qt6fbsupportprivate_pld_metatypes.json

%files -n Qt6Gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Gui.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Gui.so.6
# loaded from src/gui/kernel/qgenericpluginfactory.cpp
%dir %{qt6dir}/plugins/generic
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
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqicns.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqjp2.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqjpeg.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqmng.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqtga.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqtiff.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqwbmp.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqwebp.so
# loaded from src/gui/kernel/qplatforminputcontextfactory.cpp
%dir %{qt6dir}/plugins/platforminputcontexts
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libcomposeplatforminputcontextplugin.so
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libibusplatforminputcontextplugin.so
# loaded from src/gui/kernel/qplatformintegrationfactory.cpp
%dir %{qt6dir}/plugins/platforms
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqminimal.so
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqoffscreen.so
# loaded from src/gui/kernel/qplatformthemefactory.cpp
%dir %{qt6dir}/plugins/platformthemes
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt6Gui

%if %{with libinput}
%files -n Qt6Gui-generic-libinput
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/generic/libqlibinputplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6QLibInputPlugin*.cmake
%endif

%if %{with tslib}
%files -n Qt6Gui-generic-tslib
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/generic/libqtslibplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6QTsLibPlugin*.cmake
%endif

%files -n Qt6Gui-generic-tuiotouch
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/generic/libqtuiotouchplugin.so
%{_libdir}/cmake/Qt6Gui/Qt6QTuioTouchPlugin*.cmake

%if %{with directfb}
%files -n Qt6Gui-platform-directfb
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqdirectfb.so
%{_libdir}/cmake/Qt6Gui/Qt6QDirectFbIntegrationPlugin*.cmake
%endif

%if %{with egl}
%files -n Qt6Gui-platform-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqminimalegl.so
%{_libdir}/cmake/Qt6Gui/Qt6QMinimalEglIntegrationPlugin*.cmake
%endif

%files -n Qt6Gui-platform-eglfs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6EglFSDeviceIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6EglFSDeviceIntegration.so.6
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqeglfs.so
%{_libdir}/cmake/Qt6Gui/Qt6QEglFSIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEglFSEmulatorIntegrationPlugin*.cmake
# loaded from src/plugins/platforms/eglfs/qeglfsdeviceintegration.cpp
%dir %{qt6dir}/plugins/egldeviceintegrations
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-emu-integration.so

%files -n Qt6Gui-platform-eglfs-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtEglFSDeviceIntegration
%attr(755,root,root) %{_libdir}/libQt6EglFSDeviceIntegration.so
%{_libdir}/cmake/Qt6EglFSDeviceIntegrationPrivate
%{_libdir}/libQt6EglFSDeviceIntegration.prl
%{qt6dir}/mkspecs/modules/qt_lib_eglfsdeviceintegration_private.pri
%{_datadir}/qt6/modules/EglFSDeviceIntegrationPrivate.json
%{_libdir}/metatypes/qt6eglfsdeviceintegrationprivate_pld_metatypes.json

%if %{with kms}
%files -n Qt6Gui-platform-eglfs-kms
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6EglFsKmsSupport.so.6
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsGbmSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6EglFsKmsGbmSupport.so.6
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-kms-integration.so
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-kms-egldevice-integration.so

%files -n Qt6Gui-platform-eglfs-kms-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsSupport.so
%attr(755,root,root) %{_libdir}/libQt6EglFsKmsGbmSupport.so
%{_includedir}/qt6/QtEglFsKmsGbmSupport
%{_includedir}/qt6/QtEglFsKmsSupport
%{_libdir}/libQt6EglFsKmsGbmSupport.prl
%{_libdir}/libQt6EglFsKmsSupport.prl
%{_libdir}/cmake/Qt6EglFsKmsGbmSupportPrivate
%{_libdir}/cmake/Qt6EglFsKmsSupportPrivate
%{_libdir}/cmake/Qt6Gui/Qt6QEglFSKmsEglDeviceIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEglFSKmsGbmIntegrationPlugin*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_eglfs_kms_support_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_eglfs_kms_gbm_support_private.pri
%{_datadir}/qt6/modules/EglFsKmsGbmSupportPrivate.json
%{_datadir}/qt6/modules/EglFsKmsSupportPrivate.json
%{_libdir}/metatypes/qt6eglfskmssupportprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6eglfskmsgbmsupportprivate_pld_metatypes.json
%endif

%files -n Qt6Gui-platform-eglfs-x11
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/egldeviceintegrations/libqeglfs-x11-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6QEglFSX11IntegrationPlugin*.cmake

%files -n Qt6Gui-platform-linuxfb
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqlinuxfb.so
%{_libdir}/cmake/Qt6Gui/Qt6QLinuxFbIntegrationPlugin*.cmake

%files -n Qt6Gui-platform-vnc
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqvnc.so

%files -n Qt6Gui-platform-vnc-devel
%defattr(644,root,root,755)
%{_libdir}/cmake/Qt6Gui/Qt6QVncIntegrationPlugin*.cmake

%files -n Qt6Gui-platform-xcb
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6XcbQpa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6XcbQpa.so.6
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqxcb.so
# loaded from src/plugins/platforms/xcb/gl_integrations/qxcbglintegrationfactory.cpp
%dir %{qt6dir}/plugins/xcbglintegrations
%{_libdir}/cmake/Qt6Gui/Qt6QXcbIntegrationPlugin*.cmake

%files -n Qt6Gui-platform-xcb-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6XcbQpa.so
%{_libdir}/libQt6XcbQpa.prl
%{_libdir}/cmake/Qt6XcbQpaPrivate
%{qt6dir}/mkspecs/modules/qt_lib_xcb_qpa_lib_private.pri
%{_datadir}/qt6/modules/XcbQpaPrivate.json
%{_libdir}/metatypes/qt6xcbqpaprivate_pld_metatypes.json

%files -n Qt6Gui-platform-xcb-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-egl-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6QXcbEglIntegrationPlugin*.cmake

%files -n Qt6Gui-platform-xcb-glx
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-glx-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6QXcbGlxIntegrationPlugin*.cmake

%if %{with gtk}
%files -n Qt6Gui-platformtheme-gtk3
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platformthemes/libqgtk3.so
%{_libdir}/cmake/Qt6Gui/Qt6QGtk3ThemePlugin*.cmake
%endif

%files -n Qt6Gui-platformtheme-xdgdesktopportal
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/platformthemes/libqxdgdesktopportal.so
%{_libdir}/cmake/Qt6Gui/Qt6QXdgDesktopPortalThemePlugin*.cmake

%files -n Qt6Gui-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/libexec/qvkgen
%attr(755,root,root) %{_libdir}/libQt6Gui.so
%{_libdir}/libQt6Gui.prl
%{_libdir}/metatypes/qt6gui_pld_metatypes.json
%{_includedir}/qt6/QtGui
%{_pkgconfigdir}/Qt6Gui.pc
%{_libdir}/cmake/Qt6Gui/Qt6Gui*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEvdevKeyboardPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEvdevMousePlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEvdevTabletPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QEvdevTouchScreenPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QGifPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QICOPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QJpegPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QComposePlatformInputContextPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QIbusPlatformInputContextPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QMinimalIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QOffscreenIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QICNSPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QJp2Plugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QMngPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QTgaPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QTiffPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QVkKhrDisplayIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QWebpPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QWbmpPlugin*.cmake
%{_libdir}/cmake/Qt6GuiTools
%{qt6dir}/mkspecs/modules/qt_lib_gui.pri
%{qt6dir}/mkspecs/modules/qt_lib_gui_private.pri
%{_datadir}/qt6/modules/Gui.json

%files -n Qt6Help -f qt_help.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Help.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Help.so.6

%files -n Qt6Help-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Help.so
%{_libdir}/libQt6Help.prl
%{_includedir}/qt6/QtHelp
%{_pkgconfigdir}/Qt6Help.pc
%{_libdir}/cmake/Qt6Help
%{qt6dir}/mkspecs/modules/qt_lib_help.pri
%{qt6dir}/mkspecs/modules/qt_lib_help_private.pri
%{_datadir}/qt6/modules/Help.json
%{_libdir}/metatypes/qt6help_pld_metatypes.json

%files -n Qt6InputSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtInputSupport
%{_libdir}/libQt6InputSupport.a
%{_libdir}/libQt6InputSupport.prl
%{_libdir}/cmake/Qt6InputSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_input_support_private.pri
%{_datadir}/qt6/modules/InputSupportPrivate.json
%{_libdir}/metatypes/qt6inputsupportprivate_pld_metatypes.json

%files -n Qt6JsonRpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6JsonRpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6JsonRpc.so.6

%files -n Qt6JsonRpc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6JsonRpc.so
%{_libdir}/libQt6JsonRpc.prl
%{_includedir}/qt6/QtJsonRpc
%{_libdir}/cmake/Qt6JsonRpcPrivate
%{_libdir}/metatypes/qt6jsonrpcprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_jsonrpc_private.pri
%{_datadir}/qt6/modules/JsonRpcPrivate.json

%files -n Qt6LanguageServer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LanguageServer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LanguageServer.so.6

%files -n Qt6LanguageServer-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LanguageServer.so
%{_libdir}/libQt6LanguageServer.prl
%{_includedir}/qt6/QtLanguageServer
%{_libdir}/cmake/Qt6LanguageServerPrivate
%{_libdir}/metatypes/qt6languageserverprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_languageserver_private.pri
%{_datadir}/qt6/modules/LanguageServerPrivate.json

%files -n Qt6KmsSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtKmsSupport
%{_libdir}/libQt6KmsSupport.a
%{_libdir}/libQt6KmsSupport.prl
%{_libdir}/cmake/Qt6KmsSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_kms_support_private.pri
%{_datadir}/qt6/modules/KmsSupportPrivate.json
%{_libdir}/metatypes/qt6kmssupportprivate_pld_metatypes.json

%files -n Qt6Mqtt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Mqtt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Mqtt.so.6

%files -n Qt6Mqtt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Mqtt.so
%{_libdir}/libQt6Mqtt.prl
%{_includedir}/qt6/QtMqtt
%{_pkgconfigdir}/Qt6Mqtt.pc
%{_libdir}/cmake/Qt6Mqtt
%{qt6dir}/mkspecs/modules/qt_lib_mqtt.pri
%{qt6dir}/mkspecs/modules/qt_lib_mqtt_private.pri
%{_datadir}/qt6/modules/Mqtt.json
%{_libdir}/metatypes/qt6mqtt_pld_metatypes.json

%if %{with doc}
%files -n Qt6Mqtt-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtmqtt

%files -n Qt6Mqtt-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtmqtt.qch
%endif

%files -n Qt6Multimedia -f qtmultimedia.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Multimedia.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Multimedia.so.6
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt6Multimedia

%files -n Qt6Multimedia-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Multimedia.so
%{_libdir}/libQt6Multimedia.prl
%{_includedir}/qt6/QtMultimedia
%{_pkgconfigdir}/Qt6Multimedia.pc
%{_libdir}/cmake/Qt6Multimedia
%{qt6dir}/mkspecs/modules/qt_lib_multimedia.pri
%{qt6dir}/mkspecs/modules/qt_lib_multimedia_private.pri
%{_datadir}/qt6/modules/Multimedia.json
%{_libdir}/metatypes/qt6multimedia_pld_metatypes.json

%if %{with doc}
%files -n Qt6Multimedia-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtmultimedia

%files -n Qt6Multimedia-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtmultimedia.qch
%endif

%files -n Qt6MultimediaQuick
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6MultimediaQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6MultimediaQuick.so.6
%dir %{qt6dir}/qml/QtMultimedia
%attr(755,root,root) %{qt6dir}/qml/QtMultimedia/libquickmultimediaplugin.so
%{qt6dir}/qml/QtMultimedia/Video.qml
%{qt6dir}/qml/QtMultimedia/plugins.qmltypes
%{qt6dir}/qml/QtMultimedia/qmldir

%files -n Qt6MultimediaQuick-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6MultimediaQuick.so
%{_libdir}/libQt6MultimediaQuick.prl
%{_libdir}/cmake/Qt6MultimediaQuickPrivate
%{_includedir}/qt6/QtMultimediaQuick
%{qt6dir}/mkspecs/modules/qt_lib_multimediaquick_private.pri
%{_datadir}/qt6/modules/MultimediaQuickPrivate.json
%{_libdir}/metatypes/qt6multimediaquickprivate_pld_metatypes.json

%files -n Qt6MultimediaWidgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6MultimediaWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6MultimediaWidgets.so.6

%files -n Qt6MultimediaWidgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6MultimediaWidgets.so
%{_libdir}/libQt6MultimediaWidgets.prl
%{_includedir}/qt6/QtMultimediaWidgets
%{_pkgconfigdir}/Qt6MultimediaWidgets.pc
%{_libdir}/cmake/Qt6MultimediaWidgets
%{qt6dir}/mkspecs/modules/qt_lib_multimediawidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_multimediawidgets_private.pri
%{_datadir}/qt6/modules/MultimediaWidgets.json
%{_libdir}/metatypes/qt6multimediawidgets_pld_metatypes.json

%files -n Qt6Network
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Network.so.6

%files -n Qt6Network-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so
%{_libdir}/libQt6Network.prl
%{_includedir}/qt6/QtNetwork
%{_pkgconfigdir}/Qt6Network.pc
%{_libdir}/cmake/Qt6Network
%{qt6dir}/mkspecs/modules/qt_lib_network.pri
%{qt6dir}/mkspecs/modules/qt_lib_network_private.pri
%{_datadir}/qt6/modules/Network.json
%{_libdir}/metatypes/qt6network_pld_metatypes.json

%files -n Qt6NetworkAuth
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6NetworkAuth.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6NetworkAuth.so.6

%files -n Qt6NetworkAuth-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6NetworkAuth.so
%{_libdir}/libQt6NetworkAuth.prl
%{_includedir}/qt6/QtNetworkAuth
%{_libdir}/cmake/Qt6NetworkAuth
%{_pkgconfigdir}/Qt6NetworkAuth.pc
%{_libdir}/qt6/mkspecs/modules/qt_lib_networkauth.pri
%{_libdir}/qt6/mkspecs/modules/qt_lib_networkauth_private.pri
%{_datadir}/qt6/modules/NetworkAuth.json
%{_libdir}/metatypes/qt6networkauth_pld_metatypes.json

%if %{with doc}
%files -n Qt6NetworkAuth-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtnetworkauth

%files -n Qt6NetworkAuth-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtnetworkauth.qch
%endif

%files -n Qt6Nfc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Nfc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Nfc.so.6

%files -n Qt6Nfc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Nfc.so
%{_libdir}/libQt6Nfc.prl
%{_includedir}/qt6/QtNfc
%{_pkgconfigdir}/Qt6Nfc.pc
%{_libdir}/cmake/Qt6Nfc
%{qt6dir}/mkspecs/modules/qt_lib_nfc.pri
%{qt6dir}/mkspecs/modules/qt_lib_nfc_private.pri
%{_datadir}/qt6/modules/Nfc.json
%{_libdir}/metatypes/qt6nfc_pld_metatypes.json

%if %{with doc}
%files -n Qt6Nfc-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtbluetooth
%{_docdir}/qt6-doc/qtnfc

%files -n Qt6Nfc-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtbluetooth.qch
%{_docdir}/qt6-doc/qtnfc.qch
%endif

%files -n Qt6OpcUa
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpcUa.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6OpcUa.so.6
%attr(755,root,root) %{_libdir}/libQt6DeclarativeOpcua.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6DeclarativeOpcua.so.6
%dir %{qt6dir}/plugins/opcua
%attr(755,root,root) %{qt6dir}/plugins/opcua/libopen62541_backend.so
%dir %{qt6dir}/qml/QtOpcUa
%attr(755,root,root) %{qt6dir}/qml/QtOpcUa/libdeclarativeopcuaplugin.so
%{qt6dir}/qml/QtOpcUa/plugins.qmltypes
%{qt6dir}/qml/QtOpcUa/qmldir

%files -n Qt6OpcUa-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpcUa.so
%attr(755,root,root) %{_libdir}/libQt6DeclarativeOpcua.so
%{_libdir}/libQt6OpcUa.prl
%{_libdir}/libQt6DeclarativeOpcua.prl
%{_includedir}/qt6/QtDeclarativeOpcua
%{_includedir}/qt6/QtOpcUa
%{_pkgconfigdir}/Qt6DeclarativeOpcua.pc
%{_pkgconfigdir}/Qt6OpcUa.pc
%{_libdir}/cmake/Qt6DeclarativeOpcua
%{_libdir}/cmake/Qt6OpcUa
%{qt6dir}/mkspecs/modules/qt_lib_declarativeopcua.pri
%{qt6dir}/mkspecs/modules/qt_lib_declarativeopcua_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_opcua.pri
%{qt6dir}/mkspecs/modules/qt_lib_opcua_private.pri
%{_datadir}/qt6/modules/DeclarativeOpcua.json
%{_datadir}/qt6/modules/OpcUa.json
%{_libdir}/metatypes/qt6declarativeopcua_pld_metatypes.json
%{_libdir}/metatypes/qt6opcua_pld_metatypes.json

%if %{with doc}
%files -n Qt6OpcUa-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtopcua

%files -n Qt6OpcUa-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtopcua.qch
%endif

%files -n Qt6OpenGL
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpenGL.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6OpenGL.so.6
%attr(755,root,root) %{_libdir}/libQt6OpenGLWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6OpenGLWidgets.so.6

%files -n Qt6OpenGL-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6OpenGL.so
%attr(755,root,root) %{_libdir}/libQt6OpenGLWidgets.so
%{_libdir}/libQt6OpenGL.prl
%{_libdir}/libQt6OpenGLWidgets.prl
%{_includedir}/qt6/QtOpenGL
%{_includedir}/qt6/QtOpenGLWidgets
%{_pkgconfigdir}/Qt6OpenGL.pc
%{_pkgconfigdir}/Qt6OpenGLWidgets.pc
%{_libdir}/cmake/Qt6OpenGL
%{_libdir}/cmake/Qt6OpenGLWidgets
%{qt6dir}/mkspecs/modules/qt_lib_opengl.pri
%{qt6dir}/mkspecs/modules/qt_lib_opengl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_openglwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_openglwidgets_private.pri
%{_datadir}/qt6/modules/OpenGL.json
%{_datadir}/qt6/modules/OpenGLWidgets.json
%{_libdir}/metatypes/qt6opengl_pld_metatypes.json
%{_libdir}/metatypes/qt6openglwidgets_pld_metatypes.json

%if %{with webengine}
%files -n Qt6Pdf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Pdf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Pdf.so.6
%attr(755,root,root) %{_libdir}/libQt6PdfQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PdfQuick.so.6
%attr(755,root,root) %{_libdir}/libQt6PdfWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PdfWidgets.so.6
%dir %{qt6dir}/qml/QtQuick/Pdf
%{qt6dir}/qml/QtQuick/Pdf/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Pdf/qmldir
%{qt6dir}/qml/QtQuick/Pdf/qml
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Pdf/libqtpdfquickplugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/imageformats/libqpdf.so

%files -n Qt6Pdf-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Pdf.so
%attr(755,root,root) %{_libdir}/libQt6PdfQuick.so
%attr(755,root,root) %{_libdir}/libQt6PdfWidgets.so
%{_libdir}/libQt6Pdf.prl
%{_libdir}/libQt6PdfQuick.prl
%{_libdir}/libQt6PdfWidgets.prl
%{_includedir}/qt6/QtPdf
%{_includedir}/qt6/QtPdfQuick
%{_includedir}/qt6/QtPdfWidgets
%{_pkgconfigdir}/Qt6Pdf.pc
%{_pkgconfigdir}/Qt6PdfQuick.pc
%{_pkgconfigdir}/Qt6PdfWidgets.pc
%{_libdir}/cmake/Qt6Gui/Qt6QPdfPlugin*.cmake
%{_libdir}/cmake/Qt6Pdf
%{_libdir}/cmake/Qt6PdfQuick
%{_libdir}/cmake/Qt6PdfWidgets
%{qt6dir}/mkspecs/modules/qt_lib_pdf.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdf_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfquick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_pdfwidgets_private.pri
%{_datadir}/qt6/modules/Pdf.json
%{_datadir}/qt6/modules/PdfQuick.json
%{_datadir}/qt6/modules/PdfWidgets.json
%{_libdir}/metatypes/qt6pdf_pld_metatypes.json
%{_libdir}/metatypes/qt6pdfquick_pld_metatypes.json
%{_libdir}/metatypes/qt6pdfwidgets_pld_metatypes.json

%if %{with doc}
%files -n Qt6Pdf-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf

%files -n Qt6Pdf-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf.qch
%endif
%endif

%files -n Qt6PrintSupport
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6PrintSupport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PrintSupport.so.6
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
%{_libdir}/cmake/Qt6PrintSupport/Qt6PrintSupport*.cmake
%if %{with cups}
%{_libdir}/cmake/Qt6PrintSupport/Qt6QCupsPrinterSupportPlugin*.cmake
%endif
%{qt6dir}/mkspecs/modules/qt_lib_printsupport.pri
%{qt6dir}/mkspecs/modules/qt_lib_printsupport_private.pri
%{_datadir}/qt6/modules/PrintSupport.json
%{_libdir}/metatypes/qt6printsupport_pld_metatypes.json

%files -n Qt6Qt5Compat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core5Compat.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Core5Compat.so.6
%dir %{qt6dir}/qml/Qt5Compat
%dir %{qt6dir}/qml/Qt5Compat/GraphicalEffects
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/*.qml
%attr(755,root,root) %{qt6dir}/qml/Qt5Compat/GraphicalEffects/libqtgraphicaleffectsplugin.so
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/plugins.qmltypes
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/qmldir
%dir %{qt6dir}/qml/Qt5Compat/GraphicalEffects/private
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/private/*.qml
%attr(755,root,root) %{qt6dir}/qml/Qt5Compat/GraphicalEffects/private/libqtgraphicaleffectsprivateplugin.so
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/private/qmldir

%files -n Qt6Qt5Compat-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core5Compat.so
%{_libdir}/libQt6Core5Compat.prl
%{_libdir}/metatypes/qt6core5compat_pld_metatypes.json
%{_includedir}/qt6/QtCore5Compat
%{_pkgconfigdir}/Qt6Core5Compat.pc
%{_libdir}/cmake/Qt6Core5Compat
%{qt6dir}/mkspecs/modules/qt_lib_core5compat.pri
%{qt6dir}/mkspecs/modules/qt_lib_core5compat_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlworkerscript_private.pri
%{_datadir}/qt6/modules/Core5Compat.json

%if %{with doc}
%files -n Qt6Qt5Compat-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcore5compat
%{_docdir}/qt6-doc/qtgraphicaleffects5compat

%files -n Qt6Qt5Compat-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtcore5compat.qch
%{_docdir}/qt6-doc/qtgraphicaleffects5compat.qch
%endif

%files -n Qt6Qml -f qtdeclarative.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LabsAnimation.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsAnimation.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsFolderListModel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsFolderListModel.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsQmlModels.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsQmlModels.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsSettings.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsSettings.so.6
%attr(755,root,root) %{_libdir}/libQt6Positioning.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Positioning.so.6
%attr(755,root,root) %{_libdir}/libQt6PositioningQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PositioningQuick.so.6
%attr(755,root,root) %{_libdir}/libQt6Qml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Qml.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlCore.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlModels.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlModels.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlWorkerScript.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlWorkerScript.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlLocalStorage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlLocalStorage.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlXmlListModel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlXmlListModel.so.6
%attr(755,root,root) %{_libdir}/libQt6StateMachine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6StateMachine.so.6
%attr(755,root,root) %{_libdir}/libQt6StateMachineQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6StateMachineQml.so.6

# loaded from src/qml/debugger/{qqmldebugserver,qqmlinspectorservice}.cpp
%dir %{qt6dir}/plugins/qmltooling
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_debugger.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_local.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_messages.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_native.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_nativedebugger.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_profiler.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_server.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_tcp.so
%dir %{qt6dir}/plugins/position
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_geoclue2.so
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_nmea.so
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_positionpoll.so

%dir %{qt6dir}/qml
%dir %{qt6dir}/qml/Qt
%dir %{qt6dir}/qml/Qt/labs
%dir %{qt6dir}/qml/Qt/labs/animation
%{qt6dir}/qml/jsroot.qmltypes

%attr(755,root,root) %{qt6dir}/qml/Qt/labs/animation/liblabsanimationplugin.so
%{qt6dir}/qml/Qt/labs/animation/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/animation/qmldir

%dir %{qt6dir}/qml/Qt/labs/folderlistmodel
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/folderlistmodel/libqmlfolderlistmodelplugin.so
%{qt6dir}/qml/Qt/labs/folderlistmodel/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/folderlistmodel/qmldir

%dir %{qt6dir}/qml/Qt/labs/platform
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/platform/libqtlabsplatformplugin.so
%{qt6dir}/qml/Qt/labs/platform/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/platform/qmldir

%dir %{qt6dir}/qml/Qt/labs/qmlmodels
%{qt6dir}/qml/Qt/labs/qmlmodels/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/qmlmodels/qmldir
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/qmlmodels/liblabsmodelsplugin.so

%dir %{qt6dir}/qml/Qt/labs/settings
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/settings/libqmlsettingsplugin.so
%{qt6dir}/qml/Qt/labs/settings/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/settings/qmldir

%dir %{qt6dir}/qml/QtQml
%attr(755,root,root) %{qt6dir}/qml/QtQml/libqmlplugin.so
%dir %{qt6dir}/qml/QtQml/Models
%attr(755,root,root) %{qt6dir}/qml/QtQml/Models/libmodelsplugin.so
%{qt6dir}/qml/QtQml/Models/plugins.qmltypes
%{qt6dir}/qml/QtQml/Models/qmldir

%dir %{qt6dir}/qml/QtPositioning
%attr(755,root,root) %{qt6dir}/qml/QtPositioning/libpositioningquickplugin.so
%{qt6dir}/qml/QtPositioning/plugins.qmltypes
%{qt6dir}/qml/QtPositioning/qmldir

%dir %{qt6dir}/qml/QtQml/StateMachine
%attr(755,root,root) %{qt6dir}/qml/QtQml/StateMachine/libqtqmlstatemachineplugin.so
%{qt6dir}/qml/QtQml/StateMachine/plugins.qmltypes
%{qt6dir}/qml/QtQml/StateMachine/qmldir

%dir %{qt6dir}/qml/QtQml/WorkerScript
%attr(755,root,root) %{qt6dir}/qml/QtQml/WorkerScript/libworkerscriptplugin.so
%{qt6dir}/qml/QtQml/WorkerScript/plugins.qmltypes
%{qt6dir}/qml/QtQml/WorkerScript/qmldir

%dir %{qt6dir}/qml/QtQml/XmlListModel
%attr(755,root,root) %{qt6dir}/qml/QtQml/XmlListModel/libqmlxmllistmodelplugin.so
%{qt6dir}/qml/QtQml/XmlListModel/plugins.qmltypes
%{qt6dir}/qml/QtQml/XmlListModel/qmldir

%{qt6dir}/qml/QtQml/plugins.qmltypes
%{qt6dir}/qml/QtQml/qmldir
%{qt6dir}/qml/builtins.qmltypes

%files -n Qt6Qml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LabsAnimation.so
%attr(755,root,root) %{_libdir}/libQt6LabsFolderListModel.so
%attr(755,root,root) %{_libdir}/libQt6LabsQmlModels.so
%attr(755,root,root) %{_libdir}/libQt6LabsSettings.so
%attr(755,root,root) %{_libdir}/libQt6Positioning.so
%attr(755,root,root) %{_libdir}/libQt6PositioningQuick.so
%attr(755,root,root) %{_libdir}/libQt6Qml.so
%attr(755,root,root) %{_libdir}/libQt6QmlCore.so
%attr(755,root,root) %{_libdir}/libQt6QmlModels.so
%attr(755,root,root) %{_libdir}/libQt6QmlWorkerScript.so
%attr(755,root,root) %{_libdir}/libQt6QmlLocalStorage.so
%attr(755,root,root) %{_libdir}/libQt6QmlXmlListModel.so
%attr(755,root,root) %{_libdir}/libQt6StateMachine.so
%attr(755,root,root) %{_libdir}/libQt6StateMachineQml.so
# static-only
%{_libdir}/libQt6PacketProtocol.a
%{_libdir}/libQt6QmlCompiler.a
%{_libdir}/libQt6QmlDebug.a
%{_libdir}/libQt6QmlDom.a
%{_libdir}/libQt6QmlLint.a
%{_libdir}/libQt6LabsAnimation.prl
%{_libdir}/libQt6LabsFolderListModel.prl
%{_libdir}/libQt6LabsQmlModels.prl
%{_libdir}/libQt6LabsSettings.prl
%{_libdir}/metatypes/qt6labsanimation_pld_metatypes.json
%{_libdir}/metatypes/qt6labsfolderlistmodel_pld_metatypes.json
%{_libdir}/metatypes/qt6labsqmlmodels_pld_metatypes.json
%{_libdir}/metatypes/qt6labssettings_pld_metatypes.json
%{_libdir}/metatypes/qt6packetprotocolprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6positioning_pld_metatypes.json
%{_libdir}/metatypes/qt6positioningquick_pld_metatypes.json
%{_libdir}/metatypes/qt6qmlcompilerprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6qmlcore_pld_metatypes.json
%{_libdir}/metatypes/qt6qmldebugprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6qmldomprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6qmllintprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6qmllocalstorage_pld_metatypes.json
%{_libdir}/metatypes/qt6qmlmodels_pld_metatypes.json
%{_libdir}/metatypes/qt6qml_pld_metatypes.json
%{_libdir}/metatypes/qt6qmlworkerscript_pld_metatypes.json
%{_libdir}/metatypes/qt6qmlxmllistmodel_pld_metatypes.json
%{_libdir}/metatypes/qt6statemachine_pld_metatypes.json
%{_libdir}/metatypes/qt6statemachineqml_pld_metatypes.json
%{_libdir}/libQt6PacketProtocol.prl
%{_libdir}/libQt6Positioning.prl
%{_libdir}/libQt6PositioningQuick.prl
%{_libdir}/libQt6QmlCompiler.prl
%{_libdir}/libQt6Qml.prl
%{_libdir}/libQt6QmlCore.prl
%{_libdir}/libQt6QmlDebug.prl
%{_libdir}/libQt6QmlDom.prl
%{_libdir}/libQt6QmlLint.prl
%{_libdir}/libQt6QmlLocalStorage.prl
%{_libdir}/libQt6QmlModels.prl
%{_libdir}/libQt6QmlWorkerScript.prl
%{_libdir}/libQt6QmlXmlListModel.prl
%{_libdir}/libQt6StateMachine.prl
%{_libdir}/libQt6StateMachineQml.prl
%{_includedir}/qt6/QtLabsAnimation
%{_includedir}/qt6/QtLabsFolderListModel
%{_includedir}/qt6/QtLabsQmlModels
%{_includedir}/qt6/QtLabsSettings
%{_includedir}/qt6/QtPositioning
%{_includedir}/qt6/QtPositioningQuick
%{_includedir}/qt6/QtStateMachine
%{_includedir}/qt6/QtStateMachineQml
%{_includedir}/qt6/QtQml
%{_includedir}/qt6/QtQmlCompiler
%{_includedir}/qt6/QtQmlCore
%{_includedir}/qt6/QtQmlDebug
%{_includedir}/qt6/QtQmlDom
%{_includedir}/qt6/QtQmlIntegration
%{_includedir}/qt6/QtQmlLint
%{_includedir}/qt6/QtQmlLocalStorage
%{_includedir}/qt6/QtQmlModels
%{_includedir}/qt6/QtQmlWorkerScript
%{_includedir}/qt6/QtPacketProtocol
%{_includedir}/qt6/QtQmlXmlListModel
%{_pkgconfigdir}/Qt6LabsAnimation.pc
%{_pkgconfigdir}/Qt6LabsFolderListModel.pc
%{_pkgconfigdir}/Qt6LabsQmlModels.pc
%{_pkgconfigdir}/Qt6LabsSettings.pc
%{_pkgconfigdir}/Qt6Qml.pc
%{_pkgconfigdir}/Qt6QmlModels.pc
%{_pkgconfigdir}/Qt6QmlWorkerScript.pc
%{_pkgconfigdir}/Qt6StateMachine.pc
%{_pkgconfigdir}/Qt6StateMachineQml.pc
%{_pkgconfigdir}/Qt6QmlCore.pc
%{_pkgconfigdir}/Qt6QmlIntegration.pc
%{_pkgconfigdir}/Qt6QmlLocalStorage.pc
%{_pkgconfigdir}/Qt6QmlXmlListModel.pc
%{_pkgconfigdir}/Qt6Positioning.pc
%{_pkgconfigdir}/Qt6PositioningQuick.pc
%{_libdir}/cmake/Qt6LabsAnimation
%{_libdir}/cmake/Qt6LabsFolderListModel
%{_libdir}/cmake/Qt6LabsQmlModels
%{_libdir}/cmake/Qt6LabsSettings
%{_libdir}/cmake/Qt6PacketProtocolPrivate
%{_libdir}/cmake/Qt6Positioning
%{_libdir}/cmake/Qt6PositioningQuick
%{_libdir}/cmake/Qt6Qml
%{_libdir}/cmake/Qt6QmlCompilerPrivate
%{_libdir}/cmake/Qt6QmlCore
%{_libdir}/cmake/Qt6QmlDebugPrivate
%{_libdir}/cmake/Qt6QmlDomPrivate
%{_libdir}/cmake/Qt6QmlImportScanner
%{_libdir}/cmake/Qt6QmlIntegration
%{_libdir}/cmake/Qt6QmlLintPrivate
%{_libdir}/cmake/Qt6QmlLocalStorage
%{_libdir}/cmake/Qt6QmlModels
%{_libdir}/cmake/Qt6StateMachine
%{_libdir}/cmake/Qt6StateMachineQml
%{_libdir}/cmake/Qt6QmlTools
%{_libdir}/cmake/Qt6QmlWorkerScript
%{_libdir}/cmake/Qt6QmlXmlListModel
%{qt6dir}/mkspecs/features/qmlcache.prf
%{qt6dir}/mkspecs/features/qmltypes.prf
%{qt6dir}/mkspecs/modules/qt_lib_labsanimation.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsanimation_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsfolderlistmodel.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsfolderlistmodel_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsqmlmodels.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsqmlmodels_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssettings.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssettings_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_packetprotocol_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioning.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioning_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioningquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioningquick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcompiler_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcore.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmldebug_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmldom_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlintegration.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlintegration_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmllint_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmllocalstorage.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmllocalstorage_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmodels.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmodels_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qml.pri
%{qt6dir}/mkspecs/modules/qt_lib_qml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltest.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltest_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlworkerscript.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlworkerscript_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlxmllistmodel.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlxmllistmodel_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachine.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachine_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachineqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachineqml_private.pri
%{_datadir}/qt6/modules/LabsAnimation.json
%{_datadir}/qt6/modules/LabsFolderListModel.json
%{_datadir}/qt6/modules/LabsQmlModels.json
%{_datadir}/qt6/modules/LabsSettings.json
%{_datadir}/qt6/modules/PacketProtocolPrivate.json
%{_datadir}/qt6/modules/Positioning.json
%{_datadir}/qt6/modules/PositioningQuick.json
%{_datadir}/qt6/modules/Qml.json
%{_datadir}/qt6/modules/QmlCompilerPrivate.json
%{_datadir}/qt6/modules/QmlCore.json
%{_datadir}/qt6/modules/QmlDebugPrivate.json
%{_datadir}/qt6/modules/QmlDomPrivate.json
%{_datadir}/qt6/modules/QmlIntegration.json
%{_datadir}/qt6/modules/QmlLintPrivate.json
%{_datadir}/qt6/modules/QmlLocalStorage.json
%{_datadir}/qt6/modules/QmlModels.json
%{_datadir}/qt6/modules/QmlWorkerScript.json
%{_datadir}/qt6/modules/QmlXmlListModel.json
%{_datadir}/qt6/modules/StateMachine.json
%{_datadir}/qt6/modules/StateMachineQml.json

%if %{with doc}
%files -n Qt6Qml-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtlabsplatform
%{_docdir}/qt6-doc/qtplatformintegration
%{_docdir}/qt6-doc/qtpositioning
%{_docdir}/qt6-doc/qtqml
%{_docdir}/qt6-doc/qtqmlcore
%{_docdir}/qt6-doc/qtqmlmodels
%{_docdir}/qt6-doc/qtqmltest
%{_docdir}/qt6-doc/qtqmlworkerscript
%{_docdir}/qt6-doc/qtqmlxmllistmodel
%{_docdir}/qt6-doc/qtstatemachine

%files -n Qt6Qml-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtlabsplatform.qch
%{_docdir}/qt6-doc/qtplatformintegration.qch
%{_docdir}/qt6-doc/qtpositioning.qch
%{_docdir}/qt6-doc/qtqmlcore.qch
%{_docdir}/qt6-doc/qtqmlmodels.qch
%{_docdir}/qt6-doc/qtqml.qch
%{_docdir}/qt6-doc/qtqmltest.qch
%{_docdir}/qt6-doc/qtqmlworkerscript.qch
%{_docdir}/qt6-doc/qtqmlxmllistmodel.qch
%{_docdir}/qt6-doc/qtstatemachine.qch
%endif

%files -n Qt6Quick
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LabsSharedImage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsSharedImage.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsWavefrontMesh.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsWavefrontMesh.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickParticles.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickParticles.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickShapes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickShapes.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickTest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickTest.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickWidgets.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Impl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Impl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickDialogs2.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2QuickImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickDialogs2QuickImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2Utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickDialogs2Utils.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickLayouts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickLayouts.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickTemplates2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickTemplates2.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickTimeline.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickTimeline.so.6

%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_inspector.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_preview.so
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_quickprofiler.so

%if %{with openvg}
%dir %{qt6dir}/plugins/scenegraph
%attr(755,root,root) %{qt6dir}/plugins/scenegraph/libqsgopenvgbackend.so
%endif

%dir %{qt6dir}/qml/Qt/labs/sharedimage
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/sharedimage/libsharedimageplugin.so
%{qt6dir}/qml/Qt/labs/sharedimage/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/sharedimage/qmldir

%dir %{qt6dir}/qml/Qt/labs/wavefrontmesh
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/wavefrontmesh/libqmlwavefrontmeshplugin.so
%{qt6dir}/qml/Qt/labs/wavefrontmesh/plugins.qmltypes
%{qt6dir}/qml/Qt/labs/wavefrontmesh/qmldir

%dir %{qt6dir}/qml/QtQuick

%dir %{qt6dir}/qml/QtQuick/Controls
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/libqtquickcontrols2plugin.so
%{qt6dir}/qml/QtQuick/Controls/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/qmldir

%dir %{qt6dir}/qml/QtQuick/Controls/Basic
%{qt6dir}/qml/QtQuick/Controls/Basic/*.qml
%{qt6dir}/qml/QtQuick/Controls/Basic/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Basic/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Basic/libqtquickcontrols2basicstyleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/Basic/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Basic/impl/libqtquickcontrols2basicstyleimplplugin.so
%{qt6dir}/qml/QtQuick/Controls/Basic/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Basic/impl/qmldir

%dir %{qt6dir}/qml/QtQuick/Controls/Fusion
%{qt6dir}/qml/QtQuick/Controls/Fusion/*.qml
%{qt6dir}/qml/QtQuick/Controls/Fusion/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Fusion/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Fusion/libqtquickcontrols2fusionstyleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/Fusion/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Fusion/impl/libqtquickcontrols2fusionstyleimplplugin.so
%{qt6dir}/qml/QtQuick/Controls/Fusion/impl/*.qml
%{qt6dir}/qml/QtQuick/Controls/Fusion/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Fusion/impl/qmldir
%dir %{qt6dir}/qml/QtQuick/Controls/Imagine
%{qt6dir}/qml/QtQuick/Controls/Imagine/*.qml
%{qt6dir}/qml/QtQuick/Controls/Imagine/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Imagine/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Imagine/libqtquickcontrols2imaginestyleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/Imagine/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Imagine/impl/libqtquickcontrols2imaginestyleimplplugin.so
%{qt6dir}/qml/QtQuick/Controls/Imagine/impl/*.qml
%{qt6dir}/qml/QtQuick/Controls/Imagine/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Imagine/impl/qmldir
%dir %{qt6dir}/qml/QtQuick/Controls/Material
%{qt6dir}/qml/QtQuick/Controls/Material/*.qml
%{qt6dir}/qml/QtQuick/Controls/Material/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Material/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Material/libqtquickcontrols2materialstyleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/Material/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Material/impl/libqtquickcontrols2materialstyleimplplugin.so
%{qt6dir}/qml/QtQuick/Controls/Material/impl/*.qml
%{qt6dir}/qml/QtQuick/Controls/Material/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Material/impl/qmldir
%dir %{qt6dir}/qml/QtQuick/Controls/Universal
%{qt6dir}/qml/QtQuick/Controls/Universal/*.qml
%{qt6dir}/qml/QtQuick/Controls/Universal/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Universal/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Universal/libqtquickcontrols2universalstyleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/Universal/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/Universal/impl/libqtquickcontrols2universalstyleimplplugin.so
%{qt6dir}/qml/QtQuick/Controls/Universal/impl/*.qml
%{qt6dir}/qml/QtQuick/Controls/Universal/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/Universal/impl/qmldir
%dir %{qt6dir}/qml/QtQuick/Controls/designer
%{qt6dir}/qml/QtQuick/Controls/designer/images
%{qt6dir}/qml/QtQuick/Controls/designer/*.qml
%{qt6dir}/qml/QtQuick/Controls/designer/qtquickcontrols2.metainfo

%dir %{qt6dir}/qml/QtQuick/Controls/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/impl/libqtquickcontrols2implplugin.so
%{qt6dir}/qml/QtQuick/Controls/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/impl/qmldir

%dir %{qt6dir}/qml/QtQuick/Dialogs
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Dialogs/libqtquickdialogsplugin.so
%{qt6dir}/qml/QtQuick/Dialogs/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Dialogs/qmldir
%dir %{qt6dir}/qml/QtQuick/Dialogs/quickimpl
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Dialogs/quickimpl/libqtquickdialogs2quickimplplugin.so
%{qt6dir}/qml/QtQuick/Dialogs/quickimpl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Dialogs/quickimpl/qml
%{qt6dir}/qml/QtQuick/Dialogs/quickimpl/qmldir

%dir %{qt6dir}/qml/QtQuick/Layouts
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Layouts/libqquicklayoutsplugin.so
%{qt6dir}/qml/QtQuick/Layouts/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Layouts/qmldir

%dir %{qt6dir}/qml/QtQuick/NativeStyle
%attr(755,root,root) %{qt6dir}/qml/QtQuick/NativeStyle/libqtquickcontrols2nativestyleplugin.so
%{qt6dir}/qml/QtQuick/NativeStyle/controls
%{qt6dir}/qml/QtQuick/NativeStyle/plugins.qmltypes
%{qt6dir}/qml/QtQuick/NativeStyle/qmldir

%dir %{qt6dir}/qml/QtQuick/LocalStorage
%attr(755,root,root) %{qt6dir}/qml/QtQuick/LocalStorage/libqmllocalstorageplugin.so
%{qt6dir}/qml/QtQuick/LocalStorage/plugins.qmltypes
%{qt6dir}/qml/QtQuick/LocalStorage/qmldir

%dir %{qt6dir}/qml/QtQuick/Particles
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Particles/libparticlesplugin.so
%{qt6dir}/qml/QtQuick/Particles/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Particles/qmldir

%dir %{qt6dir}/qml/QtQuick/Shapes
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Shapes/libqmlshapesplugin.so
%{qt6dir}/qml/QtQuick/Shapes/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Shapes/qmldir

%dir %{qt6dir}/qml/QtQuick/Templates
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Templates/libqtquicktemplates2plugin.so
%{qt6dir}/qml/QtQuick/Templates/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Templates/qmldir

%dir %{qt6dir}/qml/QtQuick/Window
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Window/libquickwindowplugin.so
%{qt6dir}/qml/QtQuick/Window/quickwindow.qmltypes
%{qt6dir}/qml/QtQuick/Window/qmldir

%attr(755,root,root) %{qt6dir}/qml/QtQuick/libqtquick2plugin.so
%{qt6dir}/qml/QtQuick/plugins.qmltypes
%{qt6dir}/qml/QtQuick/qmldir

%dir %{qt6dir}/qml/QtTest
%attr(755,root,root) %{qt6dir}/qml/QtTest/libquicktestplugin.so
%{qt6dir}/qml/QtTest/plugins.qmltypes
%{qt6dir}/qml/QtTest/qmldir
%{qt6dir}/qml/QtTest/testlogger.js
%{qt6dir}/qml/QtTest/*.qml

%dir %{qt6dir}/qml/QtQuick/tooling
%attr(755,root,root) %{qt6dir}/qml/QtQuick/tooling/libquicktoolingplugin.so
%{qt6dir}/qml/QtQuick/tooling/quicktooling.qmltypes
%{qt6dir}/qml/QtQuick/tooling/qmldir
%{qt6dir}/qml/QtQuick/tooling/*.qml

%files -n Qt6Quick-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/bin/qmldom
%attr(755,root,root) %{qt6dir}/bin/qmlls
%attr(755,root,root) %{qt6dir}/bin/qmltc
%{_libdir}/libQt6QuickControlsTestUtils.a
%{_libdir}/libQt6QuickTestUtils.a
%attr(755,root,root) %{_libdir}/libQt6LabsSharedImage.so
%attr(755,root,root) %{_libdir}/libQt6LabsWavefrontMesh.so
%attr(755,root,root) %{_libdir}/libQt6Quick.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Impl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2QuickImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2Utils.so
%attr(755,root,root) %{_libdir}/libQt6QuickLayouts.so
%attr(755,root,root) %{_libdir}/libQt6QuickParticles.so
%attr(755,root,root) %{_libdir}/libQt6QuickShapes.so
%attr(755,root,root) %{_libdir}/libQt6QuickTemplates2.so
%attr(755,root,root) %{_libdir}/libQt6QuickTest.so
%attr(755,root,root) %{_libdir}/libQt6QuickTimeline.so
%attr(755,root,root) %{_libdir}/libQt6QuickWidgets.so
%{_libdir}/libQt6LabsSharedImage.prl
%{_libdir}/libQt6LabsWavefrontMesh.prl
%{_libdir}/libQt6Quick.prl
%{_libdir}/libQt6QuickControls2Impl.prl
%{_libdir}/libQt6QuickControls2.prl
%{_libdir}/libQt6QuickControlsTestUtils.prl
%{_libdir}/libQt6QuickDialogs2.prl
%{_libdir}/libQt6QuickDialogs2QuickImpl.prl
%{_libdir}/libQt6QuickDialogs2Utils.prl
%{_libdir}/libQt6QuickLayouts.prl
%{_libdir}/libQt6QuickParticles.prl
%{_libdir}/libQt6QuickShapes.prl
%{_libdir}/libQt6QuickTemplates2.prl
%{_libdir}/libQt6QuickTest.prl
%{_libdir}/libQt6QuickTestUtils.prl
%{_libdir}/libQt6QuickTimeline.prl
%{_libdir}/libQt6QuickWidgets.prl
%{_libdir}/metatypes/qt6quick_pld_metatypes.json
%{_libdir}/metatypes/qt6quicktest_pld_metatypes.json
%{_includedir}/qt6/QtLabsSharedImage
%{_includedir}/qt6/QtLabsWavefrontMesh
%{_includedir}/qt6/QtQuick
%{_includedir}/qt6/QtQuickControls2
%{_includedir}/qt6/QtQuickControls2Impl
%{_includedir}/qt6/QtQuickControlsTestUtils
%{_includedir}/qt6/QtQuickDialogs2
%{_includedir}/qt6/QtQuickDialogs2QuickImpl
%{_includedir}/qt6/QtQuickDialogs2Utils
%{_includedir}/qt6/QtQuickLayouts
%{_includedir}/qt6/QtQuickParticles
%{_includedir}/qt6/QtQuickShapes
%{_includedir}/qt6/QtQuickTemplates2
%{_includedir}/qt6/QtQuickTest
%{_includedir}/qt6/QtQuickTestUtils
%{_includedir}/qt6/QtQuickTimeline
%{_includedir}/qt6/QtQuickWidgets
%{_pkgconfigdir}/Qt6LabsSharedImage.pc
%{_pkgconfigdir}/Qt6LabsWavefrontMesh.pc
%{_pkgconfigdir}/Qt6Quick.pc
%{_pkgconfigdir}/Qt6QuickTest.pc
%{_pkgconfigdir}/Qt6QuickTimeline.pc
%{_pkgconfigdir}/Qt6QuickWidgets.pc
%{_pkgconfigdir}/Qt6QuickControls2.pc
%{_pkgconfigdir}/Qt6QuickControls2Impl.pc
%{_pkgconfigdir}/Qt6QuickDialogs2.pc
%{_pkgconfigdir}/Qt6QuickDialogs2QuickImpl.pc
%{_pkgconfigdir}/Qt6QuickDialogs2Utils.pc
%{_pkgconfigdir}/Qt6QuickLayouts.pc
%{_pkgconfigdir}/Qt6QuickTemplates2.pc
%{_libdir}/cmake/Qt6LabsSharedImage
%{_libdir}/cmake/Qt6LabsWavefrontMesh
%{_libdir}/cmake/Qt6Quick
%{_libdir}/cmake/Qt6QuickControls2
%{_libdir}/cmake/Qt6QuickControls2Impl
%{_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate
%{_libdir}/cmake/Qt6QuickDialogs2
%{_libdir}/cmake/Qt6QuickDialogs2QuickImpl
%{_libdir}/cmake/Qt6QuickDialogs2Utils
%{_libdir}/cmake/Qt6QuickLayouts
%{_libdir}/cmake/Qt6QuickParticlesPrivate
%{_libdir}/cmake/Qt6QuickShapesPrivate
%{_libdir}/cmake/Qt6QuickTemplates2
%{_libdir}/cmake/Qt6QuickTest
%{_libdir}/cmake/Qt6QuickTestUtilsPrivate
%{_libdir}/cmake/Qt6QuickTimeline
%{_libdir}/cmake/Qt6QuickWidgets
%{qt6dir}/mkspecs/features/qtquickcompiler.prf
%{qt6dir}/mkspecs/modules/qt_lib_labssharedimage.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssharedimage_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labswavefrontmesh.pri
%{qt6dir}/mkspecs/modules/qt_lib_labswavefrontmesh_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2impl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2impl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrolstestutilsprivate_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2quickimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2quickimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2utils.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2utils_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicklayouts.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicklayouts_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickparticles_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickshapes_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktemplates2.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktemplates2_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktestutilsprivate_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktimeline.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktimeline_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickwidgets_private.pri
%{_datadir}/qt6/modules/LabsSharedImage.json
%{_datadir}/qt6/modules/LabsWavefrontMesh.json
%{_datadir}/qt6/modules/Quick.json
%{_datadir}/qt6/modules/QuickControls2.json
%{_datadir}/qt6/modules/QuickControls2Impl.json
%{_datadir}/qt6/modules/QuickControlsTestUtilsPrivate.json
%{_datadir}/qt6/modules/QuickDialogs2.json
%{_datadir}/qt6/modules/QuickDialogs2QuickImpl.json
%{_datadir}/qt6/modules/QuickDialogs2Utils.json
%{_datadir}/qt6/modules/QuickLayouts.json
%{_datadir}/qt6/modules/QuickParticlesPrivate.json
%{_datadir}/qt6/modules/QuickShapesPrivate.json
%{_datadir}/qt6/modules/QuickTemplates2.json
%{_datadir}/qt6/modules/QuickTest.json
%{_datadir}/qt6/modules/QuickTestUtilsPrivate.json
%{_datadir}/qt6/modules/QuickTimeline.json
%{_datadir}/qt6/modules/QuickWidgets.json
%{_libdir}/metatypes/qt6labssharedimage_pld_metatypes.json
%{_libdir}/metatypes/qt6labswavefrontmesh_pld_metatypes.json
%{_libdir}/metatypes/qt6quickcontrols2_pld_metatypes.json
%{_libdir}/metatypes/qt6quickcontrols2impl_pld_metatypes.json
%{_libdir}/metatypes/qt6quickcontrolstestutilsprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6quickdialogs2_pld_metatypes.json
%{_libdir}/metatypes/qt6quickdialogs2quickimpl_pld_metatypes.json
%{_libdir}/metatypes/qt6quickdialogs2utils_pld_metatypes.json
%{_libdir}/metatypes/qt6quicklayouts_pld_metatypes.json
%{_libdir}/metatypes/qt6quickparticlesprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6quickshapesprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6quicktemplates2_pld_metatypes.json
%{_libdir}/metatypes/qt6quicktestutilsprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6quicktimeline_pld_metatypes.json
%{_libdir}/metatypes/qt6quickwidgets_pld_metatypes.json

%if %{with doc}
%files -n Qt6Quick-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick
%{_docdir}/qt6-doc/qtquickcontrols
%{_docdir}/qt6-doc/qtquickdialogs

%files -n Qt6Quick-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick.qch
%{_docdir}/qt6-doc/qtquickcontrols.qch
%{_docdir}/qt6-doc/qtquickdialogs.qch
%endif

%files -n Qt6Quick-Timeline
%defattr(644,root,root,755)
%dir %{qt6dir}/qml/QtQuick/Timeline
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Timeline/libqtquicktimelineplugin.so
%{qt6dir}/qml/QtQuick/Timeline/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Timeline/qmldir

%if %{with doc}
%files -n Qt6Quick-Timeline-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquicktimeline

%files -n Qt6Quick-Timeline-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquicktimeline.qch
%endif

%files -n Qt6Quick3D
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3D.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3D.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetImport.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DAssetImport.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DAssetUtils.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DEffects.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DEffects.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DGlslParser.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DGlslParser.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DHelpers.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DHelpers.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DIblBaker.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DIblBaker.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticleEffects.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DParticleEffects.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticles.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DParticles.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DRuntimeRender.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DRuntimeRender.so.6
%attr(755,root,root) %{_libdir}/libQt6Quick3DUtils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DUtils.so.6
%attr(755,root,root) %{qt6dir}/bin/balsam
%attr(755,root,root) %{qt6dir}/bin/meshdebug
%dir %{qt6dir}/plugins/assetimporters
%attr(755,root,root) %{qt6dir}/plugins/assetimporters/libassimp.so
%attr(755,root,root) %{qt6dir}/plugins/assetimporters/libuip.so
%dir %{qt6dir}/plugins/qmltooling
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_quick3dprofiler.so
%dir %{qt6dir}/qml/QtQuick3D
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/libqquick3dplugin.so
%{qt6dir}/qml/QtQuick3D/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/qmldir
%{qt6dir}/qml/QtQuick3D/designer
%dir %{qt6dir}/qml/QtQuick3D/AssetUtils
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/AssetUtils/libqtquick3dassetutilsplugin.so
%{qt6dir}/qml/QtQuick3D/AssetUtils/designer
%{qt6dir}/qml/QtQuick3D/AssetUtils/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/AssetUtils/qmldir
%dir %{qt6dir}/qml/QtQuick3D/Effects
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Effects/libqtquick3deffectplugin.so
%{qt6dir}/qml/QtQuick3D/Effects/qmldir
%{qt6dir}/qml/QtQuick3D/Effects/*.qml
%{qt6dir}/qml/QtQuick3D/Effects/designer
%{qt6dir}/qml/QtQuick3D/Effects/Quick3DEffects.qmltypes
%dir %{qt6dir}/qml/QtQuick3D/Helpers
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Helpers/libqtquick3dhelpersplugin.so
%{qt6dir}/qml/QtQuick3D/Helpers/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/Helpers/qmldir
%{qt6dir}/qml/QtQuick3D/Helpers/*.qml
%{qt6dir}/qml/QtQuick3D/Helpers/meshes
%{qt6dir}/qml/QtQuick3D/Helpers/designer
%dir %{qt6dir}/qml/QtQuick3D/ParticleEffects
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/ParticleEffects/libqtquick3dparticleeffectsplugin.so
%{qt6dir}/qml/QtQuick3D/ParticleEffects/Quick3DParticleEffects.qmltypes
%{qt6dir}/qml/QtQuick3D/ParticleEffects/designer
%{qt6dir}/qml/QtQuick3D/ParticleEffects/qmldir
%dir %{qt6dir}/qml/QtQuick3D/Particles3D
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Particles3D/libqtquick3dparticles3dplugin.so
%{qt6dir}/qml/QtQuick3D/Particles3D/designer
%{qt6dir}/qml/QtQuick3D/Particles3D/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/Particles3D/qmldir

%files -n Qt6Quick3D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3D.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetImport.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetUtils.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DEffects.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DGlslParser.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DHelpers.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DIblBaker.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticleEffects.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticles.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DRuntimeRender.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DUtils.so
%{_libdir}/libQt6Quick3D.prl
%{_libdir}/libQt6Quick3DAssetImport.prl
%{_libdir}/libQt6Quick3DAssetUtils.prl
%{_libdir}/libQt6Quick3DEffects.prl
%{_libdir}/libQt6Quick3DGlslParser.prl
%{_libdir}/libQt6Quick3DHelpers.prl
%{_libdir}/libQt6Quick3DIblBaker.prl
%{_libdir}/libQt6Quick3DParticleEffects.prl
%{_libdir}/libQt6Quick3DParticles.prl
%{_libdir}/libQt6Quick3DRuntimeRender.prl
%{_libdir}/libQt6Quick3DUtils.prl
%{_includedir}/qt6/QtQuick3D
%{_includedir}/qt6/QtQuick3DAssetImport
%{_includedir}/qt6/QtQuick3DAssetUtils
%{_includedir}/qt6/QtQuick3DGlslParser
%{_includedir}/qt6/QtQuick3DHelpers
%{_includedir}/qt6/QtQuick3DIblBaker
%{_includedir}/qt6/QtQuick3DParticles
%{_includedir}/qt6/QtQuick3DRuntimeRender
%{_includedir}/qt6/QtQuick3DUtils
%{_pkgconfigdir}/Qt6Quick3D.pc
%{_pkgconfigdir}/Qt6Quick3DAssetImport.pc
%{_pkgconfigdir}/Qt6Quick3DRuntimeRender.pc
%{_pkgconfigdir}/Qt6Quick3DUtils.pc
%{_pkgconfigdir}/Qt6Quick3DAssetUtils.pc
%{_pkgconfigdir}/Qt6Quick3DEffects.pc
%{_pkgconfigdir}/Qt6Quick3DHelpers.pc
%{_pkgconfigdir}/Qt6Quick3DIblBaker.pc
%{_pkgconfigdir}/Qt6Quick3DParticleEffects.pc
%{_pkgconfigdir}/Qt6Quick3DParticles.pc
%{_libdir}/cmake/Qt6Quick3D
%{_libdir}/cmake/Qt6Quick3DAssetImport
%{_libdir}/cmake/Qt6Quick3DAssetUtils
%{_libdir}/cmake/Qt6Quick3DEffects
%{_libdir}/cmake/Qt6Quick3DGlslParserPrivate
%{_libdir}/cmake/Qt6Quick3DHelpers
%{_libdir}/cmake/Qt6Quick3DIblBaker
%{_libdir}/cmake/Qt6Quick3DParticleEffects
%{_libdir}/cmake/Qt6Quick3DParticles
%{_libdir}/cmake/Qt6Quick3DRuntimeRender
%{_libdir}/cmake/Qt6Quick3DTools
%{_libdir}/cmake/Qt6Quick3DUtils
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetimport.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetimport_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetutils.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetutils_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3deffects.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3deffects_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dglslparser_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpers.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpers_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3diblbaker.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3diblbaker_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dparticleeffects.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dparticleeffects_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dparticles.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dparticles_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3d.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3d_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3druntimerender.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3druntimerender_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dutils.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dutils_private.pri
%{_datadir}/qt6/modules/Quick3D.json
%{_datadir}/qt6/modules/Quick3DAssetImport.json
%{_datadir}/qt6/modules/Quick3DAssetUtils.json
%{_datadir}/qt6/modules/Quick3DEffects.json
%{_datadir}/qt6/modules/Quick3DGlslParserPrivate.json
%{_datadir}/qt6/modules/Quick3DHelpers.json
%{_datadir}/qt6/modules/Quick3DIblBaker.json
%{_datadir}/qt6/modules/Quick3DParticleEffects.json
%{_datadir}/qt6/modules/Quick3DParticles.json
%{_datadir}/qt6/modules/Quick3DRuntimeRender.json
%{_datadir}/qt6/modules/Quick3DUtils.json
%{_libdir}/metatypes/qt6quick3d_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dassetimport_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dassetutils_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3deffects_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dglslparserprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dhelpers_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3diblbaker_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dparticleeffects_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dparticles_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3druntimerender_pld_metatypes.json
%{_libdir}/metatypes/qt6quick3dutils_pld_metatypes.json

%if %{with doc}
%files -n Qt6Quick3D-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick3d

%files -n Qt6Quick3D-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick3d.qch
%endif

%files -n Qt6RemoteObjects
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6RemoteObjects.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6RemoteObjects.so.6
%attr(755,root,root) %{_libdir}/libQt6RemoteObjectsQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6RemoteObjectsQml.so.6
%attr(755,root,root) %{qt6dir}/libexec/repc
%dir %{qt6dir}/qml/QtRemoteObjects
%attr(755,root,root) %{qt6dir}/qml/QtRemoteObjects/libdeclarative_remoteobjectsplugin.so
%{qt6dir}/qml/QtRemoteObjects/plugins.qmltypes
%{qt6dir}/qml/QtRemoteObjects/qmldir

%files -n Qt6RemoteObjects-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6RemoteObjects.so
%attr(755,root,root) %{_libdir}/libQt6RemoteObjectsQml.so
%{_libdir}/libQt6RemoteObjects.prl
%{_libdir}/libQt6RemoteObjectsQml.prl
%{_includedir}/qt6/QtRemoteObjects
%{_includedir}/qt6/QtRemoteObjectsQml
%{_includedir}/qt6/QtRepParser
%{_pkgconfigdir}/Qt6RemoteObjects.pc
%{_pkgconfigdir}/Qt6RemoteObjectsQml.pc
%{_pkgconfigdir}/Qt6RepParser.pc
%{_libdir}/cmake/Qt6RemoteObjects
%{_libdir}/cmake/Qt6RemoteObjectsQml
%{_libdir}/cmake/Qt6RemoteObjectsTools
%{_libdir}/cmake/Qt6RepParser
%{qt6dir}/mkspecs/features/remoteobjects_repc.prf
%{qt6dir}/mkspecs/features/repc*.pri
%{qt6dir}/mkspecs/features/repparser.prf
%{qt6dir}/mkspecs/modules/qt_lib_remoteobjects.pri
%{qt6dir}/mkspecs/modules/qt_lib_remoteobjects_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_remoteobjectsqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_remoteobjectsqml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_repparser.pri
%{qt6dir}/mkspecs/modules/qt_lib_repparser_private.pri
%{_datadir}/qt6/modules/RemoteObjects.json
%{_datadir}/qt6/modules/RemoteObjectsQml.json
%{_datadir}/qt6/modules/RepParser.json
%{_libdir}/metatypes/qt6remoteobjects_pld_metatypes.json
%{_libdir}/metatypes/qt6remoteobjectsqml_pld_metatypes.json

%if %{with doc}
%files -n Qt6RemoteObjects-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtremoteobjects

%files -n Qt6RemoteObjects-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtremoteobjects.qch
%endif

%files -n Qt6Scxml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Scxml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Scxml.so.6
%attr(755,root,root) %{_libdir}/libQt6ScxmlQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ScxmlQml.so.6
%attr(755,root,root) %{qt6dir}/libexec/qscxmlc
%dir %{qt6dir}/qml/QtScxml
%attr(755,root,root) %{qt6dir}/qml/QtScxml/libdeclarative_scxmlplugin.so
%{qt6dir}/qml/QtScxml/plugins.qmltypes
%{qt6dir}/qml/QtScxml/qmldir
%dir %{qt6dir}/plugins/scxmldatamodel
%attr(755,root,root) %{qt6dir}/plugins/scxmldatamodel/libqscxmlecmascriptdatamodel.so

%files -n Qt6Scxml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Scxml.so
%attr(755,root,root) %{_libdir}/libQt6ScxmlQml.so
%{_libdir}/libQt6Scxml.prl
%{_libdir}/libQt6ScxmlQml.prl
%{_includedir}/qt6/QtScxml
%{_includedir}/qt6/QtScxmlQml
%{_pkgconfigdir}/Qt6Scxml.pc
%{_pkgconfigdir}/Qt6ScxmlQml.pc
%{_libdir}/cmake/Qt6Scxml
%{_libdir}/cmake/Qt6ScxmlQml
%{_libdir}/cmake/Qt6ScxmlTools
%{qt6dir}/mkspecs/features/qscxmlc.prf
%{qt6dir}/mkspecs/modules/qt_lib_scxml.pri
%{qt6dir}/mkspecs/modules/qt_lib_scxml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_scxmlqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_scxmlqml_private.pri
%{_datadir}/qt6/modules/Scxml.json
%{_datadir}/qt6/modules/ScxmlQml.json
%{_libdir}/metatypes/qt6scxml_pld_metatypes.json
%{_libdir}/metatypes/qt6scxmlqml_pld_metatypes.json

%if %{with doc}
%files -n Qt6Scxml-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtscxml

%files -n Qt6Scxml-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtscxml.qch
%endif

%files -n Qt6Sensors
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sensors.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Sensors.so.6
%attr(755,root,root) %{_libdir}/libQt6SensorsQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6SensorsQuick.so.6
%dir %{qt6dir}/plugins/sensors
%attr(755,root,root) %{qt6dir}/plugins/sensors/libqtsensors_dummy.so
%attr(755,root,root) %{qt6dir}/plugins/sensors/libqtsensors_generic.so
%attr(755,root,root) %{qt6dir}/plugins/sensors/libqtsensors_iio-sensor-proxy.so
%dir %{qt6dir}/qml/QtSensors
%attr(755,root,root) %{qt6dir}/qml/QtSensors/libsensorsquickplugin.so
%{qt6dir}/qml/QtSensors/plugins.qmltypes
%{qt6dir}/qml/QtSensors/qmldir

%files -n Qt6Sensors-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sensors.so
%attr(755,root,root) %{_libdir}/libQt6SensorsQuick.so
%{_libdir}/libQt6Sensors.prl
%{_libdir}/libQt6SensorsQuick.prl
%{_includedir}/qt6/QtSensors
%{_includedir}/qt6/QtSensorsQuick
%{_pkgconfigdir}/Qt6Sensors.pc
%{_pkgconfigdir}/Qt6SensorsQuick.pc
%{_libdir}/cmake/Qt6Sensors
%{_libdir}/cmake/Qt6SensorsQuick
%{qt6dir}/mkspecs/modules/qt_lib_sensors.pri
%{qt6dir}/mkspecs/modules/qt_lib_sensors_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_sensorsquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_sensorsquick_private.pri
%{_datadir}/qt6/modules/Sensors.json
%{_datadir}/qt6/modules/SensorsQuick.json
%{_libdir}/metatypes/qt6sensors_pld_metatypes.json
%{_libdir}/metatypes/qt6sensorsquick_pld_metatypes.json

%if %{with doc}
%files -n Qt6Sensors-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtsensors

%files -n Qt6Sensors-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtsensors.qch
%endif

%files -n Qt6SerialBus
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6SerialBus.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6SerialBus.so.6
%attr(755,root,root) %{qt6dir}/bin/canbusutil
%dir %{qt6dir}/plugins/canbus
%attr(755,root,root) %{qt6dir}/plugins/canbus/libqtpassthrucanbus.so
%attr(755,root,root) %{qt6dir}/plugins/canbus/libqtpeakcanbus.so
%attr(755,root,root) %{qt6dir}/plugins/canbus/libqtsocketcanbus.so
%attr(755,root,root) %{qt6dir}/plugins/canbus/libqttinycanbus.so
%attr(755,root,root) %{qt6dir}/plugins/canbus/libqtvirtualcanbus.so

%files -n Qt6SerialBus-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6SerialBus.so
%{_libdir}/libQt6SerialBus.prl
%{_includedir}/qt6/QtSerialBus
%{_pkgconfigdir}/Qt6SerialBus.pc
%{_libdir}/cmake/Qt6SerialBus
%{qt6dir}/mkspecs/modules/qt_lib_serialbus.pri
%{qt6dir}/mkspecs/modules/qt_lib_serialbus_private.pri
%{_datadir}/qt6/modules/SerialBus.json
%{_libdir}/metatypes/qt6serialbus_pld_metatypes.json

%if %{with doc}
%files -n Qt6SerialBus-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialbus

%files -n Qt6SerialBus-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialbus.qch
%endif

%files -n Qt6SerialPort -f qtserialport.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6SerialPort.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6SerialPort.so.6

%files -n Qt6SerialPort-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6SerialPort.so
%{_libdir}/libQt6SerialPort.prl
%{_includedir}/qt6/QtSerialPort
%{_pkgconfigdir}/Qt6SerialPort.pc
%{_libdir}/cmake/Qt6SerialPort
%{qt6dir}/mkspecs/modules/qt_lib_serialport.pri
%{qt6dir}/mkspecs/modules/qt_lib_serialport_private.pri
%{_datadir}/qt6/modules/SerialPort.json
%{_libdir}/metatypes/qt6serialport_pld_metatypes.json

%if %{with doc}
%files -n Qt6SerialPort-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialport

%files -n Qt6SerialPort-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialport.qch
%endif

%files -n qt6-shadertools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qsb-qt6
%attr(755,root,root) %{qt6dir}/bin/qsb

%files -n Qt6ShaderTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6ShaderTools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ShaderTools.so.6

%files -n Qt6ShaderTools-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6ShaderTools.so
%{_libdir}/libQt6ShaderTools.prl
%{_includedir}/qt6/QtShaderTools
%{_libdir}/cmake/Qt6ShaderTools
%{_libdir}/cmake/Qt6ShaderToolsTools
%{_libdir}/metatypes/qt6shadertools_pld_metatypes.json
%{_pkgconfigdir}/Qt6ShaderTools.pc
%{qt6dir}/mkspecs/modules/qt_lib_shadertools.pri
%{qt6dir}/mkspecs/modules/qt_lib_shadertools_private.pri
%{_datadir}/qt6/modules/ShaderTools.json

%if %{with doc}
%files -n Qt6ShaderTools-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtshadertools

%files -n Qt6ShaderTools-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtshadertools.qch
%endif

%files -n Qt6Sql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sql.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Sql.so.6
# loaded from src/sql/kernel/qsqldatabase.cpp
%dir %{qt6dir}/plugins/sqldrivers
# common for base -devel and plugin-specific files
%dir %{_libdir}/cmake/Qt6Sql

%if %{with db2}
%files -n Qt6Sql-sqldriver-db2
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqldb2.so
%{_libdir}/cmake/Qt6Sql/Qt6QDB2DriverPlugin*.cmake
%endif

%if %{with ibase}
%files -n Qt6Sql-sqldriver-ibase
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlibase.so
%{_libdir}/cmake/Qt6Sql/Qt6QIBaseDriverPlugin*.cmake
%endif

%if %{with sqlite3}
%files -n Qt6Sql-sqldriver-sqlite3
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlite.so
%{_libdir}/cmake/Qt6Sql/Qt6QSQLiteDriverPlugin*.cmake
%endif

%if %{with mysql}
%files -n Qt6Sql-sqldriver-mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlmysql.so
%{_libdir}/cmake/Qt6Sql/Qt6QMYSQLDriverPlugin*.cmake
%endif

%if %{with oci}
%files -n Qt6Sql-sqldriver-oci
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqloci.so
%{_libdir}/cmake/Qt6Sql/Qt6QOCIDriverPlugin*.cmake
%endif

%if %{with odbc}
%files -n Qt6Sql-sqldriver-odbc
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlodbc.so
%{_libdir}/cmake/Qt6Sql/Qt6QODBCDriverPlugin*.cmake
%endif

%if %{with pgsql}
%files -n Qt6Sql-sqldriver-pgsql
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqlpsql.so
%{_libdir}/cmake/Qt6Sql/Qt6QPSQLDriverPlugin*.cmake
%endif

%if %{with freetds}
%files -n Qt6Sql-sqldriver-tds
%defattr(644,root,root,755)
#%attr(755,root,root) %{qt6dir}/plugins/sqldrivers/libqsqltds.so
#%{_libdir}/cmake/Qt6Sql/Qt6QTDSDriverPlugin*.cmake
%endif

%files -n Qt6Sql-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sql.so
%{_libdir}/libQt6Sql.prl
%{_includedir}/qt6/QtSql
%{_pkgconfigdir}/Qt6Sql.pc
%{_libdir}/cmake/Qt6Sql/Qt6Sql*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_sql.pri
%{qt6dir}/mkspecs/modules/qt_lib_sql_private.pri
%{_datadir}/qt6/modules/Sql.json
%{_libdir}/metatypes/qt6sql_pld_metatypes.json

%files -n Qt6Svg
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Svg.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Svg.so.6
%attr(755,root,root) %{_libdir}/libQt6SvgWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6SvgWidgets.so.6
%attr(755,root,root) %{qt6dir}/plugins/iconengines/libqsvgicon.so
%attr(755,root,root) %{qt6dir}/plugins/imageformats/libqsvg.so

%files -n Qt6Svg-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Svg.so
%attr(755,root,root) %{_libdir}/libQt6SvgWidgets.so
%{_libdir}/libQt6Svg.prl
%{_libdir}/libQt6SvgWidgets.prl
%{_includedir}/qt6/QtSvg
%{_includedir}/qt6/QtSvgWidgets
%{_pkgconfigdir}/Qt6Svg.pc
%{_pkgconfigdir}/Qt6SvgWidgets.pc
%{_libdir}/cmake/Qt6Svg
%{_libdir}/cmake/Qt6SvgWidgets
%{_libdir}/cmake/Qt6Gui/Qt6QSvgIconPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QSvgPlugin*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_svg.pri
%{qt6dir}/mkspecs/modules/qt_lib_svg_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_svgwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_svgwidgets_private.pri
%{_datadir}/qt6/modules/Svg.json
%{_datadir}/qt6/modules/SvgWidgets.json
%{_libdir}/metatypes/qt6svg_pld_metatypes.json
%{_libdir}/metatypes/qt6svgwidgets_pld_metatypes.json

%if %{with doc}
%files -n Qt6Svg-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtsvg

%files -n Qt6Svg-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtsvg.qch
%endif

%files -n Qt6Test
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Test.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Test.so.6

%files -n Qt6Test-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Test.so
%{_libdir}/libQt6Test.prl
%{_includedir}/qt6/QtTest
%{_pkgconfigdir}/Qt6Test.pc
%{_libdir}/cmake/Qt6BuildInternals/QtStandaloneTestTemplateProject
%{_libdir}/cmake/Qt6BuildInternals/StandaloneTests
%{_libdir}/cmake/Qt6Test
%{qt6dir}/mkspecs/modules/qt_lib_testlib.pri
%{qt6dir}/mkspecs/modules/qt_lib_testlib_private.pri
%{_datadir}/qt6/modules/Test.json
%{_libdir}/metatypes/qt6test_pld_metatypes.json
%attr(755,root,root) %{qt6dir}/libexec/qt-internal-configure-tests
%attr(755,root,root) %{qt6dir}/libexec/qt-testrunner.py

%files -n Qt6UiTools
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6UiTools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6UiTools.so.6

%files -n Qt6UiTools-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6UiTools.so
%{_libdir}/libQt6UiTools.prl
%{_includedir}/qt6/QtUiPlugin
%{_includedir}/qt6/QtUiTools
%{_pkgconfigdir}/Qt6UiPlugin.pc
%{_pkgconfigdir}/Qt6UiTools.pc
%{_libdir}/cmake/Qt6UiPlugin
%{_libdir}/cmake/Qt6UiTools
%{qt6dir}/mkspecs/modules/qt_lib_uiplugin.pri
%{qt6dir}/mkspecs/modules/qt_lib_uitools.pri
%{qt6dir}/mkspecs/modules/qt_lib_uitools_private.pri
%{_datadir}/qt6/modules/UiPlugin.json
%{_datadir}/qt6/modules/UiTools.json
%{_libdir}/metatypes/qt6uitools_pld_metatypes.json

%files -n Qt6VirtualKeyboard
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6HunspellInputMethod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6HunspellInputMethod.so.6
%attr(755,root,root) %{_libdir}/libQt6VirtualKeyboard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6VirtualKeyboard.so.6
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libqtvirtualkeyboardplugin.so
%dir %{qt6dir}/plugins/virtualkeyboard
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_hangul.so
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_hunspell.so
%if %{with lipi}
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_lipi.so
%endif
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_openwnn.so
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_pinyin.so
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_tcime.so
%attr(755,root,root) %{qt6dir}/plugins/virtualkeyboard/libqtvirtualkeyboard_thai.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/libqtquickvirtualkeyboardplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/qmldir
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/libqtquickvirtualkeyboardsettingsplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/qmldir
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/libqtquickvirtualkeyboardstylesplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/qmldir
%if %{with lipi}
%dir %{qt6dir}/plugins/lipi_toolkit
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libactivedtw.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libboxfld.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libl7.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/liblipiengine.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/liblogger.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libneuralnet.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libnn.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libnpen.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libpointfloat.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libpreproc.so
%attr(755,root,root) %{qt6dir}/plugins/lipi_toolkit/libsubstroke.so
%dir %{_datadir}/qt6/qtvirtualkeyboard
%{_datadir}/qt6/qtvirtualkeyboard/lipi_toolkit
%endif

%files -n Qt6VirtualKeyboard-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6HunspellInputMethod.so
%attr(755,root,root) %{_libdir}/libQt6VirtualKeyboard.so
%{_libdir}/libQt6HunspellInputMethod.prl
%{_libdir}/libQt6VirtualKeyboard.prl
%{_includedir}/qt6/QtHunspellInputMethod
%{_includedir}/qt6/QtVirtualKeyboard
%{_pkgconfigdir}/Qt6VirtualKeyboard.pc
%{_libdir}/cmake/Qt6Gui/Qt6QVirtualKeyboardPlugin*.cmake
%{_libdir}/cmake/Qt6VirtualKeyboard
%{_libdir}/cmake/Qt6HunspellInputMethodPrivate
%{qt6dir}/mkspecs/modules/qt_lib_hunspellinputmethod_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboard.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboard_private.pri
%{_datadir}/qt6/modules/HunspellInputMethodPrivate.json
%{_datadir}/qt6/modules/VirtualKeyboard.json
%{_libdir}/metatypes/qt6virtualkeyboard_pld_metatypes.json
%{_libdir}/metatypes/qt6hunspellinputmethodprivate_pld_metatypes.json

%if %{with doc}
%files -n Qt6VirtualKeyboard-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtvirtualkeyboard

%files -n Qt6VirtualKeyboard-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtvirtualkeyboard.qch
%endif

%files -n Qt6WaylandCompositor
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositor.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandEglCompositorHwIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandEglCompositorHwIntegration.so.6
%attr(755,root,root) %{_libdir}/libQt6WlShellIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WlShellIntegration.so.6
%dir %{qt6dir}/plugins/wayland-graphics-integration-server
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-dmabuf-server-buffer.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-drm-egl-server-buffer.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-linux-dmabuf-unstable-v1.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-shm-emulation-server.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-vulkan-server.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-egl.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-server/libqt-wayland-compositor-wayland-eglstream-controller.so
# dir shared Qt6WaylandClient
%dir %{qt6dir}/qml/QtWayland
%dir %{qt6dir}/qml/QtWayland/Compositor
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/libqwaylandcompositorplugin.so
%{qt6dir}/qml/QtWayland/Compositor/qmldir
%{qt6dir}/qml/QtWayland/Compositor/WaylandCompositor.qmltypes
%dir %{qt6dir}/qml/QtWayland/Compositor/TextureSharingExtension
%{qt6dir}/qml/QtWayland/Compositor/qmlfiles
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/TextureSharingExtension/libwaylandtexturesharingextensionplugin.so
%{qt6dir}/qml/QtWayland/Compositor/TextureSharingExtension/qmldir
%dir %{qt6dir}/qml/QtWayland/Compositor/IviApplication
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/IviApplication/libwaylandcompositoriviapplicationplugin.so
%{qt6dir}/qml/QtWayland/Compositor/IviApplication/plugins.qmltypes
%{qt6dir}/qml/QtWayland/Compositor/IviApplication/qmldir
%dir %{qt6dir}/qml/QtWayland/Compositor/PresentationTime
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/PresentationTime/libwaylandcompositorpresentationtimeplugin.so
%{qt6dir}/qml/QtWayland/Compositor/PresentationTime/qmldir
%dir %{qt6dir}/qml/QtWayland/Compositor/QtShell
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/QtShell/libwaylandcompositorqtshellplugin.so
%{qt6dir}/qml/QtWayland/Compositor/QtShell/plugins.qmltypes
%{qt6dir}/qml/QtWayland/Compositor/QtShell/qmldir
%dir %{qt6dir}/qml/QtWayland/Compositor/WlShell
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/WlShell/libwaylandcompositorwlshellplugin.so
%{qt6dir}/qml/QtWayland/Compositor/WlShell/plugins.qmltypes
%{qt6dir}/qml/QtWayland/Compositor/WlShell/qmldir
%dir %{qt6dir}/qml/QtWayland/Compositor/XdgShell
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Compositor/XdgShell/libwaylandcompositorxdgshellplugin.so
%{qt6dir}/qml/QtWayland/Compositor/XdgShell/plugins.qmltypes
%{qt6dir}/qml/QtWayland/Compositor/XdgShell/qmldir

%files -n Qt6WaylandCompositor-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositor.so
%attr(755,root,root) %{_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%attr(755,root,root) %{_libdir}/libQt6WlShellIntegration.so
%{_libdir}/libQt6WaylandCompositor.prl
%{_libdir}/libQt6WlShellIntegration.prl
%{_libdir}/libQt6WaylandEglCompositorHwIntegration.prl
%{_includedir}/qt6/QtWaylandCompositor
%{_includedir}/qt6/QtWaylandEglCompositorHwIntegration
%{_includedir}/qt6/QtWaylandGlobal
%{_includedir}/qt6/QtWlShellIntegration
%{_pkgconfigdir}/Qt6WaylandCompositor.pc
%{_libdir}/cmake/Qt6WaylandCompositor
%{_libdir}/cmake/Qt6WaylandGlobalPrivate
%{_libdir}/cmake/Qt6WlShellIntegrationPrivate
%{_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositor.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositor_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wayland_egl_compositor_hw_integration_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandglobal_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wl_shell_integration_private.pri
%{_datadir}/qt6/modules/WaylandCompositor.json
%{_datadir}/qt6/modules/WaylandEglCompositorHwIntegrationPrivate.json
%{_datadir}/qt6/modules/WaylandGlobalPrivate.json
%{_datadir}/qt6/modules/WlShellIntegrationPrivate.json
%{_libdir}/metatypes/qt6waylandcompositor_pld_metatypes.json
%{_libdir}/metatypes/qt6waylandeglcompositorhwintegrationprivate_pld_metatypes.json
%{_libdir}/metatypes/qt6wlshellintegrationprivate_pld_metatypes.json

%if %{with doc}
%files -n Qt6WaylandCompositor-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwaylandcompositor

%files -n Qt6WaylandCompositor-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwaylandcompositor.qch
%endif

%files -n Qt6WaylandClient
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WaylandClient.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandClient.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandEglClientHwIntegration.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandEglClientHwIntegration.so.6
%attr(755,root,root) %{qt6dir}/libexec/qtwaylandscanner
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqwayland-egl.so
%attr(755,root,root) %{qt6dir}/plugins/platforms/libqwayland-generic.so
%dir %{qt6dir}/plugins/wayland-decoration-client
%attr(755,root,root) %{qt6dir}/plugins/wayland-decoration-client/libbradient.so
%dir %{qt6dir}/plugins/wayland-graphics-integration-client
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-client/libdmabuf-server.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-client/libdrm-egl-server.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-client/libqt-plugin-wayland-egl.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-client/libshm-emulation-server.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-graphics-integration-client/libvulkan-server.so
%dir %{qt6dir}/plugins/wayland-shell-integration
%attr(755,root,root) %{qt6dir}/plugins/wayland-shell-integration/libfullscreen-shell-v1.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-shell-integration/libivi-shell.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-shell-integration/libqt-shell.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-shell-integration/libwl-shell-plugin.so
%attr(755,root,root) %{qt6dir}/plugins/wayland-shell-integration/libxdg-shell.so
# dir shared Qt6WaylandCompositor
%dir %{qt6dir}/qml/QtWayland
%dir %{qt6dir}/qml/QtWayland/Client
%dir %{qt6dir}/qml/QtWayland/Client/TextureSharing
%attr(755,root,root) %{qt6dir}/qml/QtWayland/Client/TextureSharing/libwaylandtexturesharingplugin.so
%{qt6dir}/qml/QtWayland/Client/TextureSharing/qmldir

%files -n Qt6WaylandClient-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WaylandClient.so
%attr(755,root,root) %{_libdir}/libQt6WaylandEglClientHwIntegration.so
%{_libdir}/libQt6WaylandClient.prl
%{_libdir}/libQt6WaylandEglClientHwIntegration.prl
%{_includedir}/qt6/QtWaylandClient
%{_includedir}/qt6/QtWaylandEglClientHwIntegration
%{_pkgconfigdir}/Qt6WaylandClient.pc
%{_libdir}/cmake/Qt6Gui/Qt6QWaylandEglPlatformIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6Gui/Qt6QWaylandIntegrationPlugin*.cmake
%{_libdir}/cmake/Qt6WaylandClient
%{_libdir}/cmake/Qt6WaylandScannerTools
%{_libdir}/cmake/Qt6WaylandEglClientHwIntegrationPrivate
%{qt6dir}/mkspecs/modules/qt_lib_waylandclient.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandclient_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wayland_egl_client_hw_integration_private.pri
%{_datadir}/qt6/modules/WaylandClient.json
%{_datadir}/qt6/modules/WaylandEglClientHwIntegrationPrivate.json
%{_libdir}/metatypes/qt6waylandclient_pld_metatypes.json
%{_libdir}/metatypes/qt6waylandeglclienthwintegrationprivate_pld_metatypes.json

%files -n Qt6Widgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Widgets.so.6
%dir %{qt6dir}/plugins/styles

%files -n Qt6Widgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so
%{_libdir}/libQt6Widgets.prl
%{_libdir}/metatypes/qt6widgets_pld_metatypes.json
%{_includedir}/qt6/QtWidgets
%{_pkgconfigdir}/Qt6Widgets.pc
%{_libdir}/cmake/Qt6Widgets
%{_libdir}/cmake/Qt6WidgetsTools
%{qt6dir}/mkspecs/modules/qt_lib_widgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_widgets_private.pri
%{_datadir}/qt6/modules/Widgets.json

%files -n Qt6WebChannel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebChannel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebChannel.so.6
%dir %{qt6dir}/qml/QtWebChannel
%attr(755,root,root) %{qt6dir}/qml/QtWebChannel/libwebchannelplugin.so
%{qt6dir}/qml/QtWebChannel/plugins.qmltypes
%{qt6dir}/qml/QtWebChannel/qmldir

%files -n Qt6WebChannel-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebChannel.so
%{_libdir}/libQt6WebChannel.prl
%{_includedir}/qt6/QtWebChannel
%{_pkgconfigdir}/Qt6WebChannel.pc
%{_libdir}/cmake/Qt6WebChannel
%{qt6dir}/mkspecs/modules/qt_lib_webchannel.pri
%{qt6dir}/mkspecs/modules/qt_lib_webchannel_private.pri
%{_datadir}/qt6/modules/WebChannel.json
%{_libdir}/metatypes/qt6webchannel_pld_metatypes.json

%if %{with doc}
%files -n Qt6WebChannel-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebchannel

%files -n Qt6WebChannel-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebchannel.qch
%endif

%if %{with webengine}
%files -n Qt6WebEngine -f qtwebengine.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebEngineCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebEngineCore.so.6
%attr(755,root,root) %{_libdir}/libQt6WebEngineQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebEngineQuick.so.6
%attr(755,root,root) %{_libdir}/libQt6WebEngineQuickDelegatesQml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebEngineQuickDelegatesQml.so.6
%attr(755,root,root) %{_libdir}/libQt6WebEngineWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebEngineWidgets.so.6
%dir %{qt6dir}/qml/QtWebEngine
%{qt6dir}/qml/QtWebEngine/plugins.qmltypes
%{qt6dir}/qml/QtWebEngine/qmldir
%{qt6dir}/qml/QtWebEngine/ControlsDelegates
%attr(755,root,root) %{qt6dir}/qml/QtWebEngine/libqtwebenginequickplugin.so
%dir %{_datadir}/qt6/resources
%{_datadir}/qt6/resources/qtwebengine*.pak
%dir %{_datadir}/qt6/translations/qtwebengine_locales
%lang(am) %{_datadir}/qt6/translations/qtwebengine_locales/am.pak
%lang(ar) %{_datadir}/qt6/translations/qtwebengine_locales/ar.pak
%lang(bg) %{_datadir}/qt6/translations/qtwebengine_locales/bg.pak
%lang(bn) %{_datadir}/qt6/translations/qtwebengine_locales/bn.pak
%lang(ca) %{_datadir}/qt6/translations/qtwebengine_locales/ca.pak
%lang(cs) %{_datadir}/qt6/translations/qtwebengine_locales/cs.pak
%lang(da) %{_datadir}/qt6/translations/qtwebengine_locales/da.pak
%lang(de) %{_datadir}/qt6/translations/qtwebengine_locales/de.pak
%lang(el) %{_datadir}/qt6/translations/qtwebengine_locales/el.pak
%lang(en) %{_datadir}/qt6/translations/qtwebengine_locales/en-GB.pak
%lang(en) %{_datadir}/qt6/translations/qtwebengine_locales/en-US.pak
%lang(es) %{_datadir}/qt6/translations/qtwebengine_locales/es.pak
%lang(es_AR,es_BO,es_CL,es_CO,es_CR,es_CU,es_DO,es_EC,es_GT,es_HN,es_MX,es_NI,es_PA,es_PE,es_PR,es_PY,es_SV,es_UY,es_VE) %{_datadir}/qt6/translations/qtwebengine_locales/es-419.pak
%lang(et) %{_datadir}/qt6/translations/qtwebengine_locales/et.pak
%lang(fa) %{_datadir}/qt6/translations/qtwebengine_locales/fa.pak
%lang(fi) %{_datadir}/qt6/translations/qtwebengine_locales/fi.pak
%lang(fil) %{_datadir}/qt6/translations/qtwebengine_locales/fil.pak
%lang(fr) %{_datadir}/qt6/translations/qtwebengine_locales/fr.pak
%lang(gu) %{_datadir}/qt6/translations/qtwebengine_locales/gu.pak
%lang(he) %{_datadir}/qt6/translations/qtwebengine_locales/he.pak
%lang(hi) %{_datadir}/qt6/translations/qtwebengine_locales/hi.pak
%lang(hr) %{_datadir}/qt6/translations/qtwebengine_locales/hr.pak
%lang(hu) %{_datadir}/qt6/translations/qtwebengine_locales/hu.pak
%lang(id) %{_datadir}/qt6/translations/qtwebengine_locales/id.pak
%lang(it) %{_datadir}/qt6/translations/qtwebengine_locales/it.pak
%lang(ja) %{_datadir}/qt6/translations/qtwebengine_locales/ja.pak
%lang(kn) %{_datadir}/qt6/translations/qtwebengine_locales/kn.pak
%lang(ko) %{_datadir}/qt6/translations/qtwebengine_locales/ko.pak
%lang(lt) %{_datadir}/qt6/translations/qtwebengine_locales/lt.pak
%lang(lv) %{_datadir}/qt6/translations/qtwebengine_locales/lv.pak
%lang(ml) %{_datadir}/qt6/translations/qtwebengine_locales/ml.pak
%lang(mr) %{_datadir}/qt6/translations/qtwebengine_locales/mr.pak
%lang(ms) %{_datadir}/qt6/translations/qtwebengine_locales/ms.pak
%lang(nb) %{_datadir}/qt6/translations/qtwebengine_locales/nb.pak
%lang(nl) %{_datadir}/qt6/translations/qtwebengine_locales/nl.pak
%lang(pl) %{_datadir}/qt6/translations/qtwebengine_locales/pl.pak
%lang(pt_BR) %{_datadir}/qt6/translations/qtwebengine_locales/pt-BR.pak
%lang(pt) %{_datadir}/qt6/translations/qtwebengine_locales/pt-PT.pak
%lang(ro) %{_datadir}/qt6/translations/qtwebengine_locales/ro.pak
%lang(ru) %{_datadir}/qt6/translations/qtwebengine_locales/ru.pak
%lang(sk) %{_datadir}/qt6/translations/qtwebengine_locales/sk.pak
%lang(sl) %{_datadir}/qt6/translations/qtwebengine_locales/sl.pak
%lang(sr) %{_datadir}/qt6/translations/qtwebengine_locales/sr.pak
%lang(sv) %{_datadir}/qt6/translations/qtwebengine_locales/sv.pak
%lang(sw) %{_datadir}/qt6/translations/qtwebengine_locales/sw.pak
%lang(ta) %{_datadir}/qt6/translations/qtwebengine_locales/ta.pak
%lang(te) %{_datadir}/qt6/translations/qtwebengine_locales/te.pak
%lang(th) %{_datadir}/qt6/translations/qtwebengine_locales/th.pak
%lang(tr) %{_datadir}/qt6/translations/qtwebengine_locales/tr.pak
%lang(uk) %{_datadir}/qt6/translations/qtwebengine_locales/uk.pak
%lang(vi) %{_datadir}/qt6/translations/qtwebengine_locales/vi.pak
%lang(zh_CN) %{_datadir}/qt6/translations/qtwebengine_locales/zh-CN.pak
%lang(zh_TW) %{_datadir}/qt6/translations/qtwebengine_locales/zh-TW.pak
%attr(755,root,root) %{_libdir}/qt6/libexec/qwebengine_convert_dict
%attr(755,root,root) %{_libdir}/qt6/libexec/QtWebEngineProcess

%files -n Qt6WebEngine-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebEngineCore.so
%attr(755,root,root) %{_libdir}/libQt6WebEngineQuick.so
%attr(755,root,root) %{_libdir}/libQt6WebEngineQuickDelegatesQml.so
%attr(755,root,root) %{_libdir}/libQt6WebEngineWidgets.so
%{_libdir}/libQt6WebEngineCore.prl
%{_libdir}/libQt6WebEngineQuick.prl
%{_libdir}/libQt6WebEngineQuickDelegatesQml.prl
%{_libdir}/libQt6WebEngineWidgets.prl
%{_includedir}/qt6/QtWebEngineCore
%{_includedir}/qt6/QtWebEngineQuick
%{_includedir}/qt6/QtWebEngineWidgets
%{_pkgconfigdir}/Qt6WebEngineCore.pc
%{_pkgconfigdir}/Qt6WebEngineQuick.pc
%{_pkgconfigdir}/Qt6WebEngineQuickDelegatesQml.pc
%{_pkgconfigdir}/Qt6WebEngineWidgets.pc
%{_libdir}/cmake/Qt6WebEngineCore
%{_libdir}/cmake/Qt6WebEngineCoreTools
%{_libdir}/cmake/Qt6WebEngineQuick
%{_libdir}/cmake/Qt6WebEngineQuickDelegatesQml
%{_libdir}/cmake/Qt6WebEngineWidgets
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequickdelegatesqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequickdelegatesqml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets_private.pri
%{_datadir}/qt6/modules/WebEngineCore.json
%{_datadir}/qt6/modules/WebEngineQuick.json
%{_datadir}/qt6/modules/WebEngineQuickDelegatesQml.json
%{_datadir}/qt6/modules/WebEngineWidgets.json
%{_libdir}/metatypes/qt6webenginecore_pld_metatypes.json
%{_libdir}/metatypes/qt6webenginequick_pld_metatypes.json
%{_libdir}/metatypes/qt6webenginequickdelegatesqml_pld_metatypes.json
%{_libdir}/metatypes/qt6webenginewidgets_pld_metatypes.json

%files -n Qt6Designer-plugin-qwebengineview
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/qt6/plugins/designer/libqwebengineview.so
%{_libdir}/cmake/Qt6Designer/Qt6QWebEngineViewPlugin*.cmake

%if %{with doc}
%files -n Qt6WebEngine-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebengine

%files -n Qt6WebEngine-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebengine.qch
%endif
%endif

%files -n Qt6WebSockets -f qtwebsockets.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebSockets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebSockets.so.6
%dir %{qt6dir}/qml/QtWebSockets
%attr(755,root,root) %{qt6dir}/qml/QtWebSockets/libqmlwebsocketsplugin.so
%{qt6dir}/qml/QtWebSockets/plugins.qmltypes
%{qt6dir}/qml/QtWebSockets/qmldir

%files -n Qt6WebSockets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebSockets.so
%{_libdir}/libQt6WebSockets.prl
%{_includedir}/qt6/QtWebSockets
%{_pkgconfigdir}/Qt6WebSockets.pc
%{_libdir}/cmake/Qt6WebSockets
%{qt6dir}/mkspecs/modules/qt_lib_websockets.pri
%{qt6dir}/mkspecs/modules/qt_lib_websockets_private.pri
%{_datadir}/qt6/modules/WebSockets.json
%{_libdir}/metatypes/qt6websockets_pld_metatypes.json

%if %{with doc}
%files -n Qt6WebSockets-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebsockets

%files -n Qt6WebSockets-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebsockets.qch
%endif

%files -n Qt6WebView
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebView.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebView.so.6
%attr(755,root,root) %{_libdir}/libQt6WebViewQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebViewQuick.so.6
%dir %{qt6dir}/plugins/webview
%dir %{qt6dir}/qml/QtWebView
%attr(755,root,root) %{qt6dir}/qml/QtWebView/libqtwebviewquickplugin.so
%{qt6dir}/qml/QtWebView/plugins.qmltypes
%{qt6dir}/qml/QtWebView/qmldir

%files -n Qt6WebView-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebView.so
%attr(755,root,root) %{_libdir}/libQt6WebViewQuick.so
%{_libdir}/libQt6WebView.prl
%{_libdir}/libQt6WebViewQuick.prl
%{_includedir}/qt6/QtWebView
%{_includedir}/qt6/QtWebViewQuick
%{_pkgconfigdir}/Qt6WebView.pc
%{_pkgconfigdir}/Qt6WebViewQuick.pc
%{_libdir}/cmake/Qt6WebView
%{_libdir}/cmake/Qt6WebViewQuick
%{qt6dir}/mkspecs/modules/qt_lib_webview.pri
%{qt6dir}/mkspecs/modules/qt_lib_webview_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webviewquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webviewquick_private.pri
%{_datadir}/qt6/modules/WebView.json
%{_datadir}/qt6/modules/WebViewQuick.json
%{_libdir}/metatypes/qt6webview_pld_metatypes.json
%{_libdir}/metatypes/qt6webviewquick_pld_metatypes.json

%if %{with webengine}
%files -n Qt6WebView-plugin-webengine
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/webview/libqtwebview_webengine.so
%{_libdir}/cmake/Qt6WebView/Qt6QWebEngineWebViewPlugin*.cmake
%endif

%if %{with doc}
%files -n Qt6WebView-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebview

%files -n Qt6WebView-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebview.qch
%endif


%files -n Qt6Xml
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Xml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Xml.so.6

%files -n Qt6Xml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Xml.so
%{_libdir}/libQt6Xml.prl
%{_includedir}/qt6/QtXml
%{_pkgconfigdir}/Qt6Xml.pc
%{_libdir}/cmake/Qt6Xml
%{qt6dir}/mkspecs/modules/qt_lib_xml.pri
%{qt6dir}/mkspecs/modules/qt_lib_xml_private.pri
%{_datadir}/qt6/modules/Xml.json
%{_libdir}/metatypes/qt6xml_pld_metatypes.json

%files -n qt6-doc-common
%defattr(644,root,root,755)
%dir %{_docdir}/qt6-doc
%{_docdir}/qt6-doc/config
%{_docdir}/qt6-doc/global

%if %{with doc}
%files doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtdoc
%{_docdir}/qt6-doc/qmake
%{_docdir}/qt6-doc/qtcmake
%{_docdir}/qt6-doc/qtconcurrent
%{_docdir}/qt6-doc/qtcore
%{_docdir}/qt6-doc/qtdbus
%{_docdir}/qt6-doc/qtgui
%{_docdir}/qt6-doc/qtimageformats
%{_docdir}/qt6-doc/qtnetwork
%{_docdir}/qt6-doc/qtopengl
%{_docdir}/qt6-doc/qtprintsupport
%{_docdir}/qt6-doc/qtsql
%{_docdir}/qt6-doc/qttestlib
%{_docdir}/qt6-doc/qtwidgets
%{_docdir}/qt6-doc/qtxml

%files doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtdoc.qch
%{_docdir}/qt6-doc/qmake.qch
%{_docdir}/qt6-doc/qtcmake.qch
%{_docdir}/qt6-doc/qtconcurrent.qch
%{_docdir}/qt6-doc/qtcore.qch
%{_docdir}/qt6-doc/qtdbus.qch
%{_docdir}/qt6-doc/qtgui.qch
%{_docdir}/qt6-doc/qtimageformats.qch
%{_docdir}/qt6-doc/qtnetwork.qch
%{_docdir}/qt6-doc/qtopengl.qch
%{_docdir}/qt6-doc/qtprintsupport.qch
%{_docdir}/qt6-doc/qtsql.qch
%{_docdir}/qt6-doc/qttestlib.qch
%{_docdir}/qt6-doc/qtwidgets.qch
%{_docdir}/qt6-doc/qtxml.qch
%endif

%files examples
%defattr(644,root,root,755)
%{_examplesdir}/qt6

%files -n qt6-build
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qt-cmake-qt6
%attr(755,root,root) %{_bindir}/moc-qt6
%attr(755,root,root) %{_bindir}/qdbuscpp2xml-qt6
%attr(755,root,root) %{_bindir}/qdbusxml2cpp-qt6
%attr(755,root,root) %{_bindir}/qdoc-qt6
%attr(755,root,root) %{_bindir}/qlalr-qt6
%attr(755,root,root) %{_bindir}/qmake-qt6
%attr(755,root,root) %{_bindir}/rcc-qt6
%attr(755,root,root) %{_bindir}/uic-qt6
%attr(755,root,root) %{qt6dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt6dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt6dir}/bin/qmake
%attr(755,root,root) %{qt6dir}/bin/qmake6
%attr(755,root,root) %{qt6dir}/bin/qt-cmake
%attr(755,root,root) %{qt6dir}/bin/qt-cmake-private
%attr(755,root,root) %{qt6dir}/bin/qt-cmake-private-install.cmake
%attr(755,root,root) %{qt6dir}/bin/qt-cmake-standalone-test
%attr(755,root,root) %{qt6dir}/libexec/moc
%attr(755,root,root) %{qt6dir}/libexec/qlalr
%attr(755,root,root) %{qt6dir}/libexec/rcc
%attr(755,root,root) %{qt6dir}/libexec/syncqt.pl
%attr(755,root,root) %{qt6dir}/libexec/uic
%attr(755,root,root) %{qt6dir}/libexec/cmake_automoc_parser
%attr(755,root,root) %{qt6dir}/libexec/ensure_pro_file.cmake
%{qt6dir}/mkspecs/aix-*
%{qt6dir}/mkspecs/android-*
%{qt6dir}/mkspecs/common
%{qt6dir}/mkspecs/cygwin-*
%{qt6dir}/mkspecs/darwin-*
%{qt6dir}/mkspecs/devices
%{qt6dir}/mkspecs/dummy
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
%{qt6dir}/mkspecs/*.pri
%{qt6dir}/mkspecs/qnx-*
%{qt6dir}/mkspecs/solaris-*
%{qt6dir}/mkspecs/unsupported
%{qt6dir}/mkspecs/wasm-emscripten
%{qt6dir}/mkspecs/win32-*
