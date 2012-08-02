#
# Conditional build:
%bcond_without	drm		# DRM compositor
%bcond_with	openwfd		# OpenWF compositor
%bcond_without	wayland		# wayland (nested) compositor
%bcond_without	x11		# X11 compositor
%bcond_without	wlaunch		# weston launch
%bcond_without	xwayland	# X server launcher
%bcond_without	sclients	# simple clients
%bcond_with	clients		# non-simple + full GL clients
#
Summary:	Weston - Wayland demos
Summary(pl.UTF-8):	Weston - programy demonstracyjne dla protokołu Wayland
Name:		weston
Version:	0.95.0
Release:	0.1
License:	MIT
Group:		Applications
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	77c87d8cc15e759ff512f9584d37e8a8
URL:		http://wayland.freedesktop.org/
BuildRequires:	Mesa-libEGL-devel >= 7.10
BuildRequires:	Mesa-libGLES-devel
# for wayland and sclients, but also desktop-shell, which is always enabled
BuildRequires:	Mesa-libwayland-egl-devel >= 8.1
BuildRequires:	cairo-devel >= 1.10.0
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libwebp-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
# wayland-server always; wayland-client if with_wayland || with_sclients || with_clients; wayland-cursor if with_clients
BuildRequires:	wayland-devel = 0.95.0
BuildRequires:	xz
%if %{with drm}
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	mtdev-devel >= 1.1.0
BuildRequires:	udev-devel >= 136
BuildRequires:	libdrm-devel >= 2.4.30
%endif
%if %{with openwfd}
BuildRequires:	Mesa-libgbm-devel
# what package?
BuildRequires	pkgconfig(openwfd)
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
%endif
%if %{with clients}
# optionally cairo-egl >= 1.11.3, [cairo-gl or cairo-glesv2]
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	poppler-glib-devel
BuildRequires	xorg-lib-libxkbcommon-devel
%endif
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

%prep
%setup -q

%build
%configure \
	%{!?with_clients:--disable-clients} \
	%{!?with_drm:--disable-drm-compositor} \
	%{!?with_sclients:--disable-simple-clients} \
	--disable-setuid-install \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static} \
	%{!?with_wlaunch:--disable-weston-launch} \
	%{!?with_x11:--disable-x11-compositor} \
	%{!?with_xwayland:--disable-xwayland}
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
# composer
%attr(755,root,root) %{_bindir}/weston
%if %{with clients}
%attr(755,root,root) %{_bindir}/weston-terminal
%attr(755,root,root) %{_libexecdir}/weston-desktop-shell
%attr(755,root,root) %{_libexecdir}/weston-tablet-shell
%endif
%dir %{_libdir}/weston
%if %{with drm}
%attr(755,root,root) %{_libdir}/weston/drm-backend.so
%endif
%if %{with openwfd}
%attr(755,root,root) %{_libdir}/weston/openwfd-backend.so
%endif
%if %{with wayland}
%attr(755,root,root) %{_libdir}/weston/wayland-backend.so
%endif
%if %{with x11}
%attr(755,root,root) %{_libdir}/weston/x11-backend.so
%endif
%attr(755,root,root) %{_libdir}/weston/desktop-shell.so
%attr(755,root,root) %{_libdir}/weston/tablet-shell.so
%{_datadir}/weston

# noinst, too common names - package in %{name}-demos with weston- prefix?
# "simple clients"
#%attr(755,root,root) %{_bindir}/simple-egl
#%attr(755,root,root) %{_bindir}/simple-shm
#%attr(755,root,root) %{_bindir}/simple-touch
%if %{with clients}
#%attr(755,root,root) %{_bindir}/dnd
#%attr(755,root,root) %{_bindir}/eventdemo
#%attr(755,root,root) %{_bindir}/flower
#%attr(755,root,root) %{_bindir}/image
#%attr(755,root,root) %{_bindir}/resizor
#%attr(755,root,root) %{_bindir}/screenshot
#%attr(755,root,root) %{_bindir}/smoke
# "full GL" clients
#%attr(755,root,root) %{_bindir}/gears
#%attr(755,root,root) %{_bindir}/wscreensaver
# poppler
#%attr(755,root,root) %{_bindir}/view
%endif
