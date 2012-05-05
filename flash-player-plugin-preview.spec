
%define name	flash-player-plugin-preview
# see http://www.adobe.com/software/flash/about/ for version test
%define version	11.2.202.235
%define plev	p3
%define tardate	111710
%define rel	1

%define distsuffix mdv
# backportability
%define _localstatedir /var

Summary:	Flash Player plugin for browsers - preview beta release
Name:		%name
Version:	%version
Release:	%mkrel %rel
License:	Proprietary
URL:		http://www.adobe.com/products/flashplayer/
Source0:	download-flash-player-plugin.in
Group:		Networking/WWW
ExclusiveArch:	x86_64
Requires:	curl
Requires(post):	curl

# obtained by objdump -x /usr/lib/mozilla/plugins/libflashplayer.so | grep NEEDED
# helper: for i in $(objdump -p libflashplayer.so  | grep NEEDED | awk '{ print $2 }'); do
#	  echo -n "$i: "; rpm -qf /usr/lib64/$i; done
#		libX11.so.6	libXext.so.6	libXt.so.6	libfreetype.so.6
Requires:	%{_lib}x11_6	%{_lib}xext6	%{_lib}xt6	%{_lib}freetype6
#		libfontconfig.so.1	libgtk-x11-2.0.so.0, libgdk-x11-2.0.so.0
Requires:       %{_lib}fontconfig1	%{_lib}gtk+2.0_0
#		libatk-1.0.so.0	libgdk_pixbuf-2.0.so.0	libpangocairo-1.0.so.0, libpango-1.0.so.0
Requires:	%{_lib}atk1.0_0	%{_lib}gdk_pixbuf2.0_0	%{_lib}pango1.0_0
#		libcairo.so.2	libgobject-2.0.so.0, libgmodule-2.0.so.0, libglib-2.0.so.0
Requires:	%{_lib}cairo2	%{_lib}glib2.0_0
#		libnss3.so, libsmime3.so, libssl3.so	libplds4.so, libplc4.so, libnspr4.so
Requires:	%{_lib}nss3				%{_lib}nspr4
# required for audio, dlopened:
Requires:	%{_lib}alsa2
# dlopened:
%if %{mdkversion} >= 200710
Requires:	%{_lib}curl4
%else
Requires:	%{_lib}curl3
%endif
#
Conflicts:	FlashPlayer < 9.0.115.0-5
Conflicts:	flash-plugin FlashPlayer-plugin flashplayer-plugin
Conflicts:	flash-player-plugin < %{version}-%{release}
%ifarch x86_64
# there is no stable flash-player-plugin on x86_64
Provides:	flash-player-plugin = %{version}-%{release}
%endif
# Conflict with free plugins to avoid user confusion as to which one is
# actually used:
Conflicts:	gnash-firefox-plugin
Conflicts:	swfdec-mozilla
Conflicts:	lightspark-mozilla-plugin
Conflicts:	libflashsupport < 0.20080000.1

%description
Adobe Flash Player plugin for browsers. Preview beta release.

NOTE: This package does not contain the Flash Player itself. The
software will be automatically downloaded from Adobe during package
installation. Alternatively you can use the command
"download-flash-player-plugin" manually.

Installing this package indicates your acceptance of the following
documents:
- Flash Player 10 License:
  http://labs.adobe.com/technologies/eula/flashplayer10.html
- Adobe.com Terms of Use: http://www.adobe.com/misc/terms.html
- Adobe Online Privacy Policy: http://www.adobe.com/misc/privacy.html

This package is in PLF because it installs software with non-free
license.

%prep
%setup -c -T

# The linuxdownload.adobe.com rpm usually stays up longer, but fpdownload.macromedia.com is faster.
# Their md5sums differ.
%ifarch %ix86
#%define downurl1 http://download.macromedia.com/pub/labs/flashplayer10/flashplayer10_2_%{plev}_32bit_linux_%{tardate}.tar.gz
%define downurl1 http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.i386.tar.gz
%define tmd5sum1 edc3326dd25adee13a8109834d8c05ce
%define downurl2 %nil
%define tmd5sum2 %nil
%define tarname install_flash_player_11_linux.i386.tar.gz
%define tartype	tar
%define srcdir	%nil
%endif
%ifarch x86_64
%define downurl1 http://fpdownload.macromedia.com/get/flashplayer/pdc/%{version}/install_flash_player_11_linux.x86_64.tar.gz
%define tmd5sum1 144b9ab0fec08d589b5369b1417d8332
%define downurl2 %nil
%define tmd5sum2 %nil
%define tarname install_flash_player_11_linux.x86_64.tar.gz
%define tartype tar
%define srcdir  %nil
%endif

cat > download-flash-player-plugin <<EOF
#!/bin/sh
TARBALLDIR="%{_localstatedir}/lib/%{name}"
FILENAME="%{tarname}"
FILETYPE="%{tartype}"
MD5SUM1="%{tmd5sum1}"
MD5SUM2="%{tmd5sum2}"
MD5SUM3=
URL1="%{downurl1}"
URL2="%{downurl2}"
URL3=
FILE1_SRC="%{srcdir}libflashplayer.so"
FILE1_DST="%{_libdir}/mozilla/plugins/libflashplayer.so"
FILE2_SRC=
EOF
cat %SOURCE0 >> download-flash-player-plugin

%ifarch %ix86
cat >> download-flash-player-plugin <<EOF
if [ "\$(uname -m)" == x86_64 ]; then
	if [ -x %{_bindir}/nspluginwrapper ]; then
		echo "Detected x86_64 with nspluginwrapper, enabling the plugin on 64bit browsers too."
		%{_bindir}/nspluginwrapper -i %{_libdir}/mozilla/plugins/libflashplayer.so
	else
		echo "Install nspluginwrapper if you want to use the plugin with 64bit browsers too."
	fi
fi
EOF
%endif

%install
rm -rf %{buildroot}

install -d -m755 %{buildroot}%{_localstatedir}/lib/%{name}
install -d -m755 %{buildroot}%{_libdir}/mozilla/plugins
%if %mdkversion < 200800
install -d -m755 %{buildroot}%{_libdir}/opera/plugins
ln -s %{_libdir}/mozilla/plugins/libflashplayer.so %{buildroot}%{_libdir}/opera/plugins/libflashplayer.so
%endif
touch %{buildroot}%{_libdir}/mozilla/plugins/libflashplayer.so
touch %{buildroot}%{_localstatedir}/lib/%{name}/%{tarname}

install -d -m755 %{buildroot}%{_sbindir}
install -m755 download-flash-player-plugin %{buildroot}%{_sbindir}

# posttrans so that we can use postun safely without if's :)
%posttrans
%{_sbindir}/download-flash-player-plugin

%ifarch %ix86
%postun
if [ -x %{_bindir}/nspluginwrapper ] && [ "$(uname -m)" == x86_64 ] && [ -f %{_prefix}/lib64/mozilla/plugins/npwrapper.libflashplayer.so ]; then
	%{_bindir}/nspluginwrapper -r %{_prefix}/lib64/mozilla/plugins/npwrapper.libflashplayer.so
fi
%endif

%files
%defattr(-,root,root)
%{_sbindir}/download-flash-player-plugin
%dir %{_localstatedir}/lib/%{name}
%ghost %{_localstatedir}/lib/%{name}/%{tarname}
%dir %{_libdir}/mozilla
%dir %{_libdir}/mozilla/plugins
%ghost %{_libdir}/mozilla/plugins/libflashplayer.so
