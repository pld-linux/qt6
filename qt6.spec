# Note on packaging .cmake files for plugins:
# Base Qt6${component}Config.cmake file includes all existing Qt6${component}_*Plugin.cmake
# files, which trigger check for presence of plugin module in filesystem.
# Thus, for plugins separated into subpackages, we package plugins .cmake file
# together with module, and the rest of .cmake files in appropriate -devel subpackage.
#
# TODO:
# - unpackaged files:
#   /usr/lib64/qt6/libexec/gn
#   /usr/lib64/qt6/mkspecs/modules/README
#   /usr/share/qt6/translations/catalogs.json
# - -doc/-doc-qch mess: make packages per library (then split qt6-doc and qt6-doc-qch) or per submodule (like in qt5)?
#
# Conditional build:
# -- build targets
%bcond_without	doc		# Documentation
%bcond_without	qt3d		# Qt 3d
%bcond_without	qtquick3d	# Qt Quick3d
%bcond_without	qtquick3dphysics	# Qt Quick3d Physics
%bcond_without	qtwebengine	# Qt WebEngine
# -- features
%bcond_without	cups		# CUPS printing support
%bcond_with	directfb	# DirectFB platform support
%bcond_without	egl		# EGL (EGLFS, minimal EGL) platform support
%bcond_with	fbx		# Autodesk FBX SDK support (proprietary)
%bcond_without	gtk		# GTK+ theme integration
%bcond_without	kerberos5	# KRB5 GSSAPI Support
%bcond_without	kms		# KMS platform support
%bcond_without	libinput	# libinput support
%bcond_with	opengl_desktop	# Use "desktop" OpenGL API
%bcond_without	openxr		# XR devices support
%bcond_with	gles		# Use OpenGL ES API
%bcond_without	pch		# pch (pre-compiled headers) in qmake
%bcond_without	statx		# build without statx()
%bcond_with	systemd		# logging to journald
%bcond_without	tslib		# tslib support
# -- databases
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
# -- system libraries
%bcond_with	qtwebengine_system_ffmpeg	# use system FFmpeg in qtwebengine
%bcond_with	qtwebengine_system_libvpx	# use system libvpx in qtwebengine (build fails QTBUG-129955)

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
%ifnarch %{x8664} aarch64
%undefine	with_qtwebengine
%endif
%if %{without qtquick3d}
%undefine	with_qtquick3dphysics
%endif
%ifarch %{x86_with_sse} %{arm_with_neon}
%define		with_simd	1
%endif
%ifnarch %{x86_with_sse2} %{arm_with_neon}
%undefine	with_qtquick3dphysics
%endif
%ifarch x32
%undefine	with_qtquick3dphysics
%endif
%define		specflags	%{!?with_simd:-DDISABLE_SIMD -DPFFFT_SIMD_DISABLE}

%define		icu_abi		73
%define		next_icu_abi	%(echo $((%{icu_abi} + 1)))

%if %{without opengl_desktop} && %{without gles}
%ifarch %{arm} aarch64
%define		with_gles		1
%else
%define		with_opengl_desktop	1
%endif
%endif

%ifarch %{x8664} aarch64 armv7hl armv7hnl pentium4
%define		with_qml_jit	1
%endif

%if %{without qtquick3d}
%undefine	with_openxr
%endif

Summary:	Qt6 Library
Summary(pl.UTF-8):	Biblioteka Qt6
Name:		qt6
Version:	6.8.1
Release:	1
License:	LGPL v3 or GPL v2 or GPL v3 or commercial
Group:		X11/Libraries
Source0:	https://download.qt.io/official_releases/qt/6.8/%{version}/single/qt-everywhere-src-%{version}.tar.xz
# Source0-md5:	4068b07ca6366bcb9ba56508bbbf20e6
Patch0:		system-cacerts.patch
Patch1:		ninja-program.patch
Patch2:		arm-no-xnnpack.patch
Patch3:		no-implicit-sse2.patch
Patch4:		x32.patch
Patch5:		qtwebengine-cmake-build-type.patch
Patch6:		qtquick3d-6.6.2-gcc14.patch
URL:		https://www.qt.io/
%{?with_directfb:BuildRequires:	DirectFB-devel}
BuildRequires:	EGL-devel
%{?with_ibase:BuildRequires:	Firebird-devel}
BuildRequires:	GConf2-devel
%if %{with kms} || %{with qtwebengine}
BuildRequires:	Mesa-libgbm-devel
%endif
BuildRequires:	OpenGL-devel
%if %{with kms} || %{with gles}
BuildRequires:	OpenGLESv2-devel
%endif
%{?with_gles:BuildRequires:	OpenGLESv3-devel}
%{?with_openxr:BuildRequires:	OpenXR-devel >= 1.0.29}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	alsa-lib-devel
%if %{with qt3d} || %{with qtquick3d}
BuildRequires:	assimp-devel >= 5
%endif
BuildRequires:	at-spi2-core-devel
%{?with_qtwebengine:BuildRequires:	bison}
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
%if %{with qtwebengine} && %{with qtwebengine_system_ffmpeg}
BuildRequires:	ffmpeg-devel < 5.0
%endif
%{?with_qtwebengine:BuildRequires:	flex}
BuildRequires:	flite-devel
BuildRequires:	fontconfig-devel
BuildRequires:	freetype-devel >= 2.2.0
%{?with_pch:BuildRequires:	gcc >= 5:4.0}
BuildRequires:	gdb
BuildRequires:	glib2-devel >= 1:2.32.0
%{?with_qtwebengine:BuildRequires:	glibc-headers >= 6:2.16}
%{?with_qtwebengine:BuildRequires:	gperf}
BuildRequires:	grpc-devel
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-gl-devel >= 1.0
BuildRequires:	gstreamer-plugins-bad-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%{?with_gtk:BuildRequires:	gtk+3-devel >= 3.6}
BuildRequires:	gypsy-devel
BuildRequires:	harfbuzz-devel >= 2.9.0
BuildRequires:	harfbuzz-subset-devel >= 2.9.0
%{?with_kerberos5:BuildRequires:	heimdal-devel}
BuildRequires:	hunspell-devel
BuildRequires:	jasper-devel
%{?with_qtwebengine:BuildRequires:	khrplatform-devel}
BuildRequires:	lcms2-devel
BuildRequires:	libb2-devel
%if %{with kms} || %{with qtwebengine}
BuildRequires:	libdrm-devel
%endif
BuildRequires:	libevent-devel
# see dependency on libicu version below
BuildRequires:	libicu-devel < %{next_icu_abi}
BuildRequires:	libicu-devel >= %{icu_abi}
%{?with_libinput:BuildRequires:	libinput-devel}
BuildRequires:	libjpeg-devel
BuildRequires:	libmng-devel
BuildRequires:	libpng-devel >= 2:1.6.0
BuildRequires:	libstdc++-devel >= 6:4.7
%{?with_qtwebengine:BuildRequires:	libtiff-devel >= 4.2.0}
BuildRequires:	libva-devel
%{?with_qtwebengine_system_libvpx:BuildRequires:	libvpx-devel >= 1.10.0}
BuildRequires:	libwebp-devel
BuildRequires:	libxcb-devel >= 1.12
BuildRequires:	libxml2-devel
%{?with_qtwebengine:BuildRequires:	libxslt-devel}
BuildRequires:	minizip-devel
BuildRequires:	mtdev-devel
%{?with_mysql:BuildRequires:	mysql-devel}
%{?with_qtwebengine:BuildRequires:	nodejs >= 14.0}
%{?with_qtwebengine:BuildRequires:	nss-devel >= 3.26}
%{?with_qtwebengine:BuildRequires:	openjpeg2-devel}
BuildRequires:	openssl-devel >= 1.1.1
BuildRequires:	opus-devel >= 1.3.1
%{?with_oci:BuildRequires:	oracle-instantclient-devel}
BuildRequires:	pciutils-devel
BuildRequires:	pcre2-16-devel >= 10.20
BuildRequires:	pcsc-lite-devel
BuildRequires:	pkgconfig
BuildRequires:	poppler-cpp-devel
%{?with_pgsql:BuildRequires:	postgresql-devel}
BuildRequires:	protobuf-c-devel
BuildRequires:	protobuf-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	python3
BuildRequires:	python3-devel-tools
BuildRequires:	python3-html5lib
BuildRequires:	python3-modules
BuildRequires:	re2-devel >=  20230601
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.007
BuildRequires:	samurai
BuildRequires:	sed >= 4.0
BuildRequires:	snappy-devel
BuildRequires:	speech-dispatcher-devel
%{?with_sqlite3:BuildRequires:	sqlite3-devel}
%{?with_systemd:BuildRequires:	systemd-devel}
BuildRequires:	tar >= 1:1.22
%{?with_tslib:BuildRequires:	tslib-devel}
BuildRequires:	udev-devel
%{?with_odbc:BuildRequires:	unixODBC-devel >= 2.3.0}
BuildRequires:	wayland-devel
BuildRequires:	xcb-util-cursor-devel >= 0.1.1
BuildRequires:	xcb-util-image-devel >= 0.3.9
BuildRequires:	xcb-util-keysyms-devel >= 0.3.9
BuildRequires:	xcb-util-renderutil-devel >= 0.3.9
BuildRequires:	xcb-util-wm-devel >= 0.3.9
BuildRequires:	xorg-lib-libICE-devel
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xorg-lib-libX11-devel
%{?with_qtwebengine:BuildRequires:	xorg-lib-libXcomposite-devel}
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXfixes-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libXinerama-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel >= 0.6
%{?with_qtwebengine:BuildRequires:	xorg-lib-libXtst-devel}
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xorg-lib-libxkbcommon-x11-devel >= 0.5.0
%{?with_qtwebengine:BuildRequires:	xorg-lib-libxkbfile-devel}
%{?with_qtwebengine:BuildRequires:	xorg-lib-libxshmfence-devel}
%{?with_qtwebengine:BuildRequires:	xorg-proto-glproto-devel}
BuildRequires:	xz
BuildRequires:	zlib-devel >= 1.0.8
BuildRequires:	zstd-devel >= 1.3
BuildConflicts:	Qt6Core
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages	0

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
# androiddeployqt,androidtestrunner: Core
# pixeltool: Core, Gui, Widgets
# qtdiag: Core Gui Network OpenGL Widgets
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
# qdoc: Core, Qml, clang-libs, llvm-libs
# qhelpgenerator: Core, Gui, Help Sql; sqldriver-sqlite3 to work
# qtattributionsscanner: Core
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Help = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Qml = %{version}
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
# lconvert,lprodump,lrelease*,lupdate-pro: Core
# linguist: Core, Gui, PrintSupport, UiTools, Widgets
# lupdate: Core, Qml, clang-libs, llvm-libs
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6PrintSupport = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6UiTools = %{version}
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
# qmlcachegen: Core Qml[+Compiler]
# qmleasing: Core Gui Qml Quick Widgets
# qmlformat: Core Qml[+Compiler]
# qmlimportscanner: Core Qml[+Compiler]
# qmljsrootgen: Core Qml
# qmllint: Core Qml[+Compiler]
# qmlplugindump: Core Gui Qml Widgets
# qmlpreview: Core Network
# qmlprofiler: Core Network
# qmlscene: Core Gui Qml Quick Widgets
# qmltestrunner: Core Quick[Test]
# qmltime: Core Gui Qml Quick
# qmltyperegistrar: Core
# svgtoqml: Core Gui Qml Quick[+Shapes] Svg
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Svg = %{version}
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
Obsoletes:	Qt6JsonRpc < 6.8.1
Obsoletes:	Qt6LanguageServer < 6.8.1

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
%requires_ge	libicu-devel
Requires:	libstdc++-devel >= 6:4.7
Requires:	pcre2-16-devel >= 10.20
Requires:	qt6-build = %{version}
# for qtpaths, but it pulls also Qt6{Gui,Network,OpenGL,Widgets} (FIXME)
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

%package -n Qt6Graphs
Summary:	Qt6 Graphs library
Summary(pl.UTF-8):	Biblioteka Qt6 Graphs
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Quick3D = %{version}
Requires:	Qt6Widgets = %{version}

%description -n Qt6Graphs
Qt6 Graphs library for data visualization.

%description -n Qt6Graphs -l pl.UTF-8
Biblioteka Qt6 Graphs do wizualizacji danych.

%package -n Qt6Graphs-devel
Summary:	Qt6 Graphs library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Graphs - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Graphs = %{version}

%description -n Qt6Graphs-devel
Qt6 Graphs library - development files.

%description -n Qt6Graphs-devel -l pl.UTF-8
Biblioteka Qt6 Graphs - pliki programistyczne.

%package -n Qt6Grpc
Summary:	Qt6 Grpc library
Summary(pl.UTF-8):	Biblioteka Qt6 Grpc
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Protobuf = %{version}

%description -n Qt6Grpc
Qt6 Grpc library for integration with gRPC services.

%description -n Qt6Grpc -l pl.UTF-8
Biblioteka Qt6 Grpc do integracji z serwisami gRPC.

%package -n Qt6Grpc-devel
Summary:	Qt6 Grpc library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Grpc - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Grpc = %{version}

%description -n Qt6Grpc-devel
Qt6 Grpc library - development files.

%description -n Qt6Grpc-devel -l pl.UTF-8
Biblioteka Qt6 Grpc - pliki programistyczne.

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
Requires:	xcb-util-cursor >= 0.1.1
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
Requires:	EGL-devel
Requires:	OpenGL-devel
%{?with_gles:Requires:	OpenGLESv3-devel}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6DBus-devel = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Vulkan-Loader-devel
Requires:	libpng-devel
Requires:	xorg-lib-libxkbcommon-devel >= 0.5.0

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

%package -n Qt6HttpServer
Summary:	Qt6 HttpServer library
Summary(pl.UTF-8):	Biblioteka Qt6 HttpServer
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6WebSockets = %{version}

%description -n Qt6HttpServer
Qt6 HttpServer library provides HTTP server framework.

%description -n Qt6HttpServer -l pl.UTF-8
Biblioteka Qt6 HttpServer dostarcza szkielet do budowy serwera HTTP.

%package -n Qt6HttpServer-devel
Summary:	Qt6 HttpServer library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 HttpServer - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6HttpServer = %{version}

%description -n Qt6HttpServer-devel
Qt6 HttpServer library - development files.

%description -n Qt6HttpServer-devel -l pl.UTF-8
Biblioteka Qt6 HttpServer - pliki programistyczne.

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

%package -n Qt6JsonRpc-devel
Summary:	Qt6 JsonRpc library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 JsonRpc - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}

%description -n Qt6JsonRpc-devel
Qt6 JsonRpc library - development files.

%description -n Qt6JsonRpc-devel -l pl.UTF-8
Biblioteka Qt6 JsonRpc - pliki programistyczne.

%package -n Qt6LanguageServer-devel
Summary:	Qt6 LanguageServer library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 LanguageServer - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}

%description -n Qt6LanguageServer-devel
Qt6 LanguageServer library - development files.

%description -n Qt6LanguageServer-devel -l pl.UTF-8
Biblioteka Qt6 LanguageServer - pliki programistyczne.

%package -n Qt6Location
Summary:	Qt6 Location library
Summary(pl.UTF-8):	Biblioteka Qt6 Location
Group:		X11/Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Positioning = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Location
Qt6 Location library provides mapping, navigation and place search via
QML and C++ interfaces.

%description -n Qt6Location -l pl.UTF-8
Biblioteka Qt6 Location udostępnia mapy, nawigowanie oraz wyszukiwanie
miejsc poprzez interfejsy QML i C++.

%package -n Qt6Location-devel
Summary:	Qt6 Location library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Location - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Location = %{version}

%description -n Qt6Location-devel
Qt6 Location library - development files.

%description -n Qt6Location-devel -l pl.UTF-8
Biblioteka Qt6 Location - pliki programistyczne.

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

%package -n Qt6Multimedia-plugin-ffmpeg
Summary:	FFmpeg plugin for Qt6 Multimedia
Summary(pl.UTF-8):	Wtyczka FFmpeg dla Qt6 Multimedia
Group:		X11/Libraries
Requires:	Qt6Multimedia = %{version}

