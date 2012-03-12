#
# Conditional build:
%bcond_with	clients		# non-simple + full GL clients
%bcond_with	openwfd		# OpenWF compositor
#
Summary:	Weston - Wayland demos
Summary(pl.UTF-8):	Weston - programy demonstracyjne dla protokołu Wayland
Name:		weston
Version:	0.85.0
Release:	1
License:	MIT
Group:		Applications
Source0:	http://wayland.freedesktop.org/releases/%{name}-%{version}.tar.xz
# Source0-md5:	fb53b5767a21cad91fad94d735835d2b
URL:		http://wayland.freedesktop.org/
BuildRequires:	Mesa-libEGL-devel >= 7.10
BuildRequires:	Mesa-libGLES-devel
BuildRequires:	Mesa-libgbm-devel
BuildRequires:	Mesa-libwayland-egl-devel
BuildRequires:	libdrm-devel >= 2.4.23
BuildRequires:	libpng-devel
BuildRequires:	libxcb-devel
BuildRequires:	pixman-devel
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 136
# wayland-{client,server}
BuildRequires:	wayland-devel = 0.85.0
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
%if %{with openwfd}
# what package?
BuildRequires	pkgconfig(openwfd)
%endif
%if %{with clients}
BuildRequires:	cairo-devel >= 1.10.0
# +optionally cairo-egl >= 1.11.3?
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	glib2-devel >= 2.0
BuildRequires:	libjpeg-devel
BuildRequires:	poppler-glib-devel
# libxkbcommon not released yet
BuildRequires	pkgconfig(xkbcommon)
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
	--disable-setuid-install \
	--disable-silent-rules \
	%{!?with_static_libs:--disable-static}
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
%attr(755,root,root) %{_libdir}/weston/drm-backend.so
%if %{with openwfd}
%attr(755,root,root) %{_libdir}/weston/openwfd-backend.so
%endif
%attr(755,root,root) %{_libdir}/weston/wayland-backend.so
%attr(755,root,root) %{_libdir}/weston/x11-backend.so
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
