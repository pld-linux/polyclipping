# The Clipper C++ crystallographic library already uses the name "clipper".
# The developer is fine with the choosen name.

# API monitoring
# http://upstream-tracker.org/versions/clipper.html

Summary:	Polygon clipping library
Name:		polyclipping
Version:	6.2.1
Release:	1
License:	Boost
Group:		Libraries
Source0:	http://downloads.sourceforge.net/polyclipping/clipper_ver%{version}.zip
# Source0-md5:	040821e66ec529f3d78f8ff7c4e256b2
URL:		http://sourceforge.net/projects/polyclipping
BuildRequires:	cmake
BuildRequires:	dos2unix
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

%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -qc

# Delete binaries
find . \( -name "*.exe" -o -name "*.dll" \) -print0 | xargs -0 rm -v

# Correct line ends and encodings
find . -type f -exec dos2unix -k {} \;

for filename in perl/perl_readme.txt README; do
	iconv -f iso8859-1 -t utf-8 "${filename}" > "${filename}".conv && \
	touch -r "${filename}" "${filename}".conv && \
	mv "${filename}".conv "${filename}"
done

# Enable use_lines
sed -i 's|^//#define use_lines$|#define use_lines|' cpp/clipper.hpp

%build
install -d cpp/build
cd cpp/build
%cmake ..
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C cpp/build install \
	DESTDIR=$RPM_BUILD_ROOT

# Install agg header with corrected include statement
sed -e 's/\.\.\/clipper\.hpp/clipper.hpp/' < cpp/cpp_agg/agg_conv_clipper.h > $RPM_BUILD_ROOT%{_includedir}/%{name}/agg_conv_clipper.h

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc License.txt README
%doc "Third\ Party/Haskell" "Third\ Party/perl" "Third\ Party/ruby" "Third\ Party/python" Documentation
%attr(755,root,root) %{_libdir}/libpolyclipping.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libpolyclipping.so.19

%files devel
%defattr(644,root,root,755)
%{_npkgconfigdir}/%{name}.pc
%{_includedir}/%{name}
%{_libdir}/libpolyclipping.so