%description -n Qt6Multimedia-plugin-ffmpeg
FFmpeg plugin for Qt6 Multimedia.

%description -n Qt6Multimedia-plugin-ffmpeg -l pl.UTF-8
Wtyczka FFmpeg dla Qt6 Multimediaa.

%package -n Qt6Multimedia-plugin-gstreamer
Summary:	GStreamer plugin for Qt6 Multimedia
Summary(pl.UTF-8):	Wtyczka GStreamer dla Qt6 Multimedia
Group:		X11/Libraries
Requires:	Qt6Multimedia = %{version}

%description -n Qt6Multimedia-plugin-gstreamer
GStreamer plugin for Qt6 Multimedia.

%description -n Qt6Multimedia-plugin-gstreamer -l pl.UTF-8
Wtyczka GStreamer dla Qt6 Multimediaa.

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

%package -n Qt6Multimedia-plugin-gstreamer-devel
Summary:	Qt6 Multimedia GStreamer plugin - development files
Summary(pl.UTF-8):	Wtyczka GStreamer dla Qt6 Multimedia - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	Qt6Multimedia-devel = %{version}

%description -n Qt6Multimedia-plugin-gstreamer-devel
Qt6 Multimedia GStreamer plugin - development files.

%description -n Qt6Multimedia-plugin-gstreamer-devel -l pl.UTF-8
Wtyczka GStreamer dla Qt6 Multimedia - pliki programistyczne.

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

%package -n Qt6Positioning
Summary:	The Qt6 Positioning library
Summary(pl.UTF-8):	Biblioteka Qt6 Positioning
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}

%description -n Qt6Positioning
Qt6 Positioning library provides positioning information via QML and
C++ interfaces.

%description -n Qt6Positioning -l pl.UTF-8
Biblioteka Qt6 Positioning udostępnia informacje o położeniu poprzez
interfejsy QML i C++.

%package -n Qt6Positioning-devel
Summary:	Qt6 Positioning library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Positioning - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Positioning = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick-devel = %{version}

%description -n Qt6Positioning-devel
Qt6 Positioning library - development files.

%description -n Qt6Positioning-devel -l pl.UTF-8
Biblioteka Qt6 Positioning - pliki programistyczne.

%package -n Qt6Positioning-doc
Summary:	Qt6 Positioning documentation in HTML format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Positioning w formacie HTML
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Positioning-doc
Qt6 Positioning documentation in HTML format.

%description -n Qt6Positioning-doc -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Positioning w formacie HTML.

%package -n Qt6Positioning-doc-qch
Summary:	Qt6 Positioning documentation in QCH format
Summary(pl.UTF-8):	Dokumentacja do biblioteki Qt6 Positioning w formacie QCH
License:	FDL v1.3
Group:		Documentation
Requires:	qt6-doc-common = %{version}
BuildArch:	noarch

%description -n Qt6Positioning-doc-qch
Qt6 Positioning documentation in QCH format.

%description -n Qt6Positioning-doc-qch -l pl.UTF-8
Dokumentacja do biblioteki Qt6 Positioning w formacie QCH.

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

%package -n Qt6Protobuf
Summary:	Qt6 Protobuf library
Summary(pl.UTF-8):	Biblioteka Qt6 Protobuf
Group:		X11/Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Protobuf
Qt6 Protobuf library provides integration with Protocol Buffers.

%description -n Qt6Protobuf -l pl.UTF-8
Biblioteka Qt6 Protobuf dostarcza integrację z Protocol Buffers.

%package -n Qt6Protobuf-devel
Summary:	Qt6 Protobuf library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Protobuf - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Protobuf = %{version}

%description -n Qt6Protobuf-devel
Qt6 Protobuf library - development files.

%description -n Qt6Protobuf-devel -l pl.UTF-8
Biblioteka Qt6 Protobuf - pliki programistyczne.

%package -n Qt6Qt5Compat
Summary:	Qt6 Qt5Compat libraries
Summary(pl.UTF-8):	Biblioteki Qt6 Qt5Compat
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Qt5Compat
Qt6 Qt5Compat libraries.

%description -n Qt6Qt5Compat -l pl.UTF-8
Biblioteki Qt6 Qt5Compat.

%package -n Qt6Qt5Compat-devel
Summary:	Qt6 Qt5Compat libraries - development files
Summary(pl.UTF-8):	Biblioteki Qt6 Qt5Compat - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Qt5Compat = %{version}

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
# Qt6LabsAnimation: Core Qml
# Qt6LabsFolderListModel: Core Qml
# Qt6LabsQmlModels: Core Qml QmlModels
# Qt6LabsSettings: Core Qml
# Qt6Qml: Core Network
# Qt6QmlCompiler: Core Qml
# Qt6QmlCore: Core Qml
# Qt6QmlLocalStorage: Core Qml Sql
# Qt6QmlModels: Core Qml
# Qt6QmlNetwork: Core Network Qml
# Qt6QmlWorkerScript: Core Network Qml
# Qt6QmlXmlListModel: Core Network Qml
# Qt6StateMachine: Core Gui [FIXME: part of scxml]
# Qt6StateMachineQml: Core Qml StateMachine [FIXME: part of scxml]
Requires:	Qt6Core = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6Sql = %{version}
# FIXME: move Qt6StateMachine
Requires:	Qt6Gui = %{version}

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
# Qt6LabsAnimation: Qml Quick
# Qt6LabsFolderListModel: Core Qml QmlModels
# Qt6LabsQmlModels: Qml QmlModels
# Qt6LabsSettings: Core Qml
# Qt6Qml: Core Network QmlIntegration
# Qt6QmlCompiler: Core Qml
# Qt6QmlCore: Core Qml
# Qt6QmlIntegration: Core
# Qt6QmlLocalStorage: Core Qml Sql
# Qt6QmlModels: Core Qml
# Qt6QmlNetwork: Core Network Qml
# Qt6QmlWorkerScript: Core Qml
# Qt6QmlXmlListModel: Core Qml
# Qt6StateMachine: Core Gui [FIXME: not here, belongs to scxml]
# Qt6StateMachineQml: Core Qml StateMachine [FIXME: not here, belongs to scxml]
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Sql-devel = %{version}

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
# Qt6LabsSharedImage: Core Gui Qml Quick
# Qt6LabsWavefrontMesh: Core Gui Qml Quick
# Qt6Quick: Core Gui Network OpenGL Qml QmlModels
# Qt6QuickControls2: Core Gui Qml Quick QuickTemplates2
# Qt6QuickControls2Basic: Core Gui Qml QuickTemplates2
# Qt6QuickControls2BasicStyleImpl: Core Gui Qml Quick QuickControls2Impl
# Qt6QuickControls2Fusion: Core Gui Qml Quick
# Qt6QuickControls2FusionStyleImpl: Core Gui Qml Quick
# Qt6QuickControls2Imagine: Core Gui Qml Quick QuickControls2 QuickTemplates2
# Qt6QuickControls2ImagineStyleImpl: Core Qml
# Qt6QuickControls2Impl: Core Gui Qml Quick QuickTemplates2
# Qt6QuickControls2Material: Core Gui Qml QuickControls2 QuickTemplates2
# Qt6QuickControls2MaterialStyleImpl: Core Gui Qml Quick QuickControls2Impl QuickTemplates2
# Qt6QuickControls2Universal: Core Gui Qml QuickControls2 QuickTemplates2
# Qt6QuickControls2UniversalStyleImpl: Core Gui Qml Quick QuickControls2Impl
# Qt6QuickDialogs2: Core Gui Qml Quick QuickDialogs2QuickImpl QuickDialogs2Utils
# Qt6QuickDialogs2QuickImpl: Core Gui Qml Quick QuickControls2Impl QuickDialogs2Utils QuickTemplates2
# Qt6QuickDialogs2Utils: Core Gui
# Qt6QuickEffects: Core Gui Qml Quick
# Qt6QuickLayouts: Core Gui Qml Quick
# Qt6QuickParticles: Core Gui Qml Quick
# Qt6QuickShapes: Core Gui Qml Quick
# Qt6QuickTemplates2: Core Gui Qml QmlModels Quick
# Qt6QuickTest: Core Gui Qml Quick Test
# Qt6QuickTimeline: Core Gui Qml Quick
# Qt6QuickTimelineBlendTrees: Core Gui Qml Quick QuickTimeline
# Qt6QuickWidgets: Core Gui Qml Quick Widgets
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Network = %{version}
Requires:	Qt6OpenGL = %{version}
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
# Qt6LabsSharedImage: Core Gui Quick
# Qt6LabsWavefrontMesh: Core Gui Quick
# Qt6Quick: Core Gui OpenGL Qml QmlModels
# Qt6QuickControls2: Core Gui Quick
# Qt6QuickControls2Impl: Core Gui Quick
# Qt6QuickDialogs2: Core Gui Quick
# Qt6QuickDialogs2QuickImpl: Core Gui Quick
# Qt6QuickDialogs2Utils: Core
# Qt6QuickLayouts: Core Gui Qml Quick
# Qt6QuickTemplates2: Core Gui QmlModels Quick
# Qt6QuickTest: Core Test
# Qt6QuickTimeline: Core Qml Quick
# Qt6QuickTimelineBlendTrees: Core Qml Quick QuickTimeline
# Qt6QuickWidgets: Core Gui Qml Quick Widgets
# bin/qmldom: Core Qml QmlCompiler
# bin/qmlls: Core JsonRpc LanguageServer Qml QmlCompiler [FIXME: part of qtlanguageserver, not qtdeclarative]
# bin/qmltc: Core Qml QmlCompiler
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Network-devel = %{version}
Requires:	Qt6OpenGL-devel = %{version}
Requires:	Qt6Qml-devel = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Test-devel = %{version}
Requires:	Qt6Widgets-devel = %{version}
# for qmlcachegen (to be verified if really required)
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

%package -n qt6-quick3d
Summary:	The Qt6 Quick3D library command line tools
Summary(pl.UTF-8):	Narzędzia linii poleceń do biblioteki Qt6 Quick3D
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Quick3D = %{version}

%description -n qt6-quick3d
The Qt6 Quick3D library command line tools.

%description -n qt6-quick3d -l pl.UTF-8
Narzędzia linii poleceń do biblioteki Qt6 Quick3D.

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
%{?with_openxr:Requires:	OpenXR-devel = 1.0.29}
Requires:	Qt6Concurrent-devel = %{version}
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Gui-devel = %{version}
Requires:	Qt6Quick3D = %{version}
Requires:	Qt6ShaderTools-devel = %{version}

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

%package -n Qt6Quick3DPhysics
Summary:	Qt6 Quick3DPhysics library
Summary(pl.UTF-8):	Biblioteka Qt6 Quick3DPhysics
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick3D = %{version}

%description -n Qt6Quick3DPhysics
Qt6 Quick3DPhysics library provides a high-level API for physics
simulation.

%description -n Qt6Quick3DPhysics -l pl.UTF-8
Biblioteka Qt6 Quick3DPhysics dostarcza wysokpoziomowe API do
symulacji fizycznych.

%package -n Qt6Quick3DPhysics-devel
Summary:	Qt6 Quick3DPhysics library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 Quick3DPhysics - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Quick3DPhysics = %{version}

%description -n Qt6Quick3DPhysics-devel
Qt6 Quick3DPhysics library - development files.

%description -n Qt6Quick3DPhysics-devel -l pl.UTF-8
Biblioteka Qt6 Quick3DPhysics - pliki programistyczne.

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

%package -n qt6-quickeffectmaker
Summary:	The Qt6 Quick Effect Maker tools
Summary(pl.UTF-8):	Narzędzia do modułu Qt6 Quick Effect Maker
Group:		Applications
Requires:	Qt6Core = %{version}

%description -n qt6-quickeffectmaker
The Qt6 Quick Effect Maker tools.

%description -n qt6-quickeffectmaker -l pl.UTF-8
Narzędzia do modułu Qt6 Quick Effect Maker.

%package -n Qt6QuickEffectMaker
Summary:	Qt6 Quick Effect Maker module
Summary(pl.UTF-8):	Moduł Qt6 Quick Effect Maker module
Group:		Libraries
Obsoletes:	Qt6QuickEffectMaker-devel < 6.5.1

%description -n Qt6QuickEffectMaker
Qt6 Quick Effect Maker moduke.

%description -n Qt6QuickEffectMaker -l pl.UTF-8
Moduł Qt6 Quick Effect Maker module.

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
Summary:	The Qt6 ShaderTools library command line tools
Summary(pl.UTF-8):	Narzędzia linii poleceń do biblioteki Qt6 ShaderTools
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6ShaderTools = %{version}

%description -n qt6-shadertools
The Qt6 ShaderTools library command line tools.

%description -n qt6-shadertools -l pl.UTF-8
Narzędzia linii poleceń do biblioteki Qt6 ShaderTools.

%package -n Qt6ShaderTools
Summary:	The Qt6 ShaderTools library
Summary(pl.UTF-8):	Biblioteka Qt6 ShaderTools
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6ShaderTools
The Qt Shader Tools module builds on the SPIR-V Open Source Ecosystem
as described at the Khronos SPIR-V web site
<https://www.khronos.org/spir/>.

%description -n Qt6ShaderTools -l pl.UTF-8
Moduł Qt Shader Tools jest zbudowany w oparciu o mający otwarte źródła
ekosystem SPIR-V, opisany na stronie Khronos SPIR-V
<https://www.khronos.org/spir/>.

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

%package -n Qt6SpatialAudio
Summary:	Qt6 SpatialAudio library
Summary(pl.UTF-8):	Biblioteka Qt6 SpatialAudio
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Multimedia = %{version}

%description -n Qt6SpatialAudio
Qt6 SpatialAudio library provides support for sound fields in 3D
space.

%description -n Qt6SpatialAudio -l pl.UTF-8
Biblioteka Qt6 SpatialAudio dostarcza wsparcia dla pól dźwiękowych w
przestrzeni 3D.

%package -n Qt6SpatialAudio-devel
Summary:	Qt6 SpatialAudio library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 SpatialAudio - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6SpatialAudio = %{version}

%description -n Qt6SpatialAudio-devel
Qt6 SpatialAudio library - development files.

%description -n Qt6SpatialAudio-devel -l pl.UTF-8
Biblioteka Qt6 SpatialAudio - pliki programistyczne.

%package -n Qt6Sql
Summary:	Qt6 Sql library
Summary(pl.UTF-8):	Biblioteka Qt6 Sql
Group:		Libraries
Requires:	Qt6Core = %{version}
Obsoletes:	Qt6Sql-sqldriver-tds < 6.7.2-4

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

%package -n Qt6TextToSpeech
Summary:	Qt6 TextToSpeech library
Summary(pl.UTF-8):	Biblioteka Qt6 TextToSpeech
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Qml = %{version}

%description -n Qt6TextToSpeech
Qt6 TextToSpeech library enables text read out by using speech
synthesis.

%description -n Qt6TextToSpeech -l pl.UTF-8
Biblioteka Qt6 TextToSpeech umożliwia odczytywanie tekstu przy użyciu
syntezatora mowy.

%package -n Qt6TextToSpeech-devel
Summary:	Qt6 TextToSpeech library - development files
Summary(pl.UTF-8):	Biblioteka Qt6 TextToSpeech - pliki programistyczne
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6TextToSpeech = %{version}

%description -n Qt6TextToSpeech-devel
Qt6 TextToSpeech library - development files.

%description -n Qt6TextToSpeech-devel -l pl.UTF-8
Biblioteka Qt6 TextToSpeech - pliki programistyczne.

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

%package -n Qt6Wayland
Summary:	Common files for Qt6 Wayland
Summary(pl.UTF-8):	Wspólne pliki dla Qt6 Wayland
Group:		Libraries
Requires:	Qt6Core = %{version}

%description -n Qt6Wayland
Common files for Qt6 Wayland.

%description -n Qt6Wayland -l pl.UTF-8
Wspólne pliki dla Qt6 Wayland.

