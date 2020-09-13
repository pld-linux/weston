#
# Conditional build:
%bcond_without	drm		# DRM compositor
%bcond_without	rdp		# RDP compositor (needs freerdp2 or freerdp >= 1.1.0)
%bcond_without	wayland		# wayland (nested) compositor
%bcond_without	x11		# X11 compositor
%bcond_without	libunwind	# libunwind usage for backtraces
%bcond_without	vaapi		# vaapi recorder
%bcond_without	wlaunch		# weston launch
%bcond_without	xwayland	# X server launcher
%bcond_without	dclients	# demo clients
%bcond_without	sclients	# simple clients
%bcond_without	clients		# non-simple clients
%bcond_without	remoting	# remoting-plugin (requires DRM compositor + GStreamer)
%bcond_with	pipewire	# pipewire plugin
%bcond_with	apidocs		# documentation (requires Sphinx 2.1+)

%if %{without drm}
%undefine	with_remoting
%endif
Summary:	Weston - Wayland demos
Summary(pl.UTF-8):	Weston - programy demonstracyjne dla protokołu Wayland
Name:		weston
Version:	9.0.0
Release:	1
License:	MIT
Group:		Applications
#Source0Download: https://wayland.freedesktop.org/releases.html
Source0:	https://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	b406da0fe9139fd39653238fde22a6cf
Patch0:		%{name}-freerdp2.patch
URL:		https://wayland.freedesktop.org/
BuildRequires:	Mesa-libEGL-devel >= 7.10
# GLESv2
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	colord-devel >= 0.1.27
BuildRequires:	dbus-devel >= 1.6
BuildRequires:	doxygen
# or freerdp >= 1.1.0 (without freerdp2 patch)
%{?with_rdp:BuildRequires:	freerdp2-devel >= 2.0.0-0.20180809.1}
BuildRequires:	glib2-devel >= 1:2.36
%if %{with remoting}
BuildRequires:	gstreamer-devel >= 1.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0
%endif
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libdrm-devel >= 2.4.86
BuildRequires:	libevdev-devel
BuildRequires:	libinput-devel >= 0.8.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%{?with_libunwind:BuildRequires:	libunwind-devel}
BuildRequires:	libwebp-devel
BuildRequires:	meson >= 0.47
BuildRequires:	ninja >= 1.5
%{?with_pipewire:BuildRequires:	pipewire-devel >= 0.2}
%{?with_pipewire:BuildRequires:	pipewire-devel < 0.3}
BuildRequires:	pixman-devel >= 0.26
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
# wayland-server always; wayland-client if with_wayland || with_sclients || with_clients; wayland-cursor if with_clients
BuildRequires:	wayland-devel >= 1.17.0
# for wayland and sclients, but also desktop-shell, which is always enabled
BuildRequires:	wayland-egl-devel
BuildRequires:	wayland-protocols >= 1.18
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.5.0
BuildRequires:	xz
%if %{with drm}
BuildRequires:	Mesa-libgbm-devel >= 17.2
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
%if %{with wlaunch}
BuildRequires:	pam-devel
%endif
%if %{with xwayland}
# xcb xcb-composite xcb-xfixes
BuildRequires:	libxcb-devel
BuildRequires:	pango-devel >= 1:1.10
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	xorg-lib-libXcursor-devel
%endif
%if %{with apidocs}
BuildRequires:	doxygen >= 1.8
BuildRequires:	python3-breathe >= 4.11
BuildRequires:	sphinx-pdg >= 2.1.0
%endif
Requires:	%{name}-libs = %{version}-%{release}
Requires:	colord-libs >= 0.1.27
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
Requires:	Mesa-libEGL-devel >= 7.10
# GLESv2
Requires:	Mesa-libGLES-devel

%description devel
Header files for Weston plugin development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek dla Westona.

%package libs
Summary:	Weston compositor libraries
Summary(pl.UTF-8):	Biblioteki serwera składania Weston
Group:		Libraries
Requires:	wayland >= 1.17.0
Requires:	pixman >= 0.26
Requires:	xorg-lib-libxkbcommon >= 0.5.0
# the rest is for modules:
Requires:	Mesa-libEGL >= 7.10
%{?with_drm:Requires:	Mesa-libgbm >= 17.2}
Requires:	cairo >= 1.10.0
Requires:	dbus-libs >= 1.6
Requires:	libdrm >= 2.4.86
Requires:	libinput >= 0.8.0
%if %{with vaapi}
Requires:	libva >= 1.2.0
Requires:	libva-drm >= 1.2.0
%endif
%{?with_x11:Requires:	libxcb >= 1.9}
%{?with_drm:Requires:	mtdev >= 1.1.0}
%{?with_wlaunch:Requires:	systemd-libs >= 1:209}
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
Requires:	wayland-devel >= 1.17.0
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
Requires:	freerdp2 >= 2.0.0-0.20180809.1

