#
# Conditional build:
%bcond_without	drm		# DRM compositor
%bcond_without	rdp		# RDP compositor
%bcond_without	wayland		# wayland (nested) compositor
%bcond_without	x11		# X11 compositor
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
Version:	14.0.1
Release:	2
License:	MIT
Group:		Applications
#Source0Download: https://gitlab.freedesktop.org/wayland/weston/-/releases/
Source0:	https://gitlab.freedesktop.org/wayland/weston/-/releases/%{version}/downloads/%{name}-%{version}.tar.xz
# Source0-md5:	cd958642f4729e6a8f9153e6790e5f5d
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
BuildRequires:	libdrm-devel >= 2.4.107
BuildRequires:	libevdev-devel
BuildRequires:	libinput-devel >= 1.2.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%{?with_drm:BuildRequires:	libseat-devel >= 0.4}
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	libwebp-devel
BuildRequires:	meson >= 0.63.0
%if %{with vnc}
BuildRequires:	neatvnc-devel >= 0.7.0
BuildRequires:	neatvnc-devel < 0.9.0
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
BuildRequires:	wayland-protocols >= 1.33
BuildRequires:	xcb-util-cursor-devel
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xz
%if %{with drm}
BuildRequires:	libdisplay-info-devel >= 0.1.1
BuildRequires:	libdisplay-info-devel < 0.3.0
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
BuildRequires:	doxygen >= 1.8
BuildRequires:	python3-breathe >= 4.11
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
Requires:	xorg-lib-libxkbcommon >= 0.5.0
# the rest is for modules:
%{?with_drm:Requires:	Mesa-libgbm >= 17.2}
Requires:	cairo >= 1.10.0
Requires:	dbus-libs >= 1.6
Requires:	lcms2 >= 2.9
Requires:	libdrm >= 2.4.107
Requires:	libinput >= 1.2.0
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
Requires:	xorg-lib-libxkbcommon-devel >= 0.5.0

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

%prep
%setup -q
%patch -P 0 -p1
%patch -P 1 -p1

%build
%meson \
	%{!?with_drm:-Dbackend-drm=false} \
	%{!?with_vaapi:-Dbackend-drm-screencast-vaapi=false} \
	%{!?with_pipewire:-Dbackend-pipewire=false} \
	%{!?with_rdp:-Dbackend-rdp=false} \
	%{!?with_x11:-Dbackend-x11=false} \
	%{!?with_dclients:-Ddemo-clients=""} \
	%{?with_apidocs:-Ddoc=true} \
	%{!?with_pipewire:-Dpipewire=false} \
	%{!?with_remoting:-Dremoting=false} \
	%{!?with_sclients:-Dsimple-clients=""} \
	%{!?with_xwayland:-Dxwayland=false}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

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
%attr(755,root,root) %{_bindir}/weston-simple-egl
%attr(755,root,root) %{_bindir}/weston-simple-shm
%attr(755,root,root) %{_bindir}/weston-simple-touch
%endif
%attr(755,root,root) %{_libexecdir}/weston-desktop-shell
%attr(755,root,root) %{_libexecdir}/weston-ivi-shell-user-interface
%attr(755,root,root) %{_libexecdir}/weston-keyboard
%attr(755,root,root) %{_libexecdir}/weston-simple-im
%dir %{_libdir}/weston
%attr(755,root,root) %{_libdir}/weston/libexec_weston.so*
%attr(755,root,root) %{_libdir}/weston/desktop-shell.so
%attr(755,root,root) %{_libdir}/weston/fullscreen-shell.so
%attr(755,root,root) %{_libdir}/weston/hmi-controller.so
%attr(755,root,root) %{_libdir}/weston/ivi-shell.so
%attr(755,root,root) %{_libdir}/weston/kiosk-shell.so
%attr(755,root,root) %{_libdir}/weston/screen-share.so
%attr(755,root,root) %{_libdir}/weston/systemd-notify.so
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
%dir %{_datadir}/libweston-14
%{_datadir}/libweston-14/protocols
%{_npkgconfigdir}/libweston-14-protocols.pc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-14.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libweston-14.so.0
%dir %{_libdir}/libweston-14
%attr(755,root,root) %{_libdir}/libweston-14/color-lcms.so
%if %{with drm}
%attr(755,root,root) %{_libdir}/libweston-14/drm-backend.so
%endif
%attr(755,root,root) %{_libdir}/libweston-14/gl-renderer.so
%attr(755,root,root) %{_libdir}/libweston-14/headless-backend.so
%if %{with pipewire}
%attr(755,root,root) %{_libdir}/libweston-14/pipewire-backend.so
%attr(755,root,root) %{_libdir}/libweston-14/pipewire-plugin.so
%endif
%if %{with remoting}
%attr(755,root,root) %{_libdir}/libweston-14/remoting-plugin.so
%endif
%if %{with vnc}
%attr(755,root,root) %{_libdir}/libweston-14/vnc-backend.so
%endif
%if %{with wayland}
%attr(755,root,root) %{_libdir}/libweston-14/wayland-backend.so
%endif
%if %{with x11}
%attr(755,root,root) %{_libdir}/libweston-14/x11-backend.so
%endif
%if %{with xwayland}
%attr(755,root,root) %{_libdir}/libweston-14/xwayland.so
%endif
%config(noreplace) %verify(not md5 mtime size) /etc/pam.d/weston-remote-access
%{_mandir}/man7/weston-vnc.7*

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-14.so
%{_includedir}/libweston-14
%{_pkgconfigdir}/libweston-14.pc

%if %{with rdp}
%files compositor-rdp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-14/rdp-backend.so
%{_mandir}/man7/weston-rdp.7*
%endif