%package -n Qt6Wayland-devel
Summary:	Common development files for Qt6 Wayland
Summary(pl.UTF-8):	Wspólne pliki programistyczne dla Qt6 Wayland
Group:		Development/Libraries
Requires:	Qt6Core-devel = %{version}
Requires:	Qt6Wayland = %{version}

%description -n Qt6Wayland-devel
Common development files for Qt6 Wayland.

%description -n Qt6Wayland-devel -l pl.UTF-8
Wspólne pliki programistyczne dla Qt6 Wayland.

%package -n Qt6WaylandCompositor
Summary:	The Qt6 WaylandCompositor library
Summary(pl.UTF-8):	Biblioteka Qt6 WaylandCompositor
Group:		Libraries
Requires:	Qt6Core = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Qml = %{version}
Requires:	Qt6Quick = %{version}
Requires:	Qt6Wayland = %{version}
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
Requires:	Qt6Wayland-devel = %{version}
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
# WaylandClient: Core Gui, wayland[client,cursor] libxkbcommon
# Qt6WaylandEglClientHwIntegration: Core Gui OpenGL WaylandClient, EGL OpenGL wayland[client] wayland-egl
Requires:	Qt6Core = %{version}
Requires:	Qt6DBus = %{version}
Requires:	Qt6Gui = %{version}
Requires:	Qt6Wayland = %{version}
Requires:	wayland >= 1.4.0
Requires:	xorg-lib-libxkbcommon >= 0.2.0
# plugins/wayland-shell-integration/libwl-shell-plugin.so requires libQt6WlShellIntegration.so.6 [TODO: verify packaging]
Requires:	Qt6WaylandCompositor = %{version}

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
Requires:	Qt6Wayland-devel = %{version}
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
%requires_ge_to	libicu libicu-devel
Requires:	libpng >= 2:1.6.0
Requires:	libtiff >= 4.2.0
%{?with_qtwebengine_system_libvpx:Requires:	libvpx >= 1.10.0}
Requires:	nss >= 3.26
Requires:	opus >= 1.3.1
Requires:	pulseaudio-libs >= 0.9.10
Requires:	re2 >=  20230601

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
%patch2 -p1 -d qtwebengine
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1 -d qtquick3d

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
	%{cmake_on_off qt3d BUILD_qt3d} \
	%{cmake_on_off qtquick3d BUILD_qtquick3d} \
	%{cmake_on_off qtquick3dphysics BUILD_qtquick3dphysics} \
	%{cmake_on_off qtwebengine BUILD_qtwebengine} \
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
	%{cmake_on_off opengl_desktop QT_FEATURE_opengl_desktop} \
	%{cmake_on_off gles QT_FEATURE_opengles2} \
	%{cmake_on_off openxr QT_FEATURE_quick3dxr_openxr} \
	%{?with_openxr:-DQT_FEATURE_system_openxr=ON} \
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
	%{cmake_on_off qtwebengine_system_ffmpeg QT_FEATURE_webengine_system_ffmpeg} \
	-DQT_FEATURE_webengine_system_freetype=ON \
	-DQT_FEATURE_webengine_system_glib=ON \
	-DQT_FEATURE_webengine_system_harfbuzz=ON \
	-DQT_FEATURE_webengine_system_icu=ON \
	-DQT_FEATURE_webengine_system_lcms2=ON \
	-DQT_FEATURE_webengine_system_libevent=ON \
	-DQT_FEATURE_webengine_system_libjpeg=ON \
	-DQT_FEATURE_webengine_system_libopenjpeg2=ON \
	-DQT_FEATURE_webengine_system_libpci=ON \
	-DQT_FEATURE_webengine_system_libpng=ON \
	-DQT_FEATURE_webengine_system_libtiff=ON \
	%{cmake_on_off qtwebengine_system_libvpx QT_FEATURE_webengine_system_libvpx} \
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
	%{cmake_on_off directfb QT_FEATURE_directfb} \
	%{cmake_on_off gtk QT_FEATURE_gtk3} \
	%{cmake_on_off egl QT_FEATURE_eglfs} \
	%{cmake_on_off statx QT_FEATURE_statx} \
	%{cmake_on_off kms QT_FEATURE_kms} \
	%{cmake_on_off libinput QT_FEATURE_libinput} \
	%{cmake_on_off tslib QT_FEATURE_tslib} \
	%{cmake_on_off qml_jit QT_FEATURE_qml_jit} \
	-DQT_GENERATE_SBOM:BOOL=OFF

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

# junk
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/objects-PLD
%{__rm} -r $RPM_BUILD_ROOT%{qt6dir}/mkspecs/qtdoc_dummy_file.txt
%{__rm} $RPM_BUILD_ROOT%{qt6dir}/libexec/sanitizer-testrunner.py
%{__rm} -r $RPM_BUILD_ROOT%{qt6dir}/qml/Qt/test/controls/objects-PLD

%if %{without qtwebengine}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/qt6/translations/qtwebengine_*.qm
%endif

# bundled libs, not required by installed components - probably no need to package
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt6BundledResonanceAudio.a
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledOpenwnn
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledPinyin
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledResonanceAudio
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledTcime
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6Bundled_Clip2Tri
%ifarch %{x8664} aarch64
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt6BundledEmbree.a
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledEmbree
%endif
%if %{with qtquick3dphysics}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libQt6BundledPhysX.a
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/cmake/Qt6BundledPhysX
%endif

%{__rm} $RPM_BUILD_ROOT%{qt6dir}/libexec/qt-android-runner.py

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
qqem \
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
qmlaotstats \
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
%if %{with qtwebengine}
find_qt6_qm qtwebengine >> qtwebengine.lang
%endif
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

%post	-n Qt6Graphs -p /sbin/ldconfig
%postun	-n Qt6Graphs -p /sbin/ldconfig

%post	-n Qt6Grpc -p /sbin/ldconfig
%postun	-n Qt6Grpc -p /sbin/ldconfig

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

%post	-n Qt6HttpServer -p /sbin/ldconfig
%postun	-n Qt6HttpServer -p /sbin/ldconfig

%post	-n Qt6Location -p /sbin/ldconfig
%postun	-n Qt6Location -p /sbin/ldconfig

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

%post	-n Qt6Positioning -p /sbin/ldconfig
%postun	-n Qt6Positioning -p /sbin/ldconfig

%post	-n Qt6PrintSupport -p /sbin/ldconfig
%postun	-n Qt6PrintSupport -p /sbin/ldconfig

%post	-n Qt6Protobuf -p /sbin/ldconfig
%postun	-n Qt6Protobuf -p /sbin/ldconfig

%post	-n Qt6Qt5Compat -p /sbin/ldconfig
%postun	-n Qt6Qt5Compat -p /sbin/ldconfig

%post	-n Qt6Qml -p /sbin/ldconfig
%postun	-n Qt6Qml -p /sbin/ldconfig

%post	-n Qt6Quick -p /sbin/ldconfig
%postun	-n Qt6Quick -p /sbin/ldconfig

%post	-n Qt6Quick3D -p /sbin/ldconfig
%postun	-n Qt6Quick3D -p /sbin/ldconfig

%post	-n Qt6Quick3DPhysics -p /sbin/ldconfig
%postun	-n Qt6Quick3DPhysics -p /sbin/ldconfig

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

%post	-n Qt6SpatialAudio -p /sbin/ldconfig
%postun	-n Qt6SpatialAudio -p /sbin/ldconfig

%post	-n Qt6Sql -p /sbin/ldconfig
%postun	-n Qt6Sql -p /sbin/ldconfig

%post	-n Qt6Svg -p /sbin/ldconfig
%postun	-n Qt6Svg -p /sbin/ldconfig

%post	-n Qt6Test -p /sbin/ldconfig
%postun	-n Qt6Test -p /sbin/ldconfig

%post	-n Qt6TextToSpeech -p /sbin/ldconfig
%postun	-n Qt6TextToSpeech -p /sbin/ldconfig

%post	-n Qt6UiTools -p /sbin/ldconfig
%postun	-n Qt6UiTools -p /sbin/ldconfig

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
%{qt6dir}/modules/Tools.json

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
%{qt6dir}/modules/Linguist.json
%{qt6dir}/mkspecs/modules/qt_lib_linguist.pri

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
%attr(755,root,root) %{_bindir}/qmlaotstats-qt6
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
%attr(755,root,root) %{qt6dir}/bin/svgtoqml
%attr(755,root,root) %{qt6dir}/libexec/qmlaotstats
%attr(755,root,root) %{qt6dir}/libexec/qmlcachegen
%attr(755,root,root) %{qt6dir}/libexec/qmlimportscanner
%attr(755,root,root) %{qt6dir}/libexec/qmljsrootgen
%attr(755,root,root) %{qt6dir}/libexec/qmltyperegistrar

%if %{with qt3d}
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
%attr(755,root,root) %{_libdir}/libQt63DQuickScene3D.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt63DQuickScene3D.so.6
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
%attr(755,root,root) %{_libdir}/libQt63DQuickScene3D.so
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
%{_libdir}/libQt63DQuickScene3D.prl
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
%{_includedir}/qt6/Qt3DQuickScene3D
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
%{_pkgconfigdir}/Qt63DQuickScene3D.pc
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
%{_libdir}/cmake/Qt63DQuickScene3D
%{_libdir}/cmake/Qt63DRender
%{qt6dir}/metatypes/qt63danimation_pld_metatypes.json
%{qt6dir}/metatypes/qt63dcore_pld_metatypes.json
%{qt6dir}/metatypes/qt63dextras_pld_metatypes.json
%{qt6dir}/metatypes/qt63dinput_pld_metatypes.json
%{qt6dir}/metatypes/qt63dlogic_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquick_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickanimation_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickextras_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickinput_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickrender_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickscene2d_pld_metatypes.json
%{qt6dir}/metatypes/qt63dquickscene3d_pld_metatypes.json
%{qt6dir}/metatypes/qt63drender_pld_metatypes.json
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
%{qt6dir}/mkspecs/modules/qt_lib_3dquickscene3d.pri
%{qt6dir}/mkspecs/modules/qt_lib_3dquickscene3d_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_3drender.pri
%{qt6dir}/mkspecs/modules/qt_lib_3drender_private.pri
%{qt6dir}/modules/3DAnimation.json
%{qt6dir}/modules/3DCore.json
%{qt6dir}/modules/3DExtras.json
%{qt6dir}/modules/3DInput.json
%{qt6dir}/modules/3DLogic.json
%{qt6dir}/modules/3DQuick.json
%{qt6dir}/modules/3DQuickAnimation.json
%{qt6dir}/modules/3DQuickExtras.json
%{qt6dir}/modules/3DQuickInput.json
%{qt6dir}/modules/3DQuickRender.json
%{qt6dir}/modules/3DQuickScene2D.json
%{qt6dir}/modules/3DQuickScene3D.json
%{qt6dir}/modules/3DRender.json

%if %{with doc}
%files -n Qt63D-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qt3d

