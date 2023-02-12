#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	pretty-show
Summary:	Tools for working with derived Show instances and generic inspection of values
Summary(pl.UTF-8):	Narzędzie do pracy z instancjami wywodzącymi się z Show i ogólnym badaniem wartości
Name:		ghc-%{pkgname}
Version:	1.10
Release:	2
License:	MIT
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/pretty-show
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	1d4c4c9c02c5865eb5ac30c29d9ffc4d
URL:		http://hackage.haskell.org/package/pretty-show
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-haskell-lexer >= 1.1
BuildRequires:	ghc-pretty >= 1
%if %{with prof}
BuildRequires:	ghc-prof
BuildRequires:	ghc-haskell-lexer-prof >= 1.1
BuildRequires:	ghc-pretty-prof >= 1
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires(post,postun):	/usr/bin/ghc-pkg
Requires:	ghc-haskell-lexer >= 1.1
Requires:	ghc-pretty >= 1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
A library and an executable for working with derived Show instances.
By using the library, we can parse derived Show instances into a
generic data structure. The ppsh tool uses the library to produce
human-readable versions of Show instances, which can be quite handy
for debugging Haskell programs. We can also render complex generic
values into an interactive HTML page, for easier examination.

%description -l pl.UTF-8
Biblioteka i program do pracy z instancjami wywodzącymi się z Show.
Przy użyciu tej biblioteki można przetwarzać instancje wywodzące się z
Show do ogólnych struktur danych. Narzędzie ppsh wykorzystuje
bibiotekę do tworzenia czytelnych dla człowieka instancji Show, co
może być przydatne do diagnostyki programów w Haskellu. Możliwe jest
także renderowanie złożonych ogólnych wartości do interaktywnej strony
HTML w celu łatwiejszego zbadania.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-haskell-lexer-prof >= 1.1
Requires:	ghc-pretty-prof >= 1

%description prof
Profiling %{pkgname} library for GHC.  Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.hs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.hs build
runhaskell Setup.hs haddock

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.hs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version} %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.hs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc CHANGELOG %{name}-%{version}-doc/*
%attr(755,root,root) %{_bindir}/ppsh
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%attr(755,root,root) %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a

%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.dyn_hi
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Show
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Show/*.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Show/*.dyn_hi

%{_datadir}/%{pkgname}-%{version}

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/*.p_hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Text/Show/*.p_hi
%endif
