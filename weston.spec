#
# Conditional build:
%bcond_without	drm		# DRM compositor
%bcond_without	rdp		# RDP compositor
%bcond_without	wayland		# wayland (nested) compositor
%bcond_without	x11		# X11 compositor
%bcond_without	vulkan		# Vulkan renderer
%bcond_without	libunwind	# libunwind usage for backtraces
%bcond_without	vaapi		# vaapi recorder
%bcond_without	vnc		# VNC backend
%bcond_without	xwayland	# X server launcher
%bcond_without	dclients	# demo clients
%bcond_without	sclients	# simple clients
%bcond_without	clients		# non-simple clients
%bcond_without	remoting	# remoting-plugin (requires DRM compositor + GStreamer)
%bcond_without	pipewire	# pipewire backend and plugin
%bcond_with	apidocs		# documentation (requires Sphinx 2.1+)

%if %{without drm}
%undefine	with_remoting
%endif
Summary:	Weston - Wayland demos
Summary(pl.UTF-8):	Weston - programy demonstracyjne dla protokołu Wayland
Name:		weston
Version:	15.0.0
Release:	1
License:	MIT
Group:		Applications
#Source0Download: https://gitlab.freedesktop.org/wayland/weston/-/releases/
Source0:	https://gitlab.freedesktop.org/wayland/weston/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
# Source0-md5:	f94d17a7f67a7f036ed89961a53ea8f5
Patch0:		%{name}-freerdp2.patch
Patch1:		%{name}-noarch-protocols.patch
URL:		https://wayland.freedesktop.org/
BuildRequires:	EGL-devel
BuildRequires:	Mesa-libgbm-devel >= 21.1.1
BuildRequires:	OpenGLESv2-devel
%if %{with vnc}
BuildRequires:	aml-devel >= 0.3.0
BuildRequires:	aml-devel < 0.4
%endif
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	dbus-devel >= 1.6
BuildRequires:	doxygen
%{?with_rdp:BuildRequires:	freerdp3-devel >= 3.0.0}
BuildRequires:	glib2-devel >= 1:2.36
%if %{with remoting}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
BuildRequires:	lcms2-devel >= 2.9
BuildRequires:	libdisplay-info-devel >= 0.2.0
BuildRequires:	libdisplay-info-devel < 0.4.0
BuildRequires:	libdrm-devel >= 2.4.107
BuildRequires:	libevdev-devel
BuildRequires:	libinput-devel >= 1.26.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%{?with_drm:BuildRequires:	libseat-devel >= 0.4}
BuildRequires:	libstdc++-devel >= 6:8
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	libwebp-devel
BuildRequires:	lua-devel >= 5.4
BuildRequires:	meson >= 0.63.0
%if %{with vnc}
BuildRequires:	neatvnc-devel >= 0.7.0
BuildRequires:	neatvnc-devel < 0.10.0
%endif
BuildRequires:	ninja >= 1.5
%{?with_pipewire:BuildRequires:	pipewire-devel >= 0.3}
BuildRequires:	pixman-devel >= 0.26
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	python3 >= 1:3
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	systemd-devel
BuildRequires:	tar >= 1:1.22
# wayland-client, wayland-cursor, wayland-server
BuildRequires:	wayland-devel >= 1.22.0
# for wayland and sclients, but also desktop-shell, which is always enabled
BuildRequires:	wayland-egl-devel
BuildRequires:	wayland-protocols >= 1.46
BuildRequires:	xcb-util-cursor-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 1.8.0
BuildRequires:	xz
%if %{with drm}
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	udev-devel >= 1:136
%endif
%if %{with vaapi}
BuildRequires:	libva-devel >= 1.2.0
BuildRequires:	libva-drm-devel >= 1.2.0
# API versions
BuildRequires:	pkgconfig(libva) >= 0.34.0
BuildRequires:	pkgconfig(libva-drm) >= 0.34.0
%endif
%if %{with x11}
# xcb >= 1.8 xcb-xkb >= 1.9 xcb-shm
BuildRequires:	libxcb-devel >= 1.9
BuildRequires:	xorg-lib-libX11-devel
%endif
%if %{with vulkan}
BuildRequires:	Vulkan-Loader-devel
BuildRequires:	glslang
%endif
%if %{with vnc}
BuildRequires:	pam-devel
%endif
%if %{with xwayland}
# xcb xcb-composite xcb-xfixes
BuildRequires:	libxcb-devel
BuildRequires:	pango-devel >= 1:1.10
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	xorg-lib-libXcursor-devel
BuildRequires:	xorg-xserver-Xwayland-devel
%endif
%if %{with apidocs}
BuildRequires:	doxygen >= 1:1.8
BuildRequires:	python3-breathe >= 4.11
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg >= 2.1.0
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Weston contains a few demo application for the Wayland project.
There's a sample compositor that can run on KMS, under X11 or under
another Wayland compositor and there's a handful of simple clients
that demonstrate various aspects of Wayland.

