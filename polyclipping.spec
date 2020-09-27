# The Clipper C++ crystallographic library already uses the name "clipper".
# The developer is fine with the choosen name.

# API monitoring
# http://upstream-tracker.org/versions/clipper.html

Summary:	Polygon clipping library
Summary(pl.UTF-8):	Biblioteka do obcinania wielokątów
Name:		polyclipping
Version:	6.4.2
Release:	2
License:	Boost
Group:		Libraries
Source0:	http://downloads.sourceforge.net/polyclipping/clipper_ver%{version}.zip
# Source0-md5:	100b4ec56c5308bac2d10f3966e35e11
Patch0:		%{name}-pc.patch
URL:		https://sourceforge.net/projects/polyclipping/
BuildRequires:	cmake >= 2.6.0
BuildRequires:	dos2unix
BuildRequires:	iconv
BuildRequires:	libstdc++-devel
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This library primarily performs the boolean clipping operations -
intersection, union, difference & xor - on 2D polygons. It also
performs polygon offsetting. The library handles complex
(self-intersecting) polygons, polygons with holes and polygons with
overlapping co-linear edges. Input polygons for clipping can use
EvenOdd, NonZero, Positive and Negative filling modes. The clipping
code is based on the Vatti clipping algorithm, and outperforms other
clipping libraries.

%description -l pl.UTF-8
Biblioteka do wykonywania logicznych operacji na wielokątach
dwuwymiarowych - przecięć, sumy, różnicy i różnicy symetrycznej.
Wykonuje także obcinanie marginesów. Biblioteka obsługuje wielokąty
złożone (samoprzecinające się), wielokąty z dziurami oraz z
nakładającymi się liniowo krawędziami. Wejściowe wielokąty mogą
używać trybu wypełniania EvenOdd, NonZero, Positive i Negative. Kod
obcinania jest oparty na algorytmie Vattiego i jest szybszy od wielu
innych bibliotek.

%package devel
Summary:	Development files for polyclipping library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki polyclipping
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files for developing applications
that use polyclipping library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących bibliotekę polyclipping.

%prep
%setup -qc
%patch0 -p1

# Delete binaries
find . \( -name "*.exe" -o -name "*.dll" \) -print0 | xargs -0 rm -v

# Correct line ends and encodings
find . -type f -exec dos2unix -k {} \;

for filename in perl/perl_readme.txt README; do
	iconv -f iso8859-1 -t utf-8 "${filename}" > "${filename}".conv && \
	touch -r "${filename}" "${filename}".conv && \
	%{__mv} "${filename}".conv "${filename}"
done

# Enable use_lines
sed -i 's|^//#define use_lines$|#define use_lines|' cpp/clipper.hpp

%build
install -d cpp/build
cd cpp/build
%cmake .. \
	-DCMAKE_INSTALL_PKGCONFIGDIR=%{_pkgconfigdir}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C cpp/build install \
	DESTDIR=$RPM_BUILD_ROOT

# Install agg header with corrected include statement
sed -e 's/\.\.\/clipper\.hpp/clipper.hpp/' < cpp/cpp_agg/agg_conv_clipper.h > $RPM_BUILD_ROOT%{_includedir}/%{name}/agg_conv_clipper.h

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc License.txt README Third?Party/{Flash,Go,Haskell,Java,LuaJIT,Matlab,ObjectiveC,perl,ruby}/*_readme.txt
%attr(755,root,root) %{_libdir}/libpolyclipping.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolyclipping.so.22

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpolyclipping.so
%{_includedir}/polyclipping
%{_pkgconfigdir}/polyclipping.pc
