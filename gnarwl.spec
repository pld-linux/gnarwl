Summary:	Gnu Neat Auto Reply With LDAP
Summary(pl.UTF-8):	Gnu Neat Auto Reply With LDAP - autoresponder korzystający z LDAP
Name:		gnarwl
Version:	3.6
Release:	3
License:	GPL
Group:		Applications/Mail
Source0:	http://www.onyxbits.de/sites/default/files/%{name}-%{version}.tgz
# Source0-md5:	832d1e2264b7e47d318b16795d63da8e
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-opt.patch
Patch2:		format-security.patch
URL:		http://www.onyxbits.de/gnarwl/
BuildRequires:	autoconf
BuildRequires:	gdbm-devel
BuildRequires:	groff
BuildRequires:	openldap-devel >= 2.4.6
BuildRequires:	rpmbuild(macros) >= 1.304
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
Provides:	group(gnarwl)
Provides:	user(gnarwl)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		schemadir	/usr/share/openldap/schema

%description
Gnarwl is a email auto reply/vacation tool, intented to be used on
mailservers, on which users may not (nescessarily) have
systemaccoounts, but where userinformation is stored in LDAP.

%description -l pl.UTF-8
Gnarwl to system automatycznego odpowiadania na listy stworzony z
myślą o serwerach poczty, na których użytkownicy nie muszą posiadać
prawdziwych kont systemowych, a informacje o użytkownikach znajdują
się w bazie LDAP.

%package -n openldap-schema-ISPEnv2
Summary:	LDAP schema for gnarwl
Summary(pl.UTF-8):	Schemat LDAP dla gnarwla
Group:		Networking/Daemons
Requires(post,postun):	sed >= 4.0
Requires:	openldap-servers
Requires:	sed >= 4.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n openldap-schema-ISPEnv2
This package contains ISPEnv2.schema to be used with gnarwl.

%description -n openldap-schema-ISPEnv2 -l pl.UTF-8
Ten pakiet zawiera schemat LDAP ISPEnv2.schema do używania z gnarwlem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__autoconf}
%configure \
	--with-homedir=/var/lib/gnarwl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -D doc/ISPEnv2.schema $RPM_BUILD_ROOT%{schemadir}/ISPEnv2.schema
rm -rf $RPM_BUILD_ROOT/usr/share/doc/packages/gnarwl

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 26 gnarwl
%useradd -u 26 -d /var/lib/gnarwl -s /usr/bin/gnarwl -c "Gnarwl User" -g gnarwl gnarwl

%post
if [ "$1" = 1 ]; then
%banner -e %{name} <<'EOF'
The OpenLDAP schema for gnarwl can be installed with openldap-schema-ISPEnv2 package.
EOF
fi

%postun
if [ "$1" = "0" ]; then
	%userremove gnarwl
	%groupremove gnarwl
fi

%post -n openldap-schema-ISPEnv2
%openldap_schema_register %{schemadir}/ISPEnv2.schema -d core,cosine
%service -q ldap restart

%postun -n openldap-schema-ISPEnv2
if [ "$1" = "0" ]; then
	%openldap_schema_unregister %{schemadir}/ISPEnv2.schema
	%service -q ldap restart
fi

%files
%defattr(644,root,root,755)
%doc doc/{AUTHORS,FAQ,HISTORY,INSTALL,ISPEnv.schema,LICENSE,README,README.upgrade,example.ldif}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_sbindir}/*
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,gnarwl) %{_sysconfdir}/gnarwl.cfg
%attr(755,root,gnarwl) %dir %{_var}/lib/gnarwl
%attr(775,root,gnarwl) %dir %{_var}/lib/gnarwl/block
%attr(755,root,gnarwl) %dir %{_var}/lib/gnarwl/bin
%attr(640,root,gnarwl) %{_var}/lib/gnarwl/.forward
%attr(660,root,gnarwl) %{_var}/lib/gnarwl/blacklist.db
%attr(660,root,gnarwl) %{_var}/lib/gnarwl/badheaders.db
%attr(640,root,gnarwl) %{_var}/lib/gnarwl/footer.txt
%attr(640,root,gnarwl) %{_var}/lib/gnarwl/header.txt
%{_mandir}/man*/*

%files -n openldap-schema-ISPEnv2
%defattr(644,root,root,755)
%{schemadir}/*.schema