%description -l pl.UTF-8
Weston zawiera kilka aplikacji demonstracyjnych dla projektu Wayland.
Jest przykładowy serwer składający, który można uruchomić pod KMS, pod
X11 lub pod innym serwerem składającym Wayland; są także proste
programy klienckie demonstrujące różne aspekty protokołu Wayland.

%package devel
Summary:	Header files for Weston plugin development
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek dla Westona
Group:		Development/Libraries
Requires:	%{name}-libs-devel = %{version}-%{release}
Requires:	EGL-devel
Requires:	OpenGLESv2-devel

%description devel
Header files for Weston plugin development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek dla Westona.

%package protocols
Summary:	Weston protocol files
Summary(pl.UTF-8):	Pliki protokołu Weston
Group:		Libraries
Conflicts:	weston < 9.0.0-2
Conflicts:	weston-libs-devel < 9.0.0-2
BuildArch:	noarch

%description protocols
Weston protocol files.

%description protocols -l pl.UTF-8
Pliki protokołu Weston.

%package libs
Summary:	Weston compositor libraries
Summary(pl.UTF-8):	Biblioteki serwera składania Weston
Group:		Libraries
Requires:	wayland >= 1.18.0
Requires:	pixman >= 0.26
Requires:	xorg-lib-libxkbcommon >= 1.8.0
# the rest is for modules:
%{?with_drm:Requires:	Mesa-libgbm >= 17.2}
Requires:	cairo >= 1.10.0
Requires:	dbus-libs >= 1.6
Requires:	lcms2 >= 2.9
Requires:	libdrm >= 2.4.107
Requires:	libinput >= 1.26.0
%{?with_drm:Requires:	libseat >= 0.4}
%if %{with vaapi}
Requires:	libva >= 1.2.0
Requires:	libva-drm >= 1.2.0
%endif
%{?with_x11:Requires:	libxcb >= 1.9}
%{?with_drm:Requires:	mtdev >= 1.1.0}
%{?with_drm:Requires:	udev-libs >= 1:136}
Requires:	wayland-egl

%description libs
Weston compositor libraries.

%description libs -l pl.UTF-8
Biblioteki serwera składania Weston.

%package libs-devel
Summary:	Header files for libweston compositors development
Summary(pl.UTF-8):	Pliki nagłówkowe do rozwijania modułów składających biblioteki libweston
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	pixman-devel >= 0.26
# wayland-server
Requires:	wayland-devel >= 1.22.0
Requires:	xorg-lib-libxkbcommon-devel >= 1.8.0

%description libs-devel
Header files for libweston compositors development.

%description libs-devel -l pl.UTF-8
Pliki nagłówkowe do rozwijania modułów składających biblioteki
libweston.

%package compositor-rdp
Summary:	RDP compositor plugin for Weston
Summary(pl.UTF-8):	Wtyczka składająca RDP dla Westona
Group:		Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	freerdp3 >= 3.0.0

%description compositor-rdp
RDP compositor plugin for Weston.

%description compositor-rdp -l pl.UTF-8
Wtyczka składająca RDP dla Westona.

%package apidocs
Summary:	Weston API documentation
Summary(pl.UTF-8):	Dokumentacja API Westona
Group:		Documentation
BuildArch:	noarch

%description apidocs
Weston API documentation.

