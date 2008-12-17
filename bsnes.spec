%define vernumber 038

Name:           bsnes
Version:        0.%{vernumber}
Release:        1%{?dist}
Summary:        SNES emulator focused on accuracy

Group:          Applications/Emulators
License:        Redistributable, no modification permitted
URL:            http://byuu.cinnamonpirate.com/?page=bsnes
Source0:        http://byuu.cinnamonpirate.com/files/%{name}_v%{vernumber}.tar.bz2
Source1:        bsnes.desktop
Source2:        README.bsnes
Patch0:         bsnes-0.037a-strip.patch
Patch1:         bsnes-system-zlib.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#bsnes does not use system snes_ntsc because the modified video processing
#filter algorithm calls back into bsnes specific c++ colortable code, that
#isn't available when the library is built stand alone
BuildRequires:  desktop-file-utils
BuildRequires:  freealut-devel
BuildRequires:  gtk2-devel
BuildRequires:  libao-devel     
BuildRequires:  libXv-devel
BuildRequires:  libXtst-devel
BuildRequires:  minizip-devel
BuildRequires:  SDL-devel
BuildRequires:  yasm

#libco, which is used by bsnes, only supports these
ExclusiveArch:  i386 x86_64

%description
bsnes is an emulator that began development on 2004-10-14. The purpose of the
emulator is a bit different from other emulators: it focuses on accuracy,
debugging functionality, and clean code.
The emulator does not focus on things that would hinder accuracy. This
includes speed and game-specific hacks for compatibility. As a result, the
minimum system requirements for bsnes are quite high.


%prep
%setup -qc
%patch0 -p0 -b .strip
%patch1 -p0 -b .system-zlib

#fix permissions and line endings
find src -type f \( -name \*.cpp -or -name \*.hpp -or -name \*.h -or -name \*.c \) -exec chmod 644 {} \;
find src -type f \( -name \*.cpp -or -name \*.hpp -or -name \*.h -or -name \*.c \) -exec sed -i 's/\r//' {} \;

#use system optflags
sed -i "s#flags = -O3#flags = %{optflags}#" src/Makefile

#install fedora-specific readme
install -pm 644 %{SOURCE2} README.Fedora


%build
pushd src
make %{?_smp_mflags} platform=x compiler=gcc enable_gzip=true enable_jma=true


%install
rm -rf $RPM_BUILD_ROOT
pushd src
make install DESTDIR=$RPM_BUILD_ROOT prefix=%{_prefix}      
desktop-file-install --vendor=rpmfusion \
       --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README.Fedora
%{_bindir}/bsnes
%{_datadir}/icons/bsnes.png
%{_datadir}/applications/rpmfusion-bsnes.desktop


%changelog
* Wed Dec 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.038-1
- Updated to 0.038
- Updated system zlib patch (.h → .hpp)
- License and readme are now accessible through the executable

* Fri Dec  5 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.037a-5
- Explained why system snes_ntsc is not used
- Explained why ExclusiveArch is used

* Sun Nov 30 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.037a-4
- Fixed README.Fedora permissions
- Added information concerning pulseaudio issues

* Sat Nov 29 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.037a-3
- Keep -fomit-frame-pointer
- $(strip) can stay
- Re-added system zlib patch

* Thu Nov 27 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.037a-2
- Patched the Makefile not to strip the binaries

* Sun Nov 23 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.037a-1
- Updated to 0.037a
- Dropped system zlib patch since bsnes uses zlib modified to support non-ansi filenames
- Added libXtst-devel to BuildRequires
- s/%%{ix86}/i386 to work around plague problem

* Tue Sep 16 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.036-1
- Updated to 0.036

* Mon Aug 25 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.035-1
- Updated to 0.035

* Sun Aug 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.033-1
- Updated to 0.033

* Wed May 28 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.032a-1
- Updated to 0.032a

* Sun May 25 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.032-1
- Updated to 0.032

* Mon Apr 14 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.031-1
- Updated to 0.031

* Thu Mar 27 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.030-1
- Updated to 0.030

* Mon Mar 17 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.029-1
- Updated to 0.029
- Dropped usleep patch
- Dropped destdir patch
- Updated system zlib patch
- Included patch approval

* Fri Feb 15 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.028.01-2
- Patched to fix CPU usage when idle
- Patched to use system zlib
- Dropped hicolor-icon-theme from Requires

* Sun Feb 10 2008 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.028.01-1
- Updated to 0.028.01
- Updated the Makefile patch
- Added freealut-devel and SDL-devel to BuildRequires

* Tue Dec 25 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.027-1
- Updated to 0.027
- Updated the Makefile patch
- Switched to yasm for all supported architectures

* Sun Nov 18 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.026-1
- Updated to 0.026
- Dropped icon conversion, PNG is now shipped in the tarball
- Icon is now installed to %%{_datadir}/pixmaps
- Dropped the icon cache scriptlets
- Dropped the wrapper, it is no longer necessary
- Added zip/gzip and jma support

* Mon Nov  5 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.025-4
- Fixed permissions and line endings of source files as well
- Fixed cart.db permissions, got missing in previous release
- Fixed date in %%changelog

* Mon Nov  5 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.025-3
- Updated the scriptlets to be in par with current guidelines
- Changed to convert the icon at build time
- Use the wrapper to avoid putting cart.db into %%{_bindir}

* Sun Nov  4 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.025-2
- Install cart.db
- Use system optflags
- Adjusted the License tag

* Sun Nov  4 2007 Julian Sikorski <belegdol[at]gmail[dot]com> - 0.025-1
- Initial RPM release
