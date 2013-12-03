#
# Conditional build:
%bcond_without	drm		# DRM compositor
%bcond_with	rdp		# RDP compositor (needs freerdp 1.1.0)
%bcond_without	wayland		# wayland (nested) compositor
%bcond_without	x11		# X11 compositor
%bcond_without	vaapi		# vaapi recorder
%bcond_without	wlaunch		# weston launch
%bcond_without	xwayland	# X server launcher
%bcond_without	sclients	# simple clients
%bcond_without	clients		# non-simple + full GL clients
#
Summary:	Weston - Wayland demos
Summary(pl.UTF-8):	Weston - programy demonstracyjne dla protokołu Wayland
Name:		weston
Version:	1.3.1
Release:	1
License:	MIT
Group:		Applications
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	ffe7c3bc0e7eb39a305cbbea8c7766f3
URL:		http://wayland.freedesktop.org/
BuildRequires:	Mesa-libEGL-devel >= 7.10
# GLESv2
BuildRequires:	Mesa-libGLES-devel
# for wayland and sclients, but also desktop-shell, which is always enabled
BuildRequires:	Mesa-libwayland-egl-devel >= 9.0-2
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	colord-devel >= 0.1.27
%{?with_rdp:BuildRequires:	freerdp-devel >= 1.1.0}
BuildRequires:	lcms2-devel >= 2
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
%if %{with vaapi}
BuildRequires:	libva-devel >= 0.34.0
BuildRequires:	libva-drm-devel >= 0.34.0
%endif
BuildRequires:	libwebp-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
# wayland-server always; wayland-client if with_wayland || with_sclients || with_clients; wayland-cursor if with_clients
BuildRequires:	wayland-devel >= 1.3.0
BuildRequires:	xorg-lib-libxkbcommon-devel >= 0.3.0
BuildRequires:	xz
%if %{with drm}
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	libdrm-devel >= 2.4.30
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	udev-devel >= 1:136
%endif
%if %{with x11}
BuildRequires:	libxcb-devel
BuildRequires:	xorg-lib-libX11-devel
%endif
%if %{with wlaunch}
BuildRequires:	libdrm-devel
BuildRequires:	pam-devel
BuildRequires:	systemd-devel
%endif
%if %{with xwayland}
BuildRequires:	libxcb-devel
BuildRequires:	pkgconfig(cairo-xcb)
BuildRequires:	xorg-lib-libXcursor-devel
%endif
%if %{with clients}
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	cairo-devel >= 1.11.3
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	pkgconfig(cairo-egl) >= 1.11.3
BuildRequires:	pkgconfig(cairo-gl)
BuildRequires:	poppler-glib-devel
%endif
Requires:	Mesa-libwayland-egl >= 9.0-2
Requires:	wayland >= 1.3.0
Requires:	xorg-lib-libxkbcommon >= 0.3.0
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
Requires:	Mesa-libEGL-devel >= 7.10
# GLESv2
Requires:	Mesa-libGLES-devel
Requires:	pixman-devel
Requires:	wayland-devel >= 1.3.0
Requires:	xorg-lib-libxkbcommon-devel >= 0.3.0

%description devel
Header files for Weston plugin development.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek dla Westona.

%prep
%setup -q

%build
%configure \
	%{!?with_clients:--disable-clients} \
	%{!?with_drm:--disable-drm-compositor} \
	%{?with_rdp:--enable-rdp-compositor} \
	%{!?with_sclients:--disable-simple-clients} \
	--disable-setuid-install \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_vaapi:--disable-vaapi-recorder} \
	%{!?with_wlaunch:--disable-weston-launch} \
	%{!?with_x11:--disable-x11-compositor} \
	%{!?with_xwayland:--disable-xwayland} \
	%{?with_clients:--with-cairo=gl}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/weston/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/wcap-decode
%attr(755,root,root) %{_bindir}/weston-info
# composer
%attr(755,root,root) %{_bindir}/weston
%if %{with wlaunch}
%attr(755,root,root) %{_bindir}/weston-launch
%endif
%if %{with clients}
%attr(755,root,root) %{_bindir}/weston-terminal
%attr(755,root,root) %{_libexecdir}/weston-desktop-shell
%attr(755,root,root) %{_libexecdir}/weston-keyboard
%attr(755,root,root) %{_libexecdir}/weston-screensaver
%attr(755,root,root) %{_libexecdir}/weston-screenshooter
%attr(755,root,root) %{_libexecdir}/weston-tablet-shell
%endif
%attr(755,root,root) %{_libexecdir}/weston-simple-im
%dir %{_libdir}/weston
%attr(755,root,root) %{_libdir}/weston/cms-colord.so
%attr(755,root,root) %{_libdir}/weston/cms-static.so
%if %{with drm}
%attr(755,root,root) %{_libdir}/weston/drm-backend.so
%endif
%attr(755,root,root) %{_libdir}/weston/fbdev-backend.so
%attr(755,root,root) %{_libdir}/weston/headless-backend.so
%if %{with rdp}
%attr(755,root,root) %{_libdir}/weston/rdp-backend.so
%endif
%if %{with wayland}
%attr(755,root,root) %{_libdir}/weston/wayland-backend.so
%endif
%if %{with x11}
%attr(755,root,root) %{_libdir}/weston/x11-backend.so
%endif
%if %{with xwayland}
%attr(755,root,root) %{_libdir}/weston/xwayland.so
%endif
%attr(755,root,root) %{_libdir}/weston/desktop-shell.so
%attr(755,root,root) %{_libdir}/weston/tablet-shell.so
%{_datadir}/weston
%{_mandir}/man1/weston.1*
%{_mandir}/man5/weston.ini.5*
%{_mandir}/man7/weston-drm.7*

# noinst by default - --enable-demo-clients and package in %{name}-demos?
# "simple clients"
#%attr(755,root,root) %{_bindir}/weston-simple-egl
#%attr(755,root,root) %{_bindir}/weston-simple-shm
#%attr(755,root,root) %{_bindir}/weston-simple-touch
%if %{with clients}
#%attr(755,root,root) %{_bindir}/weston-calibrator
#%attr(755,root,root) %{_bindir}/weston-clickdot
#%attr(755,root,root) %{_bindir}/weston-editor
#%attr(755,root,root) %{_bindir}/weston-eventdemo
#%attr(755,root,root) %{_bindir}/weston-fullscreen
#%attr(755,root,root) %{_bindir}/weston-cliptest
#%attr(755,root,root) %{_bindir}/weston-dnd
#%attr(755,root,root) %{_bindir}/weston-flower
#%attr(755,root,root) %{_bindir}/weston-image
#%attr(755,root,root) %{_bindir}/weston-resizor
#%attr(755,root,root) %{_bindir}/weston-smoke
#%attr(755,root,root) %{_bindir}/weston-transformed
# "full GL" clients
#%attr(755,root,root) %{_bindir}/weston-gears
# poppler
#%attr(755,root,root) %{_bindir}/weston-view
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/weston
%{_pkgconfigdir}/weston.pc