%files -n Qt63D-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qt3d.qch
%endif
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
%{qt6dir}/metatypes/qt6bluetooth_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_bluetooth.pri
%{qt6dir}/mkspecs/modules/qt_lib_bluetooth_private.pri
%{qt6dir}/modules/Bluetooth.json

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
%{qt6dir}/metatypes/qt6bodymovinprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_bodymovin_private.pri
%{qt6dir}/modules/BodymovinPrivate.json

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
%{qt6dir}/metatypes/qt6charts_pld_metatypes.json
%{qt6dir}/metatypes/qt6chartsqml_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_charts.pri
%{qt6dir}/mkspecs/modules/qt_lib_charts_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_chartsqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_chartsqml_private.pri
%{qt6dir}/modules/Charts.json
%{qt6dir}/modules/ChartsQml.json

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
%{qt6dir}/metatypes/qt6coap_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_coap.pri
%{qt6dir}/mkspecs/modules/qt_lib_coap_private.pri
%{qt6dir}/modules/Coap.json

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
%{qt6dir}/metatypes/qt6concurrent_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_concurrent.pri
%{qt6dir}/mkspecs/modules/qt_lib_concurrent_private.pri
%{qt6dir}/modules/Concurrent.json

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
%dir %{qt6dir}/modules
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
%dir %{qt6dir}/metatypes
%{qt6dir}/metatypes/qt6core_pld_metatypes.json
%dir %{_includedir}/qt6
%dir %{_includedir}/qt6/QtSolutions
%{_includedir}/qt6/QtCore
%{_pkgconfigdir}/Qt6Core.pc
%{_pkgconfigdir}/Qt6Platform.pc
%{_libdir}/cmake/Qt6
%{_libdir}/cmake/Qt6Core
%{_libdir}/cmake/Qt6CoreTools
%{_libdir}/cmake/Qt6HostInfo
%dir %{_libdir}/cmake/Qt6BuildInternals
%{_libdir}/cmake/Qt6BuildInternals/*.cmake
%attr(755,root,root) %{qt6dir}/libexec/tracegen
%{qt6dir}/mkspecs/modules/qt_lib_core.pri
%{qt6dir}/mkspecs/modules/qt_lib_core_private.pri
%{qt6dir}/modules/Core.json

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
%{qt6dir}/metatypes/qt6datavisualization_pld_metatypes.json
%{qt6dir}/metatypes/qt6datavisualizationqml_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_datavisualization.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualization_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualizationqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_datavisualizationqml_private.pri
%{qt6dir}/modules/DataVisualization.json
%{qt6dir}/modules/DataVisualizationQml.json

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
%{qt6dir}/metatypes/qt6dbus_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_dbus.pri
%{qt6dir}/mkspecs/modules/qt_lib_dbus_private.pri
%{qt6dir}/modules/DBus.json

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
%{qt6dir}/modules/Designer.json
%{qt6dir}/modules/DesignerComponentsPrivate.json
%{qt6dir}/metatypes/qt6designercomponentsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6designer_pld_metatypes.json

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
%{qt6dir}/modules/DeviceDiscoverySupportPrivate.json
%{qt6dir}/metatypes/qt6devicediscoverysupportprivate_pld_metatypes.json

%files -n Qt6FbSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtFbSupport
%{_libdir}/libQt6FbSupport.a
%{_libdir}/libQt6FbSupport.prl
%{_libdir}/cmake/Qt6FbSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_fb_support_private.pri
%{qt6dir}/modules/FbSupportPrivate.json
%{qt6dir}/metatypes/qt6fbsupportprivate_pld_metatypes.json

%files -n Qt6Graphs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Graphs.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Graphs.so.6
%attr(755,root,root) %{_libdir}/libQt6GraphsWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6GraphsWidgets.so.6
%dir %{qt6dir}/qml/QtGraphs
%{qt6dir}/qml/QtGraphs/Graphs.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtGraphs/libgraphsplugin.so
%dir %{qt6dir}/qml/QtGraphs/designer
%{qt6dir}/qml/QtGraphs/designer/*.qml
%{qt6dir}/qml/QtGraphs/designer/qtgraphs.metainfo
%{qt6dir}/qml/QtGraphs/designer/qtgraphs2d.metainfo
%dir %{qt6dir}/qml/QtGraphs/designer/default
%{qt6dir}/qml/QtGraphs/designer/default/*.qml
%dir %{qt6dir}/qml/QtGraphs/designer/images
%{qt6dir}/qml/QtGraphs/designer/images/*.png
%{qt6dir}/qml/QtGraphs/qmldir

%files -n Qt6Graphs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Graphs.so
%attr(755,root,root) %{_libdir}/libQt6GraphsWidgets.so
%{_libdir}/libQt6Graphs.prl
%{_libdir}/libQt6GraphsWidgets.prl
%{_includedir}/qt6/QtGraphs
%{_includedir}/qt6/QtGraphsWidgets
%{_libdir}/cmake/Qt6Graphs
%{_libdir}/cmake/Qt6GraphsWidgets
%{qt6dir}/metatypes/qt6graphs_pld_metatypes.json
%{qt6dir}/metatypes/qt6graphswidgets_pld_metatypes.json
%{_pkgconfigdir}/Qt6Graphs.pc
%{_pkgconfigdir}/Qt6GraphsWidgets.pc
%{qt6dir}/mkspecs/modules/qt_lib_graphs.pri
%{qt6dir}/mkspecs/modules/qt_lib_graphs_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_graphswidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_graphswidgets_private.pri
%{qt6dir}/modules/Graphs.json
%{qt6dir}/modules/GraphsWidgets.json

%files -n Qt6Grpc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Grpc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Grpc.so.6
%attr(755,root,root) %{_libdir}/libQt6GrpcQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6GrpcQuick.so.6
%dir %{qt6dir}/qml/QtGrpc
%attr(755,root,root) %{qt6dir}/qml/QtGrpc/libgrpcquickplugin.so
%{qt6dir}/qml/QtGrpc/plugins.qmltypes
%{qt6dir}/qml/QtGrpc/qmldir

%files -n Qt6Grpc-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Grpc.so
%attr(755,root,root) %{_libdir}/libQt6GrpcQuick.so
%{_libdir}/libQt6Grpc.prl
%{_libdir}/libQt6GrpcQuick.prl
%{_includedir}/qt6/QtGrpc
%{_includedir}/qt6/QtGrpcQuick
%{_libdir}/cmake/Qt6Grpc
%{_libdir}/cmake/Qt6GrpcQuick
%{_libdir}/cmake/Qt6GrpcTools
%{_libdir}/cmake/Qt6ProtobufTools
%attr(755,root,root) %{qt6dir}/libexec/qtgrpcgen
%attr(755,root,root) %{qt6dir}/libexec/qtprotobufgen
%{qt6dir}/metatypes/qt6grpc_pld_metatypes.json
%{qt6dir}/metatypes/qt6grpcquick_pld_metatypes.json
%{_pkgconfigdir}/Qt6Grpc.pc
%{_pkgconfigdir}/Qt6GrpcQuick.pc
%{qt6dir}/mkspecs/modules/qt_lib_grpc.pri
%{qt6dir}/mkspecs/modules/qt_lib_grpc_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_grpcquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_grpcquick_private.pri
%{qt6dir}/modules/Grpc.json
%{qt6dir}/modules/GrpcQuick.json

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
%{qt6dir}/modules/EglFSDeviceIntegrationPrivate.json
%{qt6dir}/metatypes/qt6eglfsdeviceintegrationprivate_pld_metatypes.json

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
%{qt6dir}/modules/EglFsKmsGbmSupportPrivate.json
%{qt6dir}/modules/EglFsKmsSupportPrivate.json
%{qt6dir}/metatypes/qt6eglfskmssupportprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6eglfskmsgbmsupportprivate_pld_metatypes.json
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
%{qt6dir}/modules/XcbQpaPrivate.json
%{qt6dir}/metatypes/qt6xcbqpaprivate_pld_metatypes.json

%files -n Qt6Gui-platform-xcb-egl
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-egl-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6QXcbEglIntegrationPlugin*.cmake

%if %{with opengl_desktop}
%files -n Qt6Gui-platform-xcb-glx
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/xcbglintegrations/libqxcb-glx-integration.so
%{_libdir}/cmake/Qt6Gui/Qt6QXcbGlxIntegrationPlugin*.cmake
%endif

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
%{qt6dir}/metatypes/qt6gui_pld_metatypes.json
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
%{qt6dir}/modules/Gui.json

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
%{qt6dir}/modules/Help.json
%{qt6dir}/metatypes/qt6help_pld_metatypes.json

%files -n Qt6HttpServer
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6HttpServer.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6HttpServer.so.6

%files -n Qt6HttpServer-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6HttpServer.so
%{_libdir}/libQt6HttpServer.prl
%{_includedir}/qt6/QtHttpServer
%{_libdir}/cmake/Qt6HttpServer
%{qt6dir}/metatypes/qt6httpserver_pld_metatypes.json
%{_pkgconfigdir}/Qt6HttpServer.pc
%{qt6dir}/mkspecs/modules/qt_lib_httpserver.pri
%{qt6dir}/mkspecs/modules/qt_lib_httpserver_private.pri
%{qt6dir}/modules/HttpServer.json

%files -n Qt6InputSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtInputSupport
%{_libdir}/libQt6InputSupport.a
%{_libdir}/libQt6InputSupport.prl
%{_libdir}/cmake/Qt6InputSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_input_support_private.pri
%{qt6dir}/modules/InputSupportPrivate.json
%{qt6dir}/metatypes/qt6inputsupportprivate_pld_metatypes.json

%files -n Qt6JsonRpc-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6JsonRpc.a
%{_libdir}/libQt6JsonRpc.prl
%{_includedir}/qt6/QtJsonRpc
%{_libdir}/cmake/Qt6JsonRpcPrivate
%{qt6dir}/metatypes/qt6jsonrpcprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_jsonrpc_private.pri
%{qt6dir}/modules/JsonRpcPrivate.json

%files -n Qt6KmsSupport-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtKmsSupport
%{_libdir}/libQt6KmsSupport.a
%{_libdir}/libQt6KmsSupport.prl
%{_libdir}/cmake/Qt6KmsSupportPrivate
%{qt6dir}/mkspecs/modules/qt_lib_kms_support_private.pri
%{qt6dir}/modules/KmsSupportPrivate.json
%{qt6dir}/metatypes/qt6kmssupportprivate_pld_metatypes.json

%files -n Qt6LanguageServer-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6LanguageServer.a
%{_libdir}/libQt6LanguageServer.prl
%{_includedir}/qt6/QtLanguageServer
%{_libdir}/cmake/Qt6LanguageServerPrivate
%{qt6dir}/metatypes/qt6languageserverprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_languageserver_private.pri
%{qt6dir}/modules/LanguageServerPrivate.json

%files -n Qt6Location
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Location.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Location.so.6
%dir %{qt6dir}/plugins/geoservices
%attr(755,root,root) %{qt6dir}/plugins/geoservices/libqtgeoservices_itemsoverlay.so
%attr(755,root,root) %{qt6dir}/plugins/geoservices/libqtgeoservices_osm.so
%dir %{qt6dir}/qml/QtLocation
%attr(755,root,root) %{qt6dir}/qml/QtLocation/libdeclarative_locationplugin.so
%{qt6dir}/qml/QtLocation/*.qml
%{qt6dir}/qml/QtLocation/plugins.qmltypes
%{qt6dir}/qml/QtLocation/qmldir

%files -n Qt6Location-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Location.so
%{_libdir}/libQt6Location.prl
%{_includedir}/qt6/QtLocation
%{_libdir}/cmake/Qt6Location
%{qt6dir}/metatypes/qt6location_pld_metatypes.json
%{_pkgconfigdir}/Qt6Location.pc
%{qt6dir}/mkspecs/modules/qt_lib_location.pri
%{qt6dir}/mkspecs/modules/qt_lib_location_private.pri
%{qt6dir}/modules/Location.json

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
%{qt6dir}/modules/Mqtt.json
%{qt6dir}/metatypes/qt6mqtt_pld_metatypes.json

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
%dir %{qt6dir}/plugins/multimedia

%files -n Qt6Multimedia-plugin-ffmpeg
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/multimedia/libffmpegmediaplugin.so

%files -n Qt6Multimedia-plugin-gstreamer
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/plugins/multimedia/libgstreamermediaplugin.so

%files -n Qt6Multimedia-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Multimedia.so
%{_libdir}/libQt6Multimedia.prl
%{_includedir}/qt6/QtMultimedia
%{_pkgconfigdir}/Qt6Multimedia.pc
%{_libdir}/cmake/Qt6Multimedia
%{qt6dir}/mkspecs/modules/qt_lib_multimedia.pri
%{qt6dir}/mkspecs/modules/qt_lib_multimedia_private.pri
%{qt6dir}/modules/Multimedia.json
%{qt6dir}/metatypes/qt6multimedia_pld_metatypes.json

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
%{qt6dir}/modules/MultimediaQuickPrivate.json
%{qt6dir}/metatypes/qt6multimediaquickprivate_pld_metatypes.json

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
%{qt6dir}/modules/MultimediaWidgets.json
%{qt6dir}/metatypes/qt6multimediawidgets_pld_metatypes.json

%files -n Qt6Multimedia-plugin-gstreamer-devel
%defattr(644,root,root,755)
%{_libdir}/libQt6QGstreamerMediaPluginImpl.a
%{_libdir}/libQt6QGstreamerMediaPluginImpl.prl
%{_includedir}/qt6/QtQGstreamerMediaPluginImpl
%{_libdir}/cmake/Qt6QGstreamerMediaPluginImplPrivate
%{qt6dir}/metatypes/qt6qgstreamermediapluginimplprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_qgstreamermediapluginimpl_private.pri
%{qt6dir}/modules/QGstreamerMediaPluginImplPrivate.json

%files -n Qt6Network
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Network.so.6
%dir %{qt6dir}/plugins/networkinformation
%attr(755,root,root) %{qt6dir}/plugins/networkinformation/libqglib.so
%attr(755,root,root) %{qt6dir}/plugins/networkinformation/libqnetworkmanager.so

%files -n Qt6Network-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Network.so
%{_libdir}/libQt6Network.prl
%{_includedir}/qt6/QtNetwork
%{_pkgconfigdir}/Qt6Network.pc
%{_libdir}/cmake/Qt6Network
%{qt6dir}/mkspecs/modules/qt_lib_network.pri
%{qt6dir}/mkspecs/modules/qt_lib_network_private.pri
%{qt6dir}/modules/Network.json
%{qt6dir}/metatypes/qt6network_pld_metatypes.json

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
%{qt6dir}/modules/NetworkAuth.json
%{qt6dir}/metatypes/qt6networkauth_pld_metatypes.json

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
%{qt6dir}/modules/Nfc.json
%{qt6dir}/metatypes/qt6nfc_pld_metatypes.json

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
%{_libdir}/cmake/Qt6QtOpcUaTools
%attr(755,root,root) %{qt6dir}/bin/qopcuaxmldatatypes2cpp
%{qt6dir}/mkspecs/modules/qt_lib_declarativeopcua.pri
%{qt6dir}/mkspecs/modules/qt_lib_declarativeopcua_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_opcua.pri
%{qt6dir}/mkspecs/modules/qt_lib_opcua_private.pri
%{qt6dir}/modules/DeclarativeOpcua.json
%{qt6dir}/modules/OpcUa.json
%{qt6dir}/metatypes/qt6declarativeopcua_pld_metatypes.json
%{qt6dir}/metatypes/qt6opcua_pld_metatypes.json

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
%{qt6dir}/modules/OpenGL.json
%{qt6dir}/modules/OpenGLWidgets.json
%{qt6dir}/metatypes/qt6opengl_pld_metatypes.json
%{qt6dir}/metatypes/qt6openglwidgets_pld_metatypes.json

%if %{with qtwebengine}
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
%{qt6dir}/qml/QtQuick/Pdf/*.qml
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Pdf/libpdfquickplugin.so
%dir %{qt6dir}/qml/QtQuick/Pdf/+Material
%{qt6dir}/qml/QtQuick/Pdf/+Material/*.qml
%dir %{qt6dir}/qml/QtQuick/Pdf/+Universal
%{qt6dir}/qml/QtQuick/Pdf/+Universal/*.qml
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
%{qt6dir}/modules/Pdf.json
%{qt6dir}/modules/PdfQuick.json
%{qt6dir}/modules/PdfWidgets.json
%{qt6dir}/metatypes/qt6pdf_pld_metatypes.json
%{qt6dir}/metatypes/qt6pdfquick_pld_metatypes.json
%{qt6dir}/metatypes/qt6pdfwidgets_pld_metatypes.json

%if %{with doc}
%files -n Qt6Pdf-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf

%files -n Qt6Pdf-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpdf.qch
%endif
%endif

%files -n Qt6Positioning
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Positioning.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Positioning.so.6
%attr(755,root,root) %{_libdir}/libQt6PositioningQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6PositioningQuick.so.6
%dir %{qt6dir}/plugins/position
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_geoclue2.so
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_gypsy.so
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_nmea.so
%attr(755,root,root) %{qt6dir}/plugins/position/libqtposition_positionpoll.so
%dir %{qt6dir}/qml/QtPositioning
%attr(755,root,root) %{qt6dir}/qml/QtPositioning/libpositioningquickplugin.so
%{qt6dir}/qml/QtPositioning/plugins.qmltypes
%{qt6dir}/qml/QtPositioning/qmldir

%files -n Qt6Positioning-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Positioning.so
%attr(755,root,root) %{_libdir}/libQt6PositioningQuick.so
%{_libdir}/libQt6Positioning.prl
%{_libdir}/libQt6PositioningQuick.prl
%{_includedir}/qt6/QtPositioning
%{_includedir}/qt6/QtPositioningQuick
%{_pkgconfigdir}/Qt6Positioning.pc
%{_pkgconfigdir}/Qt6PositioningQuick.pc
%{_libdir}/cmake/Qt6Positioning
%{_libdir}/cmake/Qt6PositioningQuick
%{qt6dir}/metatypes/qt6positioning_pld_metatypes.json
%{qt6dir}/metatypes/qt6positioningquick_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_positioning.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioning_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioningquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_positioningquick_private.pri
%{qt6dir}/modules/Positioning.json
%{qt6dir}/modules/PositioningQuick.json

%if %{with doc}
%files -n Qt6Positioning-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpositioning

%files -n Qt6Positioning-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtpositioning.qch
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
%{qt6dir}/modules/PrintSupport.json
%{qt6dir}/metatypes/qt6printsupport_pld_metatypes.json

%files -n Qt6Protobuf
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Protobuf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Protobuf.so.6
%attr(755,root,root) %{_libdir}/libQt6ProtobufQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ProtobufQuick.so.6
%attr(755,root,root) %{_libdir}/libQt6ProtobufQtCoreTypes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ProtobufQtCoreTypes.so.6
%attr(755,root,root) %{_libdir}/libQt6ProtobufQtGuiTypes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ProtobufQtGuiTypes.so.6
%attr(755,root,root) %{_libdir}/libQt6ProtobufWellKnownTypes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6ProtobufWellKnownTypes.so.6
%dir %{qt6dir}/qml/QtProtobuf
%attr(755,root,root) %{qt6dir}/qml/QtProtobuf/libprotobufquickplugin.so
%{qt6dir}/qml/QtProtobuf/plugins.qmltypes
%{qt6dir}/qml/QtProtobuf/qmldir

%files -n Qt6Protobuf-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Protobuf.so
%attr(755,root,root) %{_libdir}/libQt6ProtobufQuick.so
%attr(755,root,root) %{_libdir}/libQt6ProtobufQtCoreTypes.so
%attr(755,root,root) %{_libdir}/libQt6ProtobufQtGuiTypes.so
%attr(755,root,root) %{_libdir}/libQt6ProtobufWellKnownTypes.so
%{_libdir}/libQt6Protobuf.prl
%{_libdir}/libQt6ProtobufQuick.prl
%{_libdir}/libQt6ProtobufQtCoreTypes.prl
%{_libdir}/libQt6ProtobufQtGuiTypes.prl
%{_libdir}/libQt6ProtobufWellKnownTypes.prl
%{_includedir}/qt6/QtProtobuf
%{_includedir}/qt6/QtProtobufQuick
%{_includedir}/qt6/QtProtobufQtCoreTypes
%{_includedir}/qt6/QtProtobufQtGuiTypes
%{_includedir}/qt6/QtProtobufWellKnownTypes
%{_libdir}/cmake/Qt6Protobuf
%{_libdir}/cmake/Qt6ProtobufQuick
%{_libdir}/cmake/Qt6ProtobufQtCoreTypes
%{_libdir}/cmake/Qt6ProtobufQtGuiTypes
%{_libdir}/cmake/Qt6ProtobufWellKnownTypes
%{qt6dir}/metatypes/qt6protobuf_pld_metatypes.json
%{qt6dir}/metatypes/qt6protobufquick_pld_metatypes.json
%{qt6dir}/metatypes/qt6protobufqtcoretypes_pld_metatypes.json
%{qt6dir}/metatypes/qt6protobufqtguitypes_pld_metatypes.json
%{qt6dir}/metatypes/qt6protobufwellknowntypes_pld_metatypes.json
%{_pkgconfigdir}/Qt6Protobuf.pc
%{_pkgconfigdir}/Qt6ProtobufQuick.pc
%{_pkgconfigdir}/Qt6ProtobufQtCoreTypes.pc
%{_pkgconfigdir}/Qt6ProtobufQtGuiTypes.pc
%{_pkgconfigdir}/Qt6ProtobufWellKnownTypes.pc
%{qt6dir}/mkspecs/modules/qt_lib_protobuf.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobuf_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufquick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufqtcoretypes.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufqtcoretypes_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufqtguitypes.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufqtguitypes_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufwellknowntypes.pri
%{qt6dir}/mkspecs/modules/qt_lib_protobufwellknowntypes_private.pri
%{qt6dir}/modules/Protobuf.json
%{qt6dir}/modules/ProtobufQuick.json
%{qt6dir}/modules/ProtobufQtCoreTypes.json
%{qt6dir}/modules/ProtobufQtGuiTypes.json
%{qt6dir}/modules/ProtobufWellKnownTypes.json

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
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/private/plugins.qmltypes
%{qt6dir}/qml/Qt5Compat/GraphicalEffects/private/qmldir

%files -n Qt6Qt5Compat-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Core5Compat.so
%{_libdir}/libQt6Core5Compat.prl
%{qt6dir}/metatypes/qt6core5compat_pld_metatypes.json
%{_includedir}/qt6/QtCore5Compat
%{_pkgconfigdir}/Qt6Core5Compat.pc
%{_libdir}/cmake/Qt6Core5Compat
%{qt6dir}/mkspecs/modules/qt_lib_core5compat.pri
%{qt6dir}/mkspecs/modules/qt_lib_core5compat_private.pri
%{qt6dir}/modules/Core5Compat.json

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
%attr(755,root,root) %{_libdir}/libQt6LabsPlatform.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsPlatform.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsQmlModels.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsQmlModels.so.6
%attr(755,root,root) %{_libdir}/libQt6LabsSettings.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6LabsSettings.so.6
%attr(755,root,root) %{_libdir}/libQt6Qml.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Qml.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlCompiler.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlCompiler.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlCore.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlCore.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlMeta.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlMeta.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlModels.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlModels.so.6
%attr(755,root,root) %{_libdir}/libQt6QmlNetwork.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QmlNetwork.so.6
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

%dir %{qt6dir}/plugins/qmllint
%attr(755,root,root) %{qt6dir}/plugins/qmllint/libquicklintplugin.so
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

%dir %{qt6dir}/qml

%dir %{qt6dir}/qml/QML
%{qt6dir}/qml/QML/plugins.qmltypes
%{qt6dir}/qml/QML/qmldir

%dir %{qt6dir}/qml/QmlTime
%{qt6dir}/qml/QmlTime/qmldir
%{qt6dir}/qml/QmlTime/qmltime.qmltypes

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
%attr(755,root,root) %{qt6dir}/qml/Qt/labs/platform/liblabsplatformplugin.so
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

%dir %{qt6dir}/qml/Qt/test

%dir %{qt6dir}/qml/Qt/test/controls
%attr(755,root,root) %{qt6dir}/qml/Qt/test/controls/libquickcontrolstestutilsprivateplugin.so
%{qt6dir}/qml/Qt/test/controls/QuickControlsTestUtilsPrivate.qmltypes
%{qt6dir}/qml/Qt/test/controls/qmldir

%dir %{qt6dir}/qml/QtNetwork
%attr(755,root,root) %{qt6dir}/qml/QtNetwork/libqmlnetworkplugin.so
%{qt6dir}/qml/QtNetwork/plugins.qmltypes
%{qt6dir}/qml/QtNetwork/qmldir

%dir %{qt6dir}/qml/QtQml
%attr(755,root,root) %{qt6dir}/qml/QtQml/libqmlplugin.so
%{qt6dir}/qml/QtQml/plugins.qmltypes
%{qt6dir}/qml/QtQml/qmldir

%dir %{qt6dir}/qml/QtQml/Models
%attr(755,root,root) %{qt6dir}/qml/QtQml/Models/libmodelsplugin.so
%{qt6dir}/qml/QtQml/Models/plugins.qmltypes
%{qt6dir}/qml/QtQml/Models/qmldir
%{qt6dir}/qml/builtins.qmltypes

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

%files -n Qt6Qml-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6LabsAnimation.so
%attr(755,root,root) %{_libdir}/libQt6LabsFolderListModel.so
%attr(755,root,root) %{_libdir}/libQt6LabsPlatform.so
%attr(755,root,root) %{_libdir}/libQt6LabsQmlModels.so
%attr(755,root,root) %{_libdir}/libQt6LabsSettings.so
%attr(755,root,root) %{_libdir}/libQt6Qml.so
%attr(755,root,root) %{_libdir}/libQt6QmlCompiler.so
%attr(755,root,root) %{_libdir}/libQt6QmlCore.so
%attr(755,root,root) %{_libdir}/libQt6QmlMeta.so
%attr(755,root,root) %{_libdir}/libQt6QmlModels.so
%attr(755,root,root) %{_libdir}/libQt6QmlNetwork.so
%attr(755,root,root) %{_libdir}/libQt6QmlWorkerScript.so
%attr(755,root,root) %{_libdir}/libQt6QmlLocalStorage.so
%attr(755,root,root) %{_libdir}/libQt6QmlXmlListModel.so
%attr(755,root,root) %{_libdir}/libQt6StateMachine.so
%attr(755,root,root) %{_libdir}/libQt6StateMachineQml.so
# static-only
%{_libdir}/libQt6PacketProtocol.a
%{_libdir}/libQt6QmlDebug.a
%{_libdir}/libQt6QmlDom.a
%{_libdir}/libQt6QmlLS.a
%{_libdir}/libQt6QmlLS.prl
%{_libdir}/libQt6QmlToolingSettings.a
%{_libdir}/libQt6QmlToolingSettings.prl
%{_libdir}/libQt6QmlTypeRegistrar.a
%{_libdir}/libQt6LabsAnimation.prl
%{_libdir}/libQt6LabsFolderListModel.prl
%{_libdir}/libQt6LabsPlatform.prl
%{_libdir}/libQt6LabsQmlModels.prl
%{_libdir}/libQt6LabsSettings.prl
%{qt6dir}/metatypes/qt6labsanimation_pld_metatypes.json
%{qt6dir}/metatypes/qt6labsfolderlistmodel_pld_metatypes.json
%{qt6dir}/metatypes/qt6labsplatform_pld_metatypes.json
%{qt6dir}/metatypes/qt6labsqmlmodels_pld_metatypes.json
%{qt6dir}/metatypes/qt6labssettings_pld_metatypes.json
%{qt6dir}/metatypes/qt6packetprotocolprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qml_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlcompiler_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlcore_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmldebugprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmldomprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmllocalstorage_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmllsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlmeta_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlmodels_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlnetwork_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmltoolingsettingsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmltyperegistrarprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlworkerscript_pld_metatypes.json
%{qt6dir}/metatypes/qt6qmlxmllistmodel_pld_metatypes.json
%{qt6dir}/metatypes/qt6statemachine_pld_metatypes.json
%{qt6dir}/metatypes/qt6statemachineqml_pld_metatypes.json
%{_libdir}/libQt6PacketProtocol.prl
%{_libdir}/libQt6Qml.prl
%{_libdir}/libQt6QmlCompiler.prl
%{_libdir}/libQt6QmlCore.prl
%{_libdir}/libQt6QmlDebug.prl
%{_libdir}/libQt6QmlDom.prl
%{_libdir}/libQt6QmlLocalStorage.prl
%{_libdir}/libQt6QmlMeta.prl
%{_libdir}/libQt6QmlModels.prl
%{_libdir}/libQt6QmlNetwork.prl
%{_libdir}/libQt6QmlTypeRegistrar.prl
%{_libdir}/libQt6QmlWorkerScript.prl
%{_libdir}/libQt6QmlXmlListModel.prl
%{_libdir}/libQt6StateMachine.prl
%{_libdir}/libQt6StateMachineQml.prl
%{_includedir}/qt6/QtLabsAnimation
%{_includedir}/qt6/QtLabsFolderListModel
%{_includedir}/qt6/QtLabsPlatform
%{_includedir}/qt6/QtLabsQmlModels
%{_includedir}/qt6/QtLabsSettings
%{_includedir}/qt6/QtPacketProtocol
%{_includedir}/qt6/QtQml
%{_includedir}/qt6/QtQmlCompiler
%{_includedir}/qt6/QtQmlCore
%{_includedir}/qt6/QtQmlDebug
%{_includedir}/qt6/QtQmlDom
%{_includedir}/qt6/QtQmlIntegration
%{_includedir}/qt6/QtQmlLS
%{_includedir}/qt6/QtQmlLocalStorage
%{_includedir}/qt6/QtQmlMeta
%{_includedir}/qt6/QtQmlModels
%{_includedir}/qt6/QtQmlNetwork
%{_includedir}/qt6/QtQmlToolingSettings
%{_includedir}/qt6/QtQmlTypeRegistrar
%{_includedir}/qt6/QtQmlWorkerScript
%{_includedir}/qt6/QtQmlXmlListModel
%{_includedir}/qt6/QtStateMachine
%{_includedir}/qt6/QtStateMachineQml
%{_pkgconfigdir}/Qt6LabsAnimation.pc
%{_pkgconfigdir}/Qt6LabsFolderListModel.pc
%{_pkgconfigdir}/Qt6LabsPlatform.pc
%{_pkgconfigdir}/Qt6LabsQmlModels.pc
%{_pkgconfigdir}/Qt6LabsSettings.pc
%{_pkgconfigdir}/Qt6Qml.pc
%{_pkgconfigdir}/Qt6QmlCompiler.pc
%{_pkgconfigdir}/Qt6QmlMeta.pc
%{_pkgconfigdir}/Qt6QmlModels.pc
%{_pkgconfigdir}/Qt6QmlNetwork.pc
%{_pkgconfigdir}/Qt6QmlWorkerScript.pc
%{_pkgconfigdir}/Qt6StateMachine.pc
%{_pkgconfigdir}/Qt6StateMachineQml.pc
%{_pkgconfigdir}/Qt6QmlCore.pc
%{_pkgconfigdir}/Qt6QmlIntegration.pc
%{_pkgconfigdir}/Qt6QmlLocalStorage.pc
%{_pkgconfigdir}/Qt6QmlXmlListModel.pc
%{_libdir}/cmake/Qt6LabsAnimation
%{_libdir}/cmake/Qt6LabsFolderListModel
%{_libdir}/cmake/Qt6LabsPlatform
%{_libdir}/cmake/Qt6LabsQmlModels
%{_libdir}/cmake/Qt6LabsSettings
%{_libdir}/cmake/Qt6PacketProtocolPrivate
%{_libdir}/cmake/Qt6Qml
%{_libdir}/cmake/Qt6QmlCompiler
%{_libdir}/cmake/Qt6QmlCore
%{_libdir}/cmake/Qt6QmlDebugPrivate
%{_libdir}/cmake/Qt6QmlDomPrivate
%{_libdir}/cmake/Qt6QmlImportScanner
%{_libdir}/cmake/Qt6QmlIntegration
%{_libdir}/cmake/Qt6QmlLSPrivate
%{_libdir}/cmake/Qt6QmlLocalStorage
%{_libdir}/cmake/Qt6QmlMeta
%{_libdir}/cmake/Qt6QmlModels
%{_libdir}/cmake/Qt6QmlNetwork
%{_libdir}/cmake/Qt6QmlTypeRegistrarPrivate
%{_libdir}/cmake/Qt6QmlToolingSettingsPrivate
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
%{qt6dir}/mkspecs/modules/qt_lib_labsplatform.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsplatform_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsqmlmodels.pri
%{qt6dir}/mkspecs/modules/qt_lib_labsqmlmodels_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssettings.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssettings_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_packetprotocol_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcompiler.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcompiler_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcore.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlcore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmldebug_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmldom_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlintegration.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlintegration_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmllocalstorage.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmllocalstorage_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlls_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmeta.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmeta_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmodels.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlmodels_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlnetwork.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlnetwork_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qml.pri
%{qt6dir}/mkspecs/modules/qt_lib_qml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltest.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltest_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltoolingsettings_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmltyperegistrar_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlworkerscript.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlworkerscript_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlxmllistmodel.pri
%{qt6dir}/mkspecs/modules/qt_lib_qmlxmllistmodel_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachine.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachine_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachineqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_statemachineqml_private.pri
%{qt6dir}/modules/LabsAnimation.json
%{qt6dir}/modules/LabsFolderListModel.json
%{qt6dir}/modules/LabsPlatform.json
%{qt6dir}/modules/LabsQmlModels.json
%{qt6dir}/modules/LabsSettings.json
%{qt6dir}/modules/PacketProtocolPrivate.json
%{qt6dir}/modules/Qml.json
%{qt6dir}/modules/QmlCompiler.json
%{qt6dir}/modules/QmlCore.json
%{qt6dir}/modules/QmlDebugPrivate.json
%{qt6dir}/modules/QmlDomPrivate.json
%{qt6dir}/modules/QmlIntegration.json
%{qt6dir}/modules/QmlLSPrivate.json
%{qt6dir}/modules/QmlLocalStorage.json
%{qt6dir}/modules/QmlMeta.json
%{qt6dir}/modules/QmlModels.json
%{qt6dir}/modules/QmlNetwork.json
%{qt6dir}/modules/QmlToolingSettingsPrivate.json
%{qt6dir}/modules/QmlTypeRegistrarPrivate.json
%{qt6dir}/modules/QmlWorkerScript.json
%{qt6dir}/modules/QmlXmlListModel.json
%{qt6dir}/modules/StateMachine.json
%{qt6dir}/modules/StateMachineQml.json

%if %{with doc}
%files -n Qt6Qml-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtlabsplatform
%{_docdir}/qt6-doc/qtplatformintegration
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
%attr(755,root,root) %{_libdir}/libQt6QuickEffects.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickEffects.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickParticles.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickParticles.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickShapes.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickShapes.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickTest.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickTest.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickVectorImage.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickVectorImage.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickVectorImageGenerator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickVectorImageGenerator.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickWidgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickWidgets.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Basic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Basic.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2BasicStyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2BasicStyleImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Fusion.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Fusion.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2FusionStyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2FusionStyleImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Imagine.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Imagine.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2ImagineStyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2ImagineStyleImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Impl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Impl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Material.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Material.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2MaterialStyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2MaterialStyleImpl.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Universal.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2Universal.so.6
%attr(755,root,root) %{_libdir}/libQt6QuickControls2UniversalStyleImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickControls2UniversalStyleImpl.so.6
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
%attr(755,root,root) %{_libdir}/libQt6QuickTimelineBlendTrees.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6QuickTimelineBlendTrees.so.6

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

%dir %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/*.qml
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/libqtquickcontrols2fluentwinui3styleplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/dark
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/dark/images
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/icons
%dir %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/impl
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/impl/*.qml
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/impl/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/impl/libqtquickcontrols2fluentwinui3styleimplplugin.so
%dir %{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/light
%{qt6dir}/qml/QtQuick/Controls/FluentWinUI3/light/images

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
%{qt6dir}/qml/QtQuick/Controls/Imagine/impl/QuickControls2ImagineStyleImpl.qmltypes
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

%dir %{qt6dir}/qml/QtQuick/Effects
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Effects/libeffectsplugin.so
%{qt6dir}/qml/QtQuick/Effects/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Effects/qmldir

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

%dir %{qt6dir}/qml/QtQuick/VectorImage
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VectorImage/libqquickvectorimageplugin.so
%{qt6dir}/qml/QtQuick/VectorImage/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VectorImage/qmldir

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
%attr(755,root,root) %{_libdir}/libQt6QuickEffects.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Basic.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2BasicStyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Fusion.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2FusionStyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Imagine.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2ImagineStyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Impl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Material.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2MaterialStyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2Universal.so
%attr(755,root,root) %{_libdir}/libQt6QuickControls2UniversalStyleImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2QuickImpl.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2.so
%attr(755,root,root) %{_libdir}/libQt6QuickDialogs2Utils.so
%attr(755,root,root) %{_libdir}/libQt6QuickLayouts.so
%attr(755,root,root) %{_libdir}/libQt6QuickParticles.so
%attr(755,root,root) %{_libdir}/libQt6QuickShapes.so
%attr(755,root,root) %{_libdir}/libQt6QuickTemplates2.so
%attr(755,root,root) %{_libdir}/libQt6QuickTest.so
%attr(755,root,root) %{_libdir}/libQt6QuickTimeline.so
%attr(755,root,root) %{_libdir}/libQt6QuickTimelineBlendTrees.so
%attr(755,root,root) %{_libdir}/libQt6QuickVectorImage.so
%attr(755,root,root) %{_libdir}/libQt6QuickVectorImageGenerator.so
%attr(755,root,root) %{_libdir}/libQt6QuickWidgets.so
%{_libdir}/libQt6LabsSharedImage.prl
%{_libdir}/libQt6LabsWavefrontMesh.prl
%{_libdir}/libQt6Quick.prl
%{_libdir}/libQt6QuickControls2.prl
%{_libdir}/libQt6QuickControls2Basic.prl
%{_libdir}/libQt6QuickControls2BasicStyleImpl.prl
%{_libdir}/libQt6QuickControls2FluentWinUI3StyleImpl.prl
%{_libdir}/libQt6QuickControls2Fusion.prl
%{_libdir}/libQt6QuickControls2FusionStyleImpl.prl
%{_libdir}/libQt6QuickControls2Imagine.prl
%{_libdir}/libQt6QuickControls2ImagineStyleImpl.prl
%{_libdir}/libQt6QuickControls2Impl.prl
%{_libdir}/libQt6QuickControls2Material.prl
%{_libdir}/libQt6QuickControls2MaterialStyleImpl.prl
%{_libdir}/libQt6QuickControls2Universal.prl
%{_libdir}/libQt6QuickControls2UniversalStyleImpl.prl
%{_libdir}/libQt6QuickControlsTestUtils.prl
%{_libdir}/libQt6QuickDialogs2.prl
%{_libdir}/libQt6QuickDialogs2QuickImpl.prl
%{_libdir}/libQt6QuickDialogs2Utils.prl
%{_libdir}/libQt6QuickEffects.prl
%{_libdir}/libQt6QuickLayouts.prl
%{_libdir}/libQt6QuickParticles.prl
%{_libdir}/libQt6QuickShapes.prl
%{_libdir}/libQt6QuickTemplates2.prl
%{_libdir}/libQt6QuickTest.prl
%{_libdir}/libQt6QuickTestUtils.prl
%{_libdir}/libQt6QuickTimeline.prl
%{_libdir}/libQt6QuickTimelineBlendTrees.prl
%{_libdir}/libQt6QuickVectorImage.prl
%{_libdir}/libQt6QuickVectorImageGenerator.prl
%{_libdir}/libQt6QuickWidgets.prl
%{qt6dir}/metatypes/qt6quick_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicktest_pld_metatypes.json
%{_includedir}/qt6/QtLabsSharedImage
%{_includedir}/qt6/QtLabsWavefrontMesh
%{_includedir}/qt6/QtQuick
%{_includedir}/qt6/QtQuickControls2
%{_includedir}/qt6/QtQuickControls2Basic
%{_includedir}/qt6/QtQuickControls2BasicStyleImpl
%{_includedir}/qt6/QtQuickControls2FluentWinUI3StyleImpl
%{_includedir}/qt6/QtQuickControls2Fusion
%{_includedir}/qt6/QtQuickControls2FusionStyleImpl
%{_includedir}/qt6/QtQuickControls2Imagine
%{_includedir}/qt6/QtQuickControls2ImagineStyleImpl
%{_includedir}/qt6/QtQuickControls2Impl
%{_includedir}/qt6/QtQuickControls2Material
%{_includedir}/qt6/QtQuickControls2MaterialStyleImpl
%{_includedir}/qt6/QtQuickControls2Universal
%{_includedir}/qt6/QtQuickControls2UniversalStyleImpl
%{_includedir}/qt6/QtQuickControlsTestUtils
%{_includedir}/qt6/QtQuickDialogs2
%{_includedir}/qt6/QtQuickDialogs2QuickImpl
%{_includedir}/qt6/QtQuickDialogs2Utils
%{_includedir}/qt6/QtQuickEffects
%{_includedir}/qt6/QtQuickLayouts
%{_includedir}/qt6/QtQuickParticles
%{_includedir}/qt6/QtQuickShapes
%{_includedir}/qt6/QtQuickTemplates2
%{_includedir}/qt6/QtQuickTest
%{_includedir}/qt6/QtQuickTestUtils
%{_includedir}/qt6/QtQuickTimeline
%{_includedir}/qt6/QtQuickTimelineBlendTrees
%{_includedir}/qt6/QtQuickVectorImage
%{_includedir}/qt6/QtQuickVectorImageGenerator
%{_includedir}/qt6/QtQuickWidgets
%{_pkgconfigdir}/Qt6LabsSharedImage.pc
%{_pkgconfigdir}/Qt6LabsWavefrontMesh.pc
%{_pkgconfigdir}/Qt6Quick.pc
%{_pkgconfigdir}/Qt6QuickTest.pc
%{_pkgconfigdir}/Qt6QuickTimeline.pc
%{_pkgconfigdir}/Qt6QuickTimelineBlendTrees.pc
%{_pkgconfigdir}/Qt6QuickWidgets.pc
%{_pkgconfigdir}/Qt6QuickControls2.pc
%{_pkgconfigdir}/Qt6QuickControls2Basic.pc
%{_pkgconfigdir}/Qt6QuickControls2BasicStyleImpl.pc
%{_pkgconfigdir}/Qt6QuickControls2FluentWinUI3StyleImpl.pc
%{_pkgconfigdir}/Qt6QuickControls2Fusion.pc
%{_pkgconfigdir}/Qt6QuickControls2FusionStyleImpl.pc
%{_pkgconfigdir}/Qt6QuickControls2Imagine.pc
%{_pkgconfigdir}/Qt6QuickControls2ImagineStyleImpl.pc
%{_pkgconfigdir}/Qt6QuickControls2Impl.pc
%{_pkgconfigdir}/Qt6QuickControls2Material.pc
%{_pkgconfigdir}/Qt6QuickControls2MaterialStyleImpl.pc
%{_pkgconfigdir}/Qt6QuickControls2Universal.pc
%{_pkgconfigdir}/Qt6QuickControls2UniversalStyleImpl.pc
%{_pkgconfigdir}/Qt6QuickDialogs2.pc
%{_pkgconfigdir}/Qt6QuickDialogs2QuickImpl.pc
%{_pkgconfigdir}/Qt6QuickDialogs2Utils.pc
%{_pkgconfigdir}/Qt6QuickLayouts.pc
%{_pkgconfigdir}/Qt6QuickTemplates2.pc
%{_pkgconfigdir}/Qt6QuickVectorImage.pc
%{_libdir}/cmake/Qt6LabsSharedImage
%{_libdir}/cmake/Qt6LabsWavefrontMesh
%{_libdir}/cmake/Qt6Quick
%{_libdir}/cmake/Qt6QuickControls2
%{_libdir}/cmake/Qt6QuickControls2Basic
%{_libdir}/cmake/Qt6QuickControls2BasicStyleImpl
%{_libdir}/cmake/Qt6QuickControls2FluentWinUI3StyleImpl
%{_libdir}/cmake/Qt6QuickControls2Fusion
%{_libdir}/cmake/Qt6QuickControls2FusionStyleImpl
%{_libdir}/cmake/Qt6QuickControls2Imagine
%{_libdir}/cmake/Qt6QuickControls2ImagineStyleImpl
%{_libdir}/cmake/Qt6QuickControls2Impl
%{_libdir}/cmake/Qt6QuickControls2Material
%{_libdir}/cmake/Qt6QuickControls2MaterialStyleImpl
%{_libdir}/cmake/Qt6QuickControls2Universal
%{_libdir}/cmake/Qt6QuickControls2UniversalStyleImpl
%{_libdir}/cmake/Qt6QuickControlsTestUtilsPrivate
%{_libdir}/cmake/Qt6QuickDialogs2
%{_libdir}/cmake/Qt6QuickDialogs2QuickImpl
%{_libdir}/cmake/Qt6QuickDialogs2Utils
%{_libdir}/cmake/Qt6QuickEffectsPrivate
%{_libdir}/cmake/Qt6QuickLayouts
%{_libdir}/cmake/Qt6QuickParticlesPrivate
%{_libdir}/cmake/Qt6QuickShapesPrivate
%{_libdir}/cmake/Qt6QuickTemplates2
%{_libdir}/cmake/Qt6QuickTest
%{_libdir}/cmake/Qt6QuickTestUtilsPrivate
%{_libdir}/cmake/Qt6QuickTimeline
%{_libdir}/cmake/Qt6QuickTimelineBlendTrees
%{_libdir}/cmake/Qt6QuickTools
%{_libdir}/cmake/Qt6QuickVectorImage
%{_libdir}/cmake/Qt6QuickVectorImageGeneratorPrivate
%{_libdir}/cmake/Qt6QuickWidgets
%{qt6dir}/mkspecs/features/qtquickcompiler.prf
%{qt6dir}/mkspecs/modules/qt_lib_labssharedimage.pri
%{qt6dir}/mkspecs/modules/qt_lib_labssharedimage_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_labswavefrontmesh.pri
%{qt6dir}/mkspecs/modules/qt_lib_labswavefrontmesh_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2basic.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2basic_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2basicstyleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2basicstyleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fluentwinui3styleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fluentwinui3styleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fusion.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fusion_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fusionstyleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2fusionstyleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2imagine.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2imagine_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2imaginestyleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2imaginestyleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2impl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2impl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2material.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2material_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2materialstyleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2materialstyleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2universal.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2universal_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2universalstyleimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrols2universalstyleimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickcontrolstestutilsprivate_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2quickimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2quickimpl_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2utils.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickdialogs2utils_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickeffects_private.pri
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
%{qt6dir}/mkspecs/modules/qt_lib_quicktimelineblendtrees.pri
%{qt6dir}/mkspecs/modules/qt_lib_quicktimelineblendtrees_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickwidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickwidgets_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickvectorimage.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickvectorimage_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quickvectorimagegenerator_private.pri
%{qt6dir}/modules/LabsSharedImage.json
%{qt6dir}/modules/LabsWavefrontMesh.json
%{qt6dir}/modules/Quick.json
%{qt6dir}/modules/QuickControls2.json
%{qt6dir}/modules/QuickControls2Basic.json
%{qt6dir}/modules/QuickControls2BasicStyleImpl.json
%{qt6dir}/modules/QuickControls2FluentWinUI3StyleImpl.json
%{qt6dir}/modules/QuickControls2Fusion.json
%{qt6dir}/modules/QuickControls2FusionStyleImpl.json
%{qt6dir}/modules/QuickControls2Imagine.json
%{qt6dir}/modules/QuickControls2ImagineStyleImpl.json
%{qt6dir}/modules/QuickControls2Impl.json
%{qt6dir}/modules/QuickControls2Material.json
%{qt6dir}/modules/QuickControls2MaterialStyleImpl.json
%{qt6dir}/modules/QuickControls2Universal.json
%{qt6dir}/modules/QuickControls2UniversalStyleImpl.json
%{qt6dir}/modules/QuickControlsTestUtilsPrivate.json
%{qt6dir}/modules/QuickDialogs2.json
%{qt6dir}/modules/QuickDialogs2QuickImpl.json
%{qt6dir}/modules/QuickDialogs2Utils.json
%{qt6dir}/modules/QuickEffectsPrivate.json
%{qt6dir}/modules/QuickLayouts.json
%{qt6dir}/modules/QuickParticlesPrivate.json
%{qt6dir}/modules/QuickShapesPrivate.json
%{qt6dir}/modules/QuickTemplates2.json
%{qt6dir}/modules/QuickTest.json
%{qt6dir}/modules/QuickTestUtilsPrivate.json
%{qt6dir}/modules/QuickTimeline.json
%{qt6dir}/modules/QuickTimelineBlendTrees.json
%{qt6dir}/modules/QuickWidgets.json
%{qt6dir}/modules/QuickVectorImage.json
%{qt6dir}/modules/QuickVectorImageGeneratorPrivate.json
%{qt6dir}/metatypes/qt6labssharedimage_pld_metatypes.json
%{qt6dir}/metatypes/qt6labswavefrontmesh_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2basic_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2basicstyleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2fluentwinui3styleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2fusion_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2fusionstyleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2imagine_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2imaginestyleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2impl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2material_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2materialstyleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2universal_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrols2universalstyleimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickcontrolstestutilsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickdialogs2_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickdialogs2quickimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickdialogs2utils_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickeffectsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicklayouts_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickparticlesprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickshapesprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicktemplates2_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicktestutilsprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicktimeline_pld_metatypes.json
%{qt6dir}/metatypes/qt6quicktimelineblendtrees_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickvectorimage_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickvectorimagegeneratorprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quickwidgets_pld_metatypes.json

%dir %{qt6dir}/plugins/qmlls
%attr(755,root,root) %{qt6dir}/plugins/qmlls/libqmllsquickplugin.so

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
%dir %{qt6dir}/qml/QtQuick/Timeline/BlendTrees
%attr(755,root,root) %{qt6dir}/qml/QtQuick/Timeline/BlendTrees/libqtquicktimelineblendtreesplugin.so
%{qt6dir}/qml/QtQuick/Timeline/BlendTrees/plugins.qmltypes
%{qt6dir}/qml/QtQuick/Timeline/BlendTrees/qmldir

%if %{with doc}
%files -n Qt6Quick-Timeline-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquicktimeline

%files -n Qt6Quick-Timeline-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquicktimeline.qch
%endif

%if %{with qtquick3d}
%files -n qt6-quick3d
%defattr(644,root,root,755)
%attr(755,root,root) %{qt6dir}/bin/balsamui
%{?with_qtquick3dphysics:%attr(755,root,root) %{qt6dir}/bin/cooker}
%attr(755,root,root) %{qt6dir}/bin/instancer
%attr(755,root,root) %{qt6dir}/bin/materialeditor
%attr(755,root,root) %{qt6dir}/bin/shadergen
%attr(755,root,root) %{qt6dir}/bin/shapegen

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
%attr(755,root,root) %{_libdir}/libQt6Quick3DHelpersImpl.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DHelpersImpl.so.6
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
%if %{with openxr}
%attr(755,root,root) %{_libdir}/libQt6Quick3DXr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DXr.so.6
%endif
%attr(755,root,root) %{qt6dir}/bin/balsam
%attr(755,root,root) %{qt6dir}/bin/meshdebug
%dir %{qt6dir}/plugins/assetimporters
%attr(755,root,root) %{qt6dir}/plugins/assetimporters/libassimp.so
%dir %{qt6dir}/plugins/qmltooling
%attr(755,root,root) %{qt6dir}/plugins/qmltooling/libqmldbg_quick3dprofiler.so
%dir %{qt6dir}/qml/QtQuick3D
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/libqquick3dplugin.so
%{qt6dir}/qml/QtQuick3D/Quick3D.qmltypes
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
%dir %{qt6dir}/qml/QtQuick3D/Helpers/impl
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Helpers/impl/libqtquick3dhelpersimplplugin.so
%{qt6dir}/qml/QtQuick3D/Helpers/impl/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/Helpers/impl/qmldir
%{qt6dir}/qml/QtQuick3D/Helpers/impl/*.qml
%{qt6dir}/qml/QtQuick3D/MaterialEditor
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
%if %{with openxr}
%dir %{qt6dir}/qml/QtQuick3D/Xr
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Xr/libquick3dxrplugin.so
%{qt6dir}/qml/QtQuick3D/Xr/plugins.qmltypes
%{qt6dir}/qml/QtQuick3D/Xr/qmldir
%{qt6dir}/qml/QtQuick3D/Xr/*.qml
%endif

%files -n Qt6Quick3D-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3D.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetImport.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DAssetUtils.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DEffects.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DGlslParser.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DHelpers.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DHelpersImpl.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DIblBaker.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticleEffects.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DParticles.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DRuntimeRender.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DUtils.so
%{?with_openxr:%attr(755,root,root) %{_libdir}/libQt6Quick3DXr.so}
%{_libdir}/libQt6Quick3D.prl
%{_libdir}/libQt6Quick3DAssetImport.prl
%{_libdir}/libQt6Quick3DAssetUtils.prl
%{_libdir}/libQt6Quick3DEffects.prl
%{_libdir}/libQt6Quick3DGlslParser.prl
%{_libdir}/libQt6Quick3DHelpers.prl
%{_libdir}/libQt6Quick3DHelpersImpl.prl
%{_libdir}/libQt6Quick3DIblBaker.prl
%{_libdir}/libQt6Quick3DParticleEffects.prl
%{_libdir}/libQt6Quick3DParticles.prl
%{_libdir}/libQt6Quick3DRuntimeRender.prl
%{_libdir}/libQt6Quick3DUtils.prl
%{?with_openxr:%{_libdir}/libQt6Quick3DXr.prl}
%{_includedir}/qt6/QtQuick3D
%{_includedir}/qt6/QtQuick3DAssetImport
%{_includedir}/qt6/QtQuick3DAssetUtils
%{_includedir}/qt6/QtQuick3DGlslParser
%{_includedir}/qt6/QtQuick3DHelpers
%{_includedir}/qt6/QtQuick3DHelpersImpl
%{_includedir}/qt6/QtQuick3DIblBaker
%{_includedir}/qt6/QtQuick3DParticles
%{_includedir}/qt6/QtQuick3DRuntimeRender
%{_includedir}/qt6/QtQuick3DUtils
%{?with_openxr:%{_includedir}/qt6/QtQuick3DXr}
%{_pkgconfigdir}/Qt6Quick3D.pc
%{_pkgconfigdir}/Qt6Quick3DAssetImport.pc
%{_pkgconfigdir}/Qt6Quick3DAssetUtils.pc
%{_pkgconfigdir}/Qt6Quick3DEffects.pc
%{_pkgconfigdir}/Qt6Quick3DHelpers.pc
%{_pkgconfigdir}/Qt6Quick3DHelpersImpl.pc
%{_pkgconfigdir}/Qt6Quick3DIblBaker.pc
%{_pkgconfigdir}/Qt6Quick3DParticleEffects.pc
%{_pkgconfigdir}/Qt6Quick3DParticles.pc
%{_pkgconfigdir}/Qt6Quick3DRuntimeRender.pc
%{_pkgconfigdir}/Qt6Quick3DUtils.pc
%{?with_openxr:%{_pkgconfigdir}/Qt6Quick3DXr.pc}
%{_libdir}/cmake/Qt6Quick3D
%{_libdir}/cmake/Qt6Quick3DAssetImport
%{_libdir}/cmake/Qt6Quick3DAssetUtils
%{_libdir}/cmake/Qt6Quick3DEffects
%{_libdir}/cmake/Qt6Quick3DGlslParserPrivate
%{_libdir}/cmake/Qt6Quick3DHelpers
%{_libdir}/cmake/Qt6Quick3DHelpersImpl
%{_libdir}/cmake/Qt6Quick3DIblBaker
%{_libdir}/cmake/Qt6Quick3DParticleEffects
%{_libdir}/cmake/Qt6Quick3DParticles
%{_libdir}/cmake/Qt6Quick3DRuntimeRender
%{_libdir}/cmake/Qt6Quick3DTools
%{_libdir}/cmake/Qt6Quick3DUtils
%{?with_openxr:%{_libdir}/cmake/Qt6Quick3DXr}
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetimport.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetimport_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetutils.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dassetutils_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3deffects.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3deffects_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dglslparser_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpers.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpers_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpersimpl.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dhelpersimpl_private.pri
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
%{?with_openxr:%{qt6dir}/mkspecs/modules/qt_lib_quick3dxr.pri}
%{?with_openxr:%{qt6dir}/mkspecs/modules/qt_lib_quick3dxr_private.pri}
%{qt6dir}/modules/Quick3D.json
%{qt6dir}/modules/Quick3DAssetImport.json
%{qt6dir}/modules/Quick3DAssetUtils.json
%{qt6dir}/modules/Quick3DEffects.json
%{qt6dir}/modules/Quick3DGlslParserPrivate.json
%{qt6dir}/modules/Quick3DHelpers.json
%{qt6dir}/modules/Quick3DHelpersImpl.json
%{qt6dir}/modules/Quick3DIblBaker.json
%{qt6dir}/modules/Quick3DParticleEffects.json
%{qt6dir}/modules/Quick3DParticles.json
%{qt6dir}/modules/Quick3DRuntimeRender.json
%{qt6dir}/modules/Quick3DUtils.json
%{?with_openxr:%{qt6dir}/modules/Quick3DXr.json}
%{qt6dir}/metatypes/qt6quick3d_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dassetimport_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dassetutils_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3deffects_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dglslparserprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dhelpers_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dhelpersimpl_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3diblbaker_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dparticleeffects_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dparticles_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3druntimerender_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dutils_pld_metatypes.json
%{?with_openxr:%{qt6dir}/metatypes/qt6quick3dxr_pld_metatypes.json}

%if %{with doc}
%files -n Qt6Quick3D-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick3d

%files -n Qt6Quick3D-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtquick3d.qch
%endif
%endif

%if %{with qtquick3dphysics}
%files -n Qt6Quick3DPhysics
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3DPhysics.so.*.*.*
%attr(755,root,root) %{_libdir}/libQt6Quick3DPhysicsHelpers.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DPhysics.so.6
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DPhysicsHelpers.so.6
%dir %{qt6dir}/qml/QtQuick3D/Physics
%{qt6dir}/qml/QtQuick3D/Physics/qmldir
%{qt6dir}/qml/QtQuick3D/Physics/plugins.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Physics/libqquick3dphysicsplugin.so
%dir %{qt6dir}/qml/QtQuick3D/Physics/Helpers
%{qt6dir}/qml/QtQuick3D/Physics/Helpers/qmldir
%{qt6dir}/qml/QtQuick3D/Physics/Helpers/plugins.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/Physics/Helpers/libqtquick3dphysicshelpersplugin.so
%{qt6dir}/qml/QtQuick3D/Physics/designer

%files -n Qt6Quick3DPhysics-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3DPhysics.so
%attr(755,root,root) %{_libdir}/libQt6Quick3DPhysicsHelpers.so
%{_libdir}/libQt6Quick3DPhysics.prl
%{_libdir}/libQt6Quick3DPhysicsHelpers.prl
%{_includedir}/qt6/QtQuick3DPhysics
%{_includedir}/qt6/QtQuick3DPhysicsHelpers
%{_libdir}/cmake/Qt6Quick3DPhysics
%{_libdir}/cmake/Qt6Quick3DPhysicsHelpers
%{qt6dir}/metatypes/qt6quick3dphysics_pld_metatypes.json
%{qt6dir}/metatypes/qt6quick3dphysicshelpers_pld_metatypes.json
%{_pkgconfigdir}/Qt6Quick3DPhysics.pc
%{_pkgconfigdir}/Qt6Quick3DPhysicsHelpers.pc
%{qt6dir}/mkspecs/modules/qt_lib_quick3dphysics.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dphysics_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dphysicshelpers.pri
%{qt6dir}/mkspecs/modules/qt_lib_quick3dphysicshelpers_private.pri
%{qt6dir}/modules/Quick3DPhysics.json
%{qt6dir}/modules/Quick3DPhysicsHelpers.json
%endif

%files -n qt6-quickeffectmaker
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/qqem-qt6
%attr(755,root,root) %{qt6dir}/bin/qqem

%files -n Qt6QuickEffectMaker
%defattr(644,root,root,755)
%{qt6dir}/qml/QtQuickEffectMaker

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
%{qt6dir}/modules/RemoteObjects.json
%{qt6dir}/modules/RemoteObjectsQml.json
%{qt6dir}/modules/RepParser.json
%{qt6dir}/metatypes/qt6remoteobjects_pld_metatypes.json
%{qt6dir}/metatypes/qt6remoteobjectsqml_pld_metatypes.json

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
%{qt6dir}/modules/Scxml.json
%{qt6dir}/modules/ScxmlQml.json
%{qt6dir}/metatypes/qt6scxml_pld_metatypes.json
%{qt6dir}/metatypes/qt6scxmlqml_pld_metatypes.json

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
%{qt6dir}/modules/Sensors.json
%{qt6dir}/modules/SensorsQuick.json
%{qt6dir}/metatypes/qt6sensors_pld_metatypes.json
%{qt6dir}/metatypes/qt6sensorsquick_pld_metatypes.json

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
%{qt6dir}/modules/SerialBus.json
%{qt6dir}/metatypes/qt6serialbus_pld_metatypes.json

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
%{qt6dir}/modules/SerialPort.json
%{qt6dir}/metatypes/qt6serialport_pld_metatypes.json

%if %{with doc}
%files -n Qt6SerialPort-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialport

%files -n Qt6SerialPort-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtserialport.qch
%endif

%files -n Qt6SpatialAudio
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3DSpatialAudio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Quick3DSpatialAudio.so.6
%attr(755,root,root) %{_libdir}/libQt6SpatialAudio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6SpatialAudio.so.6
%dir %{qt6dir}/qml/QtQuick3D/SpatialAudio
%{qt6dir}/qml/QtQuick3D/SpatialAudio/qmldir
%{qt6dir}/qml/QtQuick3D/SpatialAudio/plugins.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtQuick3D/SpatialAudio/libquick3dspatialaudioplugin.so

%files -n Qt6SpatialAudio-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Quick3DSpatialAudio.so
%attr(755,root,root) %{_libdir}/libQt6SpatialAudio.so
%{_libdir}/libQt6Quick3DSpatialAudio.prl
%{_libdir}/libQt6SpatialAudio.prl
%{_includedir}/qt6/QtQuick3DSpatialAudio
%{_includedir}/qt6/QtSpatialAudio
%{_libdir}/cmake/Qt6Quick3DSpatialAudioPrivate
%{_libdir}/cmake/Qt6SpatialAudio
%{qt6dir}/metatypes/qt6quick3dspatialaudioprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6spatialaudio_pld_metatypes.json
%{_pkgconfigdir}/Qt6SpatialAudio.pc
%{qt6dir}/mkspecs/modules/qt_lib_quick3dspatialaudio_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_spatialaudio.pri
%{qt6dir}/mkspecs/modules/qt_lib_spatialaudio_private.pri
%{qt6dir}/modules/Quick3DSpatialAudioPrivate.json
%{qt6dir}/modules/SpatialAudio.json

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
%{qt6dir}/metatypes/qt6shadertools_pld_metatypes.json
%{_pkgconfigdir}/Qt6ShaderTools.pc
%{qt6dir}/mkspecs/modules/qt_lib_shadertools.pri
%{qt6dir}/mkspecs/modules/qt_lib_shadertools_private.pri
%{qt6dir}/modules/ShaderTools.json

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

%files -n Qt6Sql-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Sql.so
%{_libdir}/libQt6Sql.prl
%{_includedir}/qt6/QtSql
%{_pkgconfigdir}/Qt6Sql.pc
%{_libdir}/cmake/Qt6Sql/Qt6Sql*.cmake
%{qt6dir}/mkspecs/modules/qt_lib_sql.pri
%{qt6dir}/mkspecs/modules/qt_lib_sql_private.pri
%{qt6dir}/modules/Sql.json
%{qt6dir}/metatypes/qt6sql_pld_metatypes.json

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
%{qt6dir}/modules/Svg.json
%{qt6dir}/modules/SvgWidgets.json
%{qt6dir}/metatypes/qt6svg_pld_metatypes.json
%{qt6dir}/metatypes/qt6svgwidgets_pld_metatypes.json

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
%attr(755,root,root) %{qt6dir}/libexec/qt-internal-configure-tests
%attr(755,root,root) %{qt6dir}/libexec/qt-testrunner.py
%{qt6dir}/metatypes/qt6test_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_testlib.pri
%{qt6dir}/mkspecs/modules/qt_lib_testlib_private.pri
%{qt6dir}/modules/Test.json

# required by Qt6BuildInternals/StandaloneTests/QtBaseTestsConfig.cmake - separate package?
#%files -n Qt6ExampleIcons-devel
#%defattr(644,root,root,755)
%{_libdir}/libQt6ExampleIcons.a
%{_libdir}/libQt6ExampleIcons.prl
%{_includedir}/qt6/QtExampleIcons
%{_libdir}/cmake/Qt6ExampleIconsPrivate
%{qt6dir}/metatypes/qt6exampleiconsprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_example_icons_private.pri
%{qt6dir}/modules/ExampleIconsPrivate.json

# required by Qt6BuildInternals/StandaloneTests/QtToolsTestsConfig.cmake - separate package?
#%files -n Qt6QDocCatch-devel
#%defattr(644,root,root,755)
%{_includedir}/qt6/QtQDocCatch
%{_includedir}/qt6/QtQDocCatchConversions
%{_includedir}/qt6/QtQDocCatchGenerators
%{_libdir}/cmake/Qt6QDocCatchConversionsPrivate
%{_libdir}/cmake/Qt6QDocCatchGeneratorsPrivate
%{_libdir}/cmake/Qt6QDocCatchPrivate
%{qt6dir}/mkspecs/modules/qt_lib_qdoccatch_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qdoccatchconversions_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_qdoccatchgenerators_private.pri
%{qt6dir}/modules/QDocCatchConversionsPrivate.json
%{qt6dir}/modules/QDocCatchGeneratorsPrivate.json
%{qt6dir}/modules/QDocCatchPrivate.json

%files -n Qt6TextToSpeech
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6TextToSpeech.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6TextToSpeech.so.6
%dir %{qt6dir}/plugins/texttospeech
%attr(755,root,root) %{qt6dir}/plugins/texttospeech/libqtexttospeech_flite.so
%attr(755,root,root) %{qt6dir}/plugins/texttospeech/libqtexttospeech_mock.so
%attr(755,root,root) %{qt6dir}/plugins/texttospeech/libqtexttospeech_speechd.so
%dir %{qt6dir}/qml/QtTextToSpeech
%{qt6dir}/qml/QtTextToSpeech/qmldir
%{qt6dir}/qml/QtTextToSpeech/plugins.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtTextToSpeech/libtexttospeechqmlplugin.so

%files -n Qt6TextToSpeech-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6TextToSpeech.so
%{_libdir}/libQt6TextToSpeech.prl
%{_includedir}/qt6/QtTextToSpeech
%{_pkgconfigdir}/Qt6TextToSpeech.pc
%{_libdir}/cmake/Qt6TextToSpeech
%{qt6dir}/metatypes/qt6texttospeech_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_texttospeech.pri
%{qt6dir}/mkspecs/modules/qt_lib_texttospeech_private.pri
%{qt6dir}/modules/TextToSpeech.json

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
%{qt6dir}/metatypes/qt6uitools_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_uiplugin.pri
%{qt6dir}/mkspecs/modules/qt_lib_uitools.pri
%{qt6dir}/mkspecs/modules/qt_lib_uitools_private.pri
%{qt6dir}/modules/UiPlugin.json
%{qt6dir}/modules/UiTools.json

%files -n Qt6VirtualKeyboard
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6HunspellInputMethod.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6HunspellInputMethod.so.6
%attr(755,root,root) %{_libdir}/libQt6VirtualKeyboard.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6VirtualKeyboard.so.6
%attr(755,root,root) %{_libdir}/libQt6VirtualKeyboardSettings.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6VirtualKeyboardSettings.so.6
%attr(755,root,root) %{qt6dir}/plugins/platforminputcontexts/libqtvirtualkeyboardplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/libqtvkbplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/qmldir
%{qt6dir}/qml/QtQuick/VirtualKeyboard/*.qml
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Components
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Components/qmldir
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Components/qtvkbcomponentsplugin.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Components/*.qml
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Components/libqtvkbcomponentsplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Layouts
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Layouts/qmldir
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Layouts/qtvkblayoutsplugin.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Layouts/libqtvkblayoutsplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/qmldir
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/qtvkbpluginsplugin.qmltypes
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/libqtvkbpluginsplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hangul
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hangul/libqtvkbhangulplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hangul/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hangul/qmldir
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hunspell
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hunspell/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hunspell/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Hunspell/libqtvkbhunspellplugin.so
%if %{with lipi}
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Lipi
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Lipi/libqtvkblipiplugin.so
%endif
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/OpenWNN
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/OpenWNN/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/OpenWNN/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/OpenWNN/libqtvkbopenwnnplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Pinyin
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Pinyin/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Pinyin/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Pinyin/libqtvkbpinyinplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/TCIme
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/TCIme/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/TCIme/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/TCIme/libqtvkbtcimeplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Thai
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Thai/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Thai/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Plugins/Thai/libqtvkbthaiplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/libqtvkbsettingsplugin.so
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Settings/qmldir
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/*.qml
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/*.js
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/libqtvkbstylesplugin.so
%dir %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/Builtin
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/Builtin/plugins.qmltypes
%{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/Builtin/qmldir
%attr(755,root,root) %{qt6dir}/qml/QtQuick/VirtualKeyboard/Styles/Builtin/libqtvkbbuiltinstylesplugin.so
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
%attr(755,root,root) %{_libdir}/libQt6VirtualKeyboardSettings.so
%{_libdir}/libQt6HunspellInputMethod.prl
%{_libdir}/libQt6VirtualKeyboard.prl
%{_libdir}/libQt6VirtualKeyboardSettings.prl
%{_includedir}/qt6/QtHunspellInputMethod
%{_includedir}/qt6/QtVirtualKeyboard
%{_includedir}/qt6/QtVirtualKeyboardSettings
%{_pkgconfigdir}/Qt6HunspellInputMethod.pc
%{_pkgconfigdir}/Qt6VirtualKeyboard.pc
%{_pkgconfigdir}/Qt6VirtualKeyboardSettings.pc
%{_libdir}/cmake/Qt6Gui/Qt6QVirtualKeyboardPlugin*.cmake
%{_libdir}/cmake/Qt6HunspellInputMethod
%{_libdir}/cmake/Qt6VirtualKeyboard
%{_libdir}/cmake/Qt6VirtualKeyboardSettings
%{qt6dir}/metatypes/qt6hunspellinputmethod_pld_metatypes.json
%{qt6dir}/metatypes/qt6virtualkeyboard_pld_metatypes.json
%{qt6dir}/metatypes/qt6virtualkeyboardsettings_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_hunspellinputmethod.pri
%{qt6dir}/mkspecs/modules/qt_lib_hunspellinputmethod_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboard.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboard_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboardsettings.pri
%{qt6dir}/mkspecs/modules/qt_lib_virtualkeyboardsettings_private.pri
%{qt6dir}/modules/HunspellInputMethod.json
%{qt6dir}/modules/VirtualKeyboard.json
%{qt6dir}/modules/VirtualKeyboardSettings.json

%if %{with doc}
%files -n Qt6VirtualKeyboard-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtvirtualkeyboard

%files -n Qt6VirtualKeyboard-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtvirtualkeyboard.qch
%endif

%files -n Qt6Wayland
%defattr(644,root,root,755)
%dir %{qt6dir}/qml/QtWayland

%files -n Qt6Wayland-devel
%defattr(644,root,root,755)
%{_includedir}/qt6/QtWaylandGlobal
%{_libdir}/cmake/Qt6WaylandGlobalPrivate
%{qt6dir}/mkspecs/modules/qt_lib_waylandglobal_private.pri
%{qt6dir}/modules/WaylandGlobalPrivate.json

%files -n Qt6WaylandCompositor
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositor.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositor.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorIviapplication.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositorIviapplication.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorPresentationTime.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositorPresentationTime.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorWLShell.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositorWLShell.so.6
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorXdgShell.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WaylandCompositorXdgShell.so.6
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
%{qt6dir}/qml/QtWayland/Compositor/PresentationTime/plugins.qmltypes
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
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorIviapplication.so
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorPresentationTime.so
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorWLShell.so
%attr(755,root,root) %{_libdir}/libQt6WaylandCompositorXdgShell.so
%attr(755,root,root) %{_libdir}/libQt6WaylandEglCompositorHwIntegration.so
%attr(755,root,root) %{_libdir}/libQt6WlShellIntegration.so
%{_libdir}/libQt6WaylandCompositor.prl
%{_libdir}/libQt6WaylandCompositorIviapplication.prl
%{_libdir}/libQt6WaylandCompositorPresentationTime.prl
%{_libdir}/libQt6WaylandCompositorWLShell.prl
%{_libdir}/libQt6WaylandCompositorXdgShell.prl
%{_libdir}/libQt6WaylandEglCompositorHwIntegration.prl
%{_libdir}/libQt6WlShellIntegration.prl
%{_includedir}/qt6/QtWaylandCompositor
%{_includedir}/qt6/QtWaylandCompositorIviapplication
%{_includedir}/qt6/QtWaylandCompositorPresentationTime
%{_includedir}/qt6/QtWaylandCompositorWLShell
%{_includedir}/qt6/QtWaylandCompositorXdgShell
%{_includedir}/qt6/QtWaylandEglCompositorHwIntegration
%{_includedir}/qt6/QtWlShellIntegration
%{_pkgconfigdir}/Qt6WaylandCompositor.pc
%{_pkgconfigdir}/Qt6WaylandCompositorIviapplication.pc
%{_pkgconfigdir}/Qt6WaylandCompositorPresentationTime.pc
%{_pkgconfigdir}/Qt6WaylandCompositorWLShell.pc
%{_pkgconfigdir}/Qt6WaylandCompositorXdgShell.pc
%{_libdir}/cmake/Qt6WaylandCompositor
%{_libdir}/cmake/Qt6WaylandCompositorIviapplication
%{_libdir}/cmake/Qt6WaylandCompositorPresentationTime
%{_libdir}/cmake/Qt6WaylandCompositorWLShell
%{_libdir}/cmake/Qt6WaylandCompositorXdgShell
%{_libdir}/cmake/Qt6WlShellIntegrationPrivate
%{_libdir}/cmake/Qt6WaylandEglCompositorHwIntegrationPrivate
%{qt6dir}/metatypes/qt6waylandcompositor_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandcompositoriviapplication_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandcompositorpresentationtime_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandcompositorwlshell_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandcompositorxdgshell_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandeglcompositorhwintegrationprivate_pld_metatypes.json
%{qt6dir}/metatypes/qt6wlshellintegrationprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositor.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositor_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositoriviapplication.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositoriviapplication_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorpresentationtime.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorpresentationtime_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorwlshell.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorwlshell_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorxdgshell.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandcompositorxdgshell_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wayland_egl_compositor_hw_integration_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wl_shell_integration_private.pri
%{qt6dir}/modules/WaylandCompositor.json
%{qt6dir}/modules/WaylandCompositorIviapplication.json
%{qt6dir}/modules/WaylandCompositorPresentationTime.json
%{qt6dir}/modules/WaylandCompositorWLShell.json
%{qt6dir}/modules/WaylandCompositorXdgShell.json
%{qt6dir}/modules/WaylandEglCompositorHwIntegrationPrivate.json
%{qt6dir}/modules/WlShellIntegrationPrivate.json

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
%attr(755,root,root) %{qt6dir}/plugins/wayland-decoration-client/libadwaita.so
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
%{qt6dir}/metatypes/qt6waylandclient_pld_metatypes.json
%{qt6dir}/metatypes/qt6waylandeglclienthwintegrationprivate_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_waylandclient.pri
%{qt6dir}/mkspecs/modules/qt_lib_waylandclient_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_wayland_egl_client_hw_integration_private.pri
%{qt6dir}/modules/WaylandClient.json
%{qt6dir}/modules/WaylandEglClientHwIntegrationPrivate.json

%files -n Qt6Widgets
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6Widgets.so.6
%dir %{qt6dir}/plugins/styles

%files -n Qt6Widgets-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6Widgets.so
%{_libdir}/libQt6Widgets.prl
%{_includedir}/qt6/QtWidgets
%{_pkgconfigdir}/Qt6Widgets.pc
%{_libdir}/cmake/Qt6Widgets
%{_libdir}/cmake/Qt6WidgetsTools
%{qt6dir}/metatypes/qt6widgets_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_widgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_widgets_private.pri
%{qt6dir}/modules/Widgets.json

%files -n Qt6WebChannel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebChannel.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebChannel.so.6
%attr(755,root,root) %{_libdir}/libQt6WebChannelQuick.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libQt6WebChannelQuick.so.6
%dir %{qt6dir}/qml/QtWebChannel
%attr(755,root,root) %{qt6dir}/qml/QtWebChannel/libwebchannelquickplugin.so
%{qt6dir}/qml/QtWebChannel/plugins.qmltypes
%{qt6dir}/qml/QtWebChannel/qmldir

%files -n Qt6WebChannel-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQt6WebChannel.so
%attr(755,root,root) %{_libdir}/libQt6WebChannelQuick.so
%{_libdir}/libQt6WebChannel.prl
%{_libdir}/libQt6WebChannelQuick.prl
%{_includedir}/qt6/QtWebChannel
%{_includedir}/qt6/QtWebChannelQuick
%{_pkgconfigdir}/Qt6WebChannel.pc
%{_pkgconfigdir}/Qt6WebChannelQuick.pc
%{_libdir}/cmake/Qt6WebChannel
%{_libdir}/cmake/Qt6WebChannelQuick
%{qt6dir}/metatypes/qt6webchannel_pld_metatypes.json
%{qt6dir}/metatypes/qt6webchannelquick_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_webchannel.pri
%{qt6dir}/mkspecs/modules/qt_lib_webchannel_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webchannelquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webchannelquick_private.pri
%{qt6dir}/modules/WebChannel.json
%{qt6dir}/modules/WebChannelQuick.json

%if %{with doc}
%files -n Qt6WebChannel-doc
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebchannel

%files -n Qt6WebChannel-doc-qch
%defattr(644,root,root,755)
%{_docdir}/qt6-doc/qtwebchannel.qch
%endif

%if %{with qtwebengine}
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
%{_datadir}/qt6/resources/v8_context_snapshot.bin
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
%attr(755,root,root) %{_libdir}/qt6/libexec/QtWebEngineProcess
%attr(755,root,root) %{_libdir}/qt6/libexec/qwebengine_convert_dict
%attr(755,root,root) %{_libdir}/qt6/libexec/webenginedriver

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
%{qt6dir}/metatypes/qt6webenginecore_pld_metatypes.json
%{qt6dir}/metatypes/qt6webenginequick_pld_metatypes.json
%{qt6dir}/metatypes/qt6webenginequickdelegatesqml_pld_metatypes.json
%{qt6dir}/metatypes/qt6webenginewidgets_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginecore_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequickdelegatesqml.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequickdelegatesqml_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginequick_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets.pri
%{qt6dir}/mkspecs/modules/qt_lib_webenginewidgets_private.pri
%{qt6dir}/modules/WebEngineCore.json
%{qt6dir}/modules/WebEngineQuick.json
%{qt6dir}/modules/WebEngineQuickDelegatesQml.json
%{qt6dir}/modules/WebEngineWidgets.json

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
%{qt6dir}/metatypes/qt6websockets_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_websockets.pri
%{qt6dir}/mkspecs/modules/qt_lib_websockets_private.pri
%{qt6dir}/modules/WebSockets.json

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
%{qt6dir}/metatypes/qt6webview_pld_metatypes.json
%{qt6dir}/metatypes/qt6webviewquick_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_webview.pri
%{qt6dir}/mkspecs/modules/qt_lib_webview_private.pri
%{qt6dir}/mkspecs/modules/qt_lib_webviewquick.pri
%{qt6dir}/mkspecs/modules/qt_lib_webviewquick_private.pri
%{qt6dir}/modules/WebView.json
%{qt6dir}/modules/WebViewQuick.json

%if %{with qtwebengine}
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
%{qt6dir}/metatypes/qt6xml_pld_metatypes.json
%{qt6dir}/mkspecs/modules/qt_lib_xml.pri
%{qt6dir}/mkspecs/modules/qt_lib_xml_private.pri
%{qt6dir}/modules/Xml.json

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

%{_docdir}/qt6-doc/qtgraphs
%{_docdir}/qt6-doc/qtgrpc
%{_docdir}/qt6-doc/qthttpserver
%{_docdir}/qt6-doc/qtlocation
%{_docdir}/qt6-doc/qtprotobuf
%{_docdir}/qt6-doc/qtqmlcompiler
%{_docdir}/qt6-doc/qtqmlnetwork
%if %{with qtquick3dphysics}
%{_docdir}/qt6-doc/qtquick3dphysics
%endif
%{_docdir}/qt6-doc/qtquickeffectmaker
%{_docdir}/qt6-doc/qtspatialaudio
%{_docdir}/qt6-doc/qttexttospeech
%{_docdir}/qt6-doc/qtwaylandclient

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

%{_docdir}/qt6-doc/qtgraphs.qch
%{_docdir}/qt6-doc/qtgrpc.qch
%{_docdir}/qt6-doc/qthttpserver.qch
%{_docdir}/qt6-doc/qtlocation.qch
%{_docdir}/qt6-doc/qtprotobuf.qch
%{_docdir}/qt6-doc/qtqmlcompiler.qch
%{_docdir}/qt6-doc/qtqmlnetwork.qch
%if %{with qtquick3dphysics}
%{_docdir}/qt6-doc/qtquick3dphysics.qch
%endif
%{_docdir}/qt6-doc/qtquickeffectmaker.qch
%{_docdir}/qt6-doc/qtspatialaudio.qch
%{_docdir}/qt6-doc/qttexttospeech.qch
%{_docdir}/qt6-doc/qtwaylandclient.qch
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
%attr(755,root,root) %{qt6dir}/bin/androiddeployqt6
%attr(755,root,root) %{qt6dir}/bin/qdbuscpp2xml
%attr(755,root,root) %{qt6dir}/bin/qdbusxml2cpp
%attr(755,root,root) %{qt6dir}/bin/qmake
%attr(755,root,root) %{qt6dir}/bin/qmake6
%attr(755,root,root) %{qt6dir}/bin/qt-cmake
%attr(755,root,root) %{qt6dir}/bin/qt-cmake-create
%attr(755,root,root) %{qt6dir}/bin/qt-configure-module
%attr(755,root,root) %{qt6dir}/libexec/moc
%attr(755,root,root) %{qt6dir}/libexec/qlalr
%attr(755,root,root) %{qt6dir}/libexec/rcc
%attr(755,root,root) %{qt6dir}/libexec/uic
%attr(755,root,root) %{qt6dir}/libexec/cmake_automoc_parser
%{qt6dir}/libexec/ensure_pro_file.cmake
%attr(755,root,root) %{qt6dir}/libexec/qt-cmake-private
%{qt6dir}/libexec/qt-cmake-private-install.cmake
%attr(755,root,root) %{qt6dir}/libexec/qt-cmake-standalone-test
%attr(755,root,root) %{qt6dir}/libexec/qt-internal-configure-examples
%attr(755,root,root) %{qt6dir}/libexec/syncqt
%attr(755,root,root) %{qt6dir}/libexec/tracepointgen
%{qt6dir}/mkspecs/*.pri
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
%{qt6dir}/mkspecs/qnx-*
%{qt6dir}/mkspecs/solaris-*
%{qt6dir}/mkspecs/unsupported
%{qt6dir}/mkspecs/vxworks-clang
%{qt6dir}/mkspecs/wasm-emscripten
%{qt6dir}/mkspecs/wasm-emscripten-64
%{qt6dir}/mkspecs/win32-*