%description apidocs -l pl.UTF-8
Dokumentacja API Westona.

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%build
%meson \
	--libexecdir="%{_libexecdir}/weston" \
	%{!?with_drm:-Dbackend-drm=false} \
	%{!?with_pipewire:-Dbackend-pipewire=false} \
	%{!?with_rdp:-Dbackend-rdp=false} \
	%{!?with_x11:-Dbackend-x11=false} \
	%{!?with_vulkan:-Drenderer-vulkan=false} \
	%{!?with_dclients:-Ddemo-clients=""} \
	%{?with_apidocs:-Ddoc=true} \
	%{!?with_pipewire:-Dpipewire=false} \
	%{!?with_remoting:-Dremoting=false} \
	%{!?with_sclients:-Dsimple-clients=""} \
	%{!?with_xwayland:-Dxwayland=false} \
	-Ddeprecated-backend-drm-screencast-vaapi=%{__true_false vaapi} \
	-Ddeprecated-screenshare=true \
	-Ddeprecated-shell-fullscreen=true \
	-Dtests=false

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with apidocs}
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/weston/{_sources,objects.inv}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc COPYING README.md
%attr(755,root,root) %{_bindir}/wcap-decode
# composer
%attr(755,root,root) %{_bindir}/weston
%attr(755,root,root) %{_bindir}/weston-calibrator
%attr(755,root,root) %{_bindir}/weston-color
%attr(755,root,root) %{_bindir}/weston-debug
%attr(755,root,root) %{_bindir}/weston-screenshooter
%attr(755,root,root) %{_bindir}/weston-terminal
%attr(755,root,root) %{_bindir}/weston-touch-calibrator
%if %{with dclients}
%attr(755,root,root) %{_bindir}/weston-clickdot
%attr(755,root,root) %{_bindir}/weston-cliptest
%attr(755,root,root) %{_bindir}/weston-constraints
%attr(755,root,root) %{_bindir}/weston-content_protection
%attr(755,root,root) %{_bindir}/weston-dnd
%attr(755,root,root) %{_bindir}/weston-editor
%attr(755,root,root) %{_bindir}/weston-eventdemo
%attr(755,root,root) %{_bindir}/weston-flower
%attr(755,root,root) %{_bindir}/weston-fullscreen
%attr(755,root,root) %{_bindir}/weston-image
%attr(755,root,root) %{_bindir}/weston-multi-resource
%attr(755,root,root) %{_bindir}/weston-presentation-shm
%attr(755,root,root) %{_bindir}/weston-resizor
%attr(755,root,root) %{_bindir}/weston-scaler
%attr(755,root,root) %{_bindir}/weston-smoke
%attr(755,root,root) %{_bindir}/weston-stacking
%attr(755,root,root) %{_bindir}/weston-subsurfaces
%attr(755,root,root) %{_bindir}/weston-tablet
%attr(755,root,root) %{_bindir}/weston-transformed
%endif
%if %{with sclients}
%attr(755,root,root) %{_bindir}/weston-simple-damage
%attr(755,root,root) %{_bindir}/weston-simple-dmabuf-egl
%attr(755,root,root) %{_bindir}/weston-simple-dmabuf-feedback
%attr(755,root,root) %{_bindir}/weston-simple-dmabuf-v4l
%{?with_vulkan:%attr(755,root,root) %{_bindir}/weston-simple-dmabuf-vulkan}
%attr(755,root,root) %{_bindir}/weston-simple-egl
%attr(755,root,root) %{_bindir}/weston-simple-shm
%attr(755,root,root) %{_bindir}/weston-simple-timing
%attr(755,root,root) %{_bindir}/weston-simple-touch
%{?with_vulkan:%attr(755,root,root) %{_bindir}/weston-simple-vulkan}
%endif
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/weston
%endif
%{_libexecdir}/weston/shell.lua
%attr(755,root,root) %{_libexecdir}/weston/weston-desktop-shell
%attr(755,root,root) %{_libexecdir}/weston/weston-ivi-shell-user-interface
%attr(755,root,root) %{_libexecdir}/weston/weston-keyboard
%attr(755,root,root) %{_libexecdir}/weston/weston-simple-im
%dir %{_libdir}/weston
%{_libdir}/weston/libexec_weston.so*
%{_libdir}/weston/desktop-shell.so
%{_libdir}/weston/fullscreen-shell.so
%{_libdir}/weston/hmi-controller.so
%{_libdir}/weston/ivi-shell.so
%{_libdir}/weston/kiosk-shell.so
%{_libdir}/weston/lua-shell.so
%{_libdir}/weston/screen-share.so
%{_libdir}/weston/systemd-notify.so
%{_datadir}/weston
%dir %{_datadir}/wayland-sessions
%{_datadir}/wayland-sessions/weston.desktop
%{_mandir}/man1/weston.1*
%{_mandir}/man1/weston-debug.1*
%{_mandir}/man5/weston.ini.5*
%{_mandir}/man7/weston-bindings.7*
%{_mandir}/man7/weston-drm.7*

%files devel
%defattr(644,root,root,755)
%{_includedir}/weston
%{_pkgconfigdir}/weston.pc

%files protocols
%defattr(644,root,root,755)
%dir %{_datadir}/libweston-15
%{_datadir}/libweston-15/protocols
%{_npkgconfigdir}/libweston-15-protocols.pc

%files libs
%defattr(644,root,root,755)
%{_libdir}/libweston-15.so.*.*.*
%ghost %{_libdir}/libweston-15.so.0
%dir %{_libdir}/libweston-15
%{_libdir}/libweston-15/color-lcms.so
%if %{with drm}
%{_libdir}/libweston-15/drm-backend.so
%endif
%{_libdir}/libweston-15/gl-renderer.so
%{_libdir}/libweston-15/headless-backend.so
%if %{with pipewire}
%{_libdir}/libweston-15/pipewire-backend.so
%{_libdir}/libweston-15/pipewire-plugin.so
%endif
%if %{with remoting}
%{_libdir}/libweston-15/remoting-plugin.so
%endif
%if %{with vnc}
%{_libdir}/libweston-15/vnc-backend.so
%endif
%if %{with vulkan}
%{_libdir}/libweston-15/vulkan-renderer.so
%endif
%if %{with wayland}
%{_libdir}/libweston-15/wayland-backend.so
%endif
%if %{with x11}
%{_libdir}/libweston-15/x11-backend.so
%endif
%if %{with xwayland}
%{_libdir}/libweston-15/xwayland.so
%endif
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/weston-remote-access
%{_mandir}/man7/weston-vnc.7*

%files libs-devel
%defattr(644,root,root,755)
%{_libdir}/libweston-15.so
%{_includedir}/libweston-15
%{_pkgconfigdir}/libweston-15.pc

%if %{with rdp}
%files compositor-rdp
%defattr(644,root,root,755)
%{_libdir}/libweston-15/rdp-backend.so
%{_mandir}/man7/weston-rdp.7*
%endif

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_docdir}/weston
%endif