%description compositor-rdp
RDP compositor plugin for Weston.

%description compositor-rdp -l pl.UTF-8
Wtyczka składająca RDP dla Westona.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	%{!?with_pipewire:-Dpipewire=false} \
	%{!?with_drm:-Dbackend-drm=false} \
	%{!?with_vaapi:-Dbackend-drm-screencast-vaapi=false} \
	%{!?with_rdp:-Dbackend-rdp=false} \
	%{!?with_x11:-Dbackend-x11=false} \
	%{!?with_dclients:-Ddemo-clients=""} \
	%{?with_apidocs:-Ddoc=true} \
	%{!?with_remoting:-Dremoting=false} \
	%{!?with_sclients:-Dsimple-clients=""} \
	%{!?with_wlaunch:-Dweston-launch=false} \
	%{!?with_xwayland:-Dxwayland=false}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

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
%attr(755,root,root) %{_bindir}/weston-info
%if %{with wlaunch}
%attr(755,root,root) %{_bindir}/weston-launch
%endif
%attr(755,root,root) %{_bindir}/weston-screenshooter
%attr(755,root,root) %{_bindir}/weston-terminal
%attr(755,root,root) %{_bindir}/weston-touch-calibrator
%if %{with dclients}
%attr(755,root,root) %{_bindir}/weston-clickdot
%attr(755,root,root) %{_bindir}/weston-cliptest
%attr(755,root,root) %{_bindir}/weston-confine
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
%attr(755,root,root) %{_bindir}/weston-transformed
%endif
%if %{with sclients}
%attr(755,root,root) %{_bindir}/weston-simple-damage
%attr(755,root,root) %{_bindir}/weston-simple-dmabuf-egl
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
%attr(755,root,root) %{_libdir}/weston/cms-colord.so
%attr(755,root,root) %{_libdir}/weston/cms-static.so
%attr(755,root,root) %{_libdir}/weston/desktop-shell.so
%attr(755,root,root) %{_libdir}/weston/fullscreen-shell.so
%attr(755,root,root) %{_libdir}/weston/hmi-controller.so
%attr(755,root,root) %{_libdir}/weston/ivi-shell.so
%attr(755,root,root) %{_libdir}/weston/kiosk-shell.so
%attr(755,root,root) %{_libdir}/weston/screen-share.so
%attr(755,root,root) %{_libdir}/weston/systemd-notify.so
%{_datadir}/libweston-9
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

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-9.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libweston-9.so.0
%attr(755,root,root) %{_libdir}/libweston-desktop-9.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libweston-desktop-9.so.0
%dir %{_libdir}/libweston-9
%if %{with drm}
%attr(755,root,root) %{_libdir}/libweston-9/drm-backend.so
%endif
%attr(755,root,root) %{_libdir}/libweston-9/fbdev-backend.so
%attr(755,root,root) %{_libdir}/libweston-9/gl-renderer.so
%attr(755,root,root) %{_libdir}/libweston-9/headless-backend.so
%{?with_pipewire:%attr(755,root,root) %{_libdir}/libweston-9/pipewire-plugin.so}
%if %{with remoting}
%attr(755,root,root) %{_libdir}/libweston-9/remoting-plugin.so
%endif
%if %{with wayland}
%attr(755,root,root) %{_libdir}/libweston-9/wayland-backend.so
%endif
%if %{with x11}
%attr(755,root,root) %{_libdir}/libweston-9/x11-backend.so
%endif
%if %{with xwayland}
%attr(755,root,root) %{_libdir}/libweston-9/xwayland.so
%endif

%files libs-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-9.so
%attr(755,root,root) %{_libdir}/libweston-desktop-9.so
%{_includedir}/libweston-9
%{_pkgconfigdir}/libweston-9.pc
%{_pkgconfigdir}/libweston-desktop-9.pc
%{_npkgconfigdir}/libweston-9-protocols.pc

%if %{with rdp}
%files compositor-rdp
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libweston-9/rdp-backend.so
%{_mandir}/man7/weston-rdp.7*
%endif
